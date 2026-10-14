"""Shared UI actions and status: neither host implements publishing policy."""
from pathlib import Path
from . import core, transport


class Publisher:
    def __init__(self, adapter, exchange=None):
        self.adapter = adapter
        self.exchange = Path(exchange or core.default_exchange()).resolve()
        self.manifest = None
        self.request_id = None
        self.message = 'Select one mesh. Publish files, or Publish & Send to Unreal.'

    def set_exchange(self, exchange):
        """Changing folders drops local revision state, never moves queued work."""
        root = Path(exchange).resolve()
        if root != self.exchange:
            self.exchange = root
            self.manifest = None
            self.request_id = None
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
        self.message = 'Sent. Waiting for Unreal acknowledgement...'
        return self.request_id

    def poll(self):
        if self.request_id:
            result = transport.response(self.request_id, self.exchange)
            if result:
                self.message = ('Imported: ' + result['asset_path'] if result['ok']
                                else 'Unreal error: ' + result['error'])
                self.request_id = None
                return result
            if not transport.receiver_status(self.exchange):
                self.message = 'Receiver offline; acknowledgement pending. Check Unreal before resending.'
        return None
