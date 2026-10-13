import {L} from './source-labels.mjs';
import fs from 'node:fs/promises';
import {readFileSync} from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {PresentationFile,FileBlob} from '@oai/artifact-tool';
import {S,slides} from './content.mjs';
const work=path.resolve('..'),repo=path.resolve('../../../../..');
const skill='C:/Users/antho/.codex/plugins/cache/openai-primary-runtime/presentations/26.1011.11113/skills/presentations';
const source=path.resolve('../../RefinedDeck20261013/output/Week_7_Python_Tooling_and_UX_Refined_v2.pptx');
const p=await PresentationFile.importPptx(await FileBlob.load(source));p.slides.keep([0]);
const C={ink:'#17151F',purple:'#6550A2',muted:'#777080',light:'#F0EBFF'};
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
function text(sl,str,x,y,w,h,size=30,color=C.ink,bold=false){const t=sl.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});t.text=str;t.text.style={typeface:'Arial',fontSize:size,color,bold};return t;}
function img(sl,file,pos,crop){const ext=path.extname(file).toLowerCase();return sl.images.add({blob:new Uint8Array(readFileSync(path.join(repo,file))),contentType:ext==='.gif'?'image/gif':'image/png',alt:path.basename(file),fit:'contain',position:pos,...(crop?{crop}:{})});}
const tableOwners=[];
for(const [i,d] of slides.entries()){
 const sl=p.slides.add({layoutId:'/ppt/slideLayouts/slideLayout6.xml'});sl.background.fill='#FFFFFF';sl.hidden=!!d.hidden;
 text(sl,d.tag||(d.hidden?'EXPLORE FURTHER':'WEEK 7'),94,60,1100,35,20,C.purple,true);
 text(sl,d.title,94,131,1100,95,46,C.ink,true);
 text(sl,'WEEK 7',94,677,300,23,15,C.muted);text(sl,d.id,1130,677,75,23,15,C.muted);
 if(d.table){
  const h=d.table.length<=4?240:d.table.length<=6?305:340;
  const table=sl.tables.add({rows:d.table.length,columns:d.table[0].length,left:94,top:238,width:1092,height:h,values:d.table});
  for(let r=0;r<d.table.length;r++)for(let c=0;c<d.table[0].length;c++){const cell=table.getCell(r,c);cell.fill=r===0?C.light:'#FFFFFF';cell.text.style={typeface:'Arial',fontSize:24,bold:r===0,color:C.ink};}
  table.borders.assign({fill:'#8D8994',width:.8,style:'solid'});tableOwners.push(i+2);
  if(d.bullets)text(sl,d.bullets.join(' · '),94,238+h+15,1080,45,23);
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
 if(d.caption||d.credit)text(sl,d.credit||d.caption,94,599,d.mediaPath?815:1092,27,16,C.muted);
 if(d.mediaPath){const t=text(sl,'Play companion clip',915,599,278,27,18,C.purple,true);t.text=[[{run:'Play companion clip',link:{uri:pathToFileURL(path.join(repo,d.mediaPath.split('#')[0])).href+'#horizon-demo',isExternal:true},style:{typeface:'Arial',color:C.purple}}]];}
 if(d.question)text(sl,d.question,94,632,1092,40,23,C.purple,true);
 const refs=(d.refs||[]).map(k=>S[k]);
 sl.speakerNotes.text=d.notes+'\n\nSources:\n'+refs.join('\n')+'\n'+(d.local||[]).map(f=>path.join(repo,f)).join('\n')+'\nVisual: '+(d.image||d.pair?.join('; ')||'Editable slide text/table')+'\n'+(d.credit||d.caption||'')+'\nReview anchor: '+d.id;
}
await fs.mkdir('../previews',{recursive:true});
await (await PresentationFile.exportPptx(p)).save('candidate.pptx');
for(let i=0;i<p.slides.items.length;i++){const b=await p.slides.items[i].export({format:'png',scale:1});await fs.writeFile(`../previews/slide-${String(i+1).padStart(2,'0')}.png`,new Uint8Array(await b.arrayBuffer()));}
await fs.writeFile('deck.json',JSON.stringify(p.toProto(),null,2));
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const version=process.env.DECK_VERSION||'v1',file=`Week_7_Expanded_Visual_Lecture_${version}.pptx`;
const result=await finalizePresentation({workspaceDir:work,candidatePath:path.join(work,'.build/candidate.pptx'),finalPath:path.join(work,'output',file),pythonExecutable:'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...tableOwners.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'reference',families:['Arial'],referencePath:source,referenceSha256:crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex')},requiredNativeTableOwnerSlides:tableOwners,verifyArtifactToolImport:true,receiptPath:path.join(work,'.build',`validation_${version}.json`)});
console.log(JSON.stringify({slides:p.slides.items.length,live:1+slides.filter(s=>!s.hidden).length,images:slides.filter(s=>s.image||s.pair).length,output:result.finalPath}));
await fs.writeFile('../slide_sources.json',JSON.stringify({sourceDeck:source,sourceKeys:S,slides},null,2));
let body=`<h1>Week 7 · expanded visual lecture</h1><nav><a href="output/${file}">Editable PowerPoint</a><a href="sources.html">Complete sources and visual register</a><a href="media.html">Motion and presentation media</a><a href="../../../Visuals/Week07/index.html">Editable diagrams</a></nav><p>${p.slides.items.length} slides; ${1+slides.filter(s=>!s.hidden).length} in the default live route. Optional depth follows the live sequence and is hidden in the normal slideshow. The original slide anchors remain stable.</p><h2>Teaching route</h2><p>Python in Unreal → bounded operation and recovery → contributor demonstrations → break → initial tool assessment → UI/UX concepts with production examples → task preparation → reciprocal peer testing → synthesis.</p><p>Use the existing 150-minute proposal as a rehearsal target: 32 minutes for opening/setup/Python, 35 for contributors, 15 break, 8 assessment, 20 UX and task preparation, 35 peer testing, 5 synthesis. The expanded visual steps share the original concept blocks; they are not extra minutes. If discussion requires longer, use the optional-depth slides in a separate session rather than compressing peer testing. Protect the four-minute task preparation.</p><p>The Maya/Unreal bridge still needs rehearsal. Offline PySide states are labelled as sample data. GDC cases describe the speakers’ production tools, not implementations students are expected to reproduce.</p><h2>Handouts</h2><p><a href="../ActivitiesDraft20261012/group-sheet.html">Initial assessment</a> · <a href="../ActivitiesDraft20261012/reveal.html">Reveal</a> · <a href="../ActivitiesDraft20261012/peer-sheet.html">Peer testing</a> · <a href="../ActivitiesDraft20261012/reflection.html">Reflection</a></p><label>Search <input id="q"></label> <label>Route <select id="route"><option value="live">Live</option><option value="all">All</option><option value="optional">Optional depth</option></select></label>`;
body+=`<details><summary>Optional depth: named slide destinations</summary><ul>${slides.filter(s=>s.hidden).map(s=>`<li><a href="#${s.id}">${s.id} · ${esc(s.title)}</a></li>`).join('')}</ul></details>`;
const all=[{id:'01',title:'Review & specialization',notes:'We will connect Python automation with the experience of the artist who uses a tool.',oldIndex:1,rationale:'Preserve the original cover and course identity.'},...slides];
for(const [i,d] of all.entries()){
 const picture=`previews/slide-${String(i+1).padStart(2,'0')}.png`;
 body+=`<article data-hidden="${!!d.hidden}" id="${d.id}"><h2>${i+1}. ${esc(d.title)} <small>Anchor ${d.id}${d.hidden?' · optional':''}</small></h2><div class="compare">${d.oldIndex?`<figure><figcaption>Previous slide ${d.oldIndex}</figcaption><img loading="lazy" src="../RefinedDeck20261013/previews/slide-${String(d.oldIndex).padStart(2,'0')}.png"></figure>`:'<p class="added">Added teaching step</p>'}<figure><figcaption>Refined slide</figcaption><a href="${picture}"><img loading="lazy" src="${picture}"></a></figure></div><p><strong>Edit:</strong> ${d.oldIndex?'Keep the topic and anchor. Use the refined title, text, visual and notes shown here.':'Insert at the indicated point in the live or optional sequence.'}</p><h3>Read-aloud notes</h3><p>${esc(d.notes)}</p><h3>Teaching rationale</h3><p>${esc(d.rationale)}</p><p><strong>Sources:</strong> ${(d.refs||[]).map(k=>`<a href="${esc(S[k])}">${esc(L[k]||k)}</a>`).join(' · ')}</p><p>${esc(d.credit||d.caption||'')}</p>${d.image?`<p><a href="../../../../${esc(d.image)}">Original visual</a></p>`:''}</article>`;
}
const script=`function filter(){const q=document.querySelector('#q').value.toLowerCase(),r=document.querySelector('#route').value;document.querySelectorAll('article').forEach(a=>a.hidden=!(r==='all'||(r==='optional')===(a.dataset.hidden==='true'))||!a.textContent.toLowerCase().includes(q));}function destination(){const a=document.getElementById(location.hash.slice(1));if(a?.tagName==='ARTICLE'){document.querySelector('#route').value=a.dataset.hidden==='true'?'all':'live';document.querySelector('#q').value='';filter();a.scrollIntoView();}}document.querySelector('#q').oninput=filter;document.querySelector('#route').onchange=filter;window.onhashchange=destination;filter();destination();`;
await fs.writeFile('../index.html',`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 7 expanded lecture</title><style>body{font:17px/1.6 Arial;background:#f6f5f9;color:#17151f;max-width:1400px;margin:auto;padding:25px}article{background:white;padding:22px;margin:24px 0;border:1px solid #ddd}.compare{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0}img{width:100%;height:auto}a{color:#6550a2}nav{display:flex;gap:20px;flex-wrap:wrap}input,select{font:inherit;padding:8px}small{font-size:16px}[hidden]{display:none}@media(max-width:850px){.compare{grid-template-columns:1fr}}</style>${body}<script>${script}</script></html>`);
