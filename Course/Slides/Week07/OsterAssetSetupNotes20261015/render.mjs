import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const deps='C:/Users/antho/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {marked}=await import(pathToFileURL(path.join(deps,'marked/lib/marked.esm.js')));
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const manifest=JSON.parse(fs.readFileSync(path.join(dir,'source-manifest.json'),'utf8'));
function nav(prefix=''){return '<nav>'+[['index.html','Overview'],['compiled-notes.html','Full compilation'],['assessment.html','Assessment & course use'],['original-script.html','Original source script']].map(([file,title])=>`<a href="${prefix+file}">${title}</a>`).join('')+'</nav>';}
function page(title,body,prefix=''){return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+'</title><link rel="stylesheet" href="'+prefix+'notes.css"></head><body><main>'+nav(prefix)+body+'<p class="foot">Refined 15 October 2026 · Isaac Oster source notes · original captures preserved · supplied lesson content and teaching adaptations are distinguished.</p></main></body></html>';}
function renderMarkdown(md){
 let html=marked.parse(md),headings=[],used=new Map();
 html=html.replace(/<h([2-3])>([\s\S]*?)<\/h\1>/g,(_,level,title)=>{const plain=title.replace(/<[^>]+>/g,'');const stem=plain.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');const n=used.get(stem)||0;used.set(stem,n+1);const id=stem+(n?'-'+n:'');headings.push({id,title:plain});return `<h${level} id="${id}">${title}</h${level}>`;});
 html=html.replace(/<img src="([^"]+)" alt="([^"]*)">/g,'<a href="$1"><img loading="lazy" src="$1" alt="$2"></a>');
 const toc='<details class="toc"><summary>On this page</summary><ul>'+headings.map(x=>`<li><a href="#${x.id}">${esc(x.title)}</a></li>`).join('')+'</ul></details>';
 return toc+'<article class="reading">'+html+'</article>';
}
for(const n of manifest.notes){
 const name=String(n.lesson).padStart(2,'0');
 const md=fs.readFileSync(path.join(dir,n.local_note),'utf8');
 fs.writeFileSync(path.join(dir,'notes',name+'.html'),page('Oster Asset Setup '+name,renderMarkdown(md),'../'));
}
for(const [file,title] of [['compiled-notes','Oster asset setup compiled notes'],['assessment','Oster notes assessment and course use']]){
 fs.writeFileSync(path.join(dir,file+'.html'),page(title,renderMarkdown(fs.readFileSync(path.join(dir,file+'.md'),'utf8'))));
}
const code=fs.readFileSync(path.join(dir,'sources/original-buildSelectedAssets.py'),'utf8');
const codeHtml='<p class="eyebrow">Preserved source example</p><h1>The supplied buildSelectedAssets script</h1><p>This is the code from Asset Setup 03, preserved with normalized line endings. It assumes the caller has imported <code>unreal</code>. It includes asset deletion, assignment and saving; it was not executed during refinement.</p><p><a href="notes/03.html">Read the refined explanation</a> · <a href="assessment.html">Read the corrections and qualifications</a> · <a href="sources/original-buildSelectedAssets.py">Open the extracted code file</a></p><pre class="source-code">'+code.split('\n').map((line,i)=>`<span id="line-${i+1}">${esc(line)||' '}</span>`).join('')+'</pre>';
fs.writeFileSync(path.join(dir,'original-script.html'),page('Original Oster setup script',codeHtml));
const labels=[['Identify imported assets','Trace operation scope, distinguish path types and retain the meshes and textures that belong to the import.'],['Inspect slots and create instances','Read StaticMaterial structures, understand class/factory pairing and make naming and replacement choices explicit.'],['Connect, assign and save','Set the parent and texture overrides, match full texture identities and distinguish mesh defaults from component overrides.']];
let body='<p class="eyebrow">Unreal Python · refined study notes</p><h1>Oster asset setup notes</h1><p class="lead">A practical sequence from imported meshes and textures to material instances, assignments and saved assets—with the assumptions and current API details made explicit.</p><p class="stats">3 refined lessons · 44 preserved captures · 5 syntax-checked teaching snippets</p><div class="notice">These are Asset Setup 01–03. The first lesson recaps the separate import/export series. The original notes and complete supplied script remain unchanged; the new examples are labeled teaching adaptations.</div><div class="cards">';
for(let i=0;i<3;i++){body+=`<section class="card"><p class="eyebrow">Asset Setup 0${i+1}</p><h2>${labels[i][0]}</h2><p>${labels[i][1]}</p><a href="notes/0${i+1}.html">Read the refined lesson →</a></section>`;}
body+='</div><h2>What changed in the refinement</h2><p>Repetitive transcript wording is organized into a clear workflow. API names, path types, structs and factories are explained precisely. Deletion, replacement, naming collisions, texture matching and assignment scope are assessed beside the relevant operations.</p><p>The import-result approach and exact texture-name parser are supplemental examples. They do not silently rewrite what Oster demonstrated. The current UE 5.7 project API was used to check selected signatures; no Unreal session or asset operation was run.</p><p><a href="compiled-notes.html">Read the complete compilation</a> · <a href="assessment.html">Assessment and course applications</a> · <a href="compiled-notes.md">Editable compilation</a> · <a href="source-manifest.json">Source and image provenance</a></p><h2>Updated notes folder</h2><p>Each original now has an adjacent <code>- REFINED.md</code> companion, and the folder has a <code>REFINED - Course Index.md</code>. The companion files retain the original Obsidian image embeds.</p><p><a href="'+esc(pathToFileURL(path.join(path.dirname(manifest.notes[0].source),'REFINED - Course Index.md')).href)+'">Open the vault index</a></p><h2>Connection to Week 7</h2><p>Use a visible mapping from source file to imported object, mesh slot, material instance and texture roles. Then ask which object will change and how to confirm the result. This complements the fuller slide explanations already being prepared and leaves room for colleagues to elaborate through demos. No slide deck or teaching-tool code was changed in this notes pass.</p>';
fs.writeFileSync(path.join(dir,'index.html'),page('Oster asset setup notes',body));
console.log('Rendered overview, three lessons, compilation, assessment and original-script reading view.');
