"""Local IPC: immutable requests + acknowledgements, no arbitrary Python execution.

The Unreal Slate tick consumes requests on its main thread. A session token keeps
requests from an earlier editor session from unexpectedly importing on restart.
"""
from pathlib import Path
import time
import uuid
from .core import atomic_json, read_json, load_manifest, default_exchange


def receiver_status(exchange=None):
    root = Path(exchange or default_exchange()).resolve()
    try:
        info = read_json(root / 'receiver.json')
        if info.get('running') and -2 < time.time() - info['heartbeat'] < 8:
            return info
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return None


def send(manifest, exchange=None):
    root = Path(exchange or default_exchange()).resolve()
    load_manifest(manifest, root)
    status = receiver_status(root)
    if not status:
        raise RuntimeError('FBX published. Unreal receiver is offline: start it, then Send published revision.')
    identity = uuid.uuid4().hex
    atomic_json(root / 'requests' / (identity + '.json'), {
        'id': identity, 'session': status['session'], 'action': 'import',
        'manifest': str(Path(manifest).resolve().relative_to(root)),
        'created_at': time.time(),
    })
    return identity


def response(identity, exchange=None):
    if len(identity) != 32 or any(c not in '0123456789abcdef' for c in identity):
        raise ValueError('Invalid request ID.')
    path = Path(exchange or default_exchange()) / 'responses' / (identity + '.json')
    try:
        return read_json(path)
    except FileNotFoundError:
        return None


class Inbox:
    """Host-independent request handling; importer is injected by the UE adapter."""
    def __init__(self, exchange, importer, session=None):
        self.root = Path(exchange).resolve()
        self.importer = importer
        self.session = session or uuid.uuid4().hex
        (self.root / 'requests').mkdir(parents=True, exist_ok=True)
        (self.root / 'responses').mkdir(exist_ok=True)

    def heartbeat(self, running=True, **details):
        atomic_json(self.root / 'receiver.json', dict(
            session=self.session, heartbeat=time.time(), running=running, **details))

    def poll(self):
        """At most one import per tick. Completed requests are never replayed."""
        for request in sorted((self.root / 'requests').glob('*.json'), key=lambda p: p.stat().st_mtime_ns):
            output = self.root / 'responses' / request.name
            if output.exists():
                continue
            result = {'id': request.stem, 'session': self.session, 'ok': False}
            try:
                data = read_json(request)
                if data.get('id') != request.stem or data.get('action') != 'import':
                    raise ValueError('Unknown request. Only import is supported.')
                if data.get('session') != self.session:
                    raise ValueError('Receiver session changed. Send the published revision again.')
                manifest = (self.root / data['manifest']).resolve()
                load_manifest(manifest, self.root)
                result.update(self.importer(manifest, self.root))
                result['ok'] = True
            except Exception as error:
                result['error'] = str(error)
            atomic_json(output, result)
            return result
        return None
