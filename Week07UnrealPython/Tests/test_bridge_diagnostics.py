"""Diagnostics must explain failure states without changing a publish or queue."""
import copy
import json
import importlib
from pathlib import Path
import sys
import tempfile
import unittest
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Content/Python'))
from week07_bridge import core, transport
from week07_bridge.client import Publisher
from test_fbx_bridge import Adapter


class DiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.publisher = Publisher(Adapter(), self.root)

    def snapshot(self, configured=None):
        state = copy.deepcopy({k: v for k, v in self.publisher.__dict__.items() if k != 'adapter'})
        files = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(self.publisher, 'poll', side_effect=AssertionError('must not poll')), \
             patch.object(self.publisher.adapter, 'export_fbx', side_effect=AssertionError('must not export')), \
             patch.object(self.publisher.adapter, 'inspect_selection', side_effect=AssertionError('must not inspect scene')), \
             patch.object(transport, 'send', side_effect=AssertionError('must not send')):
            report = json.loads(self.publisher.diagnostics(configured))
        self.assertEqual(state, {k: v for k, v in self.publisher.__dict__.items() if k != 'adapter'})
        self.assertEqual(files, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        return report

    def test_offline_and_different_configured_folder(self):
        report = self.snapshot(str(self.root / 'other'))
        self.assertFalse(report['receiver_online'])
        self.assertNotEqual(report['exchange'], report['configured_exchange'])
        self.assertIn('unavailable', report['receiver'])
        self.assertTrue(report['python_version'])
        self.assertTrue(report['python_executable'])
        self.assertTrue(Path(report['bridge_module']).is_file())
        self.assertIsNone(report['request'])

    def test_pending_and_acknowledged_before_poll(self):
        inbox = transport.Inbox(self.root, lambda *_: {'asset_path': '/Game/Test'})
        inbox.heartbeat(project='ExpectedProject.uproject')
        self.publisher.publish('SM_Test', send=True)
        identity = self.publisher.request_id
        pending = self.snapshot()
        self.assertEqual(identity, pending['pending_request_id'])
        self.assertEqual(inbox.session, pending['request']['session'])
        self.assertEqual('ExpectedProject.uproject', pending['receiver']['project'])
        inbox.poll()
        report = self.snapshot()
        self.assertEqual(identity, self.publisher.request_id)
        self.assertTrue(report['result']['ok'])
        self.publisher.poll()
        report = self.snapshot()
        self.assertIsNone(report['pending_request_id'])
        self.assertEqual(identity, report['last_request_id'])
        self.assertTrue(report['result']['ok'])

    def test_failed_result_survives_poll_and_clears_on_exchange_change(self):
        def fail(*_):
            raise ValueError('Importer failed')
        inbox = transport.Inbox(self.root, fail)
        inbox.heartbeat()
        self.publisher.publish('SM_Test', send=True)
        inbox.poll()
        self.publisher.poll()
        report = self.snapshot()
        self.assertFalse(report['result']['ok'])
        self.assertEqual('Importer failed', report['result']['error'])
        self.publisher.set_exchange(self.root / 'new')
        report = self.snapshot()
        self.assertIsNone(report['last_request_id'])
        self.assertIsNone(report['result'])

    def test_stale_or_malformed_receiver_and_response(self):
        inbox = transport.Inbox(self.root, lambda *_: {})
        inbox.heartbeat()
        self.publisher.publish('SM_Test', send=True)
        core.atomic_json(self.root / 'receiver.json', {'running': True, 'heartbeat': 0, 'session': 'old'})
        report = self.snapshot()
        self.assertFalse(report['receiver_online'])
        self.assertEqual('old', report['receiver']['session'])
        (self.root / 'receiver.json').write_text('[]')
        (self.root / 'responses' / (self.publisher.request_id + '.json')).write_text('{')
        report = self.snapshot()
        self.assertFalse(report['receiver_online'])
        self.assertIn('unavailable', report['result'])

    def test_blender_copy_operator_preserves_pending_request(self):
        bpy = ModuleType('bpy')
        bpy.types = SimpleNamespace(Operator=type('Operator', (), {}), Panel=type('Panel', (), {}))
        bpy.props = SimpleNamespace(BoolProperty=lambda **_: None)
        bpy.path = SimpleNamespace(abspath=lambda value: value)
        inbox = transport.Inbox(self.root, lambda *_: {})
        inbox.heartbeat()
        self.publisher.publish('SM_Test', send=True)
        before = dict(self.publisher.__dict__)
        context = SimpleNamespace(scene=SimpleNamespace(w7_bridge_exchange=str(self.root / 'other')),
                                  window_manager=SimpleNamespace(clipboard=''))
        with patch.dict(sys.modules, {'bpy': bpy}):
            module = importlib.import_module('week07_bridge.blender_ui')
            try:
                module._client = self.publisher
                operator = module.W7_OT_diagnostics()
                operator.report = lambda *_: None
                with patch.object(module, 'client', side_effect=AssertionError('must not switch exchange')):
                    self.assertEqual({'FINISHED'}, operator.execute(context))
                report = json.loads(context.window_manager.clipboard)
                self.assertEqual(before['request_id'], report['pending_request_id'])
                self.assertNotEqual(report['exchange'], report['configured_exchange'])
                self.assertEqual(before, self.publisher.__dict__)
            finally:
                sys.modules.pop('week07_bridge.blender_ui', None)


if __name__ == '__main__':
    unittest.main()
