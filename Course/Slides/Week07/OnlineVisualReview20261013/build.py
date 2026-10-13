"""Build a source-audited imagery review without modifying the PowerPoint."""
from pathlib import Path
import json, shutil, hashlib, html, zipfile, xml.etree.ElementTree as ET
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
VIS=ROOT/'Course/Visuals'
LIB=VIS/'Week07/Online20261013'
TMP=ROOT/'tmp/week07-online-visuals'
DECKDIR=HERE.parent/'FinalClass20261013'
DECK=DECKDIR/'output/Week_7_Final_Class_v2.pptx'
LIB.mkdir(parents=True,exist_ok=True)
H=lambda s:html.escape(str(s),quote=True)
records=json.loads((TMP/'candidates.json').read_text())
lookup={r['id']:r for r in records}
slide_data=json.loads((DECKDIR/'slide_sources.json').read_text(encoding='utf-8-sig'))
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
slides=[]
with zipfile.ZipFile(DECK) as z:
    for n in range(1,72):
        e=ET.fromstring(z.read(f'ppt/slides/slide{n}.xml'))
        s={'id':'01','title':'Review & specialization'} if n==1 else slide_data['slides'][n-2]
        slides.append(dict(number=n,anchor=s['id'],title=s['title'],hidden=e.get('show')=='0',text=[t.text or '' for t in e.findall('.//a:t',ns)]))

policies={
 'nng':dict(url='https://www.nngroup.com/contents/terms-and-conditions/',label='NN/g Articles and Videos: educational illustration use with company, author and source link; preserve logos and watermarks. Current dated terms checked 2026-10-13. This is not an open-content license. An older reprint page is more restrictive; this review records the September 2026 terms explicitly.'),
 'microsoft':dict(url='https://www.microsoft.com/en-us/legal/intellectualproperty/copyright/permissions',label='Microsoft screenshot guidance permits specified uses subject to its conditions. Keep the complete screenshot, resize only, and include “Used with permission from Microsoft.” No cropped or redrawn version is supplied here.'),
 'epic':dict(url='https://legal.epicgames.com/epicgames/tos?lang=en-US',label='Epic-published documentation media; no standalone open redistribution license confirmed. Original files are staged for attributed instructional commentary and review, not relicensed as course artwork. Retain the publisher link; do not treat public access or the Fan Content Policy as blanket clearance for every publication.'),
 'w3c':dict(url='https://www.w3.org/WAI/about/using-wai-material/',label='WAI allows attributed use under its stated conditions. Preserve the unmodified figure, title, source URL, copyright and Draft status. This is a web accessibility illustration, not proof of desktop-tool conformance.'),
}
selected={
 'epic-actors-3':('shared-mesh-materials.png','Epic Games · Static Mesh Actors · three Actors using one mesh with different materials','epic',[10]),
 'epic-actors-4':('material-override.gif','Epic Games · Static Mesh Actors · changing one Actor material','epic',[15]),
 'powerrename-1':('powerrename-preview.png','Microsoft PowerToys PowerRename · Microsoft Learn · Used with permission from Microsoft.','microsoft',[34,52]),
 'errors-13':('vistaprint-warning.jpg','Tim Neusesser and Evan Sunwall · Nielsen Norman Group · Error-Message Guidelines · Vistaprint example','nng',[28]),
 'errors-14':('zazzle-print-area.jpg','Tim Neusesser and Evan Sunwall · Nielsen Norman Group · Error-Message Guidelines · Zazzle example','nng',[28]),
 'errors-11':('attachment-warning.jpg','Tim Neusesser and Evan Sunwall · Nielsen Norman Group · Error-Message Guidelines · attachment warning example','nng',[38]),
 'paper-5':('paper-dropdown.jpg','Kelley Gordon · Nielsen Norman Group · Paper Prototyping: A Cutout Kit · dropdown simulation','nng',[31]),
 'w3c-focus-0':('visible-keyboard-focus.png','W3C WAI · Visible Keyboard Focus – Easy Checks (Draft) · Kevin White, editor · 19 March 2024 · Copyright W3C','w3c',[39]),
}
assets=[]
for key,(filename,credit,policy,nums) in selected.items():
    r=lookup[key];dest=LIB/filename;shutil.copy2(ROOT/r['file'],dest)
    im=Image.open(dest)
    a=dict(id=key,file=filename,source_url=r['url'],source_page=r['page'],credit=credit,rights=policies[policy],dimensions=r['size'],frames=r['frames'],sha256=r['sha256'],method='Unmodified downloaded publisher image; full pixel contents preserved',crop=None,slides=nums,transparent=False,downloaded='2026-10-13')
    if r['frames']>1:
        a['duration_seconds']=next(x['duration_seconds'] for x in json.loads((TMP/'motion.json').read_text()) if x['id']==key)
        poster=LIB/(Path(filename).stem+'-poster.png');im.seek(0);im.convert('RGBA').save(poster);a['poster']=poster.name;a['poster_method']='Decoded full first frame, no crop or annotations'
    assets.append(a)
