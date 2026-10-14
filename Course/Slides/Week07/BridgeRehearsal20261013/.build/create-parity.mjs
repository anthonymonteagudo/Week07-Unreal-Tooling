import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const work=path.resolve('..');
const source=path.resolve('../../CheckpointDeck20261013/output/Week_7_Runnable_API_Checkpoints_v8.pptx');
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const p=await PresentationFile.importPptx(await FileBlob.load(source));
p.slides.keep([0]);
const sl=p.slides.add({layoutId:'/ppt/slideLayouts/slideLayout6.xml'});
sl.background.fill='#EFF9F6';
function text(str,x,y,w,h,size=28,color='#17151F',bold=false){
 const t=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=str;t.text.style={typeface:'Arial',fontSize:size,color,bold};return t;
}
text('03  API calls in working tools',94,60,1100,35,20,'#096962',true);
text('Maya and Blender: one publishing pipeline',94,131,1100,70,44,'#17151F',true);
text('Shared: Publisher, FBX + JSON, request / acknowledgement, Unreal import',94,218,1092,60,27,'#096962',true);
const rows=[
 ['Host-specific work','Blender','Maya'],
 ['Scene access','bpy; evaluated mesh copy','cmds; duplicate, freeze copy'],
 ['Units and pivot','Scene scale to cm; origin','Require cm; rotate pivot'],
 ['FBX export','bpy.ops.export_scene.fbx','fbxmaya / MEL FBXExport'],
 ['UI and timer','Native sidebar; bpy timer','PySide6 dialog; QTimer']
];
const table=sl.tables.add({rows:5,columns:3,left:94,top:291,width:1092,height:285,columnWidths:[256,418,418],values:rows});
table.borders.assign({fill:'#D9D2E5',width:1});
for(let r=0;r<5;r++){
 table.rows[r].height=57;
 for(let c=0;c<3;c++){
  const cell=table.getCell(r,c);cell.fill=r===0?'#DBEFEA':'#EFF9F6';
  cell.text.style={typeface:'Arial',fontSize:24,color:r===0?'#096962':'#17151F',bold:r===0};
 }
}
text('Stable asset path: one reimport updates both existing placements.',94,596,1092,40,27,'#17151F',true);
text('Which code stays unchanged? What would you like to trace together?',94,641,1092,32,23,'#096962',true);
text('WEEK 7  /  BR-PARITY',94,677,600,23,15,'#777080');
sl.speakerNotes.text=`Both buttons call the same Publisher class. We do not maintain a Blender copy of the naming rules, JSON writer, transport or Unreal importer. We substitute BlenderAdapter for MayaAdapter. Each adapter has just two entry points: inspect_selection and export_fbx.

Blender reads a selected object through bpy and evaluates its modifiers into a disposable mesh. Maya reads a mesh transform through cmds, duplicates it and freezes the duplicate. Neither path applies those changes to the original mesh. Blender converts its scene scale to centimeters and uses the object origin. Maya requires centimeter working units and uses the rotate pivot. The adapter handles axis conversion before the shared receiver sees the asset.

Now follow the click. The shared core validates, exports the FBX, hashes it and commits the JSON manifest. Send queues a request for the running receiver session. Unreal checks that pair, imports into the stable asset path, verifies dimensions and saves. A response travels back to the publisher. Sent means queued. Imported means the receiver reported success.

The two placed props share one Unreal asset. Keep the name and destination stable and a new revision updates both placements without replacing either Actor. Try the matching roof edit in Maya: forty centimeters on Y. In the supplied Blender scene it was point four meters on Z. Both revised assets should be 220 centimeters high.

The status and recovery rules are shared as well. Publish alone never sends. A failed export cannot leave an older revision selected for sending. While an acknowledgement is pending, another send is blocked. Changing the exchange folder clears local tracking; it does not cancel work already queued in the old folder.

One qualification: parity here means the same publishing contract and intended geometry. FBX triangulation and smoothing can differ. The screenshots show different smoothing, so compare shape, dimensions and pivot separately from shading.

Which code stays unchanged when we switch applications? What would you like us to trace together before the live revision?

Facilitation: latest reference is Week_7_Runnable_API_Checkpoints_v8. Use after slide 18 / stable anchor 10, or as a reference during slide 22 / anchor 10D. Keep the 150-minute schedule: allocate 60 seconds within the existing four-minute bridge demo, including 20 seconds for student questions, rather than extending the lesson. Expected answer: Publisher, core, transport and receiver. Trace a requested boundary, then return to the two-instance update. Open Week07UnrealPython/Docs/Bridge/parity.html for the exercise. Existing main lecture deck is unchanged.

Evidence: project-owned week07_bridge/client.py, core.py, transport.py, blender_adapter.py, maya_adapter.py, blender_ui.py, maya_ui.py and unreal_receiver.py. Earlier verification.json records real import/reimport from both hosts and two-instance updates. Blender has actual UI rehearsal captures; Maya has background integration and offscreen UI evidence, not a full interactive UI rehearsal. Current client changes passed ordinary Python regression tests, not a new live engine rehearsal.

Review anchor: BR-PARITY`;
p.slides.keep([1]);
await (await PresentationFile.exportPptx(p)).save('parity-candidate.pptx');
await fs.writeFile(path.join(work,'parity-preview.png'),new Uint8Array(await (await sl.export({format:'png',scale:1})).arrayBuffer()));
await fs.writeFile(path.join(work,'parity-speaker-notes.txt'),sl.speakerNotes.text);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const result=await finalizePresentation({workspaceDir:work,candidatePath:path.join(work,'.build/parity-candidate.pptx'),finalPath:path.join(work,'output/Maya_Blender_Bridge_Parity_v2.pptx'),
 explicitTotalSlideCount:1,requiredNativeTableOwnerSlides:[1],pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','1'],
 fontPolicy:{basis:'reference',families:['Arial'],referencePath:source,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex')},
 verifyArtifactToolImport:true,receiptPath:path.join(work,'.build/parity-validation-v2.json')});
console.log(result.finalPath);
