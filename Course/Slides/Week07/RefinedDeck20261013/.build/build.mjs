import fs from 'node:fs/promises';
import {readFileSync} from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import crypto from 'node:crypto';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
import {S,slides} from './content.mjs';
const work=path.resolve('..'), repo=path.resolve('../../../../..');
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const source=path.resolve('../../AgendaRevision20261011/Week_7_Agenda_330_to_600.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(source));
p.slides.keep([0]);
p.slides.items[0].speakerNotes.text='Today we connect Python editor automation with artist-facing tool design. Keep scope, evidence, and recovery in view as we move from Maya to Unreal, then assess and test each other’s tools.\n\nSource: Course Week 7 agenda and refined source compilation.';
const C={ink:'#17151F',purple:'#6550A2',muted:'#777080',light:'#F0EBFF'};
const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function text(sl,str,x,y,w,h,size=30,color=C.ink,bold=false){const t=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=str;t.text.style={typeface:'Arial',fontSize:size,color,bold};return t;}
function image(sl,file,pos,crop){sl.images.add({blob:new Uint8Array(readFileSync(path.join(repo,file))),contentType:'image/png',alt:file,fit:'contain',position:pos,...(crop?{crop}:{})});}
const tableOwners=[];
for(const [i,d] of slides.entries()){
 const sl=p.slides.add({layoutId:'/ppt/slideLayouts/slideLayout6.xml'});sl.background.fill='#FFFFFF';sl.hidden=!!d.hidden;
 text(sl,d.tag||(d.hidden?'EXPLORE FURTHER':'WEEK 7'),94,60,1100,35,20,C.purple,true);
 text(sl,d.title,94,131,1100,95,46,C.ink,true);
 text(sl,'WEEK 7',94,665,300,26,15,C.muted);
 text(sl,d.id,1130,665,75,26,15,C.muted);
 if(d.table){
  const h=d.table.length<=4?240:d.table.length<=6?305:340;
  const table=sl.tables.add({rows:d.table.length,columns:d.table[0].length,left:94,top:238,width:1092,height:h,values:d.table});
  for(let r=0;r<d.table.length;r++)for(let c=0;c<d.table[0].length;c++){let cell=table.getCell(r,c);cell.fill=r===0?C.light:'#FFFFFF';cell.text.style={typeface:'Arial',fontSize:24,bold:r===0,color:C.ink};}
  table.borders.assign({fill:'#8D8994',width:0.8,style:'solid'});tableOwners.push(i+2);
  if(d.bullets)text(sl,d.bullets.join(' · '),94,238+h+15,1080,45,23);
 }else if(d.image){
  if(d.side){
   const regions=d.id==='15'?[
    {top:.11,bottom:.77,left:.015,right:.34},
    {top:.417,bottom:.438,left:.018,right:.34},
    {top:.88,bottom:.055,left:.68,right:.018}
   ]:[
    {top:.11,bottom:.77,left:.015,right:.34},
    {top:.23,bottom:.675,left:.015,right:.34},
    {top:.88,bottom:.055,left:.68,right:.018}
   ];
   regions.forEach((crop,j)=>image(sl,d.image,{left:94,top:238+j*115,width:745,height:103},crop));
   d.side.forEach((v,j)=>text(sl,v,880,250+j*115,305,90,28));
  }
  else image(sl,d.image,{left:94,top:220,width:1092,height:370});
  text(sl,d.caption,94,589,1092,28,16,C.muted);
 }else if(d.code){
  const n=d.code.split('\n').length;const y=240;const h=n*32+12;
  text(sl,d.code,100,y,1080,h,27,C.ink);
  if(d.bullets)text(sl,d.bullets.join('\n'),100,y+h+12,1080,100,26,C.ink);
 }else if(d.links){
  for(const [j,[label,k]] of d.links.entries()){const t=text(sl,label,100,245+j*65,1080,52,30);t.text=[[{run:label,link:{uri:S[k],isExternal:true},style:{color:C.purple}}]];}
 }else{
  (d.bullets||[]).forEach((b,j)=>text(sl,b,100,260+j*90,1080,78,32));
 }
 if(d.question)text(sl,d.question,94,617,1092,44,23,C.purple,true);
 const refs=(d.refs||[]).map(k=>S[k]);
 const locals=(d.local||[]).map(x=>path.join(repo,x).replaceAll('\\','/'));
 sl.speakerNotes.text=d.notes+'\n\nSources:\n'+[...refs,...locals].join('\n')+(d.image?'\nVisual: '+path.join(repo,d.image).replaceAll('\\','/')+'\nExisting course capture; original screenshot pixels embedded without retouching.':'')+'\nReview anchor: '+d.id;
}
await fs.mkdir('../previews',{recursive:true});
await (await PresentationFile.exportPptx(p)).save('candidate.pptx');
for(let i=0;i<p.slides.items.length;i++){
 const blob=await p.slides.items[i].export({format:'png',scale:1});await fs.writeFile(`../previews/slide-${String(i+1).padStart(2,'0')}.png`,new Uint8Array(await blob.arrayBuffer()));
}
await fs.writeFile('deck.json',JSON.stringify(p.toProto(),null,2));
const fontPolicy={basis:'reference',families:['Arial'],referencePath:source,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex')};
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const output=path.join(work,'output/Week_7_Python_Tooling_and_UX_Refined_v2.pptx');
const result=await finalizePresentation({workspaceDir:work,candidatePath:path.join(work,'.build/candidate.pptx'),finalPath:output,pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy,requiredNativeTableOwnerSlides:tableOwners,verifyArtifactToolImport:true,receiptPath:path.join(work,'.build/validation_v2.json')});
console.log(JSON.stringify(result));
await fs.writeFile('../slide_sources.json',JSON.stringify({sourceDeck:source,slides:[{id:'01',title:'Review & specialization',notes:'Original cover retained.'},...slides],sourceKeys:S},null,2));
let body='<h1>Week 7 · Python tooling in Unreal and tool UX</h1><p><a href="output/Week_7_Python_Tooling_and_UX_Refined_v2.pptx">Editable PowerPoint</a> · <a href="../ProductionHandoff20261013/source_audit.html">Complete source audit</a> · <a href="slide_sources.json">Structured slide sources</a></p><p>Original Week 7 style retained. The appendix slides are hidden from the normal slideshow. Captures marked offline use fictional rehearsal data; Unreal captures are existing course evidence. The Maya → Unreal import/reimport demonstration still needs rehearsal in the teaching engine.</p><h2>Timing proposal for the 150-minute session</h2><p>3:30 introduction (5m); 3:35 setup (8m); 3:43 concepts and bridge explanation (17m); 4:00 instructor showcase (2m); 4:02 co-teacher (15m); 4:17 TA (20m); 4:37 break (15m); 4:52 assessment (8m); 5:00 UI/UX and preparation (20m); 5:20 peer briefing, rounds and synthesis (40m).</p><p>This proposal recovers ten minutes from the earlier setup/introduction allocation while preserving contributor durations, break, and all three peer rounds. It is a proposed running order, not a newly confirmed schedule; the deck avoids unconfirmed intermediate clock times.</p><h2>Handouts</h2><p><a href="../ActivitiesDraft20261012/group-sheet.html">Group sheet</a> · <a href="../ActivitiesDraft20261012/peer-sheet.html">Peer review</a> · <a href="../ActivitiesDraft20261012/reflection.html">Reflection</a></p><label>Find <input id="q" type="search"></label><label>Show <select id="filter"><option value="live">Live slides</option><option value="all">All slides</option><option value="appendix">Appendix</option></select></label>';
for(const [i,d] of [{id:'01',title:'Review & specialization',notes:'Original cover retained.'},...slides].entries())body+=`<article data-hidden="${!!d.hidden}"><h2>${i+1} · ${escape(d.title)} <small>(${d.id})</small></h2><img src="previews/slide-${String(i+1).padStart(2,'0')}.png" alt="${escape(d.title)}"><h3>Speaker notes</h3><p>${escape(d.notes)}</p><p>${(d.refs||[]).map(k=>`<a href="${escape(S[k])}">${escape(k)}</a>`).join(' · ')}</p>${d.local?'<p>Local evidence: '+d.local.map(x=>`<a href="../../../../${escape(x)}">${escape(x)}</a>`).join(' · ')+'</p>':''}</article>`;
const js="function filter(){const q=document.querySelector('#q').value.toLowerCase(),f=document.querySelector('#filter').value;document.querySelectorAll('article').forEach(a=>a.hidden=!(f==='all'||(f==='appendix')===(a.dataset.hidden==='true'))||!a.textContent.toLowerCase().includes(q));}document.querySelector('#q').oninput=filter;document.querySelector('#filter').onchange=filter;filter();";
await fs.writeFile('../index.html',`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 7 refined deck</title><style>body{font:17px/1.6 Arial;background:#f6f5f9;color:#17151f;max-width:1200px;margin:auto;padding:25px}article{background:white;padding:20px;margin:24px 0;border:1px solid #ddd}img{width:100%;height:auto}a{color:#6550a2}input,select{font:inherit;padding:8px}label{margin-right:20px}small{font-size:16px}[hidden]{display:none}</style>${body}<script>${js}</script></html>`);
console.log('Final deck and review:',p.slides.items.length,'slides');



