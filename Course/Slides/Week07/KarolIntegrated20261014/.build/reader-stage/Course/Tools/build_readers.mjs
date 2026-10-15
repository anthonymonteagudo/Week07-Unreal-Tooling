/** Local document reading views. No network fetches; original sources remain intact. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const course=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const workspace=path.dirname(course), output=path.join(course,'Readers');
const deps=process.env.COURSE_NODE_MODULES||'C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {marked}=await import(pathToFileURL(path.join(deps,'marked/lib/marked.esm.js')));
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const slash=s=>s.replaceAll('\\','/');
const relative=(from,to)=>slash(path.relative(path.dirname(from),to)).split('/').map(encodeURIComponent).join('/');
const id=s=>s.replace(/<[^>]*>/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');
const priorPath=path.join(output,'manifest.json');
const prior=fs.existsSync(priorPath)?JSON.parse(fs.readFileSync(priorPath,'utf8')).documents:[];
const docs=new Map();
fs.mkdirSync(output,{recursive:true});
function register(file){
 const local=path.relative(workspace,file);
 if(local.startsWith('..')||path.isAbsolute(local)||!fs.existsSync(file)||!fs.statSync(file).isFile())return null;
 if(!['.md','.csv'].includes(path.extname(file).toLowerCase()))return null;
 const key=slash(local),name=id(path.basename(file,path.extname(file)))+'-'+crypto.createHash('sha256').update(key).digest('hex').slice(0,8)+'.html';
 if(!docs.has(key))docs.set(key,{source:key,file,reader:name});
 return docs.get(key);
}
for(const doc of prior)register(path.resolve(workspace,doc.source));
function resolveLocal(raw,from){
 let value=raw.replaceAll('&amp;','&');
 if(value.startsWith('#')||/^(https?:|mailto:|data:|app:|codex:|javascript:)/i.test(value))return null;
 const hash=value.indexOf('#'),fragment=hash>=0?value.slice(hash):'';if(hash>=0)value=value.slice(0,hash);
 const query=value.indexOf('?');if(query>=0)value=value.slice(0,query);
 try{value=decodeURIComponent(value);}catch{return null;}
 if(value.startsWith('file:')){try{value=fileURLToPath(value);}catch{return null;}}
 if(/^\/[A-Za-z]:/.test(value))value=value.slice(1);
 // Wiki Markdown intentionally uses paths relative to the generated Wiki page.
 const wikiContent=path.join(course,'Wiki','content')+path.sep;
 const base=from.startsWith(wikiContent)&&from.endsWith('.md')?path.join(course,'Wiki'):path.dirname(from);
 return {file:path.resolve(base,value),fragment};
}
function mapHref(href,from,to){
 const local=resolveLocal(href,from);if(!local)return href;
 const doc=register(local.file);
 return (doc?relative(to,path.join(output,doc.reader)):relative(to,local.file))+local.fragment;
}
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(d=>{
 if(d.name==='Readers'||d.name==='Wiki'||d.name==='Archive'||d.name==='node_modules'||d.name==='__pycache__')return[];
 const file=path.join(dir,d.name);return d.isDirectory()?walk(file):file.endsWith('.html')?[file]:[];
});}
let rewritten=0;
const changed=[];
// Wiki's explicitly labeled editable-source links should remain source links.
for(const filename of fs.readdirSync(path.join(course,'Wiki')).filter(n=>n.endsWith('.html'))){
 const file=path.join(course,'Wiki',filename),original=fs.readFileSync(file,'utf8');
 const updated=original.replace(/\bhref="([^"]+)"/g,(all,href)=>{
  const local=resolveLocal(href,file);if(!local||path.dirname(local.file)!==output)return all;
  const doc=prior.find(d=>d.reader===path.basename(local.file));
  return doc?'href="'+esc(relative(file,path.resolve(workspace,doc.source))+local.fragment)+'"':all;
 });
 if(updated!==original){fs.writeFileSync(file,updated);changed.push(slash(path.relative(workspace,file)));}
}
for(const file of walk(course)){
 const original=fs.readFileSync(file,'utf8');
 const result=original.replace(/\bhref="([^"]+)"/g,(all,href)=>{
  const local=resolveLocal(href,file);if(!local||!register(local.file))return all;
  return 'href="'+esc(mapHref(href,file,file))+'"';
 });
 if(result!==original){fs.writeFileSync(file,result);rewritten++;changed.push(slash(path.relative(workspace,file)));}
}
function csvRows(raw){
 const rows=[];let row=[],cell='',quoted=false;
 for(let i=0;i<raw.length;i++){const ch=raw[i];if(ch==='"'){if(quoted&&raw[i+1]==='"'){cell+='"';i++;}else quoted=!quoted;}
 else if(ch===','&&!quoted){row.push(cell);cell='';}
 else if((ch==='\n'||ch==='\r')&&!quoted){if(ch==='\r'&&raw[i+1]==='\n')i++;row.push(cell);if(row.some(s=>s.length))rows.push(row);row=[];cell='';}
 else cell+=ch;}
 if(cell.length||row.length){row.push(cell);rows.push(row);}return rows;
}
const css=`:root{color-scheme:light}*{box-sizing:border-box}body{margin:0;background:#fff;color:#183746;font:18px/1.75 Arial,sans-serif}header{background:#f0f6f6;border-top:6px solid #029990;padding:28px max(24px,calc((100% - 1040px)/2))}main{max-width:1088px;margin:auto;padding:24px}h1{font-size:38px;line-height:1.18}h2{font-size:28px;line-height:1.25;margin-top:42px;scroll-margin-top:20px}h3{font-size:22px;line-height:1.3;margin-top:30px}p,li{max-width:90ch}a{color:#0759a0;text-underline-offset:3px;overflow-wrap:anywhere}nav{display:flex;gap:12px 24px;flex-wrap:wrap}code{font:0.88em Consolas,monospace;background:#edf3f5;padding:2px 5px;overflow-wrap:anywhere}pre{padding:20px;background:#edf3f5;overflow:auto}pre code{padding:0}img{max-width:100%;height:auto}table{border-collapse:collapse;width:100%;font-size:16px}td,th{border:1px solid #ccd9de;padding:12px;vertical-align:top;text-align:left;overflow-wrap:anywhere}th{background:#e7f0f2}.table-wrap{overflow:auto;margin:20px 0}blockquote{border-left:4px solid #ed9c03;margin:24px 0;padding:8px 20px;background:#fff8e8}.meta{font-size:14px;color:#506675}details{margin:18px 0;padding:14px 18px;border:1px solid #ccd9de;border-radius:5px}summary{cursor:pointer;font-weight:bold}dt{font-weight:bold;margin-top:12px}dd{margin:2px 0 14px;overflow-wrap:anywhere}.toc{columns:2;padding-left:22px}.toc li{font-size:15px;margin:6px 0}button{font:inherit;padding:7px 12px;border:1px solid #8eaab4;background:white;cursor:pointer}@media(max-width:700px){body{font-size:16px}h1{font-size:29px}.toc{columns:1}main{padding:18px}}@media print{header nav,.toc,button{display:none}body{font-size:11pt}header{background:white;padding:12px 0}main{max-width:none;padding:0}details{break-inside:avoid}h2,h3{break-after:avoid}table{font-size:10pt}}`;
fs.writeFileSync(path.join(output,'reader.css'),css);
const renderer=new marked.Renderer();
renderer.html=token=>/^<br\s*\/?\s*>$/i.test(token.text.trim())?'<br>':esc(token.text);
for(const doc of docs.values()){
 const raw=fs.readFileSync(doc.file,'utf8').replace(/^\uFEFF/,'');
 if(raw.length>2500000)throw Error('Prepared document too large for reader: '+doc.source);
 const destination=path.join(output,doc.reader);
 let title,body;
 if(doc.file.toLowerCase().endsWith('.csv')){
  const rows=csvRows(raw),headers=rows.shift()||[];title=path.basename(doc.file,'.csv').replaceAll('_',' ');
  body='<p>Open a record to read its fields. Values are reproduced from the CSV; a readiness label is the source document’s recorded state, not a new runtime verification.</p>'+rows.map((row,i)=>`<details${i===0?' open':''}><summary>${esc(row.slice(0,2).join(' · ')||'Record '+(i+1))}</summary><dl>${headers.map((h,j)=>row[j]?`<dt>${esc(h)}</dt><dd>${esc(row[j]).replaceAll('\n','<br>')}</dd>`:'').join('')}</dl></details>`).join('');
 }else{
  const cleaned=raw.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/,'').replace(/^<!-- diagram-design-profile[\s\S]*?-->\s*/,'');
  title=(cleaned.match(/^#\s+(.+)$/m)?.[1]||cleaned.match(/^\*\*(.+)\*\*$/m)?.[1]||path.basename(doc.file,'.md').replaceAll('_',' ')).replaceAll('**','');
  body=marked.parse(cleaned,{renderer});
 }
 const used=new Set();const headings=[];
 body=body.replace(/<h([1-4])>(.*?)<\/h\1>/g,(_,level,text)=>{const base=id(text)||'section';let key=base,n=2;while(used.has(key))key=base+'-'+n++;used.add(key);if(level<4)headings.push({text:text.replace(/<[^>]*>/g,''),key});return `<h${level} id="${key}">${text}</h${level}>`;});
 body=body.replace(/\b(href|src)="([^"]+)"/g,(_,kind,url)=>{
  if(kind==='href')return `href="${esc(mapHref(url,doc.file,destination))}"`;
  const local=resolveLocal(url,doc.file);return `src="${esc(local?relative(destination,local.file)+local.fragment:url)}"`;
 }).replaceAll('<table>','<div class="table-wrap"><table>').replaceAll('</table>','</table></div>');
 const sourceLink=relative(destination,doc.file),modified=fs.statSync(doc.file).mtime.toISOString();
 const toc=headings.length>3?`<details><summary>Jump to a section</summary><ul class="toc">${headings.map(h=>`<li><a href="#${h.key}">${esc(h.text)}</a></li>`).join('')}</ul></details>`:'';
 const html=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><link rel="stylesheet" href="reader.css"></head><body><header><nav><a href="index.html">Prepared documents</a><a href="../Slides/Week02/ReviewRefined20260909/index.html">Latest Week 2 review</a><a href="${sourceLink}" download>Download editable source</a><button type="button" onclick="window.print()">Print / save PDF</button></nav><p class="meta">Formatted local document · source: ${esc(doc.source)}<br>Source modified: ${modified}. Content is reproduced from this document; earlier reviews retain their original slide numbering and proposal status.</p></header><main>${toc}${body}</main></body></html>`;
 fs.writeFileSync(destination,html);doc.title=title;doc.sha256=crypto.createHash('sha256').update(raw).digest('hex');doc.modified=modified;
}
const manifest={documents:[...docs.values()].map(({file,...d})=>d),rewritten_html_files:changed};
fs.writeFileSync(priorPath,JSON.stringify(manifest,null,2)+'\n');
const groups=[
 ['Museum integration',d=>d.source.startsWith('TechArtMuseumIntegration/')||d.source.startsWith('SourceArtDepot/')],
 ['Latest Week 2 review',d=>d.source.includes('ReviewRefined20260909/')],
 ['Visual system and skill',d=>d.source.includes('/Visuals/')||d.source.includes('/Skills/')],
 ['Earlier review and prepared examples',d=>d.source.includes('/Slides/Week02/Review/')],
 ['Course organization',d=>!d.source.includes('/Wiki/')],
 ['Wiki source references',d=>true]
];
const remaining=new Set(docs.values());
const indexSections=groups.map(([title,test])=>{const items=[...remaining].filter(test).sort((a,b)=>a.title.localeCompare(b.title));for(const item of items)remaining.delete(item);if(!items.length)return '';const list='<ul>'+items.map(d=>`<li><a href="${d.reader}">${esc(d.title)}</a><br><span class="meta">${esc(d.source)}</span></li>`).join('')+'</ul>';return title==='Wiki source references'?`<details><summary>${title} (${items.length})</summary><p>The normal course wiki already provides readable student pages. These views retain the editable-source context.</p>${list}</details>`:`<section><h2>${title}</h2>${list}</section>`;}).join('');
fs.writeFileSync(path.join(output,'index.html'),`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prepared course documents</title><link rel="stylesheet" href="reader.css"><header><h1>Prepared course documents</h1><nav><a href="../Slides/Week02/ReviewRefined20260909/index.html">Latest review</a><a href="../Visuals/index.html">Visual library</a><a href="../Wiki/index.html">Course wiki</a></nav><p>Readable local views with section navigation, images, and printable layouts. These are prepared course documents; external primary references remain clearly separate.</p></header><main>${indexSections}</main></html>`);
console.log(JSON.stringify({readers:docs.size,html_files_with_updated_document_links:rewritten}));
