from pathlib import Path
import json, re, html, hashlib, zipfile, xml.etree.ElementTree as ET, shutil
R=Path.cwd(); O=R/'Course/Slides/Week07/KarolIntegrated20261014'; N=Path('C:/Users/antho/OneDrive/Desktop/Notes/anthony/personal/Duke Tech Art Course Notes/16 Karol UE Python Course')
M=json.loads((O/'slide-map.json').read_text()); esc=html.escape
D={
0:('Covered','3, 6, 19, 24','Automation scope and production uses already frame the opening.'),
1:('Covered','4–5','Plugins, restart and host readiness already covered. Keep engine-version package differences in preparation.'),
2:('Covered','8–9','IDE stub path is for autocomplete; runtime remains Unreal. No extra installation lecture.'),
3:('Reference','K2 / 76','Typed Map reinforces boundary types. Full typing syntax and legacy comments remain notes.'),
6:('Integrated','13; K3 / 117','Discoverability, qualified package names and host search paths.'),
7:('Integrated','13','File execution versus cached import, and intentional reload with cleanup.'),
8:('Deferred','Course notes','Headless commandlet and startup readiness are useful later pipeline depth; not required for the current interactive demos.'),
9:('Integrated','13; K3 / 117','Startup/import cache context in narration. Avoid implicit classroom receiver startup.'),
10:('Covered','10–18, 25','Subsystems, actors/assets, selection and path forms already explicit.'),
11:('Covered','21, 23','Inheritance-aware filtering already visible. Library filters and benchmark comparison remain reference.'),
12:('Integrated','21, 23','Project suffix rules, report versus apply and actual/expected messages. Keep current _Normal conventions.'),
13:('Integrated','21 narration','A notifying setter may rebuild dependent data. Inspect actual appearance as well as assigned values; no universal sRGB rewrite.'),
14:('Integrated','106 (formerly 105) narration','Validate parameter names, read back results, and treat clear-all-overrides as a separate consequential operation.'),
15:('Deferred','Course notes','Duplicate placement detection is a candidate report, not proof of redundant actors. Do not expand the chosen Material/VFX scope.'),
16:('Deferred','Course notes','ImporterRules is an external framework. Automatic metadata-based moving could break the bridge’s stable destination/ownership contract.'),
17:('Integrated','13 narration; course reference','Reload requires callback cleanup; a module flag is not reload-safe. Do not add post-import auto-moving to the bridge.'),
18:('Deferred','Course notes','Referencer queries depend on saved state and cannot prove dynamic non-use. Force deletion is outside the demo and is not an Undo example.'),
19:('Covered','29, 67–69','Task fields, imported paths and explicit current importer behavior exist. Preserve material and destination policy.'),
20:('Reference','Course notes','AutomatedAssetImportData returns objects; task imports expose result paths. Keep one import API in the live bridge explanation.'),
21:('Integrated','23 narration','Rules are project policy, unsupported inputs are skipped, and useful failure messages identify actual/expected values.'),
22:('Reference','23; course notes','Full EditorValidatorBase registration and historical override signatures remain optional. No unverified version migration.'),
23:('Integrated','23 narration; audit','Square and allowed dimensions are independent checks. 300x300 is square, while 256x512 is not.'),
24:('Integrated','23 narration; audit','The explicit allowed tuple excludes 1 and sizes over 8192. Do not describe it as merely a maximum-size rule.'),
25:('Reference','23; course notes','Missing registry triangle tags are NOT_VALIDATED, not a pass. Counts are project budgets, not proof of runtime cost.'),
26:('Covered','7, 10; K1 / 107','dir/help and signatures support API reading. Avoid unnecessary print(help(...)) or new live material.'),
27:('Reference','K3 / 117; course notes','Interpreter-compatible dependency setup is retained. Live debugger attachment can pause the editor; keep it in preparation.'),
29:('Reference','61, 75; course notes','ToolMenu entry ownership/lifecycle useful for packaging; existing UI entry points already satisfy the lesson.'),
30:('Deferred','Course notes','Slate style keys are version/context dependent. Icon implementation is detail beyond this integration.'),
31:('Reference','Course notes','ToolMenus.Edit and supported entry types useful for advanced UI authoring, not required for publisher diagnostics.'),
32:('Reference','13, 61 narration','Explicit owner cleanup supports deliberate reload. Do not confuse owner name with submenu path.'),
33:('Integrated','44 narration; K5 / 119','Progress requires consistent units and cooperative cancellation. Cancellation leaves completed work in place.'),
34:('Integrated','44, 59; K5 / 119','Transaction scope groups supported changes; imports/files require separate recovery. Existing material assignment Undo remains accurate.'),
35:('Integrated','K6 / 120','Distinguish runner/plugin setup and excluded tests from passes. Keep ordinary bridge unittest separate.'),
36:('Integrated','46 narration; K6 / 120','Explicit call and deliberate failure prove the check is actually exercised.'),
37:('Integrated','46, 98; K6 / 120','Meaningful boundary/failure cases, isolated state and full workflow evidence. Implemented in diagnostics tests.'),
38:('Integrated','K6 narration','Expected logs must come from the real condition. Synthetic matching warnings are not verification.'),
39:('Integrated','61 narration','UI calls reusable operations; adapters handle host APIs. Do not wrap an Unreal Array as a single list item.'),
40:('Integrated','75; K2 / 76','Named Python output variable and Blueprint pin match. Execution success is separate from domain success.'),
41:('Reference','K4 / 118','Remote Control is an optional alternative transport, not the prepared file bridge.'),
42:('Deferred','Course notes','Preset/web interface is a useful later museum-control example. Avoid adding server/plugin setup to this lesson.'),
43:('Deferred','Course notes','Controllers can bind one input to multiple compatible properties. Keep this as later museum-control study.'),
44:('Integrated','K4 / 118','Inspect HTTP response and exposed method result. JSON-string returns require a second decode only for that contract.'),
45:('Integrated','K5 narration; course reference','Multi-request modal lifetime requires finally cleanup; do not transplant fragile remote progress into the existing bridge.'),
46:('Integrated','29; bridge diagnostics','Export, send, acknowledgement and inspection are separate evidence. Current selected-mesh scope is explicit.'),
47:('Integrated','K4 / 118','Discover the default-object path from the registered class. Path regression and HTTP reachability are separate checks.'),
48:('Integrated','13, 61; K3 / 117; Copy diagnostics','Identify interpreter/module folder and nested failure. Preserve dependency direction and package-qualified imports.'),
49:('Integrated','10 narration','Retrieve the editor-managed subsystem. This is not a blanket ban on Unreal constructors.'),
50:('Integrated','10; K2 / 76; 106 narration','Direct array iteration, explicit typed Map boundary, and struct construction distinct from parameter assignment.')}
rows=[]
for f in sorted(N.rglob('* - REFINED.md'),key=lambda p:p.name):
    num=int(f.name[:2]); content=f.read_text(encoding='utf-8'); status,where,decision=D[num]
    rows.append(dict(lesson=num,title=f.stem,source=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),words=len(content.split()),images=len(re.findall(r'!\[\[',content)),status=status,destination=where,decision=decision))
