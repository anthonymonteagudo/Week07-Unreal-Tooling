assert unreal.Week07EditorLibrary.capture_tools(str(REHEARSAL/'captures/native-vfx-duplicate.png'))
assert unreal.Week07EditorLibrary.undo_demo()
record('Native VFX Undo: batch removed')
assert not EVIDENCE['steps'][-1]['effects']
print(live_demo.select_material())
import week07_tools as w7
qt=w7.show_assistants()
qt.name.setText('MI_Crate_Qt')
