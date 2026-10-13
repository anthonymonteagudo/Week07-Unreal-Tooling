import fs from 'node:fs';
let f='build.mjs',s=fs.readFileSync(f,'utf8');
s=s.replace('../../RefinedDeck20261013/output/Week_7_Python_Tooling_and_UX_Refined_v2.pptx','../../ExpandedDeck20261013/output/Week_7_Expanded_Visual_Lecture_v3.pptx').replaceAll('Week_7_Expanded_Visual_Lecture_','Week_7_Teaching_Revision_').replaceAll('../RefinedDeck20261013/previews/','../ExpandedDeck20261013/previews/').replaceAll('expanded visual lecture','teaching revision').replaceAll('Week 7 expanded lecture','Week 7 teaching revision');
s=s.replace("text(sl,d.title,94,131,1100,95,46,C.ink,true);","text(sl,d.title,94,131,d.divider?570:1100,d.divider?180:95,d.divider?58:46,C.ink,true);");
s=s.replace(' if(d.table){',` if(d.divider){
  img(sl,d.image,{left:690,top:235,width:500,height:340},d.crop);
  (d.bullets||[]).forEach((b,j)=>text(sl,b,100,355+j*64,545,56,29));
 }else if(d.strips){
  d.strips.forEach((f,j)=>img(sl,f,{left:94,top:240+j*115,width:1092,height:84}));
  text(sl,d.bullets.join(' · '),94,510,1092,75,29);
 }else if(d.split){
  img(sl,d.image,{left:735,top:240,width:465,height:340},d.crop);
  if(d.code)text(sl,d.code,94,250,625,320,23);
  else (d.bullets||[]).forEach((b,j)=>text(sl,b,94,255+j*100,605,88,31));
 }else if(d.table){`);
s=s.replace("sl.speakerNotes.text=d.notes+'\\n\\nSources:","sl.speakerNotes.text=d.notes+'\\n\\nSource insight (instructor): '+(d.insight||'')+'\\n\\nFacilitation (not narration): '+(d.facilitation||'')+'\\n\\nSources:");
s=s.replace('<a href="sources.html">Complete sources and visual register</a>','<a href="sources.html">Complete sources and visual register</a><a href="assessment.html">Source assessment and revision audit</a>');
s=s.replace('<h3>Teaching rationale</h3>', '<h3>Source insight</h3><p>${esc(d.insight||\'See the source-linked narration and assessment page for the evidence boundary.\')}</p><h3>Facilitation</h3><p>${esc(d.facilitation||\'\')}</p><h3>Teaching rationale</h3>');
s=s.replace("images:slides.filter(s=>s.image||s.pair).length","images:slides.filter(s=>s.image||s.pair||s.strips).length");
fs.writeFileSync(f,s);
let c=fs.readFileSync('companion.mjs','utf8').replace('d.pair||[d.image].filter(Boolean)','d.pair||d.strips||[d.image].filter(Boolean)').replace('<a href="sources.html">All sources</a>','<a href="sources.html">All sources</a><a href="assessment.html">Latest source assessment</a>');fs.writeFileSync('companion.mjs',c);
