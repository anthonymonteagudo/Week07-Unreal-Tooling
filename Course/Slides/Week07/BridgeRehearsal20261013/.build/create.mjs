import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const work=path.resolve('..');
const source=path.resolve('../../FinalClass20261013/output/Week_7_Final_Class_v3.pptx');
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const p=await PresentationFile.importPptx(await FileBlob.load(source));
await fs.writeFile('template-layout.ndjson',(await p.inspect({kind:'layout',maxChars:12000})).ndjson);
p.slides.keep([0]);
const sl=p.slides.add({layoutId:'/ppt/slideLayouts/slideLayout6.xml'});
sl.background.fill='#FFFFFF';
function text(str,x,y,w,h,size=30,color='#17151F',bold=false){
 const t=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 t.text=str;t.text.style={typeface:'Arial',fontSize:size,color,bold};return t;
}
text('WEEK 7',94,60,1100,35,20,'#6550A2',true);
text('Blender uses the same Unreal handoff',94,131,1100,95,46,'#17151F',true);
text('Before: 180 cm',94,236,510,34,25,'#6550A2',true);
text('After: 220 cm',658,236,528,34,25,'#6550A2',true);
for(const [file,x] of [['03-unreal-before.png',94],['07-unreal-both-updated.png',658]]){
 sl.images.add({blob:new Uint8Array(await fs.readFile(path.join(work,'assets',file))),contentType:'image/png',
  alt:file.startsWith('03')?'Actual Unreal baseline: two blue Blender placements, 180 cm tall':'Actual Unreal result: both blue Blender placements now 220 cm tall',
  fit:'contain',position:{left:x,top:278,width:528,height:310},
  crop:{left:185/1288,right:(1288-959)/1288,top:137/726,bottom:(726-686)/726}});
}
text('New host adapter. Shared FBX + JSON contract and Unreal receiver.',94,598,1092,30,22,'#777080');
text('Why did both placements change after one publish?',94,632,1092,40,23,'#6550A2',true);
text('WEEK 7',94,677,300,23,15,'#777080');text('10B',1130,677,75,23,15,'#777080');
sl.speakerNotes.text=`Here is the same handoff from Blender. The blue props are two placements of one Unreal mesh asset. The orange props came through Maya and give us a comparison.

I select the four roof vertices in Blender and move them up forty centimetres. The base and origin stay in place. Back in Object Mode, I click Publish and Send. The button exports an FBX and a JSON manifest, then asks the Unreal receiver to import that revision. The acknowledgement confirms that Unreal accepted it.

Watch both blue placements. They become taller together because both reference the same asset. We did not replace either actor. The orange meshes remain unchanged at 180 centimetres.

The host-specific work is selection, geometry evaluation and FBX export. Blender uses bpy and evaluated meshes. Maya uses its own scene and FBX APIs. The naming rules, revision handling, manifest, send operation and Unreal receiver stay shared. Which values must remain stable for this update to reach the intended asset?

Facilitation: insert after current slide 13, stable anchor 10, in Week_7_Final_Class_v3. Allow 60–90 seconds or use the GIF fallback. Open index.html beside this companion for the capture sequence. The GIF is an animation of actual UI stills, not continuous video. Source scene: BridgeCompare_UI_Rehearsal.blend. Reset by publishing BridgeCompare.blend before repeating. Do not confuse material shading differences with mesh dimensions.

Evidence: actual Blender 5.1.1 and Unreal 5.7.4 UI rehearsal, 2026-10-13. Capture files 03-unreal-before.png and 07-unreal-both-updated.png use the same camera and lighting, cropped to the viewport. verification.json confirms two existing actors reference SM_Compare_Blender, with height 220 cm and unit actor scales. Original baseline acknowledgement reports 180 cm.

Sources: independently authored week07_bridge implementation; Karol Kowalczyk / Tech Art Corner course import-task and remote-call examples consulted locally, not redistributed. https://www.udemy.com/course/unreal-engine-5-python-automation/
Requested broader character-workflow reference: https://www.youtube.com/watch?v=5Liq0JckHqA . This lesson covers static meshes, not the video's rigging/animation workflow.
Review anchor: 10B`;
p.slides.keep([1]);
await fs.mkdir(path.join(work,'output'),{recursive:true});
await (await PresentationFile.exportPptx(p)).save('candidate.pptx');
await fs.writeFile(path.join(work,'slide-preview.png'),new Uint8Array(await (await sl.export({format:'png',scale:1})).arrayBuffer()));
await fs.writeFile(path.join(work,'speaker-notes.txt'),sl.speakerNotes.text);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const result=await finalizePresentation({workspaceDir:work,candidatePath:path.join(work,'.build/candidate.pptx'),finalPath:path.join(work,'output/Blender_Unreal_Bridge_Companion.pptx'),
 explicitTotalSlideCount:1,pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],
 fontPolicy:{basis:'reference',families:['Arial'],referencePath:source,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex')},
 verifyArtifactToolImport:true,receiptPath:path.join(work,'.build/validation.json')});
console.log(result.finalPath);
