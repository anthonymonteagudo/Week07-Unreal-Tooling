"""Shared UI actions and status: neither host implements publishing policy."""
from pathlib import Path
import json
import platform
import sys
from . import core, transport


class Publisher:
    def __init__(self, adapter, exchange=None):
        self.adapter = adapter
        self.exchange = Path(exchange or core.default_exchange()).resolve()
        self.manifest = None
        self.request_id = None
        self.last_request_id = None
        self.last_result = None
        self.message = 'Select one mesh. Publish files, or Publish & Send to Unreal.'

    def set_exchange(self, exchange):
        """Changing folders drops local revision state, never moves queued work."""
        root = Path(exchange).resolve()
        if root != self.exchange:
            self.exchange = root
            self.manifest = None
            self.request_id = None
            self.last_request_id = None
            self.last_result = None
            self.message = ('Exchange changed. Publish again. Any request already sent '
                            'remains in the previous exchange.')

    @property
    def connected(self):
        return bool(transport.receiver_status(self.exchange))

    def _require_idle(self):
        self.poll()
        if self.request_id:
            raise RuntimeError('Acknowledgement pending. Check Unreal before publishing or resending.')

    def publish(self, name, destination=core.DESTINATION, send=False):
        self._require_idle()
        # A failed new export must not leave an older revision available to send.
        self.manifest = None
        self.last_request_id = None
        self.last_result = None
        self.manifest = core.publish(self.adapter, self.exchange, name, destination)
        self.message = 'Published: ' + str(self.manifest)
        if send:
            self.send()
        return self.manifest

    def send(self):
        self._require_idle()
        if self.manifest is None:
            raise ValueError('Publish a mesh first.')
        self.request_id = transport.send(self.manifest, self.exchange)
        self.last_request_id = self.request_id
        self.last_result = None
        self.message = 'Sent. Waiting for Unreal acknowledgement...'
        return self.request_id

    def poll(self):
        if self.request_id:
            result = transport.response(self.request_id, self.exchange)
            if result:
                self.last_result = result
                self.message = ('Imported: ' + result['asset_path'] if result['ok']
                                else 'Unreal error: ' + result['error'])
                self.request_id = None
                return result
            if not transport.receiver_status(self.exchange):
                self.message = 'Receiver offline; acknowledgement pending. Check Unreal before resending.'
        return None

    def diagnostics(self, configured_exchange=None):
        """Read a snapshot without polling, changing folders, or touching the scene.

        An uncommitted UI folder is reported separately from the active exchange.
        Missing/malformed files are evidence, not a reason to lose the report.
        """
        def read_record(path):
            try:
                return core.read_json(path)
            except (OSError, ValueError) as error:
                return {'unavailable': str(error)}

        identity = self.request_id or self.last_request_id
        receiver = read_record(self.exchange / 'receiver.json')
        request = (read_record(self.exchange / 'requests' / (identity + '.json'))
                   if identity else None)
        result = (read_record(self.exchange / 'responses' / (identity + '.json'))
                  if identity else None)
        if isinstance(result, dict) and 'unavailable' in result and self.last_result:
            result = dict(self.last_result)
        try:
            online = bool(transport.receiver_status(self.exchange))
        except (AttributeError, TypeError):
            online = False
        configured = str(configured_exchange) if configured_exchange is not None else str(self.exchange)
        try:
            host = self.adapter.environment()
        except Exception as error:
            host = {'unavailable': str(error)}
        return json.dumps({
            'report': 'Week 7 bridge diagnostics',
            'host_adapter': type(self.adapter).__module__ + '.' + type(self.adapter).__name__,
            'host': host,
            'python_version': platform.python_version(),
            'python_executable': sys.executable,
            'bridge_module': str(Path(__file__).resolve()),
            'exchange': str(self.exchange),
            'configured_exchange': configured,
            'receiver_online': online,
            'receiver': receiver,
            'manifest': str(self.manifest) if self.manifest else None,
            'pending_request_id': self.request_id,
            'last_request_id': self.last_request_id,
            'request': request,
            'result': result,
            'status_message': self.message,
        }, indent=2, ensure_ascii=False)
