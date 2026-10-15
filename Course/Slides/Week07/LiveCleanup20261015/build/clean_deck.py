from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import json,posixpath,copy
R=Path('Course/Slides/Week07/LiveCleanup20261015'); inv=json.loads((R/'build/inventory.json').read_text())
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with ZipFile(R/'build/source-v6.pptx') as z:d={n:z.read(n) for n in z.namelist()}
original_data=dict(d)
master=E.fromstring(d['ppt/slideMasters/slideMaster1.xml'])
master_footer=next(sp for sp in master.findall('.//p:sp',NS) if sp.find('.//p:ph[@type="ftr"]',NS) is not None)
footer_style=master_footer.find('p:txBody/a:lstStyle',NS)
def inherited_footer_transform(part,idx):
 relpart=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
 if relpart in original_data:
  rels=E.fromstring(original_data[relpart])
  for rel in rels:
   if not rel.get('Type','').endswith('/slideLayout'):continue
   layout=posixpath.normpath(posixpath.join(posixpath.dirname(part),rel.get('Target')))
   lx=E.fromstring(original_data[layout])
   for sp in lx.findall('.//p:sp',NS):
    ph=sp.find('.//p:ph',NS)
    if ph is not None and ph.get('type')=='ftr' and ph.get('idx')==idx:
     transform=sp.find('p:spPr/a:xfrm',NS)
     if transform is not None:return transform
 return master_footer.find('p:spPr/a:xfrm',NS)
