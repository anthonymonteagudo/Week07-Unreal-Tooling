assert qt.result_present and not qt.apply_button.isEnabled()
qt.resize(1120,900)
record('Live Qt material Apply')
s=EVIDENCE['steps'][-1]
assert s['cubes']['W07_Crate_Target']['material'].endswith('MI_Crate_Qt.MI_Crate_Qt')
assert s['cubes']['W07_Crate_Protected']['material'].startswith('/Engine/BasicShapes/')
cap=unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(REHEARSAL/'captures/material-result.png'),delay=.3,force_game_view=True)
