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

    def publish(self, name, destination=core.DESTINATION, send=False):
        self.request_id = None
        self.manifest = core.publish(self.adapter, self.exchange, name, destination)
        self.message = 'Published: ' + str(self.manifest)
        if send:
            self.send()
        return self.manifest

    def send(self):
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
