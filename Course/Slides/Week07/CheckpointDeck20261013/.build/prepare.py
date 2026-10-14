from pathlib import Path
import zipfile
import json
import xml.etree.ElementTree as ET

repo = Path(__file__).resolve().parents[5]
lesson = repo / 'Week07UnrealPython/lesson_materials/week_07_api_checkpoints'
replacements = {
 'options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)': 'mesh_type = unreal.FBXImportType.FBXIT_STATIC_MESH\noptions.set_editor_property("mesh_type_to_import", mesh_type)',
 '    raise RuntimeError("Open the Week07UnrealPython project with Samples included.")': '    raise RuntimeError("Open Week07UnrealPython with Samples included.")',
 '    unreal.SystemLibrary.execute_console_command(None, flag + " " + str(previous))': '    restore = flag + " " + str(previous)\n    unreal.SystemLibrary.execute_console_command(None, restore)',
 'if package + "." + asset_name not in paths or not isinstance(mesh, unreal.StaticMesh):': 'expected_path = package + "." + asset_name\nif expected_path not in paths or not isinstance(mesh, unreal.StaticMesh):',
 '    raise RuntimeError("Expected mesh missing. Inspect importer output and Content Browser.")': '    raise RuntimeError("Expected mesh missing. Inspect importer output.")',
 'print("Not saved. Inspect size, axes and pivot. Import is not a general Undo transaction.")': 'print("Not saved. Inspect size, axes and pivot.")\nprint("Import is not a general Undo transaction.")',
 'if level.is_in_play_in_editor() or map_path != "/Game/Week07/Maps/W07_MaterialVFXLab":': 'teaching_map = "/Game/Week07/Maps/W07_MaterialVFXLab"\nif level.is_in_play_in_editor() or map_path != teaching_map:',
 '    raise RuntimeError("The target must have one mesh component with slot zero.")': '    raise RuntimeError("Need one mesh component with slot zero.")',
 '    raise RuntimeError("Select one existing material in the Content Browser.")': '    raise RuntimeError("Select one material in the Content Browser.")',
}
for p in lesson.rglob('*.py'):
    t = p.read_text(encoding='utf-8-sig')
    for old, new in replacements.items():
        t = t.replace(old, new)
    p.write_text(t, encoding='utf-8')

here = Path(__file__).parent
p = here / 'build.mjs'
t = p.read_text(encoding='utf-8-sig').replace('1092,292,24,C.ink', '1092,300,23,C.ink').replace("typeface:'Consolas',fontSize:24", "typeface:'Consolas',fontSize:23")
p.write_text(t, encoding='utf-8')
old = here.parents[1] / 'SectionsAndAPI20261013/output/Week_7_Sections_and_Unreal_API_v7.pptx'
ns = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(old) as z:
    rows = [{'number':i,'text':'\n'.join(ET.fromstring(z.read(f'ppt/slides/slide{i}.xml')).itertext())} for i in []]
    for i in range(1,87):
        root = ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'))
        rows.append({'number':i,'text':'\n'.join(e.text or '' for e in root.findall('.//a:t',ns))})
(here.parent/'original-text.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')

p = here.parents[1] / 'SectionsAndAPI20261013/.build/review.mjs'
t = p.read_text(encoding='utf-8-sig').replace("../../FinalClass20261013/.build/content.mjs", "../../SectionsAndAPI20261013/.build/content.mjs")
t = t.replace('../FinalClass20261013/previews/', '../SectionsAndAPI20261013/previews/').replace('Original v3 slide', 'Previous v7 slide')
t = t.replace('Week_7_Sections_and_Unreal_API_v7.pptx', 'Week_7_Runnable_API_Checkpoints_v8.pptx')
t = t.replace('preserves the previous v3', 'preserves the previous v7').replace('49 live slides, 37 hidden references', '${1+slides.filter(s=>!s.hidden).length} live slides, ${slides.filter(s=>s.hidden).length} hidden references')
t = t.replace('<a href="audit.html">', '<a href="checkpoints.html">Runnable checkpoints and copy buttons</a><a href="audit.html">',1)
t = t.replace('<p><strong>Editing directions:</strong>', '${s.checkpoint?`<p><a href="checkpoints.html#${s.checkpoint.id}">Open ${s.checkpoint.id}: full runnable source and setup</a> — ${esc(s.checkpoint.dependency)}</p>`:""}<p><strong>Editing directions:</strong>')
t = t.replace('<h1>Week 7 teaching route</h1>', '<h1>Week 7 teaching route</h1><section><h2>Checkpoint rhythm</h2><p>Predict → run one prepared file → inspect the output → change one input → rerun. Execute UE01, UE02, UE05, UE06, BL01 and BL02 at their named pauses. Trace the other API slides before the prepared tool demonstrations; their complete runnable files are available in the guide. The denser opening remains 32 minutes, so do not execute every reference checkpoint live.</p><p>Before class: stage the teaching map and its material, textures and protected cube; stage Blender in Object Mode with one mesh. Open both hosts’ Python output and keep the source files ready. Read the prerequisites and recovery for each checkpoint. New checkpoint host execution still requires rehearsal; offline tests do not certify Unreal or Blender behavior.</p><a href="checkpoints.html">Runnable guide</a></section>')
(here/'review.mjs').write_text(t,encoding='utf-8')

