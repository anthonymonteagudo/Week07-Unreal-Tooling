import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const browser=await chromium.launch({headless:true,channel:'msedge'});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
for(const [file,label] of [['../index.html','deck'],['../../ProductionHandoff20261013/source_audit.html','sources']]){
 await page.goto(pathToFileURL(path.resolve(file)).href);
 console.log(label,await page.evaluate(()=>({title:document.title,articles:document.querySelectorAll('article').length,brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length,overflow:document.documentElement.scrollWidth>innerWidth})));
 if(label==='deck') {await page.selectOption('#filter','all'); console.log('all slides visible',await page.locator('article:visible').count()); await page.selectOption('#filter','appendix');console.log('appendix visible',await page.locator('article:visible').count());await page.selectOption('#filter','live');}
 await page.screenshot({path:`qa-${label}.png`});
}
await browser.close();
