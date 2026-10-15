import fs from 'node:fs';
import {S,sections,catalog,checkpoint} from '../../MaterialsWalkthrough20261013/.build/content.mjs';
export {S,sections,catalog,checkpoint};
const prior=JSON.parse(fs.readFileSync(new URL('../../MaterialsWalkthrough20261013/slide_sources.json',import.meta.url),'utf8'));
export const slides=prior.slides.map((s,i)=>({...structuredClone(s),sourceNumber:i+2}));
const notes=fs.readFileSync(new URL('../../BridgeRehearsal20261013/parity-speaker-notes.txt',import.meta.url),'utf8').split('\n\nFacilitation:')[0].trim();
const parity={
 id:'BR-PARITY',title:'Maya and Blender: one publishing pipeline',section:'demos',tag:sections.demos.name,parity:true,
 subtitle:'Shared: Publisher, FBX + JSON, request / acknowledgement, Unreal import',
 table:[['Host-specific work','Blender','Maya'],['Scene access','bpy; evaluated mesh copy','cmds; duplicate, freeze copy'],['Units and pivot','Scene scale to cm; origin','Require cm; rotate pivot'],['FBX export','bpy.ops.export_scene.fbx','fbxmaya / MEL FBXExport'],['UI and timer','Native sidebar; bpy timer','PySide6 dialog; QTimer']],
 caption:'Stable asset path: one reimport updates both existing placements.',
 question:'Which code stays unchanged? What would you like to trace together?',
 notes,refs:[],
 local:['Week07UnrealPython/Docs/Bridge/parity.html','Course/Slides/Week07/BridgeRehearsal20261013/output/Maya_Blender_Bridge_Parity_v2.pptx'],
 facilitation:'Use 40 seconds to compare the adapters and 20 seconds for questions. This minute comes from the former four-minute bridge demo. Continue through the import API slides, then run the three-minute bridge revision. Blender has UI rehearsal evidence; Maya has recorded API integration and offscreen UI evidence, not a complete interactive UI rehearsal.'
};
slides.splice(slides.findIndex(s=>s.id==='10')+1,0,parity);
const minutes=Object.fromEntries(prior.timing.map(t=>[t.id,t.minutes]));
minutes['BR-PARITY']=1;minutes['10D']-=1;
let elapsed=0;
export const timing=[{id:'01',title:'Week 7',section:'intro'},...slides.filter(s=>!s.hidden)].map(s=>{
 const duration=minutes[s.id];if(duration===undefined)throw Error('Missing time '+s.id);
 const row={id:s.id,title:s.title,section:s.section,minutes:duration,start:elapsed,end:elapsed+duration};elapsed+=duration;return row;
});
if(elapsed!==150)throw Error('Timing '+elapsed);
for(const s of slides){const t=timing.find(t=>t.id===s.id);s.facilitation=(s.facilitation||'').replace(/ Time: .*$/s,'')+(t?` Time: ${t.minutes} min; elapsed ${t.start}–${t.end}.`:'');}
export const bindings=slides.flatMap((s,i)=>s.checkpoint?[{slide:i+2,anchor:s.id,...s.checkpoint,hidden:!!s.hidden}]:[]);
