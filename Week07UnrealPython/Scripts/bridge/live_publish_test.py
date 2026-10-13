"""Run in background Blender/mayapy while bridge_live_test.py runs in Unreal."""
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'Content/Python'))
from week07_bridge import core, fixture
from week07_bridge.client import Publisher

host = sys.argv[-1]
exchange = ROOT / 'Saved/BridgeLiveTest'
if host == 'blender':
    import bpy
    assert bpy.app.background
    from week07_bridge.blender_adapter import BlenderAdapter
    bpy.ops.wm.read_factory_settings(use_empty=True)
    from week07_bridge import blender_ui
    blender_ui.register()
    # Registration itself is checked in real Blender, not a bpy stub.
    assert hasattr(bpy.types, 'W7_PT_bridge')
    publisher = Publisher(BlenderAdapter(), exchange)
    create = fixture.create_blender
else:
    import maya.standalone
    maya.standalone.initialize(name='python')
    import maya.cmds as cmds
    from week07_bridge.maya_adapter import MayaAdapter
    publisher = Publisher(MayaAdapter(), exchange)
    create = fixture.create_maya
results = []
for revised in (False, True):
    create(revised)
    publisher.publish('SM_Live_' + host.title(), send=True)
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        result = publisher.poll()
        if result:
            assert result['ok'], result
            results.append(result)
            break
        time.sleep(.2)
    else:
        raise TimeoutError(publisher.message)
core.atomic_json(exchange / (host + '_client_result.json'), {'status': 'PASS', 'results': results})
print(host + ': two publishes acknowledged by Unreal')
if host == 'maya':
    maya.standalone.uninitialize()
