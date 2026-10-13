"""Build a small, standalone UE 5.7 project with the same source, no copied core."""
from pathlib import Path
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Deliverables/Week07_Bridge_Student_Pack.zip'
OUT.parent.mkdir(parents=True, exist_ok=True)
files = []
for directory in ['Content/Python/week07_bridge', 'Samples/Bridge', 'Docs/Bridge', 'Scripts/bridge']:
    files.extend(p for p in (ROOT / directory).rglob('*') if p.is_file()
                 and '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.blend1'))
for name in ['SM_Compare_Blender.uasset', 'SM_Compare_Maya.uasset', 'M_BridgeBlender.uasset',
             'M_BridgeMaya.uasset', 'W07_BridgeComparison.umap']:
    files.append(ROOT / 'Content/Week07/Bridge' / name)
files.append(ROOT / 'Tests/test_fbx_bridge.py')
files.extend(ROOT / 'Scripts/editor' / name for name in [
    'bridge_smoke_test.py', 'bridge_live_test.py', 'bridge_portable_smoke.py',
    'prepare_bridge_demo.py', 'capture_bridge_demo.py'])
project = {'FileVersion': 3, 'EngineAssociation': '5.7', 'Category': 'Teaching',
           'Description': 'Maya and Blender publish through one FBX + JSON bridge.',
           'Plugins': [{'Name': name, 'Enabled': True} for name in
                       ['PythonScriptPlugin', 'EditorScriptingUtilities', 'ProceduralMeshComponent']]}
readme = '''WEEK 7: MAYA / BLENDER TO UNREAL

Extract this entire folder to a writable location before running.
Open Week07BridgeDemo.uproject with Unreal 5.7.4.
Read Docs/Bridge/README.md for both source-application launchers.

In Unreal's Output Log, select Python and run:
from week07_bridge import unreal_receiver; unreal_receiver.install_menu(); unreal_receiver.start()

Open Samples/Bridge/BridgeCompare.blend or BridgeCompare.ma in the matching host.
Run Scripts/bridge/open_blender.py (Blender Text Editor), or open_maya.py via
runpy.run_path (Maya Python Script Editor). Both publish to this folder's
Saved/BridgeExchange by default. Use Publish & Send, then inspect the result.

The package contains the identical bridge code from the teaching project.
The guide's instructor machine path is an example: substitute this extracted
folder. Unreal materials and the comparison map are included. After moving the
project, publish from the source app to establish the new local FBX source path.

Samples/Bridge/Handoffs contains inspectable example FBX + JSON pairs.
Those are reference copies; Publish creates new, valid exchange revisions.

Ordinary Python contract tests:
python -m unittest discover -s Tests -p test_fbx_bridge.py -v

Tested host versions: Blender 5.1.1, Maya 2027 (PySide6), Unreal 5.7.4.
Static meshes only. No additional pip packages or network service are required.
'''
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(files):
        archive.write(path, path.relative_to(ROOT).as_posix())
    archive.writestr('Week07BridgeDemo.uproject', json.dumps(project, indent=2))
    archive.writestr('Config/DefaultEngine.ini',
        '[/Script/EngineSettings.GameMapsSettings]\nEditorStartupMap=/Game/Week07/Bridge/W07_BridgeComparison\n')
    archive.writestr('START_HERE.txt', readme)
with zipfile.ZipFile(OUT) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(set(archive.namelist()))
print(str(OUT))
print(str(OUT.stat().st_size) + ' bytes')
