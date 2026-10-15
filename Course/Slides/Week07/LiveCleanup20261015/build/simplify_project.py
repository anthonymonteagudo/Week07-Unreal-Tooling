from pathlib import Path
import json
r=Path('Week07UnrealPython').resolve(); a=(r.parent/'Course/InstructorArchive/Week07/20261015').resolve();a.mkdir(parents=True,exist_ok=True)
assert a.is_relative_to(r.parent/'Course') and not a.is_relative_to(r)
# Move duplicated guidance out of the student project; keep recoverable instructor history.
import shutil
moved=[]
for rel in ['Docs','START_HERE.txt','lesson_materials/week_07_unreal_python/SEQUENCING.md','lesson_materials/week_07_unreal_python/stage_05_ui_progression/README.md']:
    src=(r/rel).resolve();dst=a/rel
    assert src.is_relative_to(r) and src.exists() and not dst.exists()
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(src),str(dst));moved.append(rel)
shutil.copy2(r/'README.md',a/'README-before.md')
for p in (r/'Scripts').rglob('*.py'):
    s=p.read_text(encoding='utf-8-sig')
    s=s.replace('Docs/Bridge','Saved/Rehearsal/Bridge').replace('Main Material/VFX demo route: Docs/DEMO_SEQUENCE.md','Main Material/VFX demo route: README.md')
    p.write_text(s,encoding='utf-8')
p=r/'AGENTS.md';s=p.read_text(encoding='utf-8').replace('Recommended native path and pending asset work: `Docs/UI/UNREAL_NATIVE_UI.md`.','Native implementation: `Plugins/Week07Tools`; current student route: `README.md`.').replace('See `Docs/UI/MATERIAL_VFX_SCOPE.md`.','The prepared map and allowed operations are described in `README.md`.');p.write_text(s,encoding='utf-8')
p=r/'Content/Python/week07_tooling/ui/assistant_style.py';s=p.read_text(encoding='utf-8').replace('Docs/UI/UX_STYLE_SHEET.md','Course/InstructorArchive/Week07/20261015/Docs/UI/UX_STYLE_SHEET.md (workspace root)');p.write_text(s,encoding='utf-8')
for p in (r/'lesson_materials').rglob('*.md'):
    s=p.read_text(encoding='utf-8').replace('../../Docs/Students/START_HERE.md','../../README.md').replace('../../Docs/DEMO_SEQUENCE.md','../../README.md').replace('`Docs/Bridge`','the instructor run sheet')
    p.write_text(s.replace(' — ', ': ').replace('—','; '),encoding='utf-8')
for p in [r/'.vscode/tasks.json',r/'Week07PythonTools.code-workspace']:
    if p.exists():p.write_text(p.read_text(encoding='utf-8').replace('—',':'),encoding='utf-8')
# Student bridge archive contains runtime launchers and one quick start, no historical audits or capture tooling.
p=r/'Scripts/bridge/package_students.py';s=p.read_text(encoding='utf-8').replace(", 'Saved/Rehearsal/Bridge'",'').replace("files.append(ROOT / 'Tests/test_fbx_bridge.py')", "files.append(ROOT / 'Tests/test_fbx_bridge.py')\nfiles = [p for p in files if p.parent != ROOT/'Scripts/bridge' or p.name in ('open_blender.py','open_maya.py')]")
s=s.replace("'prepare_bridge_demo.py', 'capture_bridge_demo.py'", "'prepare_bridge_demo.py'")
s=s.replace('Read Saved/Rehearsal/Bridge/README.md for both source-application launchers.','Use the launchers below for your source application.').replace("The guide's instructor machine path is an example: substitute this extracted\nfolder.","Use the paths inside this extracted folder.")
p.write_text(s,encoding='utf-8')
(a/'relocations.json').write_text(json.dumps({'moved_from_student_project':moved,'reason':'Remove redundant supplementary student documentation; retained for instructor provenance.'},indent=2),encoding='utf-8')
print('Archived redundant project docs:',moved)
