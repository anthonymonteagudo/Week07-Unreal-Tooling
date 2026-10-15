# Additional live interaction guards through the real widget event handlers.
qt.preview_button.click()
assert 'already occupies' in qt.status.text() and not qt.apply_button.isEnabled()
assert qt.grab().save(str(REHEARSAL/'captures/qt-vfx-duplicate.png'))
assert unreal.Week07EditorLibrary.undo_demo()
record('Live Qt VFX Undo')
assert not EVIDENCE['steps'][-1]['effects']
qt.preview_button.click();assert qt.apply_button.isEnabled()
actor_sub.set_selected_level_actors([])
qt.apply_button.click()
assert 'Apply stopped' in qt.status.text() and not qt.apply_button.isEnabled()
record('Live stale-selection Apply blocked without mutation')
assert not EVIDENCE['steps'][-1]['effects']
assert qt.grab().save(str(REHEARSAL/'captures/qt-stale-block.png'))
qt.preview_button.click()
assert 'Needs attention' in qt.status.text() and not qt.apply_button.isEnabled()
print('LIVE GUARDS:',qt.status.text())
qt.tabs.setCurrentIndex(0);qt.name.setText('MI_Crate_Final');live_demo.select_material()