gen=Path(r'C:/Users/antho/.codex/generated_images/01a133fd-2261-7193-8c22-0032d9f5c61f/exec-cf76998b-769c-4e27-bf37-151efbf71550.png')
shutil.copy2(gen,LIB/'artist-inspecting-prop.png')
prompt=json.loads((HERE/'generation.json').read_text())
assets.append(dict(id='artist-inspecting-prop',file='artist-inspecting-prop.png',source_page=None,source_url=None,credit='Generated course illustration · ImageGen · 13 October 2026',rights={'url':None,'label':'Generated illustration; not photographed evidence or a software capture. Reference badges retain their separate existing provenance.'},dimensions=[1536,1024],frames=1,sha256=hashlib.sha256(gen.read_bytes()).hexdigest(),method='ImageGen, one call; output preserved without retouching',raster_only=True,editable_master=None,transparent=True,slides=[30],generation=prompt))
byid={a['id']:a for a in assets}
for name in ['white','paper','navy']:
    shutil.copy2(TMP/f'generated-{name}.jpg',LIB/f'artist-preview-{name}.jpg')

proposals=[
dict(n=10,kind='Add',priority='Strong',assets=['epic-actors-3'],heading='One mesh, visibly different Actors',
 why='The source explicitly identifies the three cubes as Actors using the same mesh with different materials. This makes the relationship concrete before the abstract reference arrows.',
 edit='Keep the title and question. Show the full three-cube image first, then reveal the existing shared-asset diagram. Keep the material override distinct from modifying the shared mesh; do not imply the existing two-node schematic describes the exact three pictured Actors.',
 layout='Wide image across roughly 70% of the content area; a click reveal switches to the existing diagram. Preserve original proportions. Use an external caption: “Same mesh; per-Actor materials.”',
 script='These three Actors use the same mesh. What differs in their appearance? Now trace the references in our diagram. Before changing a material, identify whether you are editing the shared asset or an override on a particular component.',
 limit='An official documentation example, separate from the course fixture. The current page is labeled UE 5.8; no claim that its pictured UI is the classroom build. The static image is sufficient for this conceptual comparison.'),
dict(n=15,kind='Companion',priority='Strong',assets=['epic-actors-4'],heading='What a component-level material change looks like',
 why='The short source animation changes the right cube’s material while the other cubes remain visually stable. It is closely related to the current Material Setup task.',
 edit='Keep the practice-tool screenshot, code behavior, PRACTICE MODE label and timing. Add a named “See a material override” link to the companion media. Use it only if students need to see the visual target of the practice operation.',
 layout='9.16-second original GIF, shown large in the companion review. Keep the full editor frame; play once, then return to the actual practice plan. No new slide or extra lecture block.',
 script='This separate Unreal example shows a material override on one Actor. Our practice panel proposes a related kind of assignment, but it does not perform this engine operation. Which object should change, and what must remain unchanged?',
 limit='Do not present the clip as execution of the course Python tool, a newly created material instance, or proof of Undo. It depicts a manual assignment in a separate scene.'),
dict(n=28,kind='Replace concept',priority='Strong',assets=['errors-13','errors-14'],heading='A design tool can let the intended result go wrong',
 why='NN/g’s published print-design examples contrast a warning about content outside the printable area with an interface that leaves the consequence unclear. This is a real visual-authoring task rather than a machine metaphor.',
 edit='Keep the title and UI/UX definitions. Show the two full screenshots on a reveal; keep the existing assessment question and connect it back to the renamer. Replace the earlier proposed crate-delivery illustration with this sourced comparison.',
 layout='Two equal-size images, labeled Vistaprint and Zazzle in editable slide text. Identify them as separate products, not a matched before/after. Use a large image reveal if text is too small alongside the definitions.',
 script='The text extends past the printable area. Which view helps you predict the consequence? Now return to the renamer: what result did the artist intend, and what evidence would establish it?',
 limit='Historical examples published in 2023, not an assessment of the products today. The pictures show interface feedback, not a purchased physical output. Preserve that distinction.'),
dict(n=30,kind='Generated',priority='Strong',assets=['artist-inspecting-prop'],heading='An artist judging the prop in context',
 why='No inspected online visual closely matched the slide’s specific user story. Reimport settings, generic developer photos and older Datasmith demonstrations change the focus. One bespoke illustration fills the conceptual gap.',
 edit='Keep the title, all three story lines and the question. Put the illustration in the right 45%; reflow the story on the left without reducing its type below the current readable size. If it crowds, use a reveal.',
 layout='Transparent 1536×1024 PNG with navy/teal continuity. Keep the complete artist and lantern scene. Use on white or the deck’s pale lavender; the navy-background preview shows weaker outline separation.',
 script='The artist wants to judge the revised prop in its surroundings. Bringing it into the engine serves that goal. What should update, and what surrounding work should remain stable?',
 limit='Generated concept art, not a before/after or evidence of reimport preservation. Raster only: no editable SVG master. Genuine alpha verified; original output has a maximum alpha of 254, which is retained.'),
dict(n=31,kind='Add',priority='Strong',assets=['paper-5'],heading='A prototype someone can actually operate',
 why='A photographed paper dropdown demonstrates how a sketch can simulate a choice. It is more informative than a polished illustration of people brainstorming.',
 edit='Keep this slide optional, its title and bullets. Replace the tiny sketch thumbnail with the full paper-dropdown photograph. Preserve the course’s two alternative layouts on live slide 32.',
 layout='Large 4:3 photo beside three short bullets. Do not crop away the hands or paper pieces: they explain the interaction. Keep the credit outside the image.',
 script='The paper pieces let a person make a choice. What could you learn from their attempt before implementing this control? What would still require a working tool?',
 limit='A browser-form prototype, not an Unreal interface. It can support discussion of interaction and labels, not execution correctness. No need to reproduce or distribute the downloadable template kit.'),
dict(n=34,kind='Alternative',priority='Strong',assets=['powerrename-1'],heading='Selection, preview and visible scope in a real rename tool',
 why='The complete PowerRename window presents selection, original names, proposed names and Apply together. The task matches the renaming assessment more closely than generic UX stock imagery.',
 edit='Keep slide 34 optional. Offer this as an alternative to its production-menu example, not a second crowded image. Retain the distinction between filtering visible rows and changing the plan. The same source is a reference option for slide 52, but use it on only one slide.',
 layout='Full screenshot with its proportions unchanged; resize only under Microsoft’s screenshot terms. Point verbally to selection and the Original/Renamed columns. Do not crop or annotate its pixels.',
 script='Before Apply, which names will change? Which controls help you inspect that? Compare what you can see here with what you needed to know in the paper renamer case.',
 limit='Microsoft PowerToys PowerRename, a Windows file tool. Its preview is not evidence of backend stale-plan protection. It is also not an Unreal Actor renamer.'),
dict(n=38,kind='Companion',priority='Useful',assets=['errors-11'],heading='A warning before an avoidable mistake',
 why='The missing-attachment warning offers a familiar example of noticing a likely problem before completing an action. It gives the class a quick comparison for actionable messages.',
 edit='Keep the course tool’s actual error screenshot as the main evidence. Add this as an optional reveal or companion link only if students need another example. Keep the existing recovery question.',
 layout='Full screenshot, large enough that the warning can be read; no decorative warning icons. If a small layout makes it illegible, leave it in the companion page.',
 script='What problem does this warning identify, and what can the person do next? Now read our tool’s message using those same questions.',
 limit='A separate email-product example published by NN/g, not a claim about the course tool. Preventing an error and recovering after a partial edit are different teaching cases.'),
dict(n=39,kind='Add',priority='Strong',assets=['w3c-focus-0'],heading='Show what visible focus actually means',
 why='The WAI figure gives “visible focus” an inspectable appearance. It fills a visual gap on a slide currently dominated by text and a short code excerpt.',
 edit='Keep the title, recovery qualifications and accessibility guidance. Add the intact WAI image alongside the focus sentence; keep its Draft status in the attribution. Preserve slide 56’s Qt-specific code as optional depth.',
 layout='Small supporting image at approximately its native 500-pixel width. Do not generatively upscale or remove the source’s annotation. Use an actual keyboard attempt in the course tool for behavior.',
 script='The outline identifies the active control. Can you tell where focus is in your own tool as you press Tab? A name in code is not enough to show that the experience works.',
 limit='A web example from a draft WAI teaching page. It demonstrates the idea; it does not certify desktop accessibility or show the course tool’s focus order.'),
dict(n=46,kind='Reuse',priority='Strong',assets=[],heading='Recover the existing facilitator–task–participant diagram',
 why='Online checking led back to the NN/g role diagram already stored in the course. Final Class v2 removed it from this slide; it still matches the briefing directly.',
 edit='Keep the current three bullets and question. Reintroduce the existing diagram only if it remains legible at the available size; the roles in the course stay Author and Reviewer. Preserve the distinct follow-up photo on slide 45.',
 layout='Existing role diagram on the right; current lab-specific wording on the left. No new generated classroom scene. If the figure is crowded, retain the current plain briefing.',
 script='The author gives the goal and observes. The reviewer attempts it and records what happened. If help is needed, record that help. Which role or instruction needs clarification before we begin?',
 limit='The diagram is a general model. Our reciprocal classroom exercise and three reviewers are not a validated population-wide usability study.'),
dict(n=49,kind='Reuse',priority='Useful',assets=[],heading='Use the established Week 1 lenses only if they aid synthesis',
 why='The four existing badges offer stronger course continuity than another illustration. Their value is retrieval of familiar questions.',
 edit='Keep the current revision instructions and retest requirement. Optionally add a small, clearly labeled strip of original badges. Do not introduce a new rubric or add another discussion block.',
 layout='Original Constraints, Systems, Leverage and Throughput badges, unchanged. Labels remain editable. Prefer the current clean slide if the badges distract from writing the revision.',
 script='Which lens helps you explain your proposed revision? Choose one observed issue and state what you expect to see when you retest.',
 limit='Reuse, not a new online find. Artistic intent remains the goal examined through the lenses, not an added fifth lens.')
]

