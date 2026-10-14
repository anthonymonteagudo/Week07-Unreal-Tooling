import fs from 'node:fs/promises';
import {readFileSync} from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
import {S,slides,sections,timing,bindings} from './content.mjs';
const work=path.resolve('..'),repo=path.resolve('../../../../..');
process.env.RUNTIME_NODE_MODULES ||= 'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
await fs.mkdir(path.join(work,'output'),{recursive:true});
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const source=path.resolve('../../CheckpointDeck20261013/output/Week_7_Runnable_API_Checkpoints_v8.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(source));await fs.writeFile('source-layout.json',JSON.stringify(await p.inspect({kind:'layout',maxChars:100000})));p.slides.keep([0]);
const C={ink:'#17151F',purple:'#6550A2',muted:'#777080',light:'#F0EBFF'};
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function text(sl,str,x,y,w,h,size=30,color=C.ink,bold=false){const t=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=str;t.text.style={typeface:'Arial',fontSize:size,color,bold};return t;}
function img(sl,file,pos,crop){const ext=path.extname(file).toLowerCase();return sl.images.add({blob:new Uint8Array(readFileSync(path.join(repo,file))),contentType:ext==='.gif'?'image/gif':'image/png',alt:path.basename(file),fit:'contain',position:pos,...(crop?{crop}:{})});}
const tableOwners=[];
for(const [i,d] of slides.entries()){
 const palette=sections[d.section]; C.purple=palette.color;C.light=palette.tint;
 const sl=p.slides.add({layoutId:'/ppt/slideLayouts/slideLayout6.xml'});sl.background.fill=d.transition?palette.color:palette.tint;sl.hidden=!!d.hidden;
 if(d.transition){
  text(sl,d.tag,94,65,1080,38,24,'#FFFFFF',true);
  text(sl,d.title,94,190,1080,190,76,'#FFFFFF',true);
  text(sl,d.subtitle,94,433,1080,90,32,'#FFFFFF');
  text(sl,d.next,94,576,1080,65,26,'#FFFFFF');
  text(sl,`WEEK 7   /   ${i+2}`,94,677,1080,23,16,'#FFFFFF');
  sl.speakerNotes.text=d.notes+'\n\nFacilitation: '+d.facilitation;
  continue;
 }
 text(sl,d.tag,94,60,1100,35,20,C.purple,true);
 text(sl,d.title,94,125,1100,95,46,C.ink,true);
 text(sl,'WEEK 7  /  '+d.id,94,677,850,23,15,C.muted);
 text(sl,String(i+2),1130,677,75,23,15,C.muted);
 if(d.api){
  const t=text(sl,d.code,94,231,1092,300,23,C.ink);
  t.text.style={typeface:'Consolas',fontSize:23,color:C.ink};
  text(sl,d.explain.split(/\n+/).map(s=>s.trim().replace(/[.:]$/,'')).filter(Boolean).join('. ')+'.',94,532,1092,62,23,C.purple);
 }else if(d.divider){
  img(sl,d.image,{left:690,top:235,width:500,height:340},d.crop);
  (d.bullets||[]).forEach((b,j)=>text(sl,b,100,355+j*64,545,56,29));
 }else if(d.strips){
  d.strips.forEach((f,j)=>img(sl,f,{left:94,top:240+j*115,width:1092,height:84}));
  text(sl,d.bullets.join(' Â· '),94,510,1092,75,29);
 }else if(d.split){
  img(sl,d.image,{left:735,top:240,width:465,height:340},d.crop);
  if(d.code)text(sl,d.code,94,250,625,320,23);
  else (d.bullets||[]).forEach((b,j)=>text(sl,b,94,255+j*100,605,88,31));
 }else if(d.table){
  const h=d.table.length<=4?240:d.table.length<=6?305:340;
  const table=sl.tables.add({rows:d.table.length,columns:d.table[0].length,left:94,top:238,width:1092,height:h,values:d.table});
  for(let r=0;r<d.table.length;r++)for(let c=0;c<d.table[0].length;c++){const cell=table.getCell(r,c);cell.fill=r===0?C.light:'#FFFFFF';cell.text.style={typeface:'Arial',fontSize:24,bold:r===0,color:C.ink};}
  table.borders.assign({fill:'#8D8994',width:.8,style:'solid'});tableOwners.push(i+2);
  if(d.bullets)text(sl,d.bullets.join(' Â· '),94,238+h+15,1080,45,23);
 }else if(d.pair){
  img(sl,d.pair[0],{left:75,top:230,width:548,height:350});img(sl,d.pair[1],{left:653,top:230,width:548,height:350});
 }else if(d.image){
  if(d.side){
   const regions=d.id==='15'?[
    {top:.11,bottom:.77,left:.015,right:.34},
    {top:.417,bottom:.438,left:.018,right:.34},
    {top:.88,bottom:.055,left:.68,right:.018}
   ]:[{top:.11,bottom:.77,left:.015,right:.34},{top:.23,bottom:.675,left:.015,right:.34},{top:.88,bottom:.055,left:.68,right:.018}];
   regions.forEach((crop,j)=>img(sl,d.image,{left:94,top:238+j*115,width:745,height:103},crop));
   d.side.forEach((v,j)=>text(sl,v,880,250+j*115,305,90,28));
  }else if(d.detail==='upper')img(sl,d.image,{left:94,top:233,width:1092,height:355},{top:.025,bottom:.51,left:.012,right:.012});
  else img(sl,d.image,{left:94,top:220,width:1092,height:380},d.crop);
 }else if(d.code){
  const n=d.code.split('\n').length,h=n*32+12;
  text(sl,d.code,100,240,1080,h,27);
  if(d.bullets)text(sl,d.bullets.join('\n'),100,252+h,1080,110,26);
 }else if(d.links){
  for(const [j,[label,k]] of d.links.entries()){const t=text(sl,label,100,245+j*65,1080,52,30);t.text=[[{run:label,link:{uri:S[k],isExternal:true},style:{typeface:'Arial',color:C.purple}}]];}
 }else(d.bullets||[]).forEach((b,j)=>text(sl,b,100,260+j*90,1080,78,32));
 if(d.caption||d.credit){const cap=text(sl,d.credit||d.caption,94,599,d.mediaPath?815:1092,27,16,C.muted);if(d.checkpoint)cap.text=[[{run:d.caption,link:{uri:pathToFileURL(path.join(work,'checkpoints.html')).href+'#'+d.checkpoint.id,isExternal:true},style:{typeface:'Arial',color:C.muted}}]];}
 if(d.mediaPath){const t=text(sl,'Play companion clip',915,599,278,27,18,C.purple,true);t.text=[[{run:'Play companion clip',link:{uri:pathToFileURL(path.join(repo,d.mediaPath.split('#')[0])).href+'#horizon-demo',isExternal:true},style:{typeface:'Arial',color:C.purple}}]];}
 if(d.question)text(sl,d.question,94,632,1092,40,23,C.purple,true);
 const refs=(d.refs||[]).map(k=>S[k]);
 sl.speakerNotes.text=d.notes+'\n\nSource insight (instructor): '+(d.insight||'')+'\n\nFacilitation (not narration): '+(d.facilitation||'')+'\n\nSources:\n'+refs.join('\n')+'\n'+(d.local||[]).map(f=>path.isAbsolute(f)?f:path.join(repo,f)).join('\n')+'\nVisual: '+(d.image||d.pair?.join('; ')||'Editable slide text/table')+'\n'+(d.credit||d.caption||'')+'\nReview anchor: '+d.id;
}
await fs.mkdir('../previews',{recursive:true});
await (await PresentationFile.exportPptx(p)).save('candidate.pptx');
for(let i=0;i<p.slides.items.length;i++){const b=await p.slides.items[i].export({format:'png',scale:1});await fs.writeFile(`../previews/slide-${String(i+1).padStart(2,'0')}.png`,new Uint8Array(await b.arrayBuffer()));}
// The slide PNGs and structured content provide the review artifacts.
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const version=process.env.DECK_VERSION||'v9',file=`Week_7_Materials_and_Walkthroughs_${version}.pptx`;
const result=await finalizePresentation({workspaceDir:work,candidatePath:path.join(work,'.build/candidate.pptx'),finalPath:path.join(work,'output',file),pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:['Arial','Consolas']},requiredNativeTableOwnerSlides:tableOwners,verifyArtifactToolImport:true,receiptPath:path.join(work,'.build',`validation_${version}.json`)});
console.log(JSON.stringify({slides:p.slides.items.length,live:1+slides.filter(s=>!s.hidden).length,images:slides.filter(s=>s.image||s.pair||s.strips).length,output:result.finalPath}));
await fs.writeFile('../slide_sources.json',JSON.stringify({sourceDeck:source,sourceKeys:S,slides,timing,sections},null,2));

await fs.writeFile('../timing.json',JSON.stringify(timing,null,2));


await fs.writeFile('../bindings.json',JSON.stringify(bindings,null,2));



