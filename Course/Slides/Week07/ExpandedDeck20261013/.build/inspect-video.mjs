import {chromium} from 'playwright';
import {pathToFileURL} from 'node:url';
import path from 'node:path';
const b=await chromium.launch({headless:true,channel:'msedge'});const p=await b.newPage({viewport:{width:1440,height:1000}});
await p.goto(pathToFileURL(path.resolve('video-check.html')).href);
await p.waitForTimeout(1000);
console.log(await p.evaluate(()=>({title:document.title,video:[...document.querySelectorAll('video')].map(v=>({duration:v.duration,w:v.videoWidth,h:v.videoHeight,error:v.error?.message}))})));
await p.screenshot({path:'video-open.png'});await b.close();

