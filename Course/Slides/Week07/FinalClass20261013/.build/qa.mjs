import {chromium} from 'playwright';import fs from 'node:fs/promises';import path from 'node:path';import {pathToFileURL,fileURLToPath} from 'node:url';
const browser=await chromium.launch({headless:true,channel:'msedge'}),p=await browser.newPage({viewport:{width:1440,height:1000}}),report=[];
for(const name of ['index','facilitator','demo','lab1','reveal','preparation','peer-sheet','reflection','examples','dashboard','review']){
 await p.goto(pathToFileURL(path.resolve('..',name+'.html')).href);
 await p.locator('img').evaluateAll(xs=>xs.forEach(i=>i.loading='eager'));
 await p.waitForFunction(()=>[...document.images].every(i=>i.complete));
 const state=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,brokenImages:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),links:[...document.querySelectorAll('a')].map(a=>a.href)}));
 const broken=[];for(const href of state.links)if(href.startsWith('file:'))try{await fs.access(fileURLToPath(href));}catch{broken.push(href);}delete state.links;
 if(['lab1','preparation','peer-sheet','reflection'].includes(name)){await p.emulateMedia({media:'print'});await p.setViewportSize({width:816,height:1056});state.print=await p.locator('.page').evaluate(e=>({height:e.clientHeight,content:e.scrollHeight}));await p.screenshot({path:'qa-'+name+'.png',fullPage:true});await p.emulateMedia({media:'screen'});await p.setViewportSize({width:1440,height:1000});}
 if(name==='dashboard'){await p.click('#start');await p.waitForTimeout(1100);await p.click('#pause');state.timerStarted=(await p.locator('#clock').innerText())!=='10:00';await p.selectOption('#round','2');state.roundReset=(await p.locator('#clock').innerText())==='10:00';await p.evaluate(()=>{elapsed=240;render();});state.swapCue=(await p.locator('#cue').innerText()).startsWith('Swap roles');await p.evaluate(()=>{elapsed=600;render();});state.endCue=(await p.locator('#cue').innerText()).startsWith('Round complete');await p.click('#reset');await p.screenshot({path:'qa-dashboard.png'});}
 report.push({name,...state,broken});
}
await browser.close();await fs.writeFile('browser-qa.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));
if(report.some(r=>r.overflow||r.brokenImages.length||r.broken.length||r.print&&r.print.content>r.print.height))process.exit(1);