rejections=[
('Ryan DowlingSoka batch-renamer article','https://ryandowlingsoka.com/unreal/batch-rename-tool/','Strong topic, weak new stills: the four inspected images are small parameters/Blueprint details, not a clear whole-tool preview. Already listed in the course references. Keep the tutorial link; do not inflate the screenshots.'),
('Epic Interchange preview and conflicts','https://dev.epicgames.com/documentation/en-us/unreal-engine/importing-assets-using-interchange-in-unreal-engine','Promising for slides 14 and 51, but three image downloads returned HTTP 403. Page descriptions were read; pixels were not inspected. Not counted as ready assets. Do not substitute a different importer UI or assert version compatibility.'),
('Epic automatic reimport','https://dev.epicgames.com/documentation/en-us/unreal-engine/reimporting-assets-automatically-in-unreal-engine','Settings screenshot and workflow explanation are useful references, but not a strong visual of an artist inspecting the revised prop.'),
('Unreal Studio Reimport feature video','https://www.youtube.com/watch?v=F4Ft5wEKdrc','Official 2018 Datasmith/Unreal Studio demonstration. Discovery and description checked, footage not inspected. Different workflow; not adopted as evidence for the current Python/import lesson.'),
('Qt Designer tab-order screenshot','https://doc.qt.io/qt-6.8/designer-tab-order.html','Directly relevant to slide 56, but only 321×227 and visibly old styling. Keep as a linked optional reference. Do not upscale it into a main slide visual or confuse numbered design-time order with runtime focus.'),
('Qt layout and signals documentation','https://doc.qt.io/qt-6/layout.html','The inspected QFormLayout image is only 262×110. The generic signals diagram adds less than the current course-specific callback schematic. Qt documentation uses GFDL 1.3; software licensing is not the artwork license.'),
('NN/g paper cutout alternatives','https://www.nngroup.com/articles/paper-prototyping-cutout-kit/','Five photos inspected. Prefer the desktop dropdown for this artist-tool course. Phone cutouts, loading panels and overlays are less closely tied to the present teaching point.'),
('NN/g error-image alternatives','https://www.nngroup.com/articles/error-message-guidelines/','Five figures inspected. The print-area pair and attachment warning survive the relevance screen. Amazon checkout and password criteria add a larger domain detour.'),
('PowerRename motion','https://learn.microsoft.com/en-us/windows/powertoys/powerrename','Two GIFs inspected through eight time samples each: 34.26-second rename sequence and 10.36-second filter sequence. The full still is easier to teach within the current budget. Motion remains linked from the publisher, not bundled as another live activity.'),
('Epic Actor placement GIF','https://dev.epicgames.com/documentation/en-us/unreal-engine/static-mesh-actors-in-unreal-engine','7.60-second drag-and-drop example inspected. Clear but less valuable than the material-override animation. It does not demonstrate reimport.'),
('NN/g testing photograph','https://www.nngroup.com/articles/usability-testing-101/','The inspected 1400×933 photograph is already on slide 45 and depicts follow-up after a task. Do not reuse it as new evidence of silent observation during an attempt.'),
('Guerrilla Horizon tools','https://www.guerrilla-games.com/read/creating-a-tools-pipeline-for-horizon-zero-dawn','Strong existing source, already represented by production screenshots and a 16-second contextual-feedback clip. Keep those assets; do not count the source again as a new visual discovery.'),
('Isaac Oster import/export','https://isaacoster.artstation.com/projects/Dvdrke','Topic and author page confirmed through web reading; direct page retrieval returned HTTP 403. No newly inspected high-resolution still, so keep as study reference rather than pretending a clip was reviewed.'),
('Generic UI/UX bottle, iceberg, maze and robot metaphors','https://www.nngroup.com/articles/definition-user-experience/','Rejected for this deck. They weaken the connection to actual tool scope, art decisions, and observed results. The newly found print-design example is more precise.')
]

