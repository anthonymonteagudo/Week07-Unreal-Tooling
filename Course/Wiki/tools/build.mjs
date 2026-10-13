import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const require=createRequire(import.meta.url);
let modulePath;
try {modulePath=require.resolve('marked')} catch {
  if(!process.env.COURSE_NODE_MODULES) throw new Error('Run npm install, or set COURSE_NODE_MODULES to an existing dependency bundle containing marked.');
  modulePath=path.join(process.env.COURSE_NODE_MODULES,'marked/lib/marked.esm.js');
}
const {marked}=await import(pathToFileURL(modulePath).href);
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const files=fs.readdirSync(path.join(root,'content')).filter(f=>f.endsWith('.md')).sort();
const pages=files.map(file=>{
  const raw=fs.readFileSync(path.join(root,'content',file),'utf8');
  const match=raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if(!match) throw new Error('Missing front matter: '+file);
  const meta=Object.fromEntries(match[1].split(/\r?\n/).filter(Boolean).map(line=>{const i=line.indexOf(':');return [line.slice(0,i).trim(),line.slice(i+1).trim()]}));
  for(const key of ['title','group','order','status','summary']) if(!meta[key]) throw new Error(file+': missing '+key);
  if(!/^\d{4}-\d{2}-\d{2}$/.test(meta.updated||'')) throw new Error(file+': updated must be YYYY-MM-DD');
  return {...meta,file,slug:file.slice(0,-3),body:match[2],order:Number(meta.order)};
}).sort((a,b)=>a.order-b.order);
const groups=['Course','Weeks','Topics','Practice','Resources'];
const nav=pages=>groups.map(group=>`<section class="nav-group"><h2>${escape(group)}</h2>${pages.filter(p=>p.group===group).map(p=>`<a href="${p.slug}.html" data-page="${p.slug}">${escape(p.title)}${p.status==='Planned'?'<span class="nav-status">Planned</span>':''}</a>`).join('')}</section>`).join('');
const index=pages.map(p=>({title:p.title,summary:p.summary,slug:p.slug,group:p.group,text:p.body.replace(/<[^>]*>/g,' ').replace(/[#*`|]/g,' ')}));
fs.writeFileSync(path.join(root,'assets/search-index.js'),'window.COURSE_INDEX='+JSON.stringify(index).replace(/</g,'\\u003c')+';\n');
for(const p of pages){
  const toc=[];const counts=new Map();
  const renderer=new marked.Renderer();
  renderer.heading=function(token){
    const label=token.text.replace(/<[^>]+>/g,'').replace(/[*`]/g,'');
    const base=label.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')||'section';
    const count=(counts.get(base)||0)+1;counts.set(base,count);const id=base+(count>1?'-'+count:'');
    if(token.depth===2)toc.push({label,id});
    return `<h${token.depth} id="${id}">${this.parser.parseInline(token.tokens)}</h${token.depth}>`;
  };
  const body=marked.parse(p.body,{renderer,gfm:true});
  const updatedLabel=new Date(p.updated+'T12:00:00Z').toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'});
  const selectedNav=nav(pages).replace(`data-page="${p.slug}"`,`data-page="${p.slug}" aria-current="page"`);
  const html=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(p.title)} · Technical Art</title><meta name="description" content="${escape(p.summary)}"><link rel="stylesheet" href="assets/wiki.css"></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="index.html">Technical Art <span>Course wiki</span></a><span class="edition">GAMEDSGN 590 · Fall 2026 · Working edition</span><a href="../Slides/index.html">Instructor slide reviews ↗</a></header><div class="shell"><aside class="sidebar"><form class="search" role="search"><label for="search-input">Find a topic</label><input id="search-input" type="search" autocomplete="off" placeholder="UVs, materials, Python…"><button type="submit">Search</button></form><nav aria-label="Course pages">${selectedNav}</nav></aside><main id="main"><section id="search-results" hidden aria-label="Search results"><div class="search-heading"><h2>Search results</h2><button id="clear-search">Close search</button></div><p id="search-count" role="status"></p><ul id="result-list"></ul></section><article id="page-content"><div class="page-meta"><span>${escape(p.group)}</span><span class="status ${p.status==='Planned'?'planned':''}">${escape(p.status)}</span><span>Updated ${escape(updatedLabel)}</span></div><h1>${escape(p.title)}</h1><p class="lead">${escape(p.summary)}</p>${p.status==='Planned'?'<p class="planned-note">Syllabus-based outline. Detailed teaching examples and exercises will be added as this week is developed.</p>':''}${toc.length>2?'<nav class="toc" aria-label="On this page"><strong>On this page</strong>'+toc.map(t=>`<a href="#${t.id}">${escape(t.label)}</a>`).join('')+'</nav>':''}${body}</article><footer class="page-footer"><p>Course materials grow through examples, questions, and verified revisions. Use the current Canvas assignment page for deadlines, grading, and submission instructions.</p><a href="content/${p.file}">Page source (Markdown)</a> · <a href="maintaining.html">Maintain this wiki</a></footer></main></div><script src="assets/search-index.js"></script><script src="assets/wiki.js"></script></body></html>`;
  fs.writeFileSync(path.join(root,p.slug+'.html'),html);
}
fs.writeFileSync(path.join(root,'pages.json'),JSON.stringify(pages.map(({body,...p})=>p),null,2)+'\n');
console.log(`Built ${pages.length} static pages and their local search index.`);
