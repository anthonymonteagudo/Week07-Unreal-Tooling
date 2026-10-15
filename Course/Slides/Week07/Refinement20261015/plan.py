"""Editorial source for the gradient-preserving Week 7 refinement."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
UX = ROOT / 'Course/Slides/Week07/UXMantras20261015'
FINAL = ROOT / 'Course/Slides/Week07/FinalClass20261013'
PRACTICE = OUT / 'assets/practice'
slides = []
sources = {
 'oster':'https://dev.epicgames.com/community/learning/tutorials/xrnE/unreal-engine-asset-setup-with-the-unreal-python-api',
 'assettools':'https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/AssetTools?application_version=5.7',
 'material':'https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MaterialEditingLibrary?application_version=5.7',
 'stories':'https://www.atlassian.com/agile/project-management/user-stories',
 'art':'https://www.getty.edu/education/teachers/building_lessons/formal_analysis.html',
 'principles':'https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html',
 'contrast':'https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html',
 'color':'https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html',
 'figma':'https://www.figma.com/design-systems/',
 'coolors':'https://coolors.co/generate',
 'testing':'https://www.nngroup.com/articles/usability-testing-101/',
}
def add(id,title,body=None,table=None,image=None,question='',notes='',refs=(),template=61,kind='body',timed=False,caption='',code=None,mantra=None):
    record=dict(id=id,title=title,body=body or [],table=table,image=str(image) if image else None,
        question=question,notes=notes,sources=[sources.get(r,r) for r in refs],template=template,
        kind=kind,timed=timed,caption=caption,code=code,mantra=mantra)
    slides.append(record)
    return id

add('O1','Import is the start of setup',table=[
 ['Stage','Evidence to carry forward'],['Import','Returned objects and source files'],
 ['Plan','Mesh slot, parent and exact texture roles'],['Configure','Instance parent and parameter values'],
 ['Assign and verify','Intended target changes; protected scope stays']],
 question='What could import successfully but still be wrong in the scene?',
 notes='Import gives us objects, but the artist needs a usable result. Oster’s setup series follows the relationships from imported meshes and textures to material instances. Retain the objects returned by the import so the next step knows its scope. Before changing anything, identify the parent, texture roles and target slot. Then inspect the result and something that must remain unchanged. A folder can contain unrelated assets, so a folder scan is a broader scope than this import’s returned objects.',
 refs=('oster','assettools'),template=35,timed=True,caption='Isaac Oster · Asset Setup series · teaching adaptation')
add('O2','A naming rule must preserve identity',table=[
 ['Mesh / texture name','Family','Role'],['SM_AirConditioning_01','AirConditioning_01','Mesh'],
 ['T_AirConditioning_01_BC','AirConditioning_01','Base color'],
 ['T_AirConditioning_010_BC','AirConditioning_010','Different asset']],
 body=['Match the complete family and a declared suffix. Require one intended texture per role.'],
 question='Why can a substring match assign the wrong base-color texture?',
 notes='Read the last two names carefully. Zero-one and zero-one-zero are different identities. Splitting at the first underscore loses useful information, and a substring can match too much. A naming convention is an agreement about data. Validate it: missing and duplicate roles are different errors. A multi-material mesh also needs a mapping for each slot. The course tool uses BaseColor, Normal and ORM suffixes; Oster’s example uses BC, N and ORM. Neither set of names is a reserved Unreal requirement.',refs=('oster',),template=35)
add('O3','A slot record is not the material',table=[
 ['Value','What it identifies'],['Slot index','Numeric position used for assignment'],
 ['Slot name','Semantic label such as Body'],['Material interface','Assigned material or instance object'],
 ['Assignment target','Shared mesh default or one component override']],
 question='Two Actors use one mesh. Which object would you edit to change only one?',
 notes='StaticMaterial is a structure with named properties. The index, slot name and assigned material are different values. Keep the index using enumerate when you inspect the array. Oster changes the StaticMesh asset’s default assignment. Our classroom tool assigns an override to the selected component. That is why the protected cube can stay unchanged even though both cubes use the same mesh. Do not delete an assigned material simply because you found a reference to it; that reference does not prove the asset is owned by this operation.',refs=('oster',),template=35)
add('O4','Verify the relationship after the call',code='library.set_material_instance_texture_parameter_value(\n    instance, "BaseColorTexture", texture)\nactual = library.get_material_instance_texture_parameter_value(\n    instance, "BaseColorTexture")\nif actual != texture:\n    raise RuntimeError("Base-color binding did not match")',
 body=['Read back the value, inspect the assignment, then check the scene.'],
 question='What does a successful return value establish—and what does it leave untested?',
 notes='This excerpt assumes unreal, library, instance and texture already refer to the intended objects. In our recorded Unreal 5.7.4 rehearsal, the setter returned false even though the value changed. The current adapter reads the value back. That observation concerns this fixture and engine build; it is not a promise about every version. The broader method is useful everywhere: verify the relationship you intended to change. Also inspect the protected target and the visible result. Saving is a separate step and needs its own result check.',refs=('material',),template=35,
 caption='Excerpt from the course backend · existing instance and loaded texture required')

add('L1P','Lab 1: predict before the reveal',table=[
 ['Selected?','Starting name','Your expected name'],['Yes','crate_A','?'],['Yes','crate_B','?'],['Yes','SM_crate_C','?'],['No','barrel_D','?']],
 body=['Rename selected assets with exactly one SM_ prefix. Preserve the rest of every name.'],
 question='What must remain unchanged? Record all four predictions.',
 notes='Work in a small group using the Lab 1 sheet. The tool is a fictional batch renamer; no installation is needed. Its promise is precise: only selected assets receive exactly one SM underscore prefix. Preserve the rest of each name. Before I reveal the result, write the four expected names, including the unselected barrel. Discuss what evidence you would inspect instead of trusting a success message. Keep your original prediction so we can revisit it after learning the UX principles.',timed=True)
add('L1R','Lab 1: compare the evidence',table=[
 ['Starting name','Expected','Reported result'],['crate_A','SM_crate_A','SM_crate_A'],['crate_B','SM_crate_B','SM_crate_B'],['SM_crate_C','SM_crate_C','SM_SM_crate_C'],['barrel_D','barrel_D','SM_barrel_D']],
 body=['The tool reports: “Success: 4 assets updated.”'],
 question='Name one observed failure, its consequence, and a precise retest.',
 notes='Compare the reported names with your predictions. The unselected barrel changed, and the already-prefixed crate received a second prefix. Those are two observations supported by this evidence. We do not yet know the internal cause, whether Undo works, or what a second run would do. Write one consequential finding and a retest with exact expected names. A proposed fix is a hypothesis. What questions do you have about separating an observation from its explanation?',timed=True)

def mantra(id,title,subtitle,question):
 add(id,title,body=[subtitle],question=question,notes='Use this principle to revisit the same artist task. '+subtitle+' '+question,kind='divider',template=59,timed=True,mantra=title)
mantra('M1','Know the task','Identify the artist, the situation, and a result worth achieving.','What is the artist trying to accomplish?')
add('S1','A user story names an outcome',table=[
 ['Part','Material-tool example'],['User and context','Environment artist trying a look on one prop'],['Desired outcome','Preview and assign a prepared texture set'],['Benefit','Compare the look while other placements stay unchanged']],
 question='What is missing from “As a user, I want a blue Apply button”?',
 notes='A user story describes an outcome and why it matters. Here an environment artist wants to compare a surface on one prop without changing other placements. The familiar As a, I want, so that wording can expose assumptions, but the conversation matters more than the sentence pattern. A blue button already chooses a solution without explaining the need. Ask the artist about starting inputs, current workarounds, frequency and constraints. Then agree on evidence that the outcome has been reached.',refs=('stories',),timed=True)
add('S2','Turn the story into observable checks',table=[
 ['Given','When','Then'],['Prepared textures + target','Preview','Target, slot and mappings are visible; scene unchanged'],['A reviewed plan','Selection changes','Apply requires a fresh preview'],['A valid reviewed plan','Apply once','Target changes; protected cube and shared mesh stay']],
 question='Which check tests the result, and which checks the boundary?',
 notes='Acceptance checks make the story observable. Given a starting state, when an action occurs, then state what should be visible. Include both the intended change and protected scope. These checks describe behavior, not an exact sequence of implementation calls. A participant task should name the goal and starting data without telling the tester every click. That lets us observe whether the interface explains itself.',refs=('stories',))
add('S3','Outline a small complete workflow',body=[
 'Start with the current workaround and prepared input.',
 'Choose → inspect scope → preview → apply → check.',
 'Include a blocked path and a way to recover.',
 'Split a large feature into a useful result the artist can try.'],
 question='Which small result could a classmate test today?',
 notes='Draw the whole task before choosing controls. A useful first slice may handle one prepared texture set and one target, provided it reaches a checkable result. A backend function by itself is not an end-to-end artist workflow. Our import story is another example: bring a revised prop into Unreal so the artist can inspect it without rebuilding its setup. That story needs checks for asset identity, geometry, material assignment and unchanged placement. The same story structure applies to both tools.',refs=('stories',))

mantra('M2','Guide the eye','Use composition to communicate priority and relationships.','Where should the artist look first, and why?')
add('V1','Value and contrast are different ideas',table=[
 ['Concept','Meaning in art and tool design'],['Value','The lightness or darkness of a visual area'],['Contrast','A difference between neighboring elements'],['Visual hierarchy','The priority suggested by size, value, spacing and emphasis']],
 body=['HSV Value is a color coordinate. It is not perceived lightness or a contrast ratio.'],
 question='Would different hues remain distinct if their light and dark values were similar?',
 notes='Recall the art lens: composition creates a reading route. In a scene, a focal area helps orient the player. In an editor tool, emphasis helps the artist find the target or next action. Value means lightness and darkness. Contrast describes a difference, which may be in value, hue, size or shape. HSV Value is a software color coordinate, not a measurement of perceived lightness. The analogy gives us a design intention; the actual screen, controls and viewing distance still need testing.',refs=('art','principles'),timed=True)
add('V2','Three quick hierarchy checks',table=[
 ['Check','Try it','Ask'],['Shape blockout','Ignore labels; reduce regions to simple masses','Are related decisions grouped?'],['Grayscale','Temporarily remove hue','Does meaning survive without color?'],['Squint test','Squint briefly or step back','Which large shapes and values dominate?']],
 question='Now restore the original. Can you read the labels and use the controls?',
 notes='Use these as quick artistic diagnostics, not pass certificates. Blockout helps us see grouping and spacing. Grayscale helps us notice dependence on hue. The squint test helps expose the largest areas of visual weight. A blur is only an approximation of squinting. None measures accessibility, text readability, keyboard behavior or actual attention. Restore the image and inspect the real controls. What would each check miss?',refs=('art','contrast'),timed=True)
add('V3','Choose color roles before choosing colors',body=[
 'Give primary actions, warnings and supporting surfaces distinct roles.',
 'Pair status color with a label, icon or shape.',
 'Explore palettes with Coolors; check actual foreground/background pairs.',
 'Text benchmark: 4.5:1 ordinary text, 3:1 large text under WCAG definitions.'],
 question='Does this palette explain “selected,” “available,” and “complete” separately?',
 notes='A palette tool helps us explore combinations, but a pleasant palette is not a complete interface. Start by assigning semantic roles. A focused control, selected item and completed step are different states. Check actual text and surface pairs in the tool. WCAG text contrast is a useful benchmark, with definitions and exceptions; using those numbers alone does not certify a desktop tool. Shader color also depends on color space, lighting and exposure, so identical RGB inputs need not produce the same visible result.',refs=('coolors','contrast','color'))
add('G1','Case study: GOLF+ Course Generator',image=UX/'assets/golf-course-generator-user-20261015.png',body=[
 'Notice: numbered stages reveal the intended sequence.',
 'Generate receives strong visual emphasis.',
 'Edit is explicitly optional.',
 'Apply: make the next step and its prerequisites easy to find.'],
 question='What does the warning beside Input mean? Can this image tell us?',
 notes='This is the supplied Course Generator capture from my GOLF+ work. Follow Input, Parameters, Generate, optional Edit, Finalize and Integrate. The staged layout makes the intended route visible and gives Generate strong emphasis. Now critique it: what does the warning beside Input mean, and should the artist proceed? A still image cannot answer those behavior questions. Muted controls and filled markers do not prove enabled or completed state. This is a visual case study, not a fresh runtime test.',caption='GOLF+ Course Generator · instructor’s production tool',timed=True)

mantra('M3','Make actions clear','Show scope, current state, and the next useful action.','Can the artist predict the result before acting?')
add('A1','State determines the next action',table=[
 ['State','Useful next action','What the UI communicates'],['No plan','Preview','Inputs can be checked without mutation'],['Valid reviewed plan','Apply','Names the operation and affected count'],['Warning','Review and acknowledge','Explains the concern; limits still apply'],['Completed','Inspect result','No repeated Apply from the consumed plan']],
 question='If an input changes, what should happen to the old preview?',
 notes='A primary button communicates the next useful action. It does not decide whether an operation is safe. In our assistant, Preview is emphasized before a plan exists. Apply becomes available after a valid review. A warning interrupts that progression until it is acknowledged, without bypassing hard limits. After completion, inspect the result. If an input or external selection changes, the previous plan becomes stale and must be reviewed again. Changing inputs does not undo an already applied result.',timed=True)
add('A2','One readiness rule becomes Qt code',code='pending = self.session.pending\nready = bool(pending) and (\n    not pending[3].get("warnings") or self.ack.isChecked())\nself.apply_button.setEnabled(ready)',body=[
 'Input-change signals invalidate the preview.',
 'The session rechecks scope when Apply runs.'],
 question='Why must the backend validate again if Apply is already enabled?',
 notes='This is an excerpt from AssistantWindow.update_apply. The surrounding class, widgets and session already exist. A pending plan and any required acknowledgement control the button’s enabled state. The backend still validates when the operation runs because selection or scene state can change outside this window. This small example grounds the visual principle without turning the UX section into a full Qt programming lesson. You can find the complete code in the project.',caption='Current PySide implementation · excerpt, not a standalone script')
add('A3','The same workflow can use different UIs',table=[
 ['Surface','Useful implementation distinction'],['PySide / Qt','Layouts and signals in a Python window'],['Native Unreal Slate','Editor tab using the host UI framework'],['Editor Utility Widget','Blueprint-based editor interface; a separate option'],['Shared workflow','Inputs → reviewed plan → guarded apply → result']],
 question='Which parts should stay consistent when the host interface changes?',
 notes='The task and safety contract should survive a toolkit change. Our project has a PySide window and a native C++ Slate tab that call the same Python workflow. A Qt window parented to Unreal is still a Qt window; it is not native docking. Editor Utility Widgets are another Unreal option and should not be confused with this Slate implementation. Choose the host integration that fits the users and deployment constraints, while keeping wording, scope and state behavior coherent.')
add('A4','Make review data readable',image=PRACTICE/'material_preview.png',body=[
 'Show exact identity and target slot.',
 'Keep Before beside After Apply.',
 'Separate the proposed result from a completed result.'],
 question='Which row would you inspect to confirm the affected component?',
 notes='The table supports a decision. It shows the new instance, parent, texture inputs and target component. The Before and After Apply columns remove the need to remember the old values. These paths belong to practice data; they are not a new Unreal run. A full path can be long, so support inspection at real window sizes and make complete values available. A table is useful here because the user is comparing corresponding values.',caption='Updated course PySide interface · sample data · no Unreal connection',kind='image')

mantra('M4','Keep a shared visual language','Record decisions so people and tools use the same meanings.','Which rules should every contributor be able to find?')
add('C1','A style sheet records design decisions',body=['Shared rules reduce drift across people, tools and releases.'],table=[
 ['Record','Example from the course tool'],['Typography and spacing','Title, field label, help text; consistent group gaps'],['Color and control roles','Primary action, focus, warning, unavailable state'],['Interaction and wording','Preview before Apply; name the affected operation'],['Examples and exceptions','Starting, blocked, completed and narrow-window views']],
 question='What would a color palette alone leave unspecified?',
 notes='A style sheet is a maintained specification of visual and interaction decisions. It explains what the rules mean, where they apply and how to recognize a correct example. Larger teams commonly use shared guides and design systems to coordinate contributors, support onboarding and keep changes consistent. The terminology and maturity vary; it is not literally universal. A design system adds reusable components and maintenance practices. CSS or QSS implements part of the appearance, but it is not the whole specification.',refs=('figma',),timed=True)
add('C2','Use the style sheet when working with AI',body=[
 'Keep design rules in a versioned style-sheet skill.',
 'Have design agents reference it before changing the UI.',
 'Review screenshots and behavior against the same rules.',
 'Record an intentional exception; update the sheet when the rule changes.'],
 question='What evidence would you request before accepting “the design is consistent”?',
 notes='In my workflow, I keep the design decisions in a style-sheet skill and have the agent working on design refer back to it. The skill gives the agent a shared source of context; it does not automatically guarantee compliance. Ask it to identify the pattern it will reuse, then review the actual result. If the team deliberately changes a rule, update the source so the next agent does not restore the old version. The same discipline helps human contributors. The course folder includes a small local example tied to our tool style sheet.',timed=True)
add('C3','Case study: keep workflow names aligned',image=UX/'assets/golf-course-generator-user-20261015.png',body=[
 'The supplied UI has six named stages.',
 'An earlier playbook used different stage terms.',
 'Reconcile the intended names in the interface, documentation and AI instructions.'],
 question='Which version would a new teammate—or an agent—treat as the source of truth?',
 notes='Revisit the same GOLF+ screenshot for a different question. The supplied interface says Input, Parameters, Generate, Edit, Finalize and Integrate. An earlier playbook used Detect, Generate, Finalize and Adopt. That difference does not prove a software defect, but it does show why a shared guide must be maintained. Confirm the intended workflow, then align the UI, examples and agent instructions. A screenshot and an old document are evidence to reconcile, not interchangeable descriptions.',caption='Same supplied GOLF+ interface · documentation consistency example')

mantra('M5','Test the whole workflow','Observe the attempt, inspect the result, and retest the revision.','What evidence would change your design decision?')
add('T1','Prototype the question you need to answer',table=[
 ['Prototype','Good question','What remains untested'],['Paper or Figma','Can a peer find the next action?','Real data and engine behavior'],['PySide practice UI','Do controls and states make sense?','Live assets and host integration'],['Prepared engine fixture','Does this operation respect scope?','Other projects and target performance']],
 question='Which is the cheapest prototype that answers your current uncertainty?',
 notes='Prototype fidelity should match the question. A paper sketch or Figma flow can test sequence and wording before a backend exists. A functioning practice UI can expose state and keyboard issues. A prepared engine fixture can test actual references and mutations. Each leaves other questions open. A game HUD, VR panel and editor tool have different input and viewing contexts, so use the intended context when that is the question. Test one uncertainty at a time and record what the prototype cannot establish.',refs=('testing',),timed=True)
add('T2','A useful finding separates evidence from explanation',table=[
 ['Part','Example'],['Observed','The tester paused at the destination field and asked for help.'],['Possible explanation','The label may not identify which folder will change.'],['Proposed revision','Name the destination and affected assets beside Preview.'],['Retest','Same task and inputs; can a new tester identify scope without help?']],
 question='What did you observe, and what are you still inferring?',
 notes='A preference is a starting point, but a usable finding names what happened and how it affected the task. The explanation is tentative. Maybe the label caused the pause, or maybe the task setup was unclear. Change one relevant thing and retest. Record strengths with the same care: a tester finding the target without help is evidence of a successful interaction. If no issue appeared, say that instead of inventing one.',refs=('testing',),timed=True)
add('T3','Events and observation answer different questions',table=[
 ['Evidence','Can help answer','Cannot establish alone'],['preview_finished','Did it complete, and how long did it take?','Did the artist understand it?'],['apply_blocked + reason','Which rule stopped the operation?','Whether the message supported recovery'],['Observed task attempt','Where did the user hesitate or need help?','Frequency across the whole user population']],
 question='Which evidence would help explain a slow task in your tool?',
 notes='Telemetry can record operation counts, durations and reasons for blocked actions. Observation can reveal hesitation, workarounds and misunderstanding. Combine them when useful, but do not equate a click count or successful call with a good experience. Collect only fields needed for the question and avoid copying project paths or user content unnecessarily. For this class, a short observation record is enough; we are not adding a telemetry implementation requirement.')

add('P1','Prepare one task a peer can attempt',template=76,table=[
 ['Specify','Example'],['User and goal','Environment artist comparing one surface'],['Input and boundary','Prepared textures + target crate; protected crate stays'],['Visible success','Expected look, correct slot and unchanged comparison object'],['Repeat / fallback','Restore prepared state; use a labeled walkthrough if blocked']],
 question='Give a goal, not a list of clicks.',
 notes='Use the preparation page to give the tester a bounded task. State the input, goal, visible success and protected scope, then let the tester choose the steps. Include a repeat or fallback method. If the tool cannot run, use a recording, paper or Figma walkthrough and label execution as untested. Do not count a walkthrough as proof of engine behavior. We will keep the same starting state and version within the review so observations can be compared.',timed=True)
add('P2','Three roles, three seven-minute rounds',table=[
 ['Round','Owner','Tester','Observer'],['1','A','B','C'],['2','B','C','A'],['3','C','A','B']],
 body=['Owner: state the goal. Tester: attempt. Observer: record evidence and help.'],
 question='Each tool gets one observed attempt with two peer perspectives.',
 notes='Form groups of three and choose A, B and C. Each round focuses on one tool. The owner explains the goal and prepared input, then watches. The tester tries the task and says what they expect. The observer records the visible evidence and any coaching. Rotate so each person owns, tests and observes once. This is one observed attempt per tool, not three independent tests of every tool. If a group has an extra member, they can observe without inflating the number of distinct attempts.',timed=True,template=76)
add('P3','One round produces evidence and a retest',table=[
 ['Elapsed','Action'],['0:00–0:45','Owner states task, input and success'],['0:45–3:45','Tester attempts; observer records'],['3:45–5:15','Compare expectation with observed result'],['5:15–6:15','Choose a strength and one revision or uncertainty'],['6:15–7:00','Write a retest; reset and rotate']],
 question='If execution is blocked, label the mode and continue with the prepared fallback.',
 notes='Keep the attempt long enough to observe meaningful behavior. Record help rather than hiding it. If setup fails, allow one brief recovery attempt, then switch to the prepared walkthrough. Use the final minute to specify the retest and reset, not to start another feature. The timer will stop at the end of the round; choose the next round deliberately. What questions do you have about the roles or the review mode?',timed=True,template=76)
add('P4','Choose a revision supported by evidence',body=[
 'Keep one strength a peer actually observed.',
 'Prioritize one issue or uncertainty by its consequence.',
 'State the change or investigation you will try.',
 'Specify the retest: input, action, expected result and protected scope.'],
 question='What changed—or strengthened—your original judgment?',
 notes='Apply the same checklist to your own tool for four minutes, then use the final three minutes to record a revision and retest. A serious failure can matter even if only one person sees it. A proposed visual change remains a hypothesis until you test it. Record which mode you used, what was observed and what remains untested. Keep one observed strength so improvement does not remove behavior that already supports the task.',timed=True,template=76)

# The source gradient deck is the authority for appearance and its revised timetable.
# Keep all original teaching examples, including embedded media, in the full deck.
order=[]
for n in range(1,77):
 if n==35: order.append(n); order += ['O1','O2','O3','O4']; continue
 if n==60: order += ['L1P','L1R','M1','S1','S2','S3']; continue
 if n==62: order += ['M2'];
 if n==64: order.append(n);order += ['V1','V2','G1'];continue
 if n==65: order.append(n);order += ['V3'];continue
 if n==66: continue
 if n==67: order += ['M3','A1','A2','A3','A4']
 if n==73: order.append(n);order += ['M4','C1','C2','C3','M5','T1',66,'T2','T3'];continue
 if n==76: order += ['P1','P2','P3','P4'];continue
 order.append(n)

# Timed route preserves the current 3:30–6:00 timetable. Full explanations stay available.
core_before=[1,2,3,4,6,7,8,9,11,12,13,15,16,17,18,19,21,22,24,25,26,27,29,30,32,33,34,35,'O1',36,38,39,40,42,43,44,47,48,49,50,51,52,53,54,56,57,58]
core_ux=[59,'L1P','L1R','M1','S1','M2','V1','V2','G1','M3','A1',72,'M4','C1','C2','M5','T1','T2',75,'P1','P2','P3','P4']
timed=core_before+core_ux
assert len(order)==len(set(map(str,order)))
assert all(str(x) in set(map(str,order)) for x in timed)
data={'slides':slides,'order':order,'timed_route':timed,'replaced_source_slides':[60,76],
 'schedule':[
 ['3:30–3:35','Introduction',5],['3:35–3:50','Unreal setup + host check',15],
 ['3:50–4:10','Selection, objects + texture validation',20],
 ['4:10–4:40','Reliability, Blender bridge, Material/VFX and selected case studies',30],
 ['4:40–4:55','Colleague demonstrations and discussion',15],['4:55–5:10','Break',15],
 ['5:10–5:18','Lab 1 prediction, reveal and finding',8],['5:18–5:30','Five UX mantras with selected examples',12],
 ['5:30–5:32','Peer task and roles',2],['5:32–5:53','Three seven-minute rounds',21],
 ['5:53–5:57','Review your own tool',4],['5:57–6:00','Revision and retest',3]]}
assert sum(row[2] for row in data['schedule'])==150
(OUT/'content-plan.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'new_or_replacement_slides':len(slides),'final_slides':len(order),'timed_route':len(timed),'minutes':150}))