for p in proposals:
    s=slides[p['n']-1];p.update(anchor=s['anchor'],title=s['title'],hidden=s['hidden'])
qlog=[
'site.ryandowlingsoka.com unreal batch rename tool preview','site.nngroup.com usability testing facilitator participant task photo','site.dev.epicgames.com Unreal Engine reimport assets auto reimport','site.nngroup.com user experience user interface ketchup bottle',
'site.nngroup.com paper prototyping photos examples','site.nngroup.com error messages guidelines examples','site.nngroup.com recognition recall user interface examples','site.nngroup.com copyright classroom images slides permission',
'site.nngroup.com Copyright permission slides','site.blender.org interface undo history','site.doc.qt.io qt widgets gallery screenshots','site.microsoft.com powertoys powerrename preview screenshots',
'Nielsen Norman Group content licensing reproduce images presentations educational permission','game artist tools UX error recovery preview GDC pipeline screenshots','paper prototyping kit photos','Unreal Engine Interchange preview reimport pipeline screenshot',
'site.microsoft.com legal intellectualproperty permissions screenshots','site.doc.qt.io documentation GNU Free Documentation','site.epicgames.com Fan Content Policy non-commercial','site.ryandowlingsoka.com license',
'site.doc.qt.io designer tab order screenshot','site.dev.epicgames.com Execute Python Script Image','site.dev.epicgames.com Static Mesh Actors Image','site.w3.org WAI focus visible example screenshot',
'site.guerrilla-games.com tools Horizon','site.gdcvault.com artist tools user interface','site.isaacoster.com unreal python material setup','site.artstation.com Isaac Oster Import Export']
audit=dict(date='2026-10-13',source_deck=str(DECK),source_sha256=hashlib.sha256(DECK.read_bytes()).hexdigest(),queries=qlog,media_candidates=records,motion_checks=json.loads((TMP/'motion.json').read_text()),proposals=proposals,rejections=[dict(title=t,url=u,reason=r) for t,u,r in rejections],generation_calls=1,slides=slides)
(HERE/'audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf8')
(LIB/'manifest.json').write_text(json.dumps({'date':'2026-10-13','assets':assets,'review':'../../../Slides/Week07/OnlineVisualReview20261013/index.html'},indent=2,ensure_ascii=False),encoding='utf8')