hide={5:'Host check repeats UE01.',7:'Autocomplete setup is reference material.',8:'Workspace settings are reference material.',16:'Script execution instructions repeat the quick start.',18:'Selection capture repeats the preceding expected-output example.',21:'Component capture repeats Actor/component/asset explanation.',25:'Asset selection result repeats UE04.',30:'Readback summary repeats the texture table and capture.',41:'Extra script-editor case study.',44:'Remote Control is beyond the current tool route.',45:'Additional pipeline platform case study.',49:'Selection reference duplicates the Blender example.',58:'Second Titan tool adds less than the ivy and environment cases.',69:'Workflow outline duplicates the user story and acceptance checks.',70:'Mental-model explanation repeats the same material story.',85:'Task-state summary duplicates the state/action table.',95:'Second GOLF+ case repeats naming consistency.',100:'Telemetry depth is optional for this observation lab.'}
repl={
13:{'Pass the subsystem class; call selection methods on the returned editor instance.':'Get the subsystem, then ask it for the selection.'},
14:{'editor is the returned subsystem. actor is one Actor from the selection.':'editor: subsystem instance. actor: one selected Actor.'},
17:{'Outliner: select only W07_Crate_Target.':'Select W07_Crate_Target.','Run the complete UE02 example.':'Run UE02.','The label matches the Outliner. The class identifies the Actor type.':'Label: Outliner identity. Class: Actor type.'},
33:{'A useful result identifies the asset, the rule and a correction.':'Name the asset, rule and correction.','Choose warning or failure to match the project policy.':'Severity follows project policy.'},
36:{'Returned objects and source files':'Objects + source files','Mesh slot, parent and exact texture roles':'Slot + parent + texture roles','Instance parent and parameter values':'Parent + parameters','Intended target changes; protected scope stays unchanged':'Target changes; protected scope stays'},
38:{'Numeric position used for assignment':'Assignment index','Semantic label such as Body':'Semantic label, e.g. Body','Assigned material or instance object':'Material or instance object','Shared mesh default or one component override':'Mesh default or component override'},
43:{'Package the logic and the entry point separately.':'Package logic + a clear entry point.'},
55:{'Inspect the proposed assignment, then check the target in the scene.':'Review the assignment. Inspect the scene.'},
56:{'Count the proposed targets. Then inspect where the effects appear.':'Preview three markers. Check three fountains.'},
67:{'Environment artist trying a look on one prop':'Environment artist comparing one prop','Preview and assign a prepared texture set':'Preview and assign prepared textures','Compare the look while other placements stay unchanged':'Compare looks without changing other placements'},
68:{'Target, slot and mappings are visible; scene unchanged':'Targets visible; scene unchanged','Apply requires a fresh preview':'Fresh preview required','A valid reviewed plan':'Valid reviewed plan'},
72:{'Assessment question: which controls belong to the same step?':'Which controls belong together?','Spacing should separate unrelated steps.':'Separate unrelated steps.','Labels should describe the artist’s task.':'Label the artist’s task.','Scope and primary action should remain easy to find.':'Expose scope and the next action.'},
74:{'In a scene: guide the eye toward the focal point.':'Scene: guide the eye.','In a tool: guide attention through the task.':'Tool: guide the task.','Use spacing, alignment and contrast to clarify scope, preview and the primary action.':'Use spacing, alignment and contrast.'},
75:{'Value and contrast are different ideas':'Value, contrast, hierarchy','HSV Value is a color coordinate. It is not perceived lightness or a contrast ratio.':'HSV Value ≠ perceived lightness ≠ contrast ratio.','Meaning in art and tool design':'Meaning','The lightness or darkness of a visual area':'Lightness or darkness','A difference between neighboring elements':'Difference between elements','The priority suggested by size, value, spacing and emphasis':'Priority from size, value and spacing','Would different hues remain distinct if their light and dark values were similar?':'Do different hues still separate in grayscale?'},
76:{'Ignore labels; reduce regions to simple masses':'Reduce the layout to masses','Are related decisions grouped?':'Are related controls grouped?','Temporarily remove hue':'Remove hue','Which large shapes and values dominate?':'What dominates?','Now restore the original. Can you read the labels and use the controls?':'Restore the original. Check labels and controls.'},
77:{'Notice: numbered stages reveal the intended sequence.':'Numbered stages show sequence.','Generate receives strong visual emphasis.':'Generate has emphasis.','Edit is explicitly optional.':'Edit is optional.','Apply: make the next step and its prerequisites easy to find.':'Make the next step easy to find.','What does the warning beside Input mean? Can this image tell us?':'What does the Input warning mean?'},
78:{'Art: palette and contrast establish emphasis.':'Art: color creates emphasis.','Tools: color supports an explicit state label.':'Tools: color supports state labels.','Do not make color the only cue. State the problem and the next action in text.':'Pair color with the problem and next action.'},
79:{'Choose color roles before choosing colors':'Choose color roles first','Give primary actions, warnings and supporting surfaces distinct roles.':'Separate actions, warnings and surfaces.','Pair status color with a label, icon or shape.':'Pair color with a label or icon.','Explore palettes with Coolors; check actual foreground/background pairs.':'Explore with Coolors. Check actual color pairs.','Text benchmark: 4.5:1 ordinary text, 3:1 large text under WCAG definitions.':'WCAG text: 4.5:1 normal; 3:1 large.','Does this palette explain “selected,” “available,” and “complete” separately?':'Can you distinguish selected, available and complete?'},
81:{'Useful next action':'Next action','What the UI communicates':'Meaning','Inputs can be checked without mutation':'No changes yet','Valid reviewed plan':'Reviewed plan','Names the operation and affected count':'Operation + affected count','Explains the concern; limits still apply':'Concern + limits','No repeated Apply from the consumed plan':'Preview consumed','If an input changes, what should happen to the old preview?':'Inputs changed. Is this preview still valid?'},
82:{'Why must the backend validate again if Apply is already enabled?':'Why recheck when Apply is enabled?'},
83:{'The same workflow can use different UIs':'One workflow, different interfaces','Useful implementation distinction':'Implementation','Layouts and signals in a Python window':'Python window: layouts + signals','Editor tab using the host UI framework':'Dockable editor tab','Blueprint-based editor interface; a separate option':'Blueprint editor interface','Inputs → reviewed plan → guarded apply → result':'Inputs → preview → apply → result','Which parts should stay consistent when the host interface changes?':'What should stay consistent across interfaces?'},
84:{'Show exact identity and target slot.':'Show the target and slot.','Separate the proposed result from a completed result.':'After completion, label it Result.','Which row would you inspect to confirm the affected component?':'Which component will change?'},
93:{'Shared rules reduce drift across people, tools and releases.':'Shared rules reduce design drift.','Example from the course tool':'Example','Title, field label, help text; consistent group gaps':'Type scale + group spacing','Primary action, focus, warning, unavailable state':'Action, focus, warning, disabled','Preview before Apply; name the affected operation':'Preview → Apply → Result','Starting, blocked, completed and narrow-window views':'Start, blocked, complete, narrow','What would a color palette alone leave unspecified?':'What does a palette leave unspecified?'},
94:{'Keep design rules in a versioned style-sheet skill.':'Version the style-sheet skill.','Have design agents reference it before changing the UI.':'Require agents to read it first.','Review screenshots and behavior against the same rules.':'Review visuals and behavior against it.','Record an intentional exception; update the sheet when the rule changes.':'Record exceptions. Update changed rules.','What evidence would you request before accepting “the design is consistent”?':'What evidence would prove consistency?'},
97:{'Prototype the question you need to answer':'Prototype your uncertainty','Can a peer find the next action?':'Is the next action clear?','Real data and engine behavior':'Data + engine behavior','Do controls and states make sense?':'Are states understandable?','Live assets and host integration':'Live host integration','Does this operation respect scope?':'Is scope respected?','Other projects and target performance':'Other projects + frame cost','Which is the cheapest prototype that answers your current uncertainty?':'What is the cheapest useful test?'},
99:{'A useful finding separates evidence from explanation':'Separate observation from explanation','The tester paused at the destination field and asked for help.':'Tester paused at Destination and asked for help.','The label may not identify which folder will change.':'The affected folder may be unclear.','Name the destination and affected assets beside Preview.':'Name the folder and affected assets.','Same task and inputs; can a new tester identify scope without help?':'Same task, new tester: identify scope unaided.','What did you observe, and what are you still inferring?':'What is observed? What is inferred?'},
103:{'Environment artist comparing one surface':'Artist comparing one surface','Prepared textures + target crate; protected crate stays':'Textures + target; protected crate unchanged','Expected look, correct slot and unchanged comparison object':'Expected look + correct slot + protected scope','Restore prepared state; use a labeled walkthrough if blocked':'Reset; labeled walkthrough if blocked'},
105:{'Choose a strength and one revision or uncertainty':'Choose one strength + one revision','If execution is blocked, label the mode and continue with the prepared fallback.':'Blocked? Label the fallback mode and continue.'}
}
changes=[]; removed=[]
for n,b in list(d.items()):
 if n.endswith('.xml') and n.startswith(('ppt/slides/','ppt/slideLayouts/','ppt/slideMasters/','ppt/notesSlides/')):
  x=E.fromstring(b); dirty=False
  for sp in x.findall('.//p:sp',NS):
   ph=sp.find('.//p:ph',NS);ts=sp.findall('.//a:t',NS);value=''.join(t.text or '' for t in ts)
   if ph is not None and ph.get('type')=='ftr' and (not value.strip() or value.strip().upper() in ('FOOTER','CLICK TO EDIT MASTER FOOTER STYLE','SAMPLE FOOTER TEXT')):
    sp.getparent().remove(sp);removed.append(n);dirty=True
   elif ph is not None and ph.get('type')=='ftr':
    # Preserve the real section label's inherited 7 pt styling before deleting
    # the sample footer definitions from layouts and the master.
    body=sp.find('p:txBody',NS);style=body.find('a:lstStyle',NS)
    if style is not None and not len(style):
     body.replace(style,copy.deepcopy(footer_style));dirty=True
    props=sp.find('p:spPr',NS)
    if props.find('a:xfrm',NS) is None:
     props.insert(0,copy.deepcopy(inherited_footer_transform(n,ph.get('idx'))));dirty=True
  for t in x.findall('.//a:t',NS):
   if t.text and '—' in t.text:t.text=t.text.replace(' — ',': ').replace('—','; ');dirty=True
   if t.text:
    replacements={
     'What does a successful return value establish; and what does it leave untested?':'What does a successful return value establish? What remains untested?',
     'Apply: define the handoff; input, result and next step; for your tool.':'Define your tool’s handoff: input, result and next step.',
     'Which version would a new teammate; or an agent; treat as the source of truth?':'Which version would a new teammate or agent trust?',
     'What changed; or strengthened; your original judgment?':'What changed or strengthened your original judgment?',
     'Instructor captures from Karol�s Unreal Python course � lesson 36 � log crops; code: classroom example':'Instructor captures from Karol’s Unreal Python course · lesson 36 · log crops; code: classroom example'
    }
    if t.text in replacements:t.text=replacements[t.text];dirty=True
  if dirty:d[n]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