assert len(rows)==48 and set(D)=={r['lesson'] for r in rows}
(O/'coverage.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
def texts(deck):
    with zipfile.ZipFile(deck) as z:
        return {int(re.search(r'slide(\d+)\.xml$',n)[1]):'\n'.join(ET.fromstring(z.read(n)).itertext()) for n in []} if False else {int(re.search(r'slide(\d+)\.xml$',n)[1]):'\n'.join(t.text or '' for t in ET.fromstring(z.read(n)).findall('.//a:t',ns)) for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)}
old=texts(Path(M['source']));new=texts(O/'.build/candidate.pptx')
style='''body{font:17px/1.55 system-ui;margin:0;color:#202332;background:#f5f6f9}main{max-width:1380px;margin:auto;padding:35px}a{color:#285c9b}h1{font-size:36px}h2{margin-top:2em}article,section.box{background:white;border:1px solid #d9dce5;border-radius:8px;padding:24px;margin:22px 0}img{max-width:100%;height:auto;border:1px solid #ddd}.pair{display:grid;grid-template-columns:1fr 1fr;gap:22px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f1f3f7;padding:16px;font:14px/1.5 Consolas,monospace}input,select{font:inherit;padding:10px;border:1px solid #aaa;border-radius:4px}nav{display:flex;gap:22px;flex-wrap:wrap}table{border-collapse:collapse;width:100%}td,th{text-align:left;border-bottom:1px solid #ddd;padding:13px;vertical-align:top}td:first-child{width:25%}.tag{font-weight:bold;color:#476153}.sub{color:#596171}.notes{max-width:1050px}.control{position:sticky;top:0;background:#f5f6f9;padding:12px;z-index:2}details{margin:14px 0}summary{cursor:pointer;font-weight:600}@media(max-width:760px){main{padding:16px}.pair{grid-template-columns:1fr}td,th{padding:7px}table{font-size:14px}}'''
head='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 7 · Karol integrated revision</title><style>'+style+'</style><main>'
body='''<h1>Week 7: Karol integration completed</h1><p>14 October 2026 · v14 · 120 slides: 54 live and 66 hidden references. The live sequence and 150-minute session remain unchanged.</p><nav><a href="output/Week_7_Python_in_Unreal_v14.pptx">Open updated PowerPoint</a><a href="#changes">Slide comparisons</a><a href="#coverage">All 48 lessons</a><a href="#diagnostics">Copy diagnostics</a><a href="gallery.html">All slides and narration</a></nav><section class="box"><h2>What this revision integrates</h2><p>The subsystem and array explanation, import recovery pointer and bridge acknowledgement sequence are now in the deck. The optional Map example follows the Blueprint overview. The full-note pass also added property-result verification, cancellation versus Undo, explicit test invocation, and parameter-override scope.</p><p>Five optional slides: K2 (76), K3 (117), K4 (118), K5 (119), K6 (120). All remain hidden during the main slide show. Existing stable anchors remain unchanged; physical slide numbers after the new Map slide shift by one.</p><p>UI/UX redesign, Golden Path imagery and motion proposals from other reviews remain separate. This revision preserves the current design and their source material rather than treating those proposals as already approved deck edits.</p><p><a href="../UnrealFirst20261013/teach.html">Existing timed teaching route</a> · <a href="../LiveTesting20261013/index.html">Instructor host rehearsal walkthrough</a> · <a href="../KarolCompletionReview20261014/index.html">Previous completion review</a></p></section>
<section class="box" id="diagnostics"><h2>Copy diagnostics in Blender and Maya</h2><p>Both publishers copy the same read-only JSON snapshot: host/Python versions, module path, active and configured exchange folders, receiver project/session/heartbeat, manifest, pending or last request ID, result and status. Reading the report does not export, import, resend or consume the pending acknowledgement.</p><p>The last completed or failed result remains available after the regular UI poll. New publishing or switching exchange folders clears that context. Missing, stale and malformed records remain diagnosable. Clipboard confirmation does not replace the operation status.</p><p>Offline tests and the Maya offscreen button/clipboard check passed. No live Unreal session or Blender UI was controlled. Reload the publishers before instructor rehearsal, then exercise offline, pending, failure and success cases and inspect the copied text. Review local paths before sharing.</p><img style="width:600px;max-width:100%" src="../../../../../../Week07UnrealPython/Docs/Bridge/maya-publisher.png" alt="Actual Maya UI rendered offscreen with Copy diagnostics and confirmation"><p><a href="../../../../../../Week07UnrealPython/Docs/Bridge/README.md">Bridge instructions and report behavior</a></p></section>
<h2 id="changes">Actual v13 content and v14 changes</h2><p>Rationale and field edits are editorial guidance. Narration is the read-aloud text stored in the updated deck.</p><div class="control"><input id="q" placeholder="Search slides or lessons" aria-label="Search"><select id="filter" aria-label="Slide route"><option value="all">All slide changes</option><option value="live">Live route</option><option value="optional">Optional material</option></select></div>'''
for s in M['slides']:
    if not s['changed']:continue
    n=s['number'];src=s['source'];kind='optional' if s['hidden'] else 'live'
    change=next((c['reason'] for c in M['changes'] if c['source']==src),'New optional slide, hidden from the live route. Reuses the deck typography and reference palette.')
    old_image=f'../UnrealFirst20261013/previews/slide-{src:02}.png' if src else ''
    if src and (O/f'.build/before-{src}.png').exists():
        (O/'before').mkdir(exist_ok=True);shutil.copyfile(O/f'.build/before-{src}.png',O/f'before/slide-{src}.png');old_image=f'before/slide-{src}.png'
    prior=f'<h3>v13 · physical {src}</h3><img loading="lazy" src="{old_image}" alt="Original slide {src}"><details><summary>Exact original slide text</summary><pre>{esc(old[src])}</pre></details>' if src else '<h3>New optional material</h3><p>No prior slide. Added after the existing Blueprint overview for K2; remaining references follow the former final reference slide.</p>'
    narration=s['notes'].split('\n\nSource insight')[0].split('\n\nFacilitation')[0]
    body+=f'<article class="entry" data-route="{kind}" id="slide-{n}"><h2>v14 slide {n} · {kind}</h2><p><b>Field edits / rationale:</b> {esc(change)}</p><div class="pair"><div>{prior}</div><div><h3>Updated slide {n}</h3><img loading="lazy" src="previews/slide-{n:03}.png" alt="Updated slide {n}"><details><summary>Exact updated slide text</summary><pre>{esc(new[n])}</pre></details></div></div><details><summary>Read-aloud narration</summary><p class="notes">{esc(narration).replace(chr(10),"<br>")}</p></details></article>'
