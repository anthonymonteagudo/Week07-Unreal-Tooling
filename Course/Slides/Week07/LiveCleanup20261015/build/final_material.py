qt.preview_button.click();assert qt.session.pending
assert qt.grab().save(str(REHEARSAL/'captures/qt-material-preview.png'))
# Final screenshot of the same Qt operation on the improved stage.
qt.apply_button.click();assert qt.result_present
assert qt.grab().save(str(REHEARSAL/'captures/qt-material-applied.png'))
record('Final Material capture: clean stage, new reviewed instance')
cap=unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(REHEARSAL/'captures/material-result.png'),delay=.3,force_game_view=True)
