assert unreal.Week07EditorLibrary.capture_tools(str(REHEARSAL/'captures/native-vfx-preview.png'))
record('Native VFX preview: no effects created')
assert not EVIDENCE['steps'][-1]['effects']
