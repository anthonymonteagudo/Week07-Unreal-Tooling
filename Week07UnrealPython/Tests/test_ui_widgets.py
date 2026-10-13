"""Actual Qt widgets, rendered offscreen. Never opens a desktop window or Unreal."""
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Content/Python'))
from week07_tooling.ui.dependencies import enable_qt, configure_headless_fonts

try:
    enable_qt()
    from PySide6 import QtCore, QtWidgets
    from week07_tooling.ui.window import ToolWindow
    from week07_tooling.ui.offline_backend import OfflineBackend
    QT_AVAILABLE = True
except RuntimeError:
    QT_AVAILABLE = False


@unittest.skipUnless(QT_AVAILABLE, 'Install requirements-ui.txt to run widget gates.')
class WidgetGates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        configure_headless_fonts(cls.app)

    def panel(self, stage):
        window = ToolWindow(OfflineBackend(), stage)
        window.timer.stop()
        window.show()
        self.app.processEvents()
        self.addCleanup(window.close)
        self.addCleanup(window.deleteLater)
        return window

    def test_gate_1_functional_all_stages(self):
        for stage in (1, 2, 3):
            with self.subTest(stage=stage):
                window = self.panel(stage)
                self.assertFalse(window.apply_button.isEnabled())
                window.select_button.click()
                window.preview_button.click()
                self.assertTrue(window.apply_button.isEnabled())
                window.apply_button.click()
                self.assertFalse(window.apply_button.isEnabled())
                self.assertEqual(len(window.controller.report), 6)
                self.assertIn('1 fixture prop still has issues', window.status.text())
                self.assertEqual(window.controller.tone, 'warning')

    def test_gate_2_review_tables_and_stale_recovery(self):
        for stage in (2, 3):
            window = self.panel(stage)
            window.select_button.click()
            window.preview_button.click()
            self.assertEqual(window.view.preview.rowCount(), 6)
            self.assertEqual(window.view.preview.item(0, 0).text(), 'prop_temp_1')
            self.assertEqual(window.view.preview.item(0, 1).text(), 'W07_Crate_01')
            self.assertEqual(window.view.preview.editTriggers(), QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
            window.controller.backend.selected.pop()
            window.poll()
            self.assertFalse(window.apply_button.isEnabled())
            self.assertEqual(window.view.preview.rowCount(), 0)
            self.assertIn('Preview again', window.status.text())

    def test_gate_3_filter_does_not_change_apply_scope(self):
        window = self.panel(3)
        window.select_button.click()
        window.preview_button.click()
        window.view.filter.setText('does not exist')
        self.assertIn('0 of 6', window.view.counts.text())
        self.assertEqual(window.controller.change_count, 6)
        self.assertIn('6 reviewed changes', window.apply_button.text())
        window.apply_button.click()
        self.assertEqual(window.controller.change_count, 0)
        self.assertTrue(window.copy_button.isEnabled())
        window.view.filter.clear()
        self.assertEqual(window.view.validation.rowCount(), 6)

    def test_gate_3_reset_cancel_is_non_destructive(self):
        window = self.panel(3)
        window.select_button.click()
        window.preview_button.click()
        with patch.object(QtWidgets.QMessageBox, 'question', return_value=QtWidgets.QMessageBox.StandardButton.Cancel):
            window.reset_button.click()
        self.assertTrue(window.apply_button.isEnabled())
        with patch.object(QtWidgets.QMessageBox, 'question', return_value=QtWidgets.QMessageBox.StandardButton.Yes):
            window.reset_button.click()
        self.assertFalse(window.apply_button.isEnabled())

    def test_gate_3_keyboard_controls_and_minimum_size(self):
        window = self.panel(3)
        window.resize(760, 570)
        self.app.processEvents()
        for button in (window.select_button, window.refresh_button, window.validate_button,
                       window.preview_button, window.apply_button):
            self.assertNotEqual(button.focusPolicy(), QtCore.Qt.FocusPolicy.NoFocus)
            self.assertTrue(button.accessibleName())
            self.assertGreaterEqual(button.width(), button.minimumSizeHint().width())
        self.assertTrue(window.status.wordWrap())

    def test_close_stops_polling(self):
        window = self.panel(3)
        window.timer.start()
        window.close()
        self.assertFalse(window.timer.isActive())

    def test_assistants_review_apply_and_input_invalidation(self):
        from week07_tooling.ui.assistants import AssistantWindow
        from week07_tooling.workflow_sample import SampleBackend
        window = AssistantWindow(SampleBackend())
        self.addCleanup(window.close)
        self.addCleanup(window.deleteLater)
        self.assertFalse(window.apply_button.isEnabled())
        window.preview_button.click()
        self.assertTrue(window.apply_button.isEnabled())
        window.name.setText('MI_New')
        self.assertFalse(window.apply_button.isEnabled())
        window.preview_button.click()
        window.apply_button.click()
        self.assertIn('created one instance', window.status.text())
        self.assertEqual(window.review.horizontalHeaderItem(2).text(), 'Applied change')
        self.assertGreater(window.review.rowCount(), 0)
        self.assertFalse(window.apply_button.isEnabled())
        window.tabs.setCurrentIndex(1)
        self.assertFalse(window.apply_button.isEnabled())
        window.preview_button.click()
        self.assertTrue(window.apply_button.isEnabled())
        window.apply_button.click()
        window.preview_button.click()
        self.assertFalse(window.apply_button.isEnabled())
        self.assertIn('already occupies', window.status.text())

    def test_assistants_invalid_practice_slot_blocks_apply_and_recovers(self):
        from week07_tooling.ui.assistants import AssistantWindow
        from week07_tooling.workflow_sample import SampleBackend
        backend = SampleBackend()
        window = AssistantWindow(backend)
        self.addCleanup(window.close)
        self.addCleanup(window.deleteLater)
        window.preview_button.click()
        self.assertTrue(window.apply_button.isEnabled())
        window.slot.setValue(1)
        window.preview_button.click()
        self.assertFalse(window.apply_button.isEnabled())
        self.assertEqual(window.review.rowCount(), 0)
        self.assertIn('only material slot 0', window.status.text())
        self.assertFalse(backend.created)
        window.slot.setValue(0)
        window.preview_button.click()
        self.assertTrue(window.apply_button.isEnabled())
        window.apply_button.click()
        self.assertEqual(len(backend.created), 1)

    def test_assistants_practice_reset_and_warning_gate(self):
        from week07_tooling.ui.assistants import AssistantWindow
        from week07_tooling.workflow_sample import SampleBackend
        backend = SampleBackend()
        window = AssistantWindow(backend)
        self.addCleanup(window.close)
        window.tabs.setCurrentIndex(1)
        backend.effects.extend({'system': 'sample://Other', 'source': '', 'location': [10000 + i * 200, 0, 0]}
                               for i in range(6))
        window.preview_button.click()
        self.assertFalse(window.apply_button.isEnabled())
        self.assertEqual(window.status.property('tone'), 'warning')
        window.ack.setChecked(True)
        self.assertTrue(window.apply_button.isEnabled())
        window.apply_button.click()
        self.assertEqual(len(backend.effects), 9)
        window.reset_button.click()
        self.assertEqual(backend.effects, [])
        self.assertFalse(window.apply_button.isEnabled())
        window.preview_button.click()
        self.assertTrue(window.apply_button.isEnabled())
        self.assertFalse(window.ack.isChecked())

    def test_assistants_unconfigured_choices_and_keyboard_layout(self):
        from week07_tooling.ui.assistants import AssistantWindow
        from week07_tooling.workflow_sample import SampleBackend
        backend = SampleBackend()
        with patch.object(backend, 'options', return_value={'materials': [], 'vfx': []}):
            window = AssistantWindow(backend)
        self.addCleanup(window.close)
        self.assertFalse(window.preview_button.isEnabled())
        self.assertFalse(window.apply_button.isEnabled())
        self.assertIn('Instructor setup needed', window.status.text())
        window.tabs.setCurrentIndex(1)
        self.assertFalse(window.preview_button.isEnabled())
        window.show()
        window.resize(800, 700)
        self.app.processEvents()
        for widget in (window.master, window.name, window.slot, window.preset, window.scale, window.apply_button):
            self.assertTrue(widget.accessibleName())
            self.assertNotEqual(widget.focusPolicy(), QtCore.Qt.FocusPolicy.NoFocus)
        for button in (window.preview_button, window.apply_button, window.reset_button):
            self.assertGreaterEqual(button.width(), button.minimumSizeHint().width())
        self.assertEqual(window.review.editTriggers(), QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


if __name__ == '__main__':
    unittest.main()
