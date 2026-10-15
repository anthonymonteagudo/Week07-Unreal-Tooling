import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Presentation,PresentationFile} from 'file:///C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const dir=path.dirname(fileURLToPath(import.meta.url));
const plan=JSON.parse(await fs.readFile(path.join(dir,'content-plan.json'),'utf8'));
const p=Presentation.create({slideSize:{width:1280,height:720}});
const font='Neue Haas Grotesk Text Pro';
function text(s,name,value,x,y,w,h,size=29,color='#FFFFFF',bold=false,face=font){
 const sh=s.shapes.add({name,geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=value;sh.text.style={fontFamily:face,fontSize:size,color,bold,verticalAlignment:'top'};
 return sh;
}
for(const a of plan.slides){
 const s=p.slides.add();s.background.fill='#08090B';
 if(a.kind==='divider'){
  text(s,a.id+'-title',a.title,46,235,1125,168,72);
  text(s,a.id+'-body',a.body.join('\n'),46,432,850,100,34);
  text(s,a.id+'-question',a.question,46,583,1110,65,27,'#FFE0BD');
 }else{
  text(s,a.id+'-title',a.title,46,74,1185,88,a.title.length>48?45:50);
  if(a.table){
   const top=a.body.length?225:183, bottom=555;
   if(a.body.length)text(s,a.id+'-intro',a.body.join('\n'),46,164,1185,55,27);
   let fractions=a.table[0].length===2?[.30,.70]:a.table[0].length===3?[.29,.34,.37]:[.16,.28,.28,.28];
   if(a.id==='O2')fractions=[.46,.35,.19];
   if(a.id==='S2')fractions=[.30,.20,.50];
   if(a.id==='L1P')fractions=[.18,.40,.42];
   if(a.id==='L1R')fractions=[.30,.35,.35];
   if(a.id==='P2')fractions=[.25,.25,.25,.25];
   const t=s.tables.add({rows:a.table.length,columns:a.table[0].length,left:46,top,width:1185,height:bottom-top,columnWidths:fractions.map(f=>f*1185),values:a.table});
   t.borders.assign({style:'solid',fill:'#66526D',width:1});
   for(let r=0;r<a.table.length;r++)for(let c=0;c<a.table[r].length;c++){
    const cell=t.getCell(r,c);cell.fill=r===0?'#302039':r%2?'#101015':'#1B151F';
    cell.text.style={fontFamily:font,fontSize:a.id==='S2'?25:27,color:'#FFFFFF',bold:r===0,verticalAlignment:'middle'};
   }
  }else if(a.code){
   text(s,a.id+'-code',a.code,46,193,1185,270,a.id==='O4'?25:30,'#FFFFFF',false,'Consolas');
   text(s,a.id+'-body',a.body.join('\n'),46,475,1160,93,28);
  }else if(a.image){
   const b=await fs.readFile(a.image);
   const wide=a.kind==='image';
   s.images.add({blob:b,contentType:'image/png',alt:a.caption||a.title,fit:'contain',position:wide?{left:46,top:180,width:760,height:385}:{left:46,top:175,width:620,height:390}});
   text(s,a.id+'-body',a.body.join('\n\n'),wide?845:710,190,wide?380:520,360,28);
  }else{
   text(s,a.id+'-body',a.body.join('\n\n'),46,190,1150,360,32);
  }
  if(a.question)text(s,a.id+'-question',a.question,46,583,1185,60,26,'#FFE0BD');
  if(a.caption)text(s,a.id+'-caption',a.caption,46,651,1130,28,17,'#FFFFFF');
 }
 s.speakerNotes.text=a.notes+'\n\nSources\n'+a.sources.join('\n');
}
await(await PresentationFile.exportPptx(p)).save(path.join(dir,'build/authored.pptx'));
await fs.writeFile(path.join(dir,'build/authored-inspect.ndjson'),(await p.inspect({kind:'slide,textbox,table,image',maxChars:1000000})).ndjson);
console.log('Authored '+plan.slides.length+' editable slide compositions.');
