import {chromium} from 'playwright';
import {pathToFileURL} from 'node:url';
import path from 'node:path';
const b=await chromium.launch({headless:true,channel:'msedge'});const p=await b.newPage({viewport:{width:1940,height:1120}});
await p.goto(pathToFileURL(path.resolve('video-check.html')).href);
await p.locator('video').evaluate(v=>{v.style.width='1920px';v.controls=false;});
for(const t of [0.2,5,10,15]){await p.locator('video').evaluate((v,t)=>new Promise(r=>{v.addEventListener('seeked',r,{once:true});v.currentTime=t;}),t);await p.locator('video').screenshot({path:`video-${t}.png`});}
await b.close();
