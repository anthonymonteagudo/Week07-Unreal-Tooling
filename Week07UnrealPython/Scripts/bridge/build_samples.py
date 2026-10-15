"""Run in a NEW background Blender or mayapy process; makes physical source files.

Blender: blender --background --factory-startup --python build_samples.py -- --host blender
Maya: mayapy build_samples.py --host maya
Never execute in the instructor's current scene: this creates a new sample scene.
"""
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'Content/Python'))
from week07_bridge import core, fixture


def main():
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', choices=['blender', 'maya'], required=True)
    options = parser.parse_args(args)
    folder = ROOT / 'Samples/Bridge'
    folder.mkdir(parents=True, exist_ok=True)
    if options.host == 'blender':
        import bpy
        if not bpy.app.background:
            raise RuntimeError('Run this builder in a separate background Blender process.')
        from week07_bridge.blender_adapter import BlenderAdapter
        from week07_bridge import blender_ui
        adapter = BlenderAdapter()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        blender_ui.register()
        obj = fixture.create_blender()
        bpy.ops.wm.save_as_mainfile(filepath=str(folder / 'BridgeCompare.blend'))
    else:
        import maya.standalone
        maya.standalone.initialize(name='python')
        import maya.cmds as cmds
        from week07_bridge.maya_adapter import MayaAdapter
        adapter = MayaAdapter()
        cmds.file(new=True, force=True)
        obj = fixture.create_maya()
        cmds.file(rename=str(folder / 'BridgeCompare.ma'))
        cmds.file(save=True, type='mayaAscii', force=True)
    exchange = ROOT / 'Saved/BridgeRehearsal'
    name = 'SM_Compare_' + options.host.title()
    before = adapter.inspect_selection()
    baseline = core.publish(adapter, exchange, name)
    assert adapter.inspect_selection() == before, 'Publish changed source/selection'
    if options.host == 'blender':
        for vertex in obj.data.vertices:
            if vertex.co.z > 0:
                vertex.co.z += .4
        obj.data.update()
        bpy.context.view_layer.update()
        bpy.ops.wm.save_as_mainfile(filepath=str(folder / 'BridgeCompare_Revised.blend'))
    else:
        for i in range(4, 8):
            cmds.move(0, 40, 0, obj + '.vtx[' + str(i) + ']', relative=True, objectSpace=True)
        cmds.file(rename=str(folder / 'BridgeCompare_Revised.ma'))
        cmds.file(save=True, type='mayaAscii', force=True)
    revised = core.publish(adapter, exchange, name)
    report = {'host': options.host, 'baseline': str(baseline), 'revised': str(revised),
              'baseline_dimensions_cm': before['dimensions_cm'],
              'revised_dimensions_cm': adapter.inspect_selection()['dimensions_cm']}
    core.atomic_json(exchange / (options.host + '_samples.json'), report)
    print(json.dumps(report, indent=2))
    if options.host == 'maya':
        maya.standalone.uninitialize()


if __name__ == '__main__':
    main()