prefix='../../../Visuals/Week07/Online20261013/'
def asset_html(a,base=prefix):
    file=base+a['file'];poster=base+a.get('poster',a['file'])
    media=f'<img loading="lazy" src="{poster}" alt="{H(a["credit"])}">'
    if a['frames']>1:media+=f'<button type="button" class="play" data-src="{file}" data-poster="{poster}">Play / pause animation</button>'
    source=f'<a href="{H(a["source_page"])}">Publisher context</a> · <a href="{H(a["source_url"])}">Publisher image</a>' if a['source_page'] else '<span>Generated illustration · raster only</span>'
    return f'<figure>{media}<figcaption>{H(a["credit"])}<br><a href="{file}" download>Download original</a> · {source}<br><small>{a["dimensions"][0]} × {a["dimensions"][1]} · '+('true alpha PNG' if a['transparent'] else 'original opaque image')+f'</small><details><summary>Provenance and use terms</summary><p>{H(a["rights"]["label"])}</p>'+ (f'<a href="{H(a["rights"]["url"])}">Publisher terms checked</a>' if a['rights']['url'] else '')+'</details></figcaption></figure>'

css='''*{box-sizing:border-box}body{font:17px/1.6 Arial,sans-serif;background:#f5f4f8;color:#201c2a;margin:0}main{max-width:1480px;margin:auto;padding:30px}header,article,section.block{background:white;padding:28px;margin:0 0 26px;border-bottom:2px solid #ddd5ea}h1{font-size:38px;line-height:1.15}h2{font-size:27px;line-height:1.25}h3{font-size:20px}a{color:#584396}nav{display:flex;gap:20px;flex-wrap:wrap}.compare{display:grid;grid-template-columns:1fr 1fr;gap:28px}.slide,img{max-width:100%;height:auto}figure{margin:0 0 18px}figure>img{display:block;max-height:520px;object-fit:contain;margin:auto}figcaption,small,.meta{font-size:14px;color:#635c70}figcaption{margin-top:10px;overflow-wrap:anywhere}.job{font-weight:bold;color:#0a4054}.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}.pair figure>img{max-height:300px}input,select,button{font:inherit;padding:8px}button{cursor:pointer}label{display:inline-block;margin:8px 15px 8px 0}details{margin:14px 0}summary{cursor:pointer;color:#584396}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #ddd;padding:10px}th{background:#eee9f6}article[hidden],tr[hidden]{display:none}.table-wrap{overflow:auto}.notes{border-left:4px solid #029990;padding-left:18px}.badge-strip{display:flex;gap:12px}.badge-strip img{width:90px}.light{background:#fff}.paper{background:#f0ebfa}.navy{background:#0a4054}@media(max-width:900px){.compare,.pair{grid-template-columns:1fr}main{padding:12px}header,article,section.block{padding:18px}}@media print{.filters,button{display:none}body{background:white}article{break-inside:avoid}}'''
articles=[]
for p in proposals:
    s=slides[p['n']-1]
    media=''.join(asset_html(byid[k]) for k in p['assets'])
    if p['n']==46:
        media='<figure><a href="../TeachingDeck20261013/assets/nng-testing-flow.png"><img src="../TeachingDeck20261013/assets/nng-testing-flow.png" alt="Existing NN/g facilitator task participant diagram"></a><figcaption>Kate Moran · Nielsen Norman Group · <a href="https://www.nngroup.com/articles/usability-testing-101/">Usability Testing 101</a> · existing course asset, not a new download</figcaption></figure>'
    if p['n']==49:
        media='<div class="badge-strip">'+''.join(f'<a href="../../../Visuals/Icons/Legacy/week1-{b}.png"><img src="../../../Visuals/Icons/Legacy/week1-{b}.png" alt="{b}"></a>' for b in ['constraints','systems','leverage','throughput'])+'</div>'
    if len(p['assets'])>1:media='<div class="pair">'+media+'</div>'
    articles.append(f'''<article id="s{p['n']}" data-route="{'optional' if s['hidden'] else 'live'}" data-kind="{H(p['kind'])}"><p class="meta">{H(p['priority'])} · {H(p['kind'])} · {'Optional depth' if s['hidden'] else 'Live'} · position {p['n']} · printed anchor {s['anchor']}</p><h2>{H(s['title'])}</h2><div class="compare"><div><h3>Current Final Class v2 slide</h3><a href="../FinalClass20261013/previews/slide-{p['n']:02}.png"><img class="slide" src="../FinalClass20261013/previews/slide-{p['n']:02}.png" alt="Current slide {p['n']}"></a><details><summary>Exact PowerPoint text</summary><ul>{''.join('<li>'+H(t)+'</li>' for t in s['text'])}</ul></details></div><div><h3>{H(p['heading'])}</h3>{media}</div></div><p class="job">{H(p['why'])}</p><h3>Field-level proposal</h3><p>{H(p['edit'])}</p><h3>Placement and reading order</h3><p>{H(p['layout'])}</p><h3>Read-aloud notes</h3><p class="notes">{H(p['script'])}</p><details><summary>Evidence boundary</summary><p>{H(p['limit'])}</p></details></article>''')

