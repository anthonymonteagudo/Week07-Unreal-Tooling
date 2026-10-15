"""Revise projected copy in place, preserving media, geometry, notes and source credits."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E
import json,posixpath,hashlib
R=Path(__file__).resolve().parents[1]
NS={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
inv=json.loads((R/'build/pre-direct-copy-inventory.json').read_text())
with ZipFile(R/'build/source-v7.pptx') as z:d={n:z.read(n) for n in z.namelist()}
titles={
 4:'Unreal Python Setup',5:'Engine and Project Check',6:'Required Plugins',7:'VS Code Autocomplete',8:'VS Code Settings',10:'Python Scene Tools',
 11:'UE01: Engine and Project',13:'Unreal Subsystems',14:'Selected Actors',15:'UE02: Actor Selection',16:'Running a Python File',17:'UE02: Expected Output',18:'UE02: Actor Selection',19:'UE03: Actor Selection',20:'TAPython Object Inspector',21:'UE03: Components and Meshes',22:'Material Overrides',23:'Actors, Components and Assets',25:'UE04: Expected Output',26:'Texture Settings',27:'Texture Validation',28:'Texture Properties',30:'UE05: Expected Values',31:'UE04–05: Texture Properties',33:'Asset Validation',34:'Unit Tests',35:'UE07: File Paths and Asset Paths',36:'Asset Setup',37:'Asset Naming',38:'Material Slots',39:'Parameter Verification',40:'Progress Bars',41:'Unreal Script Editor',42:'Python from Blueprints',43:'Tool Distribution',44:'Remote Control',45:'AYON Pipeline Tools',46:'Unreal Python Q&A',48:'BL01: Blender Selection',49:'Blender Objects',50:'Blender Properties and Operators',51:'BL02: Blender Bridge',53:'Demo Setup',54:'Material Parameters',55:'Material Setup Tool',56:'VFX Placement Tool',57:'Project Titan Ivy Tool',58:'Project Titan Train Rig',59:'Project Titan Environment',64:'Lab 1: Batch Renaming',65:'Lab 1: Results',66:'Know the Task',67:'User Stories',68:'Acceptance Criteria',69:'Workflow Scope',70:'The Artist’s Mental Model',71:'Guide the Eye',72:'Grouping and Hierarchy',73:'Blender UI Redesign',74:'Composition and UI Layout',75:'Value and Contrast',76:'Visual Hierarchy Checks',77:'GOLF+ Course Generator',78:'Color in UI',79:'UI Color Roles',80:'Make Actions Clear',81:'UI States',82:'Enabling Apply in Qt',83:'UI Frameworks',84:'Preview Tables',85:'Task Feedback',86:'PowerRename',87:'Material Parameters Helper',88:'Click Feedback',90:'Undo',91:'Contextual Tools',92:'Keep It Consistent',93:'Style Sheets',94:'Style Sheets for AI',95:'Consistent Naming',96:'Test the Workflow',97:'Prototyping',98:'NN/g Layout Testing',99:'Observations and Assumptions',100:'Usage Logs and Observation',101:'Useful Feedback',103:'Test Setup',104:'Peer Review Roles',105:'Seven-Minute Round',106:'Revision Plan'
}
# Exact paragraph replacements. Empty values remove redundant projected copy.
copy={
3:{'Enable editor scripting and check the project before running code.':'Run Python inside the Unreal Editor.'},
7:{'Open the Week07UnrealPython folder in VS Code.\u2003Install microsoft python and pylance.In Unreal: Editor Preferences > Plugins > Python > Developer Mode. Restart Unreal. Confirm Intermediate/PythonStub/unreal.py exists in this project.':'Open the project folder in VS Code and install the Python and Pylance extensions.\nEnable Developer Mode under Unreal’s Python preferences, then restart.\nCheck for Intermediate/PythonStub/unreal.py.'},
8:{'Save in .vscode/settings.json. Type unreal. in a Python file to check suggestions.':'Save as .vscode/settings.json, then type unreal. to check autocomplete.'},
9:{'Read the selection, inspect its objects, and validate texture settings.':'Use the editor’s selection as input to a Python tool.'},
10:{'Notice: an input drives a visible scene change.':'Changing an input updates the scene.','Apply: expose the input and show what it affects.':''},
13:{'Get the subsystem, then ask it for the selection.':'EditorActorSubsystem provides access to level Actors.','Ask the running editor for a subsystem.':'Get the editor subsystem.','Class argument: which subsystem we need.':'The subsystem class to request.','Call on that instance. No explicit arguments.':'Return the selected Actors.','Keep the returned Array[Actor] to inspect.':'Store the returned Actor array.'},
14:{'editor: subsystem instance. actor: one selected Actor.':'editor is the subsystem. actor is an Actor from its selection.','Use in an artist tool':'What it does','Show the artist-facing Actor label in a report.':'Read the label shown in the Outliner.','Report the selected object’s Unreal class.':'Read the Actor’s class name.'},
15:{'get_selected_level_actors() returns Actor objects. len counts them; the loop reads each label and class.':'The loop prints the label and class of every selected Actor.'},
16:{'Read the Output Log. Change the Outliner selection and execute the file again.':'Change the Outliner selection and rerun to compare the Output Log.'},
17:{'Select W07_Crate_Target.':'Select W07_Crate_Target and run UE02.','Run UE02.':'','Label: Outliner identity. Class: Actor type.':'The output identifies the Actor by its Outliner label and class.'},
18:{'One Actor. The label and class identify exactly what the script read.':'The log identifies the selected Actor.'},
19:{'Same selection setup as UE02. The complete UE03 file also reads components and meshes.':'UE03 uses this selection to read components and their mesh assets.'},
20:{'Notice: properties belong to specific objects.':'The inspector shows properties for the selected object.','Apply: identify the target before exposing an edit.':''},
21:{'The selected Actor owns a StaticMeshComponent.':'The Actor’s StaticMeshComponent references the Cube asset.','That component refers to the engine Cube asset.':'','Actor label, component name and asset path describe different objects.':'The Actor, component and mesh asset are separate objects.'},
22:{'Same mesh. Different material assignments.':'Two Actors share a mesh but use different materials.','Which placement changed? What stayed shared?':'Which object owns the material override?'},
23:{'Use in an artist tool':'What it does'},
24:{'This selection supplies assets, independently of the Outliner.':'Content Browser selection is separate from Outliner selection.'},
25:{'Select T_Crate_BaseColor in the Content Browser.':'Select T_Crate_BaseColor in the Content Browser and run UE04.','Run the complete UE04 file.':'','Try another asset and rerun. Reset by reselecting the texture.':'Try another asset and compare the output.','Read the name, class and object path; not the Outliner selection.':''},
26:{'Prepared compression':'Compression'},
27:{'Normal-map image, but compression is set to Masks. What should the validator flag?':'This normal map uses Masks compression. What should change?'},
28:{'Read first. Compare with the asset’s intended role before proposing a fix.':'Compare each texture’s settings with its intended use.','Use in an artist tool':'What it does','Read Content Browser selection, not level selection.':'Read selected Content Browser assets.'},
29:{'Read compression and sRGB. Non-texture selections are counted and skipped.':'The script prints each texture’s settings and skips other asset types.'},
30:{'Expected values; enum formatting may differ. No edits are made.':'Reading these properties does not change the textures.'},
31:{'Actual UE04 + UE05 output':'Output Log','T_Crate_Normal reads as TC_NORMALMAP with sRGB False.':'Normal map: Normalmap compression, sRGB off.'},
32:{'Excerpt: run the complete UE06 file to initialize textures, expected mode and counters.':'Run the complete UE06 file to initialize the variables used here.'},
33:{'Name the asset, rule and correction.':'A validation error should identify the failing asset and explain the fix.','Project rule: Blueprint names start with BP_.':'Example rule: Blueprint names must start with BP_.','Severity follows project policy.':'','Asset validation checks content. It does not prove that the validator code is correct.':'The validator itself also needs tests.'},
34:{'Unit check: a small rule with a known answer':'A small function with known results','Karol’s test wiring check':'Test Execution','Deliberately fail once: prove the runner actually executes the check.':'Force a failure once to confirm that the test actually runs.'},
35:{'The filesystem path and Unreal object path name different things.':'A file path points to disk. An Unreal object path identifies an asset.'},
36:{'Evidence to carry forward':'Required data','Objects + source files':'Imported objects and source files','Slot + parent + texture roles':'Material slot and texture mapping','Parent + parameters':'Instance parent and parameters','Intended target changes; protected scope stays':'Assignment on the intended target'},
37:{'Match the complete family and a declared suffix. Require one intended texture per role.':'Match the full asset name so _01 cannot accidentally match _010.','Why can a substring match assign the wrong base-color texture?':'What would a substring search match here?'},
38:{'Semantic label, e.g. Body':'Label such as Body','Two Actors use one mesh. Which object would you edit to change only one?':'Where would you assign a material to change only one Actor?'},
39:{'Read back the value, inspect the assignment, then check the scene.':'Read the parameter again to confirm that the assignment succeeded.','What does a successful return value establish? What remains untested?':'Does a successful return value guarantee the correct result?','Excerpt from the course backend · existing instance and loaded texture required':'Requires library, instance and texture.'},
40:{'Count the work. Show the current step. Check Cancel between items.':'Use ScopedSlowTask for batch operations.','ScopedSlowTask(total, message)':'ScopedSlowTask(total, message)\nCreate the task with its total work count.','make_dialog(can_cancel=True)':'make_dialog(can_cancel=True)\nShow a progress bar with a Cancel button.','should_cancel() → stop remaining work':'should_cancel()\nCheck inside the loop and break when requested.','enter_progress_frame(1) → advance one unit':'enter_progress_frame(1)\nAdvance progress by one unit.','Cancel stops future iterations; it does not undo completed edits.':'Cancel stops the remaining work without undoing completed edits.'},
41:{'Python/Qt editor: files, temporary scripts and familiar editing controls.':'Edit and run Python scripts inside Unreal.','Notice: users can organize and run scripts in one place.':'','Apply: give artists a clear entry point for a repeatable task.':''},
42:{'Selected assets + material choice → Execute Python Script':'Pass Blueprint inputs into Execute Python Script.','Inputs become Python variables. Set output variables to report a result.':'Input pins become Python variables. Output variables return the result.','Use in Editor Utility Blueprints or Widgets; Python remains editor-only.':'Available in Editor Utility Blueprints and Widgets.'},
43:{'Package logic + a clear entry point.':'Include what another artist needs to install and use the tool.','Version + supported engine':'Supported engine version','Install / enable instructions':'Installation instructions','Known limits + recovery':'Known limits and recovery','A clean-project smoke test':'Test in a clean project','Release check: can another artist install it and complete the example without you?':'Can another artist complete the example without your help?'},
44:{'Remote Control is another entry point. It still needs scope, validation and useful feedback.':'An external app can call exposed Unreal functions over HTTP.'},
45:{'Notice: the tools follow distinct pipeline tasks.':'','Define your tool’s handoff: input, result and next step.':''},
46:{'Where does the code run?':'Questions about running Python in Unreal?','Which object owns the state we change?':'','What would you like clarified about success or recovery?':''},
47:{'Same Python language, different application API.':'Blender exposes its Python API through bpy.'},
48:{'bpy.context.selected_objects supplies Blender Objects. Unreal uses its own editor APIs.':'bpy.context.selected_objects returns the selected Blender Objects.','Run in Blender. Complete example.':'Run in Blender.'},
49:{'The active Object and the full selection answer different questions.':'The active Object is one object within the selection.','Use in an artist tool':'What it does','Read the selected Objects. This is a property.':'Read the selected Objects.'},
50:{'Use in an artist tool':'What it does','Read local position. Assigning a value moves it.':'Read or change local position.','Apply rotation and scale to selected Objects. Requires Object Mode.':'Apply rotation and scale in Object Mode.'},
51:{'Rehearsal: republish the baseline mesh under the same asset name to reset.':'Reset by republishing the original mesh under the same asset name.'},
52:{'Watch the input, the affected objects, and the visible result.':'Check which objects each tool changes.'},
53:{'Unreal: Check and stage the classroom scene':'Run in Unreal’s Python console','Material & VFX: ready.':'Material & VFX: ready.','Target and textures selected.':'Target and textures selected.','Open Tools > Material & VFX Tools.':'Open Tools > Material & VFX Tools.','The bridge is checked separately.':''},
55:{'Review the assignment. Inspect the scene.':'','One target changes.':'Only the selected crate receives the material.','The protected cube stays.':''},
56:{'Preview three markers. Check three fountains.':'','Three placements.':'One fountain per marker.','Performance needs a separate check.':'Placement limits do not measure frame cost.'},
57:{'Notice':'Controls','Apply':'','Expose controls for':'','shape and variation.':'','Houdini digital asset in Unreal: a procedural tool, not a Python-only example.':'A Houdini digital asset running in Unreal.'},
58:{'Notice':'Workflow','Apply':'','Check the result at':'','each handoff.':''},
59:{'Notice: repeated systems support an authored environment.':'Procedural tools handle repeated details while artists control the composition.','Apply: automate one repeatable step; preserve artistic choices.':''},
63:{'Use the same observation method for case studies, peers, and your own tool.':'Can someone else use your tool without help?'},
64:{'What must remain unchanged? Record all four predictions.':'Write the expected result for all four assets.'},
65:{'Name one observed failure, its consequence, and a precise retest.':'Which results are wrong, and how would you test a fix?'},
66:{'Identify the artist, the situation, and a result worth achieving.':'Start with the artist’s goal.','What is the artist trying to accomplish?':''},
67:{'A user story names an outcome':'User Stories','What is missing from “As a user, I want a blue Apply button”?':'What goal is missing from “I want a blue Apply button”?'},
68:{'Targets visible; scene unchanged':'Preview lists targets without changing the scene','Target changes; protected cube and shared mesh stay':'Only the target’s material assignment changes','Which check tests the result, and which checks the boundary?':'Which test catches a change to the wrong object?'},
69:{'Start with the current workaround and prepared input.':'Define the starting input and the result the artist needs.','Choose → inspect scope → preview → apply → check.':'','Include a blocked path and a way to recover.':'Include error handling and a reset.','Split a large feature into a useful result the artist can try.':'Test one complete task before adding features.','Which small result could a classmate test today?':''},
70:{'Find Actor, inspect components, assign material.':'Assign a material to an Actor’s mesh component.','Show the target, material choice, preview and commit.':'Let the artist preview the material on the selected prop.','Assessment question: can the artist predict what the control will do?':'Can the artist predict what the control does?'},
71:{'Use composition to communicate priority and relationships.':'The most important control should stand out.','Where should the artist look first, and why?':''},
72:{'Which controls belong together?':'Group controls that belong to the same task.','Separate unrelated steps.':'Use spacing to separate different tasks.','Label the artist’s task.':'','Expose scope and the next action.':''},
73:{'Notice: grouping and alignment make control relationships clearer.':'Related controls sit together, with spacing between separate tasks.','Apply: group one tool by task, then test whether a peer finds the next control.':''},
74:{'Scene: guide the eye.':'Spacing and contrast guide attention in both scenes and interfaces.','Tool: guide the task.':'','Use spacing, alignment and contrast.':''},
75:{'HSV Value ≠ perceived lightness ≠ contrast ratio.':'HSV Value does not measure perceived lightness or text contrast.','Priority from size, value and spacing':'The order in which elements attract attention'},
76:{'Restore the original. Check labels and controls.':'Use the original view to check readability afterward.'},
77:{'Numbered stages show sequence.':'Numbered stages show the order of the workflow.','Generate has emphasis.':'Generate stands out as the primary action.','Edit is optional.':'','Make the next step easy to find.':'','What does the Input warning mean?':'Does the Input warning explain what needs fixing?'},
78:{'Art: color creates emphasis.':'Color can draw attention to an action or warning.','Tools: color supports state labels.':'','Pair color with the problem and next action.':'Use a label or icon so the meaning survives without color.'},
79:{'Separate actions, warnings and surfaces.':'Use consistent colors for actions and status.','Pair color with a label or icon.':'','Explore with Coolors. Check actual color pairs.':'Coolors helps build palettes. Check contrast on the actual UI.','WCAG text: 4.5:1 normal; 3:1 large.':'WCAG text contrast: 4.5:1 normal, 3:1 large.','Can you distinguish selected, available and complete?':'Can you identify a disabled control without relying on color?'},
80:{'Show scope, current state, and the next useful action.':'Make the result of each action predictable.','Can the artist predict the result before acting?':''},
81:{'Inputs changed. Is this preview still valid?':'Should Apply stay enabled after the selection changes?','Preview consumed':'Preview again before another Apply'},
82:{'Input-change signals invalidate the preview.':'Changing an input invalidates the preview.','The session rechecks scope when Apply runs.':'Apply checks the selection again before making changes.','Current PySide implementation · excerpt, not a standalone script':'Inside AssistantWindow.update_apply()'},
83:{'Surface':'Framework','What should stay consistent across interfaces?':'Which behavior should every version preserve?'},
84:{'Show the target and slot.':'Put Before and After Apply side by side so the change is easy to compare.','Keep Before beside After Apply.':'','After completion, label it Result.':'After Apply succeeds, rename the column Result.','Which component will change?':''},
85:{'Assessment includes behavior, keyboard use and recovery.':'','What the interface should make clear':'What the user needs to know'},
86:{'Notice: original and proposed filenames appear together.':'Review each filename before renaming the batch.','Apply: preview asset-name changes before committing.':''},
87:{'Notice: filters determine which parameters appear.':'Filter the parameter list to find the controls you need.','Apply: group controls and make the active filter obvious.':''},
88:{'Notice: the counter changes immediately after the click.':'The counter updates immediately when you click.','Apply: show a result or progress state after every action.':'','Input':'','Click a control.':'','Visible state':'','The counter updates.':''},
90:{'Undo restored the assignment. The newly created material asset remained.':'Undo restores the assignment but leaves the new material asset in the Content Browser.'},
91:{'Notice: inspection stays in the scene’s spatial context.':'Feedback appears beside the object being edited.','Apply: show feedback beside the affected object or region.':''},
92:{'Record decisions so people and tools use the same meanings.':'Use the same design rules across the tool.','Which rules should every contributor be able to find?':''},
93:{'Shared rules reduce design drift.':'A style sheet defines the design rules the team follows.','What does a palette leave unspecified?':'What rules does a color palette leave out?'},
94:{'Version the style-sheet skill.':'Store the style sheet as a versioned skill and require agents to read it.','Require agents to read it first.':'','Review visuals and behavior against it.':'Check UI changes against the sheet and record intentional exceptions.','Record exceptions. Update changed rules.':'','What evidence would prove consistency?':'Does the result follow the sheet?'},
95:{'The supplied UI has six named stages.':'Use the same stage names in the interface and documentation.','An earlier playbook used different stage terms.':'','Reconcile the intended names in the interface, documentation and AI instructions.':'Include those names in AI instructions.','Which version would a new teammate or agent trust?':''},
96:{'Observe the attempt, inspect the result, and retest the revision.':'Watch someone use the tool without coaching.','What evidence would change your design decision?':''},
97:{'Good question':'What it tests','What remains untested':'Limits','What is the cheapest useful test?':'Which prototype answers your question fastest?'},
98:{'Three rounds of testing.':'Three rounds included new and returning users.','New and returning users.':'','Notice':'Result','Users liked the grid,':'Users preferred the list','but preferred the list':'after trying both layouts.','after seeing alternatives.':'','Apply: compare two layouts with the same task; observe hesitation and completion.':'Test both layouts with the same task.'},
99:{'Same task, new tester: identify scope unaided.':'Can a new tester identify the affected folder without help?','What is observed? What is inferred?':'Which part is an assumption?'},
100:{'Cannot establish alone':'Limits'},
101:{'Describe what happened, how it affected the task, and what to change and test.':'Tie feedback to a specific moment in the test.'},
102:{'A task, an observation, a revision to test':'Test a classmate’s tool.'},
103:{'Textures + target; protected crate unchanged':'Textures and target crate, with the other crate unchanged','Expected look + correct slot + protected scope':'Material on the intended component and slot','Reset; labeled walkthrough if blocked':'Reset or use the capture walkthrough','Give a goal, not a list of clicks.':'Describe the goal without coaching each click.'},
104:{'Owner: state the goal. Tester: attempt. Observer: record evidence and help.':'Rotate roles after each seven-minute round.','Each tool gets one observed attempt with two peer perspectives.':'Each tool gets one test with two peers.'},
105:{'Tester attempts; observer records':'Tester works while the observer records','Write a retest; reset and rotate':'Write the retest and rotate roles','Blocked? Label the fallback mode and continue.':'If blocked, continue with a labeled capture walkthrough.'},
106:{'Keep one strength a peer actually observed.':'Keep one demonstrated strength.','Prioritize one issue or uncertainty by its consequence.':'Pick the issue that most affects the task.','State the change or investigation you will try.':'Describe your fix or next investigation.','Specify the retest: input, action, expected result and protected scope.':'Write a retest with the same input and a clear expected result.','What changed or strengthened your original judgment?':'What feedback changed your mind?'}
}
credits_prefix=('Instructor captures from','Isaac Oster ·','UI/UX course connection','Left: Week 2','GOLF+ Course Generator ·','Same supplied GOLF+','Updated course PySide interface','Simon Verstraete / SideFX','Blender Foundation ·','Kathryn Whitenton & Sarah Gibbons /','Course rehearsal sequence','SideFX · Project Titan')
credits_exact={'cgerchenhp • click video to play','TAPython • click video to play','Epic Games • click video to play','Microsoft • click video to play','Ryan DowlingSoka • click video to play','Guerrilla Games • click video to play'}
# Final copy review: remove generic prompts and use concrete names.
copy[21]['Actual UE03 output']='Output Log'
copy[37]['Match the complete family and a declared suffix. Require one intended texture per role.']='Match the asset family exactly so _01 cannot match _010.'
copy[46]['Where does the code run?']=''
copy[60]={'Maya face technical-animation tool':'Maya facial animation tool'}
copy[69].update({'Start with the current workaround and prepared input.':'Start with one task: assign a material to a selected prop.','Include a blocked path and a way to recover.':'Make that task work, including errors and reset, before adding batch operations.','Split a large feature into a useful result the artist can try.':''})
copy[81].update({'Operation + affected count':'Action and affected objects','Concern + limits':'Warning details'})
copy[97].update({'Prepared engine fixture':'Unreal test scene','Live host integration':'Connection to Unreal','Is scope respected?':'Does it change the right objects?','Other projects + frame cost':'Other projects and performance'})
copy[100].update({'Whether the message supported recovery':'Did the message help the user recover?','Frequency across the whole user population':'How common the issue is'})
changes=[];moved=[];missing=[]
def paragraph_text(p):return ''.join(p.xpath('.//a:t/text()',namespaces=NS))
def write_paragraph(p,value):
 ts=p.findall('.//a:t',NS)
 if not ts:return
 ts[0].text=value
 for t in ts[1:]:t.text=''
 for br in p.findall('a:br',NS):p.remove(br)
def note_part(part):
 rp=posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')
 for rel in E.fromstring(d[rp]):
  if rel.get('Type','').endswith('/notesSlide'):
   return posixpath.normpath(posixpath.join(posixpath.dirname(part),rel.get('Target')))
def append_note(np,label,texts):
 x=E.fromstring(d[np]);body=next(sp.find('p:txBody',NS) for sp in x.findall('.//p:sp',NS) if sp.find('.//p:ph[@type="body"]',NS) is not None)
 for value in [label]+texts:
  p=E.SubElement(body,'{'+NS['a']+'}p');r=E.SubElement(p,'{'+NS['a']+'}r');E.SubElement(r,'{'+NS['a']+'}t').text=value
 d[np]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
for s in inv:
 n=s['number'];part=s['part'];x=E.fromstring(d[part]);before=' '.join(x.xpath('.//a:t/text()',namespaces=NS));replacements=dict(copy.get(n,{}));removed=[];source_credits=[]
 if n in titles:
  original_title={7:'VS Code: Python Autocomplete',8:'VS Code: Workspace Settings'}.get(n,s['title'])
  replacements[original_title]=titles[n]
 seen=set()
 for sp in list(x.findall('.//p:sp',NS)):
  ps=sp.findall('p:txBody/a:p',NS);full=' '.join(paragraph_text(p) for p in ps).strip()
  if full.startswith(credits_prefix) or full in credits_exact:
   source_credits.append(full);sp.getparent().remove(sp);continue
  for p in ps:
   old=paragraph_text(p)
   if old not in replacements:continue
   seen.add(old);value=replacements[old]
   if value:write_paragraph(p,value)
   else:removed.append(old);p.getparent().remove(p)
  # Empty text-only placeholders can display editing prompts in PowerPoint.
  if ps and not ''.join(sp.xpath('.//a:t/text()',namespaces=NS)).strip():sp.getparent().remove(sp)
 # Table cells also contain short explanations.
 for p in x.findall('.//a:tc/a:txBody/a:p',NS):
  old=paragraph_text(p)
  if old in replacements:seen.add(old);write_paragraph(p,replacements[old])
 missing.extend({'slide':n,'text':t} for t in set(replacements)-seen if replacements[t]!=t)
 if source_credits:
  append_note(note_part(part),'Visual sources',source_credits)
  moved.extend({'slide':n,'credit':t} for t in source_credits)
 if removed:append_note(note_part(part),'Additional teaching context',removed)
 after=' '.join(x.xpath('.//a:t/text()',namespaces=NS))
 if before!=after:changes.append({'slide':n,'before':before,'after':after,'before_words':len(before.split()),'after_words':len(after.split()),'source_credits_moved':source_credits})
 d[part]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
# Progress Bars uses an API table-like text block already in the source. Keep it compact.
part=inv[39]['part'];x=E.fromstring(d[part])
for sp in x.findall('.//p:sp',NS):
 full=''.join(sp.xpath('.//a:t/text()',namespaces=NS))
 if 'ScopedSlowTask(total, message)' in full:
  for p in sp.findall('.//a:p',NS):
   t=paragraph_text(p)
   value=t.replace('ScopedSlowTask(total, message)\nCreate the task with its total work count.','ScopedSlowTask(total, message)').replace('make_dialog(can_cancel=True)\nShow a progress bar with a Cancel button.','make_dialog(can_cancel=True)').replace('should_cancel()\nCheck inside the loop and break when requested.','should_cancel() → check for Cancel').replace('enter_progress_frame(1)\nAdvance progress by one unit.','enter_progress_frame(1) → advance progress')
   write_paragraph(p,value)
d[part]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
progress_change=next(c for c in changes if c['slide']==40)
progress_change['after']=' '.join(x.xpath('.//a:t/text()',namespaces=NS))
progress_change['after_words']=len(progress_change['after'].split())
# The progress explanation is for delivery, while source details stay in the notes.
np=note_part(part);nx=E.fromstring(d[np])
body=next(sp.find('p:txBody',NS) for sp in nx.findall('.//p:sp',NS) if sp.find('.//p:ph[@type="body"]',NS) is not None)
first=body.find('a:p',NS)
write_paragraph(first,'ScopedSlowTask displays progress for a batch operation. Set the total work, open the dialog, and advance the bar as items finish. If cancellation is enabled, check should_cancel inside the loop and stop before the next item. Cancel leaves completed edits in place. Use a transaction or another recovery step when those changes also need to be reversed.')
d[np]=E.tostring(nx,xml_declaration=True,encoding='UTF-8',standalone=True)
# Crop the slide 51 composite to the actual Unreal window. The original image
# stays embedded unchanged; version/date metadata belongs in speaker notes.
part=inv[50]['part'];x=E.fromstring(d[part])
pic=x.find('.//p:pic',NS);fill=pic.find('p:blipFill',NS)
crop=E.Element('{'+NS['a']+'}srcRect',l='5417',t='12903',r='5417',b='9247')
fill.insert(1,crop)
xf=pic.find('p:spPr/a:xfrm',NS);off=xf.find('a:off',NS);ext=xf.find('a:ext',NS)
old_height=int(ext.get('cy'));new_height=round(int(ext.get('cx'))*724/1284)
off.set('y',str(int(off.get('y'))+(old_height-new_height)//2));ext.set('cy',str(new_height))
d[part]=E.tostring(x,xml_declaration=True,encoding='UTF-8',standalone=True)
append_note(note_part(part),'Bridge capture context',['Actual UI rehearsal: Blender 5.1.1 and Unreal 5.7.4, 13 October 2026. Both blue placements update to 220 cm; orange Maya props stay 180 cm. The slide crops the surrounding caption and footer while preserving the original embedded image.'])
assert not missing,missing
with ZipFile(R/'build/candidate-v8.pptx','w',ZIP_DEFLATED) as z:
 for n,b in d.items():z.writestr(n,b)
report={'source':'build/source-v7.pptx','source_sha256':hashlib.sha256((R/'build/source-v7.pptx').read_bytes()).hexdigest(),'edits':changes,'credits_moved':moved,'hidden_unchanged':18,'slide_count':106}
(R/'qa/direct-copy-changes.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'slides_changed':len(changes),'credits_moved':len(moved),'words_before':sum(x['before_words'] for x in changes),'words_after':sum(x['after_words'] for x in changes)}))
