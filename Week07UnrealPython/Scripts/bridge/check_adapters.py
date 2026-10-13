"""Real-host preservation checks. Run only in new background Blender/mayapy."""
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'Content/Python'))
from week07_bridge import fixture

host = sys.argv[-1]
if host == 'blender':
    import bpy
    from week07_bridge.blender_adapter import BlenderAdapter
    assert bpy.app.background
    bpy.ops.wm.read_factory_settings(use_empty=True)
    obj = fixture.create_blender()
    obj.location = (4, 2, 1)
    obj.rotation_euler.z = .3
    obj.scale = (2, 1, 1)
    modifier = obj.modifiers.new('Teaching bevel', 'BEVEL')
    modifier.width = .02
    adapter = BlenderAdapter()
    def state():
        return (list(bpy.data.objects), list(bpy.data.meshes), list(bpy.context.selected_objects),
                bpy.context.view_layer.objects.active, bpy.context.scene.unit_settings.scale_length,
                tuple(obj.matrix_world), len(obj.modifiers), [tuple(v.co) for v in obj.data.vertices])
    bpy.context.view_layer.update()
else:
    import maya.standalone
    maya.standalone.initialize(name='python')
    import maya.cmds as cmds
    from week07_bridge.maya_adapter import MayaAdapter
    obj = fixture.create_maya()
    cmds.move(400, 100, 200, obj)
    cmds.rotate(0, 20, 0, obj)
    cmds.scale(2, 1, 1, obj)
    # Load once before state capture; exporter plugin initialization is intentional.
    cmds.loadPlugin('fbxmaya', quiet=True)
    adapter = MayaAdapter()
    def state():
        return (cmds.ls(type='transform'), cmds.ls(selection=True),
                cmds.xform(obj, query=True, worldSpace=True, matrix=True),
                cmds.file(query=True, modified=True), cmds.undoInfo(query=True, state=True))
before = state()
with tempfile.TemporaryDirectory() as temporary:
    adapter.export_fbx(Path(temporary) / 'fixture.fbx')
    assert state() == before, 'Export changed source scene state'
print(host + ': evaluated/transformed mesh export preserves source scene state')
if host == 'maya':
    maya.standalone.uninitialize()
