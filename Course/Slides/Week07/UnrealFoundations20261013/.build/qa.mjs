import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
const browser=await chromium.launch({headless:true,channel:'msedge'});
const page=await browser.newPage({viewport:{width:1440,height:1000}}),results=[];
for(const name of ['index','teach','audit','checkpoints','walkthrough','maya']){
 await page.goto(pathToFileURL(path.resolve('..',name+'.html')).href);
 await page.locator('img').evaluateAll(xs=>xs.forEach(i=>i.loading='eager'));
 await page.waitForFunction(()=>[...document.images].every(i=>i.complete));
 const r=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,brokenImages:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),links:[...document.querySelectorAll('a')].map(a=>a.href)}));
 const broken=[];for(const href of r.links)if(href.startsWith('file:'))try{await fs.access(fileURLToPath(href));}catch{broken.push(href);}
 delete r.links;r.brokenLinks=broken;
 await page.setViewportSize({width:780,height:1000});r.narrowOverflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
 await page.setViewportSize({width:1440,height:1000});
 if(name==='index')await page.screenshot({path:'review-desktop.png'});
 results.push({name,...r});
}
await browser.close();await fs.writeFile('browser-check.json',JSON.stringify(results,null,2));
console.log(JSON.stringify(results));if(results.some(r=>r.overflow||r.narrowOverflow||r.brokenImages.length||r.brokenLinks.length))process.exitCode=1;
