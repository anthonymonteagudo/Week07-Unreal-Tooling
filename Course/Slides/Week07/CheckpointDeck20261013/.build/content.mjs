import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {S as priorS,slides as prior,timing as priorTiming,sections as priorSections} from '../../SectionsAndAPI20261013/.build/content.mjs';
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../../../..');
const lessonRoot=path.join(repo,'Week07UnrealPython/lesson_materials/week_07_api_checkpoints');
export const catalog=JSON.parse(fs.readFileSync(path.join(lessonRoot,'sequence.json'),'utf8')).steps;
export const S={...priorS};
export const sections={...priorSections,blender:{name:'02  Blender API comparison',color:'#93551E',tint:'#FFF5E8'},demos:{name:'03  API calls in working tools',color:'#096962',tint:'#EFF9F6'},contributors:{...priorSections.contributors,name:'04  Contributor demos'},lab:{...priorSections.lab,name:'05  Lab 1: tool assessment'},ux:{...priorSections.ux,name:'06  UI/UX for artist tools'},prep:{...priorSections.prep,name:'07  Peer-test preparation'},peer:{...priorSections.peer,name:'08  Lab 2: peer testing'},synthesis:{...priorSections.synthesis,name:'09  Reflection'}};
const map=new Map(prior.map((s,i)=>[s.id,{...structuredClone(s),sourceNumber:i+2}]));
function extract(step){const text=fs.readFileSync(path.join(lessonRoot,step.file),'utf8');const blocks={};let key=null;for(const line of text.split(/\r?\n/)){if(line.startsWith('# %% ')){key=line.slice(5).trim();blocks[key]=[];}else if(key)blocks[key].push(line);}return Object.fromEntries(Object.entries(blocks).map(([k,v])=>[k,v.join('\n').trim()]));}
export function checkpoint(id){return catalog.find(s=>s.id===id);}
function lesson(anchor,id,blocks,explain,question,mode='focus',hidden=false){
 const step=checkpoint(id),source=extract(step),old=map.get(anchor),code=blocks.map(b=>source[b]).join('\n\n');
 if(blocks.some(b=>!source[b]))throw Error('Missing block '+id);
 const preceding=step.blocks.slice(0,step.blocks.indexOf(blocks[0]));
 const dependency=mode==='complete'?'Complete checkpoint shown. No previous script required.':`First run ${id}: ${preceding.length?preceding.join(' + '):'no preceding blocks'}. Then run the shown block(s).`;
 const refs=step.references.map((url,i)=>{const key=id+'-'+i;S[key]=url;return key;});
 const s={id:anchor,title:`${id}: ${step.title}`,sourceNumber:old?.sourceNumber,hidden,api:true,code,explain,
 caption:`${step.host.toUpperCase()} / ${id} / ${blocks.join(' + ')} / ${mode==='complete'?'whole checkpoint':preceding.length?'after '+preceding.join(' + '):'start here'} / open source guide`,
 question,refs,section:old?.section||'appendix',
 local:['Week07UnrealPython/lesson_materials/week_07_api_checkpoints/'+step.file],
 checkpoint:{id,blocks,mode,preceding,file:step.file,dependency},
 notes:`${explain} ${dependency} ${step.expected} ${question} ${step.experiment}`,
 facilitation:`Host: ${step.host}. Before running: ${step.prerequisites} Recovery: ${step.recovery} Run the full saved checkpoint to jump here with a fresh namespace. Source: ${step.file}`};
 map.set(anchor,s);return s;
}
lesson('04','UE01',['setup','focus'],'One host check before any scene operation.','Which project did Unreal report?','complete');
map.set('04A',{...map.get('04A'),title:'One checkpoint, one run',code:'import week07_lessons\n\n# Optional launcher: runs the readable UE02 file.\nweek07_lessons.run("UE02")\n\n# Inspect the actual API code before running.\nprint(week07_lessons.source("UE02"))',explain:'Or execute the saved .py file. Each checkpoint repeats its setup. Copy buttons in the guide provide a complete runnable file.',caption:'Run in Unreal. The launcher is convenience, not the lesson implementation.',notes:'We will use one prepared file per topic, as we did in Week 3. Read the API lines, predict their result, run the checkpoint, and inspect the output. The launcher runs the actual file in a fresh namespace. You can also open the file with Execute Python Script. In Blender use its Text Editor. A Setup block prepares variables only within that file.',question:'What would you inspect before executing a checkpoint?',local:['Week07UnrealPython/Content/Python/week07_lessons.py'],refs:[]});
lesson('07','UE02',['setup','focus'],'Run, then change the Outliner selection and rerun.','What should an empty selection print?','complete');
lesson('07C','UE03',['focus'],'Setup reads the current Actor selection. This block inspects each component.','Can one Actor have zero mesh components?');
lesson('UE04','UE04',['setup','focus'],'This selection supplies assets, independently of the Outliner.','Which selection supplies textures to the material tool?','complete');
lesson('09G','UE05',['setup','focus'],'Read compression and sRGB. Non-texture selections are counted and skipped.','Would changing a shared texture affect more than one material?','complete');
lesson('09H','UE06',['focus'],'Setup defines textures, expected compression and counters. Check prints the final totals.','Why does zero checked not establish a pass?');
lesson('07A','UE07',['setup','focus'],'The filesystem path and Unreal object path name different things.','Does loading a mesh place it in the level?','complete');
map.set('SB',{id:'SB',title:'Blender API\ncomparison',transition:true,section:'blender',subtitle:'Same Python ideas, different host objects',next:'Selection, Object and shared mesh data',notes:'We will compare the same ideas in Blender. The language is familiar, but the host module and object model change. Open the prepared scene and inspect the small checkpoint files.'});
lesson('BL01','BL01',['setup','focus'],'Blender supplies bpy.context. Run this file in its Text Editor.','Which part of the selection loop stays familiar?','complete');
lesson('BL02','BL02',['setup','focus'],'An Object has a transform. Its mesh datablock may have several users.','What would editing shared mesh data affect?','complete');
lesson('10C','UE11',['options'],'UE11 Setup defines paths. These FbxImportUI options describe a static-mesh import.','Which setting prevents new materials from being imported?');
lesson('10A','UE11',['task'],'Run UE11 Setup and Options first. This block prepares a task without importing.','Which line would permit an overwrite?');
lesson('UE12','UE12',['focus'],'Run the full UE12 checkpoint. It repeats setup and refuses an existing destination.','Why restore the previous importer setting even after failure?');
lesson('09I','UE08',['focus'],'Run UE08 Setup and Eligibility first. The full file checks the resulting slot.','What happens if this material is already assigned?');
lesson('09F','PY01',['setup','focus'],'Ordinary Python teaching data. A changed target invalidates the reviewed copy.','Which line makes the preview stale?','complete');
lesson('09J','UE10',['focus'],'Setup reads selected Actors. Inspect the effects after the prepared VFX tool places them.','Does a system reference tell us its frame cost?');
lesson('09L','UE09',['focus'],'Setup validates one selected material instance. Read back its texture parameters.','Which returned path would you compare with the expected input?','focus',true);
lesson('BL03','BL03',['focus'],'Setup requires one mesh in Object Mode. Always release the temporary evaluated mesh.','Why can source and evaluated polygon counts differ?','focus',true);
lesson('BL04','BL04',['focus'],'Setup checks one mesh and creates a new temporary output folder. Check verifies the FBX exists.','What does file existence leave unverified?','focus',true);
lesson('UE11S','UE11',['setup'],'This is the real source file and destination used by UE11 and UE12.','Which path is on disk and which belongs to Unreal?','focus',true);
lesson('UE08S','UE08',['setup'],'Map and PIE checks precede any material edit.','Why identify the teaching map before changing a component?','focus',true);
lesson('UE08E','UE08',['eligibility'],'The guarded target and existing material are the inputs to UE08.','Which check protects the other cube?','focus',true);
lesson('UE12C','UE12',['check'],'UE12 verifies the returned asset identity, then prints bounds for inspection.','Does an imported mesh necessarily have the intended size?','focus',true);
// Make the limits of retained UI excerpts explicit.
for(const id of ['15G','15B','15F','A2']){const s=map.get(id);s.caption='Existing UI excerpt, not a standalone API checkpoint';s.notes+=' This UI fragment requires the surrounding widget instance. Use the checkpoint guide for independently runnable Unreal and Blender examples.';}
map.get('S1').subtitle='Checkpoint files: inspect the host, objects and properties';
map.get('S1').next='Predict. Run one step. Inspect. Change one input.';
map.get('S1A').title='API calls in\nworking tools';
map.get('S1A').subtitle='Prepared import, material and VFX demonstrations';
map.get('10').notes+=' The short BL01 and BL02 checkpoints explain the Blender host boundary. The production bridge additionally handles transformation, unit, pivot and transport concerns. Its complete publisher is the capstone, not the first API exercise.';
map.get('10D').notes+=' Use one prepared publisher for the live revision. The basic UE12 import checkpoint creates a separate unsaved lesson asset and does not replace this bridge’s reimport/acknowledgement contract.';
map.get('09').notes+=' UE08 separately demonstrates assignment of an already existing material. This full assistant also creates and verifies an instance. These are deliberately different scopes.';
map.get('09D').notes+=' Run UE10 afterward when you want to inspect the resulting component/system references directly.';
map.get('02').table=[['Time','Section'],['3:30–4:02','01 Unreal checkpoints, 02 Blender, 03 Working tools'],['4:02–4:37','04 Contributor demos'],['4:37–4:52','Break'],['4:52–5:00','05 Lab 1: tool assessment'],['5:00–5:20','06 UI/UX, 07 Task preparation'],['5:20–6:00','08 Peer testing, 09 Reflection']];
const opening=['02','S1','03','04','04A','07','07C','06A','UE04','09G','09H','07A','SB','BL01','BL02','S1A','10','10C','10A','UE12','10D','09I','09','09F','08A','09J','09D','09K'];
const liveRest=prior.filter(s=>!s.hidden&&!priorTiming.find(t=>t.id===s.id&&t.end<=32)).map(s=>s.id);
// The remainder begins with contributor demos, retaining the activity clock.
export const slides=opening.map(id=>map.get(id));
for(const id of liveRest)slides.push(map.get(id));
const seen=new Set(slides.map(s=>s.id));
slides.push(map.get('SX'));seen.add('SX');
for(const s of map.values())if(!seen.has(s.id)){s.hidden=true;s.section='appendix';slides.push(s);}
const times={'01':.25,'02':.5,S1:.25,'03':.5,'04':.5,'04A':.75,'07':1,'07C':1,'06A':1,UE04:.75,'09G':.75,'09H':1.25,'07A':.75,SB:.25,BL01:.75,BL02:.75,S1A:.25,'10':.5,'10C':.75,'10A':.75,UE12:.75,'10D':4,'09I':1.25,'09':4,'09F':.75,'08A':1,'09J':.75,'09D':4,'09K':2.25};
let elapsed=0;export const timing=[{id:'01',title:'Week 7',section:'intro'},...slides.filter(s=>!s.hidden)].map(s=>{let minutes=times[s.id]??priorTiming.find(t=>t.id===s.id)?.minutes;if(minutes===undefined)throw Error('No timing '+s.id);const t={id:s.id,title:s.title,section:s.section,minutes,start:elapsed,end:elapsed+minutes};elapsed+=minutes;return t;});
if(elapsed!==150)throw Error('Timing should be 150, got '+elapsed);
const pythonIDs=new Set(opening.slice(1,opening.indexOf('SB')));
for(const s of slides){
 if(opening.includes(s.id)){s.hidden=false;s.section=s.id==='02'?'intro':pythonIDs.has(s.id)?'python':['SB','BL01','BL02'].includes(s.id)?'blender':'demos';}
 s.tag=sections[s.section].name;
 const t=timing.find(t=>t.id===s.id);
 if(t)t.section=s.section;
 s.facilitation=(s.checkpoint?s.facilitation:'')+(s.hidden?' Optional reference, outside the 150-minute route.':` Time: ${t.minutes} min; elapsed ${t.start}–${t.end}. Run selected checkpoints at the named demonstration pauses, and trace the others. See the run sheet. Questions fit within this time.`);
}
export const bindings=slides.flatMap((s,i)=>s.checkpoint?[{slide:i+2,anchor:s.id,...s.checkpoint,hidden:!!s.hidden}]:[]);

