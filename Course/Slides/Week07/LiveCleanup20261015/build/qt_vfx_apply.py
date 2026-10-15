assert qt.result_present
assert qt.grab().save(str(REHEARSAL/'captures/qt-vfx-applied.png'))
record('Live Qt VFX Apply')
assert len(EVIDENCE['steps'][-1]['effects'])==3
cap=unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(REHEARSAL/'captures/vfx-result.png'),delay=.5,force_game_view=True)
