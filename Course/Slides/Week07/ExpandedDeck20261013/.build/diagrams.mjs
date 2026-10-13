import fs from 'node:fs/promises';
import sharp from 'sharp';
import path from 'node:path';
const root=path.resolve('../../../../..'), dir=path.join(root,'Course/Visuals/Week07');
await fs.mkdir(dir,{recursive:true});
const ink='#0A4054', accent='#029990';
const tx=(x,y,s,size=34,color=ink)=>`<text x="${x}" y="${y}" text-anchor="middle" font-family="Arial,sans-serif" font-size="${size}" fill="${color}">${s}</text>`;
const box=(x,y,w,h,s,sub='',focus=false)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="none" stroke="${focus?accent:ink}" stroke-width="4"/>${tx(x+w/2,y+h/2+(sub?-6:12),s,36)}${sub?tx(x+w/2,y+h/2+36,sub,27):''}`;
const arr=(d,dash=false)=>`<path d="${d}" stroke="${accent}" stroke-width="6" fill="none" ${dash?'stroke-dasharray="12 9"':''} marker-end="url(#arrow)"/>`;
const defs=`<defs><marker id="arrow" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0L5 2.5L0 5Z" fill="${accent}"/></marker></defs>`;
const items=[
 ['shared-asset','Two Actor components reference one asset','06A',arr('M360 130H545Q560 130 560 145V210H650')+arr('M360 370H545Q560 370 560 355V290H650')+box(40,60,320,140,'Actor A','Mesh component')+box(40,300,320,140,'Actor B','Mesh component')+box(675,160,450,180,'Static Mesh asset','Shared geometry',true)+tx(500,95,'references',27)+tx(500,422,'references',27)],
 ['handoff','Maya export and Unreal reimport loop','10',arr('M350 180H465')+arr('M770 180H885')+arr('M1035 270V390Q1035 405 1020 405H205Q190 405 190 390V275',true)+box(40,100,310,170,'Maya source','Pivot / units / slots')+box(475,100,290,170,'FBX file','Known location')+box(895,100,335,170,'Unreal asset','Known destination',true)+tx(410,145,'export',25)+tx(830,145,'import',25)+tx(625,455,'Revise • reimport • verify',30)],
 ['reviewed-plan','Tool state transitions','09C',arr('M255 230H333')+arr('M570 230H648')+arr('M885 230H963')+arr('M450 320V425H155V325',true)+box(20,150,235,170,'Inputs','Selection')+box(335,150,235,170,'Preview','Exact changes',true)+box(650,150,235,170,'Applied','Reported result')+box(965,150,285,170,'Verified','Expected result')+tx(295,118,'inspect',25)+tx(609,118,'apply',25)+tx(925,118,'check',25)+tx(330,470,'Input changed? Preview again.',28)],
 ['interface-backend','Interfaces call a shared Python operation','08A',arr('M350 100H470V245H590')+arr('M350 380H470V275H590')+arr('M890 260H990')+box(30,40,320,130,'Qt / PySide','Python UI')+box(30,320,320,130,'Editor Utility','Blueprint UI')+box(600,180,290,160,'Python','Tool operation',true)+box(1000,180,245,160,'Unreal','Editor API')+tx(620,455,'Same rules • different interfaces',30)],
 ['tool-layouts','Two sketches for one import task','14D',box(35,50,525,400,'')+box(700,50,525,400,'')+tx(300,100,'Single view',34)+tx(960,100,'Guided steps',34)+tx(300,170,'Source + destination',30)+tx(300,240,'Change preview',30)+tx(300,335,'Import selected',30)+tx(960,170,'1  Choose inputs',30)+arr('M960 195V235')+tx(960,280,'2  Review changes',30)+arr('M960 303V343')+tx(960,390,'3  Import',30)],
 ['test-loop','Repeat a task after a targeted change','16E',arr('M390 130H770')+arr('M945 210V330')+arr('M770 405H400')+arr('M210 330V220')+box(40,60,350,150,'Observe','Task attempt')+box(785,60,350,150,'Interpret','Possible cause')+box(785,330,350,150,'Revise','One change',true)+box(40,330,350,150,'Retest','Same goal')+tx(590,160,'Record evidence',27)+tx(590,448,'Check the prediction',27)]
];
const manifest=[];
for(const [id,title,slide,body] of items){
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="520" viewBox="0 0 1280 520"><title>${title}</title>${defs}${body}</svg>`;
 await fs.writeFile(path.join(dir,id+'.svg'),svg);
 await sharp(Buffer.from(svg)).resize(2560,1040).png().toFile(path.join(dir,id+'.png'));
 const stats=await sharp(path.join(dir,id+'.png')).stats();
 if(!stats.channels[3]||stats.channels[3].min!==0)throw Error('No transparent background '+id);
 manifest.push({id,title,slide,svg:id+'.svg',png:id+'.png',method:'Original course schematic, editable SVG and alpha PNG',rights:'Original teaching diagram',font:'Arial course fallback',transparent:true,source:'Conceptual teaching model, not a software capture'});
}
await fs.writeFile(path.join(dir,'manifest.json'),JSON.stringify(manifest,null,2));
await fs.writeFile(path.join(dir,'index.html'),`<!doctype html><html lang="en"><meta charset="utf-8"><title>Week 7 diagrams</title><style>body{font:18px Arial;max-width:1200px;margin:30px auto;color:${ink}}img{width:100%}section{margin:30px 0}.dark{background:#f0ebff;padding:20px}a{color:#6550a2}</style><h1>Week 7 diagrams</h1><p>Transparent original teaching schematics with editable SVG masters. Labels use Arial, the course fallback. These describe relationships, not a captured tool execution. Use these ink-colored diagrams on white or light backgrounds; the purple preview is supplied by the page, not baked into the PNG.</p>${manifest.map(d=>`<section><h2>${d.title} (${d.slide})</h2><div class="dark"><img src="${d.png}" alt="${d.title}"></div><a href="${d.svg}">Editable SVG</a> · <a href="${d.png}">Transparent PNG</a></section>`).join('')}</html>`);
console.log('Six diagrams with alpha exports');
