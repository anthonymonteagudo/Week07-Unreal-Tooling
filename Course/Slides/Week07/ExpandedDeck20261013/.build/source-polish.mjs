import fs from 'node:fs/promises';
import {L} from './source-labels.mjs';
for(const file of ['build.mjs','companion.mjs']){
let s=await fs.readFile(file,'utf8');s="import {L} from './source-labels.mjs';\n"+s;
if(file==='build.mjs')s=s.replace('${esc(k)}</a>','${esc(L[k]||k)}</a>');
else s=s.replace('url,title:k,origin:', 'url,title:L[k]||k,origin:');
await fs.writeFile(file,s);
}
let s=await fs.readFile('../index.html','utf8');for(const [k,label]of Object.entries(L))s=s.replaceAll(`>${k}</a>`,`>${label}</a>`);await fs.writeFile('../index.html',s);
s=await fs.readFile('diagrams.mjs','utf8');const sentence='Use these ink-colored diagrams on white or light backgrounds; the purple preview is supplied by the page, not baked into the PNG.';s=s.replace(sentence+' '+sentence,sentence);await fs.writeFile('diagrams.mjs',s);
