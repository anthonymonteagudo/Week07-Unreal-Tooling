"""Behavior gate shared by every UI stage. No Qt or Unreal required."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Content/Python'))
from week07_tooling.ui.controller import ToolController
from week07_tooling.ui.offline_backend import OfflineBackend


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.backend = OfflineBackend()
        self.tool = ToolController(self.backend)
        self.tool.refresh()

    def preview(self):
        self.tool.select_demo()
        self.tool.preview()

    def test_empty_selection_cannot_apply(self):
        self.tool.preview()
        self.assertFalse(self.tool.can_apply)
        with self.assertRaises(ValueError):
            self.tool.apply()

    def test_preview_read_only_apply_verified_and_consumed(self):
        self.tool.select_demo()
        before = deepcopy(self.backend.records)
        self.tool.preview()
        self.assertEqual(self.backend.records, before)
        self.assertEqual(self.tool.change_count, 6)
        self.assertEqual(self.tool.apply(), 6)
        self.assertFalse(self.tool.can_apply)
        self.assertEqual([r['issues'] for r in self.tool.report if r['issues']], [['MISSING_MESH']])
        self.tool.preview()
        self.assertFalse(self.tool.can_apply)

    def test_selection_scene_and_mesh_changes_invalidate_plan(self):
        changes = [lambda b: b.selected.pop(),
                   lambda b: b.records[0].update(label='changed'),
                   lambda b: b.records[0]['location'].append(100),
                   lambda b: b.records[0].update(has_mesh=False)]
        for change in changes:
            with self.subTest(change=change):
                backend = OfflineBackend()
                tool = ToolController(backend)
                tool.select_demo()
                tool.preview()
                change(backend)
                self.assertTrue(tool.refresh())
                self.assertFalse(tool.can_apply)
                with self.assertRaises(ValueError):
                    tool.apply()

    def test_context_loss_invalidates_plan_and_report(self):
        self.preview()
        with patch.object(self.backend, 'snapshot', side_effect=RuntimeError('Wrong map')):
            with self.assertRaises(RuntimeError):
                self.tool.refresh()
        self.assertIsNone(self.tool.snapshot)
        self.assertFalse(self.tool.can_apply)
        self.assertEqual(self.tool.report, [])

    def test_backend_failure_consumes_plan(self):
        self.preview()
        with patch.object(self.backend, 'apply', side_effect=RuntimeError('Collision')):
            with self.assertRaises(RuntimeError):
                self.tool.apply()
        self.assertFalse(self.tool.can_apply)

    def test_verification_failure_does_not_claim_apply_failed(self):
        self.preview()
        with patch.object(self.backend, 'check', side_effect=RuntimeError('Fixture changed')):
            self.assertEqual(self.tool.apply(), 6)
        self.assertIn('Applied 6 changes, but verification failed', self.tool.message)
        self.assertEqual(self.tool.tone, 'error')
        self.assertFalse(self.tool.can_apply)

    def test_mixed_selection_rejected_and_reset_requires_new_preview(self):
        self.backend.selected = ['sample://unrelated']
        with self.assertRaises(ValueError):
            self.tool.preview()
        self.assertFalse(self.tool.can_apply)
        self.preview()
        self.tool.reset()
        self.assertFalse(self.tool.can_apply)


if __name__ == '__main__':
    unittest.main()
