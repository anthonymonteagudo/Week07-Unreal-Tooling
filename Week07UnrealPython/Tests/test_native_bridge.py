"""Test the native-widget Python contract using offline data; no engine or Qt."""
from pathlib import Path
import sys
import json
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Content/Python'))
from week07_tooling.editor import native_bridge as bridge
from week07_tooling.ui.offline_backend import OfflineBackend


class NativeBridgeTests(unittest.TestCase):
    def setUp(self):
        self.backend = OfflineBackend()
        self.session = bridge.open_session(self.backend)

    def tearDown(self):
        bridge.close_all()

    def test_workflow_and_pin_types(self):
        bridge.dispatch(self.session, 'select_demo')
        view = bridge.dispatch(self.session, 'preview')
        self.assertTrue(view['can_apply'])
        self.assertEqual(view['change_count'], 6)
        self.assertIn('W07_Crate_01', view['preview_text'])
        self.assertTrue(all(type(v) in (str, int, bool) for v in view.values()))
        view = bridge.dispatch(self.session, 'apply')
        self.assertFalse(view['can_apply'])
        self.assertIn('Missing mesh reference', view['validation_text'])

    def test_stale_selection_rejected(self):
        bridge.dispatch(self.session, 'select_demo')
        bridge.dispatch(self.session, 'preview')
        self.backend.selected.pop()
        view = bridge.dispatch(self.session, 'apply')
        self.assertFalse(view['ok'])
        self.assertFalse(view['can_apply'])
        self.assertEqual(self.backend.records[0]['label'], 'prop_temp_1')

    def test_expired_session_and_unsupported_action_fail_closed(self):
        self.assertFalse(bridge.dispatch(self.session, '__dict__')['ok'])
        bridge.close_session(self.session)
        view = bridge.dispatch(self.session, 'apply')
        self.assertFalse(view['session_valid'])
        self.assertFalse(view['can_apply'])

    def test_two_tabs_do_not_share_preview(self):
        other = bridge.open_session(self.backend)
        bridge.dispatch(self.session, 'select_demo')
        bridge.dispatch(self.session, 'preview')
        self.assertFalse(bridge.dispatch(other, 'apply')['ok'])

    def test_reset_requires_explicit_confirmation(self):
        self.backend.records[0]['label'] = 'custom'
        self.assertFalse(bridge.dispatch(self.session, 'reset')['ok'])
        self.assertEqual(self.backend.records[0]['label'], 'custom')
        self.assertTrue(bridge.dispatch(self.session, 'reset', reset_confirmed=True)['ok'])
        self.assertEqual(self.backend.records[0]['label'], 'prop_temp_1')

    def test_workflow_bridge_and_reload_expiry(self):
        from week07_tooling.workflow_sample import SampleBackend
        session = bridge.open_workflow_session(SampleBackend())
        result = json.loads(bridge.dispatch_workflow(session, 'preview', 'vfx',
                            json.dumps({'preset': 'steam_demo', 'scale': 1.0})))
        self.assertTrue(result['can_apply'])
        result = json.loads(bridge.dispatch_workflow(session, 'apply'))
        self.assertTrue(result['ok'])
        bridge.close_all()
        self.assertFalse(json.loads(bridge.dispatch_workflow(session, 'apply'))['ok'])

    def test_workflow_invalid_json_does_not_keep_old_plan(self):
        from week07_tooling.workflow_sample import SampleBackend
        session = bridge.open_workflow_session(SampleBackend())
        bridge.dispatch_workflow(session, 'preview', 'vfx', '{"preset":"steam_demo","scale":1}')
        self.assertFalse(json.loads(bridge.dispatch_workflow(session, 'preview', 'vfx', 'bad json'))['can_apply'])
        self.assertFalse(json.loads(bridge.dispatch_workflow(session, 'apply'))['ok'])

    def test_prop_and_assistant_sessions_cannot_apply_each_others_plans(self):
        from week07_tooling.workflow_sample import SampleBackend
        sample = SampleBackend()
        workflow = bridge.open_workflow_session(sample)
        bridge.dispatch(self.session, 'select_demo')
        bridge.dispatch(self.session, 'preview')
        bridge.dispatch_workflow(workflow, 'preview', 'vfx', '{"preset":"steam_demo","scale":1}')
        self.assertFalse(bridge.dispatch(workflow, 'apply')['ok'])
        self.assertFalse(json.loads(bridge.dispatch_workflow(self.session, 'apply'))['ok'])
        self.assertEqual(sample.effects, [])
        self.assertEqual(self.backend.records[0]['label'], 'prop_temp_1')
        self.assertTrue(bridge.dispatch(self.session, 'apply')['ok'])
        self.assertTrue(json.loads(bridge.dispatch_workflow(workflow, 'apply'))['ok'])
        self.assertEqual(len(sample.effects), 3)
        bridge.close_all()
        self.assertFalse(bridge.dispatch(self.session, 'apply')['session_valid'])
        self.assertFalse(json.loads(bridge.dispatch_workflow(workflow, 'apply'))['ok'])