proposal_lookup={p['n']:p for p in proposals}
def disposition(s):
    n=s['number']
    if n in proposal_lookup:return proposal_lookup[n]['kind'],proposal_lookup[n]['heading']
    if n in [1,2,5,22,23,24,27]:return 'Keep','Section/agenda clarity is more useful than added decoration.'
    if n in [7,8,11,12,14,16,17,18,21,33,36,37,50,54,55,59,60]:return 'Keep evidence','Retain the real course/API content. Source links support it; generated UI would add no evidence.'
    if n in [19,20,53]:return 'Keep evidence','Existing fixture comparison; preserve its separate scene and recording limitations.'
    if n in [25,26]:return 'Keep reveal','Preserve the prediction/evidence table and reveal order; do not telegraph the error.'
    if n in [4,29,35,40,41,57,62,64,65,66,67,68]:return 'Keep production','Strong production examples already present; new web finds do not improve their relevance.'
    if n in [44,47,48]:return 'Keep instructions','Protect task writing, timing and rotations. Clear text/table is the appropriate visual.'
    if n==45:return 'Keep photo','Existing NN/g follow-up photograph; do not relabel it as an observed independent attempt.'
    if n==51:return 'Link only','Interchange conflicts source is relevant; image retrieval blocked and importer version differs. Retain the prediction table.'
    if n==52:return 'Alternative','PowerRename is a visible-preview comparison only. Keep the course diagram for stale-plan behavior; avoid repeating the image from 34.'
    if n==56:return 'Link only','Qt Designer tab-order example is directly relevant but too small for a main visual. Actual focus behavior still needs a real tool check.'
    if n==13:return 'Keep schematic','A reimport video from another pipeline would imply unsupported equivalence. Retain the precise Maya → Unreal handoff.'
    if n in [6,9,32,42,43,58]:return 'Keep teaching visual','Existing concept/table/diagram is more exact than the alternatives inspected.'
    return 'Keep','No strongly applicable replacement found that improves the current teaching job.'
