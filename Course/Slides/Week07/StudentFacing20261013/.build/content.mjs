import fs from 'node:fs';
import {catalog,checkpoint} from '../../IntegratedBridge20261013/.build/content.mjs';
export {catalog,checkpoint};
const data=JSON.parse(fs.readFileSync(new URL('../../IntegratedBridge20261013/slide_sources.json',import.meta.url),'utf8'));
export const S=data.sourceKeys,sections=data.sections,timing=data.timing;
export const slides=data.slides.map((s,i)=>({...structuredClone(s),sourceNumber:i+2}));
for(const s of slides){
 if(s.id==='03'){
  s.facilitation+=' Source images are historical course setup captures. Verify UI placement in the teaching engine before class.';
  s.caption='';
 }
 if(s.checkpoint){
  const c=s.checkpoint,host=c.id.startsWith('UE')?'Unreal':c.id.startsWith('BL')?'Blender':'Python';
  s.caption=c.mode==='complete'?`Run in ${host}. Complete example.`:
   c.preceding.length?`Run in ${host}. First run ${c.id}: ${c.preceding.join(', ')}.`:`Run in ${host}. Start with this setup.`;
 }
 if(['15G','15B','15F','A2'].includes(s.id))s.caption='Requires the surrounding widget class.';
 if(s.id==='04A')s.caption='Run one saved example in Unreal.';
}
export const bindings=slides.flatMap((s,i)=>s.checkpoint?[{slide:i+2,anchor:s.id,...s.checkpoint,hidden:!!s.hidden}]:[]);