body+='<h2 id="coverage">Full REFINED collection: 48 lesson decisions</h2><p>Read every existing REFINED lesson, including code and caveats. This pass assesses teaching integration; it does not claim to revalidate every historical screenshot against the current engine. Lessons 04, 05 and 28 are absent from the collection. Original and refined note files are unchanged in this pass.</p><table><thead><tr><th>Lesson</th><th>Decision / destination</th><th>Technical context retained</th></tr></thead><tbody>'
for r in rows:
    body+=f'<tr class="lesson"><td><a href="{Path(r["source"]).as_uri()}">{esc(r["title"].removesuffix(" - REFINED"))}</a></td><td><b>{r["status"]}</b><br>{esc(r["destination"])}</td><td>{esc(r["decision"])}</td></tr>'
body+='</tbody></table><section class="box"><h2>Integration boundaries</h2><p>Automatic asset moving/deletion, remote web control, icon/menu construction and commandlet deployment remain reference topics. They would add new workflow requirements or duplicate existing demonstrations. The current bridge keeps its stable asset identity, material-preservation policy, explicit file transport and recovery path.</p><p>Source credit: Karol Kowalczyk / Tech Art Corner for supplemental course material and the typed-Map capture. The original Northwood project remains the instructor’s result of following Isaac Oster’s course; the classroom tooling is its preparation spinoff.</p></section>'
body+='''<script>function filter(){let q=document.querySelector('#q').value.toLowerCase(),f=document.querySelector('#filter').value;document.querySelectorAll('.entry').forEach(e=>e.hidden=!(e.textContent.toLowerCase().includes(q)&&(f==='all'||e.dataset.route===f)));document.querySelectorAll('.lesson').forEach(e=>e.hidden=!e.textContent.toLowerCase().includes(q));}document.querySelector('#q').oninput=filter;document.querySelector('#filter').onchange=filter;</script></main></html>'''
# Relative project links: report directory is Course/Slides/Week07/<revision>, four levels below repo.
body=body.replace('../../../../../../Week07UnrealPython/','../../../../Week07UnrealPython/')
(O/'index.html').write_text(head+body,encoding='utf-8')
gallery=head+'<h1>Week 7 v14: all slides</h1><p><a href="index.html">Back to integration review</a> · Slides 1–54 are live. Slides 55–120 are hidden references.</p>'
for s in M['slides']:
    n=s['number'];gallery+=f'<article id="slide-{n}"><h2>Slide {n} · {"optional" if s["hidden"] else "live"}</h2><img loading="lazy" src="previews/slide-{n:03}.png" alt="Slide {n}"><details><summary>Slide text and notes</summary><pre>{esc(new[n])}</pre><p>{esc(s["notes"]).replace(chr(10),"<br>")}</p></details></article>'
(O/'gallery.html').write_text(gallery+'</main></html>',encoding='utf-8')
print('48 lessons,',len([s for s in M['slides'] if s['changed']]),'changed/new slides; report written')