rows=''.join(f'<tr data-route="{"optional" if s["hidden"] else "live"}"><td><a href="../FinalClass20261013/previews/slide-{s["number"]:02}.png">{s["number"]}</a> / {s["anchor"]}</td><td>{H(s["title"])}</td><td>{"Optional" if s["hidden"] else "Live"}</td><td>{H(disposition(s)[0])}</td><td>{H(disposition(s)[1])}</td></tr>' for s in slides)
reject_html=''.join(f'<li><a href="{H(u)}">{H(t)}</a> — {H(r)}</li>' for t,u,r in rejections)
head=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 7 · online imagery assessment</title><style>{css}</style></head><body><main><header><p class="meta">13 October 2026 · online-first visual review · Final Class v2</p><h1>Existing imagery first; one generated gap</h1><p>Most of the earlier illustration concepts can be replaced by actual software examples, published interaction photographs, or visuals already in the course. The strongest new additions are the shared-mesh cubes, a print-area warning comparison, a paper dropdown, and visible keyboard focus. One generated artist-and-prop illustration remains useful for the user-story slide.</p><p><strong>Scope:</strong> 28 targeted web searches; 27 concrete image/GIF candidates identified; 24 retrieved and visually inspected, including sampled motion from four GIFs; three Interchange images blocked. All 71 slide positions have a disposition below. This is a curated review and asset package; the PowerPoint has not been edited.</p><nav><a href="#shortlist">Shortlist</a><a href="#coverage">All 71 slides</a><a href="#rejected">Rejected / already covered</a><a href="../../../Visuals/Week07/Online20261013/index.html">Asset gallery and downloads</a><a href="audit.json" download>Audit data</a><a href="../FinalClass20261013/output/Week_7_Final_Class_v2.pptx">Reviewed deck</a><a href="../ImageryReview20261013/index.html">Earlier brainstorm</a></nav><p class="meta">The newer Final Class v2 supersedes the paced deck used in the earlier brainstorm. Twelve slide previews changed; these were re-inspected. Existing practice screenshots describe offline practice data, not live Unreal operations.</p></header>
<section class="block" id="shortlist"><h2>Recommended integration order</h2><ol><li><a href="#s10">Slide 10:</a> Epic’s shared mesh / different materials example.</li><li><a href="#s28">Slide 28:</a> a real authoring consequence in the print-area comparison.</li><li><a href="#s30">Slide 30:</a> the one generated artist-goal illustration.</li><li><a href="#s39">Slide 39:</a> an intact visible-focus example.</li><li><a href="#s31">Slide 31, optional:</a> a photographed paper interaction.</li></ol><p>The remaining proposals are companion, optional, or reuse choices. Do not insert all of them automatically. Preserve the original typography and slide theme, live route, demonstration budget, and four-minute task-writing period. Proposed image reveals occupy existing explanation time.</p><p>Media are shown with their original opaque backgrounds where appropriate. Only the generated cutout is transparent. Each preview links to its original file and provenance; publisher availability is not presented as an open license.</p></section>
<div class="filters"><label>Search <input id="q" type="search" placeholder="Slide, topic, source"></label><label>Route <select id="route"><option value="all">All</option><option value="live">Live</option><option value="optional">Optional</option></select></label></div>'''
tail=f'''<section class="block" id="coverage"><h2>Complete deck coverage</h2><p>Position / printed anchor are both preserved. Keeping a slide is an assessed choice, not an unfinished search.</p><div class="table-wrap"><table><thead><tr><th>Slide</th><th>Title</th><th>Route</th><th>Decision</th><th>Reason / action</th></tr></thead><tbody>{rows}</tbody></table></div></section><section class="block" id="rejected"><h2>Why other candidates were not selected</h2><ul>{reject_html}</ul></section><section class="block"><h2>Generation decision and verification</h2><p>The artist-and-prop illustration was generated once after the search. The other proposed generated scenes were dropped, replaced by sourced material, or judged unnecessary. The illustration’s alpha channel includes 697,730 fully transparent pixels of 1,572,864; its maximum alpha is 254. White and lavender presentation previews are clean. Dark navy reduces outline separation, so a dark-slide variant is not claimed.</p><div class="pair"><figure><img src="{prefix}artist-preview-white.jpg" alt="Generated illustration checked on white"><figcaption>White-background QA preview</figcaption></figure><figure><img src="{prefix}artist-preview-paper.jpg" alt="Generated illustration checked on lavender"><figcaption>Deck-paper QA preview</figcaption></figure></div><p><a href="generation.json">Exact prompt and reference</a> · <a href="../../../Visuals/Week07/Online20261013/verification.json">Asset verification</a>. Generated artwork is a raster illustration, not an editable diagram. No generated software interfaces or inferred before/after evidence.</p></section></main><script>const q=document.querySelector('#q'),r=document.querySelector('#route');function filter(){{document.querySelectorAll('article,tbody tr').forEach(a=>a.hidden=!(a.textContent.toLowerCase().includes(q.value.toLowerCase())&&(r.value==='all'||a.dataset.route===r.value)))}}q.oninput=filter;r.onchange=filter;document.querySelectorAll('.play').forEach(b=>b.onclick=()=>{{const im=b.previousElementSibling;const play=!b.dataset.playing;im.src=play?b.dataset.src:b.dataset.poster;b.dataset.playing=play?'yes':'';b.textContent=play?'Pause animation':'Play animation'}});window.addEventListener('hashchange',()=>{{const a=document.getElementById(location.hash.slice(1));if(a?.tagName==='ARTICLE'){{q.value='';r.value='all';filter();a.scrollIntoView()}}}});</script></body></html>'''
(HERE/'index.html').write_text(head+''.join(articles)+tail,encoding='utf8')
gallery=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 7 sourced assets and one illustration</title><style>{css}</style></head><body><main><header><h1>Week 7 · selected visual assets</h1><p>Eight publisher assets and one generated illustration. Files remain unmodified; original source, intended use and rights status are recorded individually. No PowerPoint edits.</p><nav><a href="../../../Slides/Week07/OnlineVisualReview20261013/index.html">Slide-by-slide review</a><a href="manifest.json">Provenance manifest</a><a href="../../index.html">Course gallery</a></nav></header>'+''.join('<section class="block"><h2>'+H(a['id'])+'</h2><p>Proposed slide positions: '+', '.join(map(str,a['slides']))+'</p>'+asset_html(a,base='')+'</section>' for a in assets)+'</main><script>document.querySelectorAll(".play").forEach(b=>b.onclick=()=>{const im=b.previousElementSibling;const play=!b.dataset.playing;im.src=play?b.dataset.src:b.dataset.poster;b.dataset.playing=play?"yes":"";b.textContent=play?"Pause animation":"Play animation"})</script></body></html>'
(LIB/'index.html').write_text(gallery,encoding='utf8')
manifest_path=VIS/'manifest.json';m=json.loads(manifest_path.read_text(encoding='utf8'))
entry=dict(id='week07-online-20261013',title='Week 7: sourced imagery and artist-goal illustration',html='Week07/Online20261013/index.html',manifest='Week07/Online20261013/manifest.json',count=len(assets))
m['collections']=[c for c in m.get('collections',[]) if c['id']!=entry['id']]+[entry]
manifest_path.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
main_gallery=VIS/'index.html';g=main_gallery.read_text(encoding='utf8')
import re
g=re.sub(r'<section id="week07-online-20261013">.*?</section>','',g,flags=re.S)
section='<section id="week07-online-20261013"><h2>Week 7 · online imagery assessment</h2><p><a href="Week07/Online20261013/index.html">Eight sourced images/animations and one generated artist-goal illustration</a> · <a href="../Slides/Week07/OnlineVisualReview20261013/index.html">Current slide comparisons and all-slide coverage</a></p></section>'
main_gallery.write_text(g.replace('</main>',section+'</main>'),encoding='utf8')
checks=[]
for a in assets:
    f=LIB/a['file'];raw=f.read_bytes();assert hashlib.sha256(raw).hexdigest()==a['sha256']
    with Image.open(f) as im:
        assert list(im.size)==a['dimensions'];item={'id':a['id'],'hash_verified':True,'dimensions':list(im.size)}
        if a['transparent']:
            assert im.mode=='RGBA';alpha=im.getchannel('A');hist=alpha.histogram();assert hist[0]>0
            assert all(alpha.getpixel(xy)==0 for xy in [(0,0),(im.width-1,0),(0,im.height-1),(im.width-1,im.height-1)])
            item.update(alpha_extrema=list(alpha.getextrema()),fully_transparent_pixels=hist[0],edge_clear=True)
        checks.append(item)
(LIB/'verification.json').write_text(json.dumps({'status':'passed','checks':checks,'visual_inspection':'All selected originals inspected; GIF time samples inspected; generated PNG checked on white, lavender and navy. Browser rendering checked separately.'},indent=2),encoding='utf8')
print(json.dumps({'review':str(HERE/'index.html'),'assets':len(assets),'proposals':len(proposals),'slides':len(slides),'candidate_count':len(records),'retrieved':sum('file' in r for r in records)}))
