import fs from 'node:fs/promises';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('../../AgendaRevision20261011/Week_7_Agenda_330_to_600.pptx'));
await fs.mkdir('reference',{recursive:true});
await fs.writeFile('reference/inspect.json',JSON.stringify(p.toProto(),null,2));
console.log((await p.inspect({kind:'layout',maxChars:1500})).ndjson);
for(let i=0;i<p.slides.items.length;i++){await fs.writeFile(`reference/${i+1}.png`,new Uint8Array(await (await p.slides.items[i].export({format:'png',scale:0.8})).arrayBuffer()));}
console.log('Rendered',p.slides.items.length);
