assert qt.session.pending and qt.apply_button.isEnabled()
assert qt.grab().save(str(REHEARSAL/'captures/qt-material-preview.png'))
record('Live Qt material preview')
