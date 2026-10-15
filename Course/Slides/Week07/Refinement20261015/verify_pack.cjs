const fs=require('node:fs'),path=require('node:path');
const {pathToFileURL,fileURLToPath}=require('node:url');
const {chromium}=require('C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'}),results=[],errors=[];
 const files=fs.readdirSync(__dirname).filter(f=>f.endsWith('.html'));
 for(const width of [1440,390]){
  const page=await browser.newPage({viewport:{width,height:1000}});page.on('pageerror',e=>errors.push(e.message));
  for(const file of files){
   await page.goto(pathToFileURL(path.join(__dirname,file)).href);
   await page.evaluate(async()=>{for(const i of document.images)i.loading='eager';await Promise.allSettled([...document.images].map(i=>i.decode()));});
   const state=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,brokenImages:[...document.images].filter(i=>!i.naturalWidth).map(i=>i.src),h1s:document.querySelectorAll('h1').length,links:[...document.querySelectorAll('a[href]')].map(a=>a.href)}));
   state.missingFiles=state.links.filter(l=>l.startsWith('file:')).filter(l=>!fs.existsSync(fileURLToPath(new URL(l))));delete state.links;
   results.push({file,width,...state});
   if(width===1440&&['index.html','dashboard.html','peer-review.html','live-demo.html'].includes(file))await page.screenshot({path:path.join(__dirname,'qa','web-'+file+'.png')});
   if(width===390&&file==='index.html')await page.screenshot({path:path.join(__dirname,'qa','web-mobile.png')});
  }
  await page.close();
 }
 const page=await browser.newPage();await page.clock.install({time:new Date('2026-10-15T12:00:00Z')});
 await page.goto(pathToFileURL(path.join(__dirname,'dashboard.html')).href);
 const checks=[];async function check(label,yes){checks.push({label,passed:Boolean(yes)});}
 await check('Starts at seven minutes',await page.locator('#time').textContent()==='07:00');
 await page.locator('#toggle').click();await page.clock.fastForward(46000);
 await check('Task phase changes to attempt',/Attempt/.test(await page.locator('#phase').textContent()));
 await page.locator('#toggle').click();const paused=await page.locator('#time').textContent();await page.clock.fastForward(10000);
 await check('Pause retains remaining time',await page.locator('#time').textContent()===paused);
 await page.locator('#toggle').click();await page.clock.fastForward(180000);
 await check('Compare phase',/Compare/.test(await page.locator('#phase').textContent()));
 await page.clock.fastForward(90000);await check('Strength and revision phase',/strength/.test(await page.locator('#phase').textContent()));
 await page.clock.fastForward(60000);await check('Retest and rotate phase',/retest/.test(await page.locator('#phase').textContent()));
 await page.clock.fastForward(60000);await check('Stops at zero without advancing',await page.locator('#time').textContent()==='00:00'&&await page.locator('#round').inputValue()==='0'&&await page.locator('#toggle').isDisabled());
 await page.locator('#next').click();await check('Next round resets deliberately',await page.locator('#round').inputValue()==='1'&&await page.locator('#time').textContent()==='07:00');
 await page.locator('#round').selectOption('2');await check('Last round disables next',await page.locator('#next').isDisabled());
 await page.locator('#toggle').focus();await page.keyboard.press('Space');await check('Keyboard starts timer',await page.locator('#toggle').textContent()==='Pause');
 await page.locator('#reset').click();await check('Reset stops and restores time',await page.locator('#time').textContent()==='07:00'&&await page.locator('#toggle').textContent()==='Start round');
 await page.goto(pathToFileURL(path.join(__dirname,'review.html')).href);
 await page.locator('#live').check();await check('Timed filter contains 70 slides',await page.locator('.slide:visible').count()===70);
 await page.locator('#search').fill('squint');await check('Search filters by topic',await page.locator('.slide:visible').count()>0&&await page.locator('.slide:visible').count()<10);
 const legacy=path.join(__dirname,'../FinalClass20261013');
 for(const [old,target] of Object.entries({'index.html':'index.html','dashboard.html':'dashboard.html','lab1.html':'lab1.html','peer-sheet.html':'peer-review.html','preparation.html':'peer-review.html','reflection.html':'peer-review.html','facilitator.html':'facilitator.html','reveal.html':'reveal.html'})){
  await page.goto(pathToFileURL(path.join(legacy,old)).href);
  await page.waitForURL(pathToFileURL(path.join(__dirname,target)).href);
  await check('Legacy '+old+' opens current '+target,true);
 }
 await page.goto(pathToFileURL(path.join(legacy,'live-demo.html')).href);
 await check('Walkthrough begins at first capture',await page.locator('.step:visible').count()===1&&await page.locator('#count').textContent()==='1 / 7');
 for(let i=0;i<6;i++)await page.locator('#next').click();
 await check('All seven captures reachable; no step beyond seven',await page.locator('#count').textContent()==='7 / 7'&&await page.locator('#next').isDisabled());
 await page.keyboard.press('ArrowLeft');await check('Walkthrough keyboard moves back',await page.locator('#count').textContent()==='6 / 7');
 await page.locator('#all').click();await check('Show all reveals seven captures',await page.locator('.step:visible').count()===7);
 const fallback=await page.evaluate(()=>({broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),links:[...document.querySelectorAll('a[href]')].map(a=>a.href)}));
 await check('Walkthrough images and local document links exist',fallback.broken.length===0&&fallback.links.filter(l=>l.startsWith('file:')).every(l=>fs.existsSync(fileURLToPath(new URL(l)))));
 await browser.close();
 const failures=results.filter(r=>r.overflow||r.brokenImages.length||r.missingFiles.length||r.h1s!==1);
 const report={pages:files.length,viewports:2,results,timer_and_review:checks,page_errors:errors,failures};
 fs.writeFileSync(path.join(__dirname,'qa/web-verification.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({pages:files.length,layout_failures:failures,interaction_failures:checks.filter(c=>!c.passed),errors},null,2));
 process.exitCode=failures.length||checks.some(c=>!c.passed)||errors.length?1:0;
})().catch(e=>{console.error(e);process.exitCode=1});
