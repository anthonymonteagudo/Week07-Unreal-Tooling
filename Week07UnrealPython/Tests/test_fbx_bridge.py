"""Contract and IPC failure tests; no DCC imports required."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Content/Python'))
from week07_bridge import core, transport
from week07_bridge.client import Publisher


class Adapter:
    def __init__(self, host='blender', fail=False):
        self.host, self.fail = host, fail

    def inspect_selection(self):
        return dict(host=self.host, source_file='', object_name='Wedge', mesh_count=1,
                    face_count=6, dimensions_cm=[120, 60, 180])

    def export_fbx(self, path):
        if self.fail:
            raise RuntimeError('Exporter failed')
        path.write_bytes(b'test double, not an actual FBX' * 4)


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def publish(self, **kwargs):
        return core.publish(Adapter(**kwargs), self.root)

    def test_hosts_share_contract_and_stable_destination(self):
        first = self.publish(host='maya')
        second = self.publish(host='blender')
        a, _ = core.load_manifest(first, self.root)
        b, _ = core.load_manifest(second, self.root)
        for key in ('schema_version', 'asset_name', 'destination_path', 'asset_type', 'dimensions_cm'):
            self.assertEqual(a[key], b[key])
        self.assertNotEqual(a['revision'], b['revision'])
        self.assertTrue(first.exists())

    def test_failed_export_never_commits_manifest_or_request(self):
        with self.assertRaisesRegex(RuntimeError, 'Exporter'):
            self.publish(fail=True)
        self.assertEqual(list(self.root.rglob('manifest.json')), [])
        self.assertFalse((self.root / 'requests').exists())

    def test_changed_fbx_is_rejected(self):
        manifest = self.publish()
        data, fbx = core.load_manifest(manifest, self.root)
        fbx.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'changed'):
            core.load_manifest(manifest, self.root)

    def test_bad_targets_rejected_before_export(self):
        for name, destination in [('Cube', core.DESTINATION), ('SM_A', '/Game/Elsewhere'),
                                  ('SM_../B', core.DESTINATION), ('SM_A', core.DESTINATION + '/../Other')]:
            with self.subTest(name=name, destination=destination), self.assertRaises(ValueError):
                core.publish(Adapter(), self.root, name, destination)
        self.assertFalse((self.root / 'publishes').exists())

    def test_manifest_escape_and_unsupported_schema(self):
        path = self.publish()
        for change in ({'filename': '../../evil.fbx'}, {'schema_version': 2}, {'schema_version': True},
                       {'dimensions_cm': [float('nan'), 1, 1]}, {'asset_type': 'SkeletalMesh'}):
            original = core.read_json(path)
            path.write_text(json.dumps(dict(original, **change)))
            with self.assertRaises(ValueError):
                core.load_manifest(path, self.root)
            core.atomic_json(path, original)
        with self.assertRaises(ValueError):
            core.load_manifest(self.root / '../manifest.json', self.root)

    def test_live_send_ack_and_no_replay(self):
        calls = []
        def importer(path, root):
            calls.append(path)
            return {'asset_path': '/Game/Week07/Bridge/SM_BridgeProp.SM_BridgeProp'}
        inbox = transport.Inbox(self.root, importer)
        inbox.heartbeat()
        publisher = Publisher(Adapter(), self.root)
        publisher.publish('SM_BridgeProp', send=True)
        identity = publisher.request_id
        self.assertIsNone(publisher.poll())
        self.assertTrue(inbox.poll()['ok'])
        self.assertTrue(publisher.poll()['ok'])
        self.assertIn('Imported:', publisher.message)
        self.assertIsNone(inbox.poll())
        self.assertEqual(len(calls), 1)
        self.assertTrue(transport.response(identity, self.root)['ok'])

    def test_offline_publish_can_be_sent_later(self):
        publisher = Publisher(Adapter(), self.root)
        with self.assertRaisesRegex(RuntimeError, 'offline'):
            publisher.publish('SM_BridgeProp', send=True)
        self.assertTrue(publisher.manifest.is_file())
        inbox = transport.Inbox(self.root, lambda *_: {'asset_path': 'test'})
        inbox.heartbeat()
        publisher.send()
        self.assertTrue(inbox.poll()['ok'])

    def test_stale_heartbeat_and_previous_session(self):
        first = transport.Inbox(self.root, lambda *_: self.fail('Should not import'))
        first.heartbeat()
        manifest = self.publish()
        identity = transport.send(manifest, self.root)
        second = transport.Inbox(self.root, lambda *_: self.fail('Should not import'))
        self.assertFalse(second.poll()['ok'])
        self.assertIn('session changed', transport.response(identity, self.root)['error'])
        with patch('week07_bridge.transport.time.time', return_value=__import__('time').time() + 30):
            self.assertIsNone(transport.receiver_status(self.root))

    def test_unknown_command_never_calls_importer(self):
        inbox = transport.Inbox(self.root, lambda *_: self.fail('Should not import'))
        core.atomic_json(self.root / 'requests/bad.json', {'id': 'bad', 'action': 'exec', 'code': 'bad'})
        self.assertFalse(inbox.poll()['ok'])

    def test_import_failure_reaches_client(self):
        def failure(*args):
            raise RuntimeError('FBX import failed')
        inbox = transport.Inbox(self.root, failure)
        inbox.heartbeat()
        publisher = Publisher(Adapter(), self.root)
        publisher.publish('SM_BridgeProp', send=True)
        self.assertFalse(inbox.poll()['ok'])
        self.assertFalse(publisher.poll()['ok'])
        self.assertEqual(publisher.message, 'Unreal error: FBX import failed')


if __name__ == '__main__':
    unittest.main()
