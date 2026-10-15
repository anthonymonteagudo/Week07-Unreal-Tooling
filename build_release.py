"""Build small student downloads from explicit teaching-file allowlists.

No editor launch, dependency install, source mutation or slide modification.
"""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / 'Week07UnrealPython'
OUT = ROOT / 'Releases'
SKIP = {'__pycache__', '.venv', '.deps', 'Saved', 'Intermediate', 'Binaries'}


def tree(base):
    return [p for p in base.rglob('*') if p.is_file() and
            not any(part in SKIP for part in p.relative_to(base).parts)
            and p.suffix not in {'.pyc', '.pdb', '.blend1'}
            and p.name != 'unreal.local.json']


def write_zip(path, entries):
    names = [name for name, _ in entries]
    assert len(names) == len(set(names)), 'Duplicate ZIP entry'
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(entries):
            assert not name.startswith('/') and '..' not in Path(name).parts
            info = zipfile.ZipInfo(name, (2026, 10, 15, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None


def build():
    OUT.mkdir(exist_ok=True)
    api = PROJECT / 'lesson_materials/week_07_api_checkpoints'
    classroom = [('Week07_Classroom/START_HERE.md', (ROOT / 'StudentMaterials/START_HERE.md').read_bytes())]
    classroom += [('Week07_Classroom/Handouts/' + p.name, p.read_bytes()) for p in (ROOT/'StudentMaterials').glob('*.pdf')]
    classroom += [('Week07_Classroom/Examples/' + p.relative_to(api).as_posix(), p.read_bytes()) for p in tree(api)]
    write_zip(OUT/'Week07_Classroom.zip', classroom)

    files = []
    for directory in ['Content/Python/week07_tooling', 'Content/Python/week07_bridge',
                      'Content/Week07', 'Samples/Bridge', 'lesson_materials',
                      'Plugins/Week07Tools/Source', 'Tests', '.vscode', 'Support']:
        files += tree(PROJECT/directory)
    # Recorded rehearsal exchanges are unnecessary to run or study the bridge.
    files = [p for p in files if 'UI-Rehearsal' not in p.parts and
             p.name not in {'W07_PythonLab.umap', 'BridgeCompare_UI_Rehearsal.blend'}]
    names = ['README.md', 'BRIDGE.md', 'Setup.ps1', 'requirements-ui.txt',
             'Week07UnrealPython.uproject', 'Week07PythonTools.code-workspace',
             'Plugins/Week07Tools/Week07Tools.uplugin', 'Config/Week07ToolPresets.json',
             'Config/DefaultEngine.ini', 'Content/Python/week07_tools.py',
             'Content/Python/week07_lessons.py', 'Content/Python/selection_demo.py']
    names += ['Scripts/'+n for n in ['dev.py', 'assistants.py', 'ui.py', 'ui_quality.py',
              'api_lessons.py', 'lessons.py', 'build_native.ps1', 'package_native.py',
              'bridge/open_blender.py', 'bridge/open_maya.py', 'editor/release_smoke.py']]
    files += [PROJECT/n for n in names]
    demo = [('Week07UnrealPython/'+p.relative_to(PROJECT).as_posix(), p.read_bytes()) for p in files]
    with zipfile.ZipFile(PROJECT/'Support/Week07Tools_Win64.zip') as z:
        for name in ['UnrealEditor-Week07Tools.dll', 'UnrealEditor.modules']:
            demo.append(('Week07UnrealPython/Plugins/Week07Tools/Binaries/Win64/'+name, z.read(name)))
    assert not any('/Northwood/' in n or '/Course/' in n for n,_ in demo)
    for name,data in demo:
        assert not data.startswith(b'version https://git-lfs.github.com/spec/v1'), 'Fetch real LFS content: '+name
    write_zip(OUT/'Week07_Demo_Windows_UE5.7.4.zip', demo)
    manifest = {'date': '2026-10-15', 'engine': '5.7.4', 'platform': 'Windows x64',
                'slides_modified': False, 'downloads': []}
    for name,entries in [('Week07_Classroom.zip',classroom),('Week07_Demo_Windows_UE5.7.4.zip',demo)]:
        p=OUT/name
        manifest['downloads'].append({'file':name,'bytes':p.stat().st_size,
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'files':len(entries)})
        print(name, p.stat().st_size, 'bytes',len(entries),'files')
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')


if __name__ == '__main__': build()
