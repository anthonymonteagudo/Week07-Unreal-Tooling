const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL,fileURLToPath} = require('node:url');
const {chromium} = require('C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const qa=path.join(__dirname,'qa'); fs.mkdirSync(qa,{recursive:true});
 const files=['index.html','notes/01.html','notes/02.html','notes/03.html','compiled-notes.html','assessment.html','original-script.html'];
 const results=[];
 for(const mobile of [false,true]){
  const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:1000}});
  for(const file of files){
   await page.goto(pathToFileURL(path.join(__dirname,file)).href);
   await page.evaluate(async()=>{for(const img of document.images)img.loading='eager';await Promise.allSettled([...document.images].map(img=>img.decode()));});
   const state=await page.evaluate(()=>({
    overflow:document.documentElement.scrollWidth>innerWidth,
    brokenImages:[...document.images].filter(x=>!x.naturalWidth).map(x=>x.src),
    images:document.images.length,
    h1s:document.querySelectorAll('h1').length,
    links:[...document.querySelectorAll('a[href]')].map(x=>x.href),
    missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(x=>!document.getElementById(decodeURIComponent(x.hash.slice(1)))).map(x=>x.hash)
   }));
   const missingFiles=state.links.filter(url=>url.startsWith('file:')).filter(url=>!fs.existsSync(fileURLToPath(new URL(url))));
   delete state.links;
   results.push({file,viewport:mobile?'mobile':'desktop',...state,missingFiles});
   if((!mobile&&['index.html','notes/01.html','assessment.html','original-script.html'].includes(file))||(mobile&&['index.html','notes/03.html'].includes(file))){
    await page.screenshot({path:path.join(qa,(mobile?'mobile-':'desktop-')+file.replaceAll('/','-')+'.png')});
   }
   if(!mobile&&file==='notes/03.html'){
    await page.locator('#avoid-the-last-texture-wins-problem').scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(qa,'desktop-naming-example.png')});
   }
  }
  await page.close();
 }
 await browser.close();
 fs.writeFileSync(path.join(__dirname,'layout-verification.json'),JSON.stringify(results,null,2));
 const failures=results.filter(x=>x.overflow||x.brokenImages.length||x.missingFiles.length||x.missingAnchors.length||x.h1s!==1);
 console.log(JSON.stringify({pages:files.length,viewports:2,failures},null,2));
 process.exitCode=failures.length?1:0;
})().catch(e=>{console.error(e);process.exitCode=1;});
