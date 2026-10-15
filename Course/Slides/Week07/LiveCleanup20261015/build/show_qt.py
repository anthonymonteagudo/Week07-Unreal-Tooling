from week07_tooling.ui import host
print(qt.geometry(),qt.frameGeometry())
qt.move(100,100);qt.resize(1000,800);qt.show();qt.raise_();qt.activateWindow()
cap=unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(REHEARSAL/'captures/material-baseline.png'),delay=.5,force_game_view=True)