for item in inv:
 num=item['number'];x=E.fromstring(d[item['part']]);old=' '.join(x.xpath('.//a:t/text()',namespaces=NS))
 if num in hide:x.set('show','0')
 for t in x.findall('.//a:t',NS):
  if t.text in repl.get(num,{}):t.text=repl[num][t.text]
 new=' '.join(x.xpath('.//a:t/text()',namespaces=NS))
 if old!=new:changes.append({'slide':num,'before':old,'after':new,'before_words':len(old.split()),'after_words':len(new.split())})
 d[item['part']]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
# Remove hidden slides from the native custom show, retain all slide parts and embedded media.
x=E.fromstring(d['ppt/presentation.xml']);ids=x.findall('p:sldIdLst/p:sldId',NS);hidden_ids={ids[n-1].get('{'+NS['r']+'}id') for n in hide}
for sl in x.findall('.//p:custShow/p:sldLst/p:sld',NS):
 if sl.get('{'+NS['r']+'}id') in hidden_ids:sl.getparent().remove(sl)
for show in x.findall('.//p:custShow',NS):show.set('name','Week 7 live route')
d['ppt/presentation.xml']=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(R/'build/text-cleaned.pptx','w',ZIP_DEFLATED) as z:
 for n,b in d.items():z.writestr(n,b)
(R/'qa/content-changes.json').write_text(json.dumps({'hidden':hide,'footer_placeholders_removed':removed,'edits':changes},indent=2),encoding='utf-8')
print(json.dumps({'hidden':len(hide),'edited':len(changes),'footer_placeholders_removed':len(removed),'words_before':sum(x['before_words'] for x in changes),'words_after':sum(x['after_words'] for x in changes),'custom_show':len(x.findall('.//p:custShow/p:sldLst/p:sld',NS))}))
