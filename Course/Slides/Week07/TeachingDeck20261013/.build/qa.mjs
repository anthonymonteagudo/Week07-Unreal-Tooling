import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
const root=path.resolve('..');const b=await chromium.launch({headless:true,channel:'msedge'});const p=await b.newPage({viewport:{width:1440,height:1000}});const result={pages:[],brokenLocal:[]};
for(const name of ['index.html','sources.html','assessment.html','media.html','../../../Visuals/Week07/index.html']){
const url=pathToFileURL(path.resolve(root,name)).href;await p.goto(url);await p.locator('img').evaluateAll(imgs=>imgs.forEach(i=>i.loading='eager'));await p.waitForFunction(()=>[...document.images].every(i=>i.complete));
const state=await p.evaluate(()=>({title:document.title,images:document.images.length,brokenImages:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),overflow:document.documentElement.scrollWidth>innerWidth,links:[...document.querySelectorAll('a[href]')].map(a=>a.href)}));
for(const u of state.links)if(u.startsWith('file:')){try{await fs.access(fileURLToPath(new URL(u)));}catch{result.brokenLocal.push(u);}}
delete state.links;result.pages.push(state);await p.screenshot({path:`qa-${path.basename(name,'.html')}${name.startsWith('../')?'-gallery':''}.png`});
if(name==='index.html'){
result.liveCount=await p.locator('article:visible').count();await p.selectOption('#route','all');result.allCount=await p.locator('article:visible').count();await p.selectOption('#route','optional');result.optionalCount=await p.locator('article:visible').count();await p.evaluate(()=>location.hash='16D');await p.waitForTimeout(200);result.anchorVisible=await p.locator('[id="16D"]').isVisible();await p.locator('[id="16D"]').screenshot({path:'qa-comparison.png'});
}
if(name==='media.html'){await p.locator('video').evaluate(async v=>{v.muted=true;await v.play();});await p.waitForTimeout(1300);result.movie=await p.locator('video').evaluate(v=>({time:v.currentTime,duration:v.duration,width:v.videoWidth,height:v.videoHeight,paused:v.paused,error:v.error?.message||null}));await p.locator('video').evaluate(v=>v.pause());}
}
await b.close();await fs.writeFile('browser-qa.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));if(result.brokenLocal.length||result.pages.some(p=>p.brokenImages.length||p.overflow)||!result.anchorVisible||result.movie.time<.5)process.exit(1);
