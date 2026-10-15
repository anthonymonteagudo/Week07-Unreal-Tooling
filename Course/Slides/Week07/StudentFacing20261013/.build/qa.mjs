import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {slides,timing,catalog,bindings} from './content.mjs';
const browser=await chromium.launch({headless:true,channel:'msedge'});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
const p=await context.newPage(),results=[];
await p.addInitScript(()=>{window.copied='';Object.defineProperty(navigator,'clipboard',{value:{writeText:async t=>window.copied=t}})});
for(const name of ['index','audit','teach','checkpoints','walkthrough','maya']){
 await p.goto(pathToFileURL(path.resolve('..',name+'.html')).href);
 if(name==='index')await p.selectOption('#route','all');
 await p.locator('img').evaluateAll(xs=>xs.forEach(i=>i.loading='eager'));
 await p.waitForFunction(()=>[...document.images].every(i=>i.complete));
 const state=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,brokenImages:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),links:[...document.querySelectorAll('a')].map(a=>a.href)}));
 const broken=[];for(const href of state.links)if(href.startsWith('file:'))try{await fs.access(fileURLToPath(href));}catch{broken.push(href);}delete state.links;
 if(name==='index'){
  await p.selectOption('#route','live');state.live=await p.locator('article:visible').count();
  await p.selectOption('#route','reference');state.references=await p.locator('article:visible').count();
  await p.selectOption('#route','live');await p.fill('#search','Read-only validation');state.search=await p.locator('article:visible').count();
  await p.fill('#search','');await p.screenshot({path:'review-desktop.png'});
 }
 if(name==='checkpoints'){
  state.steps=await p.locator('article').count();state.copyMatches=true;
  for(const s of catalog){await p.locator(`[data-copy="${s.id}"]`).click();const copied=await p.evaluate(()=>window.copied);const source=await fs.readFile(path.resolve('../../../../../Week07UnrealPython/lesson_materials/week_07_api_checkpoints',s.file),'utf8');if(copied!==source)state.copyMatches=false;}
  await p.locator('[data-copy="UE08-through-focus"]').click();const code=await p.evaluate(()=>window.copied);state.cumulative=code.includes('import unreal')&&code.includes('W07_MaterialTarget')&&code.includes('set_material');
  await p.fill('#search','UE12');state.search=await p.locator('article:visible').count();await p.fill('#search','');
  await p.goto(pathToFileURL(path.resolve('../checkpoints.html')).href+'#UE02');await p.screenshot({path:'checkpoint-desktop.png'});
 }
 await p.setViewportSize({width:780,height:1000});state.mobileOverflow=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);await p.setViewportSize({width:1440,height:1000});
 results.push({name,...state,broken});
}
await browser.close();
await fs.writeFile('browser-qa.json',JSON.stringify(results,null,2));
console.log(JSON.stringify({results,timingMinutes:timing.at(-1).end,bindings:bindings.length}));
if(results.some(r=>r.overflow||r.mobileOverflow||r.brokenImages.length||r.broken.length)||results[0].live!==57||results[0].references!==45||results[0].search!==1||!results[3].copyMatches||!results[3].cumulative||results[3].steps!==17)process.exit(1);
