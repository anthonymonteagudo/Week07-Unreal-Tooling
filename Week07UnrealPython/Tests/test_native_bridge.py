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


class NativePanelWorkflowTests(unittest.TestCase):
    def setUp(self):
        from week07_tooling.workflow_sample import SampleBackend
        self.backend = SampleBackend()
        self.identity = bridge.open_workflow_session(self.backend)

    def tearDown(self):
        bridge.close_all()

    def dispatch(self, action):
        from week07_tooling.editor.native_panel import dispatch
        return json.loads(dispatch(json.dumps({'action': action, 'session': self.identity,
                          'kind': 'material', 'name': 'MI_Regression', 'slot': 0})))

    def test_selection_is_visible_without_approving_mutations(self):
        result = self.dispatch('selection')
        self.assertTrue(result['presentation']['rows'])
        self.assertFalse(result['can_apply'])
        self.assertFalse(self.dispatch('apply')['ok'])
        self.assertFalse(self.backend.created)

    def test_invalid_slot_keeps_actor_and_reason_then_recovers(self):
        self.backend.materials.update(targets=[], mixed_selection=True,
            selection_errors=['Cube: slot 4 is unavailable. Available slots: 0.'],
            selection_rows=[['Cube', 'Invalid target', 'Available slots: 0.']])
        result = self.dispatch('preview')
        self.assertFalse(result['can_apply'])
        self.assertIn('slot 4', result['message'])
        self.assertEqual(result['presentation']['rows'][0][0], 'Cube')
        self.assertFalse(self.dispatch('apply')['ok'])
        self.backend.reset_practice()
        self.assertTrue(self.dispatch('preview')['can_apply'])
        self.assertTrue(self.dispatch('apply')['ok'])
        self.assertIn('MI_Regression', self.backend.created)

    def test_failed_texture_validation_retains_selection_and_clears_plan(self):
        self.assertTrue(self.dispatch('preview')['can_apply'])
        self.backend.materials['textures'].pop()
        result = self.dispatch('preview')
        self.assertFalse(result['can_apply'])
        self.assertTrue(result['presentation']['rows'])
        self.assertFalse(self.dispatch('apply')['ok'])
        self.assertFalse(self.backend.created)

    def test_refresh_invalidates_previous_approval(self):
        self.assertTrue(self.dispatch('preview')['can_apply'])
        self.assertFalse(self.dispatch('selection')['can_apply'])
        self.assertFalse(self.dispatch('apply')['ok'])
        self.assertTrue(self.dispatch('preview')['can_apply'])
        self.assertTrue(self.dispatch('apply')['ok'])
