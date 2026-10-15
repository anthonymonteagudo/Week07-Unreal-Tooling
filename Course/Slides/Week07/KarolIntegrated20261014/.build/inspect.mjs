import fs from 'node:fs/promises';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('../../UnrealFirst20261013/output/Week_7_Python_in_Unreal_v13.pptx'));
await fs.writeFile('inspect.ndjson',(await p.inspect({kind:'slide,textbox,table,notes,layout',maxChars:1000000})).ndjson);
const rows=p.slides.items.map((s,i)=>({number:i+1,id:s.id,hidden:s.hidden,shapes:s.shapes.items.map(t=>({id:t.id,text:String(t.text),position:t.position})),notes:s.speakerNotes.text}));
await fs.writeFile('shapes.json',JSON.stringify(rows,null,2));
console.log('Inspected',rows.length);
for(const n of [10,13,21,23,29,61,75,106])await fs.writeFile(`before-${n}.png`,new Uint8Array(await (await p.slides.items[n-1].export({format:'png',scale:1})).arrayBuffer()));
