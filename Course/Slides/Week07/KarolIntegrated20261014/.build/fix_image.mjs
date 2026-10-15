import fs from 'node:fs/promises';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
const p=await PresentationFile.importPptx(await FileBlob.load('candidate.pptx'));
const s=p.slides.items[42];s.images.items[0].position={left:94+(1092-1092*320/380)/2,top:220,width:1092*320/380,height:320};
await (await PresentationFile.exportPptx(p)).save('candidate.pptx');
await fs.writeFile('../previews/slide-043.png',new Uint8Array(await (await s.export({format:'png',scale:1})).arrayBuffer()));
