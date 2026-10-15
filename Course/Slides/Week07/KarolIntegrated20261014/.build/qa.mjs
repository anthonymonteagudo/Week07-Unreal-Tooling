import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {chromium} from 'playwright';
const browser=await chromium.launch({channel:'msedge',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(String(e)));
await page.goto(pathToFileURL(path.resolve('../index.html')).href);
if(await page.locator('.entry').count()!==18)throw Error('Wrong changes count');
if(await page.locator('.lesson').count()!==48)throw Error('Wrong lesson count');
await page.locator('#filter').selectOption('live');if(await page.locator('.entry:visible').count()!==8)throw Error('Live filter');
await page.locator('#filter').selectOption('optional');if(await page.locator('.entry:visible').count()!==10)throw Error('Optional filter');
await page.locator('#filter').selectOption('all');await page.locator('#q').fill('interpreter');if(await page.locator('.lesson:visible').count()<1)throw Error('Search');await page.locator('#q').fill('');
await page.screenshot({path:'review-desktop.png'});
await page.locator('#slide-76').scrollIntoViewIfNeeded();await page.locator('#slide-76').screenshot({path:'review-map.png'});
await page.setViewportSize({width:390,height:844});await page.goto(pathToFileURL(path.resolve('../index.html')).href);
const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);if(overflow){console.log(await page.evaluate(()=>Array.from(document.querySelectorAll('*')).filter(e=>e.getBoundingClientRect().right>391).slice(0,12).map(e=>({tag:e.tagName,cls:e.className,width:e.getBoundingClientRect().width,text:e.textContent.slice(0,60)}))));throw Error('Mobile overflow');}await page.screenshot({path:'review-mobile.png'});
await page.goto(pathToFileURL(path.resolve('../readers/bridge-guide.html')).href);if(!await page.getByText('Copy diagnostics',{exact:false}).count())throw Error('Missing diagnostics guide');
if(errors.length)throw Error(errors.join('\n'));await browser.close();console.log('Review search, live/optional filters, 48 lessons, mobile width, bridge reader and JS checks passed.');


