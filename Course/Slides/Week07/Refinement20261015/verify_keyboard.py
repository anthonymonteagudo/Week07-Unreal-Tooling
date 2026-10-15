"""Exercise actual Qt key events offscreen; this is not a desktop accessibility audit."""
from pathlib import Path
import os,sys,json
os.environ['QT_QPA_PLATFORM']='offscreen'
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT.parents[3]/'Week07UnrealPython/Content/Python'))
from week07_tooling.ui.dependencies import enable_qt
enable_qt()
from PySide6 import QtWidgets,QtCore,QtTest
from week07_tooling.ui.assistants import AssistantWindow
from week07_tooling.workflow_sample import SampleBackend
app=QtWidgets.QApplication([]);window=AssistantWindow(SampleBackend(),ui_stage=3)
window.show();app.processEvents();checks=[]
def check(label,value):checks.append({'label':label,'passed':bool(value)})
def key(k):QtTest.QTest.keyClick(app.focusWidget(),k);app.processEvents()
window.master.setFocus();app.processEvents()
for target,label in [(window.name,'name'),(window.slot,'slot'),(window.review,'review')]:
 key(QtCore.Qt.Key.Key_Tab);check('Material Tab reaches '+label,app.focusWidget() is target or target.isAncestorOf(app.focusWidget()))
for _ in range(10):
 if app.focusWidget() is window.preview_button:break
 key(QtCore.Qt.Key.Key_Tab)
check('Hidden VFX inputs and disabled Apply are skipped',app.focusWidget() is window.preview_button)
key(QtCore.Qt.Key.Key_Space);check('Space activates Preview',window.session.pending is not None and window.apply_button.isEnabled())
key(QtCore.Qt.Key.Key_Tab);check('Tab reaches enabled Apply',app.focusWidget() is window.apply_button)
key(QtCore.Qt.Key.Key_Space);check('Space applies once and disables repeat',len(window.session.backend.created)==1 and not window.apply_button.isEnabled())
window.name.setFocus();window.name.selectAll();QtTest.QTest.keyClicks(window.name,'MI_KeyboardReview');app.processEvents()
check('Typed input clears preview without undoing prior result',window.session.pending is None and len(window.session.backend.created)==1 and 'does not undo' in window.summary.text())
window.tabs.setCurrentIndex(1)
window.session.backend.effects.extend({'system':'sample://Other','source':'','location':[10000+i*200,0,0]} for i in range(6))
window.preview_button.setFocus();key(QtCore.Qt.Key.Key_Space)
check('Warning does not enable Apply',window.ack.isVisible() and not window.apply_button.isEnabled())
key(QtCore.Qt.Key.Key_Backtab);check('Shift Tab reaches warning acknowledgment',app.focusWidget() is window.ack)
key(QtCore.Qt.Key.Key_Space);check('Space acknowledges warning',window.ack.isChecked() and window.apply_button.isEnabled())
key(QtCore.Qt.Key.Key_Tab);key(QtCore.Qt.Key.Key_Tab);check('Forward Tab reaches Apply after acknowledgment',app.focusWidget() is window.apply_button)
window.close()
report={'mode':'Offscreen Qt key-event smoke check; sample backend only','checks':checks}
(OUT/'qa/keyboard-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
failed=[c for c in checks if not c['passed']];print(json.dumps({'checks':len(checks),'failed':failed},indent=2))
raise SystemExit(bool(failed))
