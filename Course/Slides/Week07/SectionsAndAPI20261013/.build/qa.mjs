import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {slides,timing} from './content.mjs';
const browser=await chromium.launch({headless:true,channel:'msedge'});
const p=await browser.newPage({viewport:{width:1440,height:1000}}),results=[];
for(const name of ['index','audit','teach']){
 await p.goto(pathToFileURL(path.resolve('..',name+'.html')).href);
 if(name==='index')await p.selectOption('#route','all');
 await p.locator('img').evaluateAll(xs=>xs.forEach(i=>i.loading='eager'));
 await p.waitForFunction(()=>[...document.images].every(i=>i.complete));
 const state=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,brokenImages:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),links:[...document.querySelectorAll('a')].map(a=>a.href)}));
 const broken=[];for(const href of state.links)if(href.startsWith('file:'))try{await fs.access(fileURLToPath(href));}catch{broken.push(href);}delete state.links;
 if(name==='index'){
  await p.selectOption('#route','live');state.live=await p.locator('article:visible').count();
  await p.selectOption('#route','reference');state.references=await p.locator('article:visible').count();
  await p.selectOption('#route','live');await p.fill('#search','validation report');state.search=await p.locator('article:visible').count();
  await p.fill('#search','');await p.screenshot({path:'review-desktop.png'});
  await p.setViewportSize({width:780,height:1000});state.mobileOverflow=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);await p.screenshot({path:'review-narrow.png'});await p.setViewportSize({width:1440,height:1000});
 }
 results.push({name,...state,broken});
}
await browser.close();
await fs.writeFile('browser-qa.json',JSON.stringify(results,null,2));
await fs.writeFile('code-snippets.json',JSON.stringify(slides.filter(s=>s.code).map(s=>({id:s.id,code:s.code})),null,2));
console.log(JSON.stringify({results,timingMinutes:timing.at(-1).end}));
if(results.some(r=>r.overflow||r.mobileOverflow||r.brokenImages.length||r.broken.length)||results[0].live!==49||results[0].references!==37||results[0].search!==1)process.exit(1);
