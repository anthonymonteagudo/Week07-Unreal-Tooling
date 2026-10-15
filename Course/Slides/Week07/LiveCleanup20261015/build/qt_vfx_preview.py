assert qt.session.pending and qt.apply_button.isEnabled()
assert qt.grab().save(str(REHEARSAL/'captures/qt-vfx-preview.png'))
record('Live Qt VFX preview')
