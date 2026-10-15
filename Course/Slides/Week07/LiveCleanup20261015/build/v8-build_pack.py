"""Current classroom entry points and an actual v7/v8 review; no student doc duplication."""
from pathlib import Path
from zipfile import ZipFile
from lxml import etree as E
from html import escape as h
import ast,json,posixpath,shutil,hashlib
OUT=Path(__file__).resolve().parent
OLD=OUT.parent/'Refinement20261015'
shutil.copy2(OLD/'pack.css',OUT/'pack.css')
(OUT/'assets/documents').mkdir(parents=True,exist_ok=True)
# Reuse the established page and Word-reading layout without executing the old builder.
helper=ast.parse((OLD/'build_pack.py').read_text(encoding='utf-8'))
for node in helper.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('page','header','table','doc_reader'):
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(OLD/'build_pack.py'),'exec'))
NAV=[('index.html','Class pack'),('route.html','Teaching route'),('review.html','Slide review'),('lab1.html','Lab 1'),('peer-review.html','Peer review'),('dashboard.html','Round timer'),('facilitator.html','Instructor guide'),('live-demo.html','Demo')]
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS={'w':W,'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
inventory=json.loads((OUT/'build/pre-direct-copy-inventory.json').read_text())
changes=json.loads((OUT/'qa/content-changes.json').read_text())
direct=json.loads((OUT/'qa/direct-copy-changes.json').read_text())
edits={c['slide']:c for c in direct['edits']}
plan=json.loads((OLD/'content-plan.json').read_text(encoding='utf-8'))
deck='output/Week 7 - Direct Copy v8.pptx'
candidate=OUT/'build/candidate-v8.pptx'
with ZipFile(candidate) as z:
 package={n:z.read(n) for n in z.namelist()}
def relationships(part):
 rp=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
 return {q.get('Id'):q.get('Target') for q in E.fromstring(package[rp])}
pres=E.fromstring(package['ppt/presentation.xml'])
ids=pres.findall('p:sldIdLst/p:sldId',NS)
id_to_number={x.get('{'+NS['r']+'}id'):i+1 for i,x in enumerate(ids)}
live=[id_to_number[x.get('{'+NS['r']+'}id')] for x in pres.findall('.//p:custShow/p:sldLst/p:sld',NS)]
slides=[]
for item in inventory:
 n=item['number'];part=item['part'];x=E.fromstring(package[part])
 texts=[''.join(p.xpath('.//a:t/text()',namespaces=NS)) for p in x.findall('.//a:p',NS)]
 titles=[]
 for sp in x.findall('.//p:sp',NS):
  value=' '.join(sp.xpath('.//a:t/text()',namespaces=NS));sizes=[int(v) for v in sp.xpath('.//a:rPr/@sz|.//a:defRPr/@sz',namespaces=NS)]
  ph=sp.find('.//p:ph',NS)
  if value and value!=str(n):titles.append((100000 if ph is not None and ph.get('type') in ('title','ctrTitle') else max(sizes or [0]),value))
 title=max(titles,default=(0,f'Slide {n}'))[1]
 title={7:'VS Code Autocomplete',8:'VS Code Settings'}.get(n,title)
 narration=''
 for target in relationships(part).values():
  if 'notesSlide' not in target:continue
  np=posixpath.normpath(posixpath.join(posixpath.dirname(part),target));nx=E.fromstring(package[np])
  for sp in nx.findall('.//p:sp',NS):
   ph=sp.find('.//p:ph',NS)
   if ph is not None and ph.get('type')=='body':narration='\n\n'.join(''.join(p.xpath('.//a:t/text()',namespaces=NS)) for p in sp.findall('.//a:p',NS))
 slides.append({'number':n,'part':part,'title':title,'text':texts,'notes':narration,'hidden':x.get('show')=='0','live':n in live,'tables':len(x.findall('.//a:tbl',NS))})
(OUT/'qa/final-slide-inventory.json').write_text(json.dumps(slides,indent=2),encoding='utf-8')
docs=[('lab1.html','Investigate a batch renamer','Week 7 Lab 1 Student Handout v5.docx'),('peer-review.html','Prepare, test and revise a tool','Week 7 Peer Review Packet v4.docx'),('facilitator.html','Facilitate the two investigations','Week 7 Lab Instructor Guide v5.docx'),('live-demo.html','Demonstrate Material and VFX workflows','Week 7 Live Demo Run Sheet v5.docx')]
for file,title,name in docs:
 extra=''
 if file=='live-demo.html':extra='<p class="note">Rehearsed live in Unreal 5.7.4 on 15 October. <a href="walkthrough.html">Open the current capture walkthrough</a>. Use it after one short recovery attempt.</p>'
 if file=='facilitator.html':extra='<p class="note">Instructor answer material. Use <a href="reveal.html">the reveal</a> after students record predictions. In a Lab 1 triad, one person can hold two paper roles.</p>'
 page(file,title,header(title,'<a href="output/'+h(name)+'">Editable Word document</a> · <a href="qa/documents/'+h(Path(name).stem)+'/render.pdf">Print PDF</a>')+extra+doc_reader(name))
# These activities and timer have unchanged behavior; their local navigation now resolves here.
for name in ('dashboard.html','reveal.html'):
 shutil.copy2(OLD/name,OUT/name)
project='../../../..'+'/Week07UnrealPython'
links=''.join('<li><a href="'+file+'">'+h(title)+'</a> · <a href="output/'+h(name)+'">Word</a></li>' for file,title,name in docs)
page('index.html','Week 7 classroom pack',header('Python tools and artist experience','The gradient deck, current Unreal demonstrations and workshop materials are ready in one place.')+f'<p class="lead"><a href="{deck}">Open the revised PowerPoint</a> · <a href="review.html">Compare v7 and v8</a></p>'+'''<div class="grid"><section class="card"><h2>Presentation</h2><p><strong>88 visible slides.</strong> Eighteen lower-priority slides are hidden and recoverable. The PowerPoint custom show <strong>Week 7 live route</strong> contains 61 slides for the fixed timetable. Slide numbers stay stable.</p><p>The gradient artwork, five UX mantras and nine embedded videos remain.</p><p><a href="route.html">Teaching route and pacing</a></p></section><section class="card"><h2>Demonstrations</h2><p>Material and VFX workflows were rehearsed in both the native Unreal panel and live PySide window. Preview, Apply, duplicate protection and Undo were checked against the prepared scene.</p><p><a href="live-demo.html">Run sheet</a> · <a href="walkthrough.html">Current captures</a></p></section></div><h2>Classroom activities</h2><p>Lab 1: 5:10–5:18. Peer review: 5:30–6:00. Triads rotate through three seven-minute rounds, then self review and one revision. <a href="dashboard.html">Open the round timer</a>.</p><ul>'''+links+f'''</ul><h2>Student project</h2><p>Start with the <a href="{project}/README.md">project quick start</a>. Redundant guides and audit notes have been moved outside the project to the instructor archive. The numbered lesson examples and lab starter remain.</p><p><a href="{project}/Deliverables/Week07_Bridge_Student_Pack.zip">Bridge student pack</a></p><details><summary>Instructor background and verification</summary><p><a href="../OsterAssetSetupNotes20261015/index.html">Refined Oster notes</a> · <a href="../UXMantras20261015/index.html">UX notes and integration</a> · <a href="quality.html">Quality checks</a></p></details>''')
route=header('Protect the class timetable','Use the shorter route and reserve time for students to predict, inspect and discuss.')+'<p>PowerPoint: Slide Show → Custom Slide Show → <strong>Week 7 live route</strong>. The regular show has 88 visible slides. The custom show selects 61. Hidden slides remain available in edit view for optional questions.</p>'
route+=table([['Time','Topic','Minutes']]+plan['schedule'])
route+='<h2>Twelve-minute UX sequence</h2>'+table([['Time','Mantra','Slides','Teaching move'],['5:18–5:20','Know the task','66–67','User, outcome, benefit and protected scope.'],['5:20–5:23','Guide the eye','71, 75–77','Value, quick visual checks and GOLF+ prediction.'],['5:23–5:25','Make actions clear','80–81, 90','State, next action and actual Undo boundary.'],['5:25–5:27','Keep it consistent','92–94','Style-sheet rules and the AI workflow.'],['5:27–5:30','Test the workflow','96–97, 99','Choose a prototype. Separate evidence from inference.']])
route+='<p class="note">Narration is preparation depth. Use one definition, one example and one response per mantra. Keep colleagues’ fifteen minutes, the break and the thirty-minute peer review intact. If a demonstration stalls, make one short recovery attempt and continue with the labeled capture walkthrough.</p><h2>Live route</h2>'+table([['Slide','Topic']]+[[s['number'],s['title']] for s in slides if s['live']])
route+='<details><summary>18 hidden slides and reasons</summary>'+table([['Slide','Reason']]+[[n,r] for n,r in changes['hidden'].items()])+'</details>'
page('route.html','Week 7 teaching route',route)
cards=[]
capture_slides=[]
manifest=json.loads((OUT/'qa/capture-manifest.json').read_text())
media_names={x['media'] for x in manifest}
for s in slides:
 n=s['number'];captured=any(posixpath.basename(t) in media_names for t in relationships(s['part']).values())
 if captured:capture_slides.append(n)
 actions=[]
 if n in edits:actions.append(f'Use direct wording and topic titles. Projected text: {edits[n]["before_words"]} to {edits[n]["after_words"]} words.')
 if n in edits and edits[n]['source_credits_moved']:actions.append('Move the source footer into speaker notes.')
 if captured:actions.append('Keep the current cursor-free capture.')
 if s['hidden']:actions.append('Keep this slide hidden and available for questions.')
 if not actions:actions.append('Keep the existing wording and example.')
 reason=changes['hidden'].get(str(n),'State the topic plainly and explain only what the example needs.')
 label='Hidden' if s['hidden'] else 'Live route' if s['live'] else 'Visible supporting slide'
 cards.append(f'<article class="slide" id="slide-{n}" data-live="{str(s["live"]).lower()}" data-hidden="{str(s["hidden"]).lower()}"><p class="eyebrow">Slide {n} · stable number</p><h2>{h(s["title"])}</h2><span class="tag">{label}</span><div class="grid"><figure><a href="qa/render-v7/slide-{n:03}.png"><img loading="lazy" src="qa/render-v7/slide-{n:03}.png" alt="Actual v7 slide {n}"></a><figcaption>Before: v7</figcaption></figure><figure><a href="qa/render-v8/slide-{n:03}.png"><img loading="lazy" src="qa/render-v8/slide-{n:03}.png" alt="Actual v8 slide {n}"></a><figcaption>After: v8</figcaption></figure></div><p><strong>Keep/change:</strong> {h(" ".join(actions))}</p><p><strong>Teaching rationale:</strong> {h(reason)}</p><details><summary>Before wording</summary><pre>{h(chr(10).join(inventory[n-1]["text"]))}</pre></details><details><summary>Current wording</summary><pre>{h(chr(10).join(s["text"]))}</pre></details><details><summary>Read-aloud classroom narration and sources</summary><p class="script">{h(s["notes"])}</p></details></article>')
script='''<script>const search=document.querySelector('#search'),live=document.querySelector('#live'),hiddenOnly=document.querySelector('#hidden-only'),cards=[...document.querySelectorAll('.slide')];function filter(){let n=0;for(const card of cards){card.hidden=(live.checked&&card.dataset.live!=='true')||(hiddenOnly.checked&&card.dataset.hidden!=='true')||!card.textContent.toLowerCase().includes(search.value.toLowerCase());if(!card.hidden)n++;}document.querySelector('#count').textContent=n+' slides shown';}for(const x of [search,live,hiddenOnly])x.addEventListener('input',filter);filter();</script>'''
page('review.html','Week 7 actual slide comparison',header('Review the copy edits','Actual v7 and v8 renders, with source credits in speaker notes.')+'<p>The copy pass covers all 106 slides. Topic titles replace slogans, explanations are shorter, and source credits are in the notes. The 18 hidden slides and 61-slide live route are unchanged.</p><div class="controls"><label for="search">Find</label><input type="search" id="search" placeholder="Topic, slide or API"><label><input id="live" type="checkbox"> Live route only</label><label><input id="hidden-only" type="checkbox"> Hidden only</label><span id="count" role="status"></span></div>'+''.join(cards),script)
steps=[('Prepared scene','material-baseline.png','Two plain cubes and three empty marker bases. Run preflight and confirm the target and textures.',''),('Preview material','native-material-preview.png','One target, slot 0 and three texture roles. Preview makes no scene changes.',''),('Apply material','native-material-applied.png','One instance is created and assigned to the target. The protected cube and shared mesh default stay unchanged.','material-result.png'),('Undo assignment','material-undo.png','Undo restores the component assignment. The created instance remains in the Content Browser; it is not a full asset rollback.',''),('Preview VFX','native-vfx-preview.png','Three reviewed markers, one fountain per marker. Confirm the intended count before Apply.',''),('Inspect three fountains','vfx-result.png','Three particle systems run at the marker locations. Check positions and the dark stage for visible particles.','native-vfx-applied.png'),('Reject a duplicate batch','native-vfx-duplicate.png','A second placement at the same anchors is blocked. No duplicate actors are created.',''),('Restore the classroom state','material-baseline.png','Undo the VFX placement batch. The three marker bases remain. The final live readback confirmed plain cubes and zero effects.','')]
walk=''
for i,(title,src,body,extra) in enumerate(steps):
 walk+=f'<section class="step card"{(" hidden" if i else "")}><h2>{i+1}. {h(title)}</h2><p>{h(body)}</p><img src="captures/{src}" alt="{h(title)}">'+(f'<details><summary>Inspect the matching result</summary><img src="captures/{extra}" alt="Matching live result"></details>' if extra else '')+'</section>'
walkscript='''<script>const steps=[...document.querySelectorAll('.step')];let at=0,all=false;const prev=document.querySelector('#prev'),next=document.querySelector('#next'),count=document.querySelector('#count');function render(){steps.forEach((s,i)=>s.hidden=!all&&i!==at);prev.disabled=all||at===0;next.disabled=all||at===steps.length-1;count.textContent=all?'All '+steps.length+' steps':(at+1)+' / '+steps.length;}prev.onclick=()=>{at=Math.max(0,at-1);render()};next.onclick=()=>{at=Math.min(steps.length-1,at+1);render()};document.querySelector('#all').onclick=()=>{all=!all;document.querySelector('#all').textContent=all?'One step at a time':'Show all';render()};document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'&&!next.disabled)next.click();if(e.key==='ArrowLeft'&&!prev.disabled)prev.click()});render();</script>'''
page('walkthrough.html','Current Material and VFX captures',header('Material and VFX walkthrough','Recorded from the prepared Unreal 5.7.4 project on 15 October 2026.')+'<p><a href="live-demo.html">Current run sheet</a>. Native panel and viewport captures contain no AI pointer overlay. These are recorded states, not a running simulation.</p><div class="controls"><button id="prev">Previous</button><span id="count" role="status"></span><button id="next">Next</button><button id="all">Show all</button></div>'+walk,walkscript)
quality=header('Quality and rehearsal evidence','Checks cover the current prepared project, deck and classroom materials.')+table([['Check','Result'],['Live Unreal rehearsal','Material and VFX in native Slate and live PySide: preview, apply, exact scope, duplicate blocking and Undo verified. Qt stale selection and empty selection blocked.'],['Actual scene','Target changed; protected cube and shared mesh default unchanged. Exactly three VFX actors at the reviewed markers. Particles visible. Darker stage saved in the baseline map.'],['Clean restart','Rehearsal-only instances discarded; no effects remain. Preflight passes. Qt panel fits the available screen.'],['Tool copy','Preview / Apply actions; After Apply becomes Result. Short labels, compact asset names and full-path tooltips. No authored UI em dashes.'],['Project simplification','Redundant Docs tree and root START_HERE moved to an instructor archive. One project README. Lesson code, lab starter and attribution retained. Bridge ZIP rebuilt.'],['Slide cleanup','18 hidden; 88 visible; 61-slide native custom show. 100 slides revised for direct wording and topic titles; 28 source footers moved to notes. Empty footer placeholders and em dashes remain absent.'],['Visuals','Gradient style, native tables and nine videos retained. 15 screenshot assets updated using actual widget/viewport captures with no AI cursor overlay.'],['Code checks','88 project tests and 18 cumulative assistant UI gates passed. Native plugin rebuilt successfully.'],['Presentation checks','106 native PowerPoint renders; zero measured text-fit failures. Projected copy and layout checked after the rewrite.'],['Documents','Four editable documents remain coherent: 1, 3, 2 and 4 pages. All ten pages inspected. Current scene captures replace old run-sheet images.'],['Teaching sequence','Oster setup reasoning precedes demos. Five UX mantras connect art, user stories and implementation. Prediction precedes reveal; peer review ends in a retest.'],['Scope','Live rehearsal covers this UE 5.7.4 fixture and both tool interfaces. It is not a cross-version, performance or full accessibility certification. GOLF+ still supports visual analysis only.']])
quality+='<p><a href="qa/live-rehearsal.json">Live engine readbacks</a> · <a href="qa/capture-manifest.json">Capture provenance</a> · <a href="qa/direct-copy-changes.json">Copy changes</a> · <a href="qa/presentation-validation-v8.json">Presentation validation</a> · <a href="qa/native-package-verification-v8.json">Native media and route check</a> · <a href="qa/web-verification.json">Web checks</a> · <a href="qa/tool-tests.txt">Project tests</a> · <a href="qa/ui-gates.txt">UI gates</a></p>'
page('quality.html','Week 7 quality checks',quality)
(OUT/'qa/package-summary.json').write_text(json.dumps({'slides':106,'visible':88,'hidden':18,'custom_show':len(live),'capture_slides':capture_slides,'capture_assets':len(manifest),'source_sha256':hashlib.sha256((OUT/'build/source-v7.pptx').read_bytes()).hexdigest(),'native_table_slides':[s['number'] for s in slides if s['tables']]},indent=2),encoding='utf-8')
print('Built current pack, actual slide review, eight-step walkthrough and document readers.')


