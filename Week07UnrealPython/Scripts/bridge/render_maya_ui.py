"""Offscreen PySide UI check in mayapy; does not open the Maya desktop."""
from pathlib import Path
import os
import sys
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'Content/Python'))
from PySide6 import QtWidgets, QtGui
app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
import maya.standalone
maya.standalone.initialize(name='python')
from week07_bridge import maya_ui
QtGui.QFontDatabase.addApplicationFont('C:/Windows/Fonts/segoeui.ttf')
window = maya_ui.show()
window.setFont(QtGui.QFont('Segoe UI', 10))
app.processEvents()
assert len(window.findChildren(QtWidgets.QPushButton)) == 5
out = ROOT / 'Docs/Bridge/maya-publisher.png'
out.parent.mkdir(parents=True, exist_ok=True)
assert window.grab().save(str(out))
window.close()
app.processEvents()
maya.standalone.uninitialize()
print(str(out))
