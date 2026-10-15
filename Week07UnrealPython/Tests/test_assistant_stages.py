"""Same Material/VFX operations and safety contract across presentation stages."""
from test_ui_widgets import QT_AVAILABLE
if QT_AVAILABLE:
    from PySide6 import QtWidgets
import unittest


@unittest.skipUnless(QT_AVAILABLE, 'Install requirements-ui.txt to run widget gates.')
class AssistantStageGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    def panel(self, stage):
        from week07_tooling.ui.assistants import AssistantWindow
        from week07_tooling.workflow_sample import SampleBackend
        window = AssistantWindow(SampleBackend(), ui_stage=stage)
        self.addCleanup(window.close)
        self.addCleanup(window.deleteLater)
        return window

    def test_gate_1_both_tasks_have_identical_plans_and_results(self):
        reference = {}
        for stage in (1, 2, 3):
            window = self.panel(stage)
            for tab, kind in enumerate(('material', 'vfx')):
                with self.subTest(stage=stage, kind=kind):
                    window.tabs.setCurrentIndex(tab)
                    self.assertFalse(window.apply_button.isEnabled())
                    window.preview_button.click()
                    plan = window.session.pending[3]
                    if stage == 1:
                        reference[kind] = plan
                        self.assertTrue(window.review.isReadOnly())
                        self.assertIn('Before:', window.review.toPlainText())
                    else:
                        self.assertEqual(plan, reference[kind])
                    self.assertTrue(window.apply_button.isEnabled())
                    window.apply_button.click()
                    self.assertIn('Completed', window.status.text())
                    self.assertFalse(window.apply_button.isEnabled())
                    if stage == 1:
                        self.assertIn('APPLIED RESULT', window.review.toPlainText())
                    window.preview_button.click()
                    self.assertFalse(window.apply_button.isEnabled())
                    self.assertIn('already exists' if kind == 'material' else 'already occupies', window.status.text())
            self.assertEqual(len(window.session.backend.created), 1)
            self.assertEqual(len(window.session.backend.effects), 3)
            window.reset_button.click()
            self.assertFalse(window.session.backend.created)
            self.assertFalse(window.session.backend.effects)

    def test_gate_1_invalid_inputs_and_stale_state_stop_every_stage(self):
        for stage in (1, 2, 3):
            with self.subTest(stage=stage):
                window = self.panel(stage)
                window.preview_button.click()
                window.slot.setValue(1)
                self.assertFalse(window.apply_button.isEnabled())
                window.preview_button.click()
                self.assertIn('only material slot 0', window.status.text())
                self.assertIsNone(window.session.pending)
                window.slot.setValue(0)
                window.preview_button.click()
                window.session.backend.materials['targets'][0]['material'] = 'sample://Changed'
                window.apply_button.click()
                self.assertIn('Apply stopped', window.status.text())
                self.assertFalse(window.session.backend.created)
                self.assertIsNone(window.session.pending)

    def test_gate_1_warning_and_hard_limit_never_depend_on_stage(self):
        for stage in (1, 2, 3):
            with self.subTest(stage=stage):
                window = self.panel(stage)
                window.tabs.setCurrentIndex(1)
                window.session.backend.effects.extend(
                    {'system': 'sample://Other', 'source': '', 'location': [10000 + i * 200, 0, 0]}
                    for i in range(6))
                window.preview_button.click()
                self.assertIn('Review needed', window.status.text())
                self.assertFalse(window.apply_button.isEnabled())
                window.ack.setChecked(True)
                self.assertTrue(window.apply_button.isEnabled())
                window.scale.setValue(0.5)
                self.assertFalse(window.apply_button.isEnabled())
                self.assertFalse(window.ack.isChecked())
                window.session.backend.vfx['profile']['max_new'] = 2
                window.preview_button.click()
                window.ack.setChecked(True)
                self.assertIn('Batch limit', window.status.text())
                self.assertFalse(window.apply_button.isEnabled())

    def test_gate_2_structured_review_preserves_the_same_information(self):
        from week07_tooling.workflow_presentation import describe_plan
        for stage in (2, 3):
            window = self.panel(stage)
            for tab in (0, 1):
                window.tabs.setCurrentIndex(tab)
                window.preview_button.click()
                expected = describe_plan(window.session.pending[3])
                self.assertEqual(window.summary.text(), expected['summary'])
                actual = [tuple(window.review.item(r, c).toolTip() for c in range(3))
                          for r in range(window.review.rowCount())]
                self.assertEqual(actual, expected['rows'])
                self.assertEqual(window.review.editTriggers(), QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
                window.apply_button.click()
                self.assertEqual(window.review.horizontalHeaderItem(2).text(), 'Result')

    def test_gate_3_progress_and_specific_action_explain_the_next_step(self):
        for stage in (1, 2, 3):
            window = self.panel(stage)
            self.assertEqual(window.steps.isHidden(), stage != 3)
            self.assertEqual(window.material_help.isHidden(), stage == 1)
            self.assertIn(f'Stage {stage}', window.mode.text())
            window.preview_button.click()
            self.assertIn('create instance' if stage == 3 else 'Apply', window.apply_button.text())
            window.tabs.setCurrentIndex(1)
            self.assertIsNone(window.session.pending)
            window.preview_button.click()
            self.assertIn('place 3 effects' if stage == 3 else 'Apply', window.apply_button.text())
            if stage == 3:
                self.assertIn('REVIEW PREVIEW', window.steps.text())
                window.apply_button.click()
                self.assertIn('CHECK RESULT', window.steps.text())

    def test_gate_3_input_edit_does_not_imply_undo_after_apply(self):
        window = self.panel(3)
        window.preview_button.click()
        window.apply_button.click()
        applied = window.session.backend.created.copy()
        self.assertTrue(applied)
        self.assertIn('already applied', window.apply_button.toolTip())
        window.name.setText('MI_Another_Review')
        self.assertEqual(window.session.backend.created, applied)
        self.assertIsNone(window.session.pending)
        self.assertFalse(window.apply_button.isEnabled())
        self.assertIn('does not undo', window.summary.text())
        self.assertIn('valid preview', window.apply_button.toolTip())
