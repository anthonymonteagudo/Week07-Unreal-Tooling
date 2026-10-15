"""Replace inherited prep scaffolding with slide-specific classroom narration."""
from pathlib import Path
import json,re
OUT=Path(__file__).resolve().parent
inv=json.loads((OUT/'source-inventory.json').read_text(encoding='utf-8'))
custom={
1:'Today we will connect Python to an artist’s task. We will read state in Unreal, inspect what an operation would affect, and use that evidence to judge a tool. Later you will test one another’s work and choose a revision you can verify.',
2:'We will begin with Unreal setup and small API examples, then connect those ideas to working tools and our colleagues’ demonstrations. After the break, we will investigate a small tool and use five UX mantras to review our own work. The final thirty minutes are reserved for peer review, reflection and a concrete retest.',
3:'Before we write an operation, establish where the code runs. Unreal supplies the editor objects. Our IDE helps us write the script; the running editor provides the state it reads.',
5:'Run this check inside Unreal. Confirm the engine version and the project directory before continuing. A successful import in the wrong project does not establish that the prepared assets are available.',
9:'We will move from selection to object ownership, then to texture inspection and validation. Keep asking which object we have and what evidence a call returns.',
19:'This setup reads the selected Actors, just as UE02 did. The complete UE03 file then visits Static Mesh Components and reads their mesh references. Use that complete file for a fresh run. A camera can be an Actor without having the mesh component we are looking for.',
42:'Where does the code run? Which object owns the state we change? What proves success, and what would recovery restore? What would you like clarified before we compare Blender’s API with Unreal’s?',
43:'The Python language stays familiar, but Blender supplies different objects and operations through bpy. We will inspect its selection and follow a small geometry revision into Unreal.',
48:'Now follow a complete artist task. Identify the input, the proposed change and the visible result. Our Material and VFX examples will keep the same preview-and-check pattern even though they edit different things.',
49:'Use the prepared classroom map. Preflight checks the Material and VFX fixture and stages the expected selection. Confirm the target and textures before opening the tool. This check does not certify the separate Blender or Maya bridge.',
50:'This material-editing capture gives us a concrete parameter and a visible preview. Which decision belongs to the artist, and which repeated assignment could the tool handle? The classroom assistant uses prepared texture parameters; it does not build a new material graph.',
51:'Read the proposed texture mappings and component assignment before applying. Then compare the target crate with its protected neighbor. The target changes; the shared mesh and the neighbor should remain unchanged. These are two separate captures from the recorded Unreal rehearsal. What would you inspect to verify the boundary?',
52:'Count the proposed markers and inspect their transforms. The recorded result contains three effects. Repeating the same placement is blocked. A count safeguard does not measure frame time: we still need to inspect the visual result and measure performance separately.',
56:'As Zoey demonstrates the face technical-animation tool, identify the artist’s goal, the controls that express it and the evidence of a completed operation. Save one observation and one question for the discussion.',
57:'As Xicheng demonstrates the Maya bridge and pipeline tool, follow the handoff. What is sent, where does it arrive, and how does the artist know it is the intended revision? What would you like to ask about that boundary?',
58:'We will take fifteen minutes. When we return, we will investigate a tool’s behavior before discussing how its interface could improve.',
59:'First, make your own prediction about a small renaming tool. After the reveal, we will use five UX mantras to explain what supports the task and what needs another test. Keep your first judgment so you can revisit it.',
75:'Prepare one bounded task that a peer can attempt. We will rotate owner, tester and observer, then apply the same lens to our own tools. A useful result is an observation and a revision with a specific retest.',
}
boiler='Both placements reference one mesh. Changing the shared mesh affects its uses. Our material demo changes only one actor component’s override. Point to the scope you would choose to preserve Actor B. What questions do you have about assets and placements?'
custom.update({
18:'The selected crate appears in the scene and the Outliner. The captured Output Log reports one Actor, its label and its class. Change the Outliner selection and predict the next count before running again. The Content Browser can remain unchanged because it is a separate selection.',
21:'Follow the relationship: the selected Actor owns a Static Mesh Component, and that component refers to the engine Cube asset. The label, component name and mesh path identify three different objects. The recorded UE03 result reads those relationships without editing them. Which of these would you change to affect one placement?',
22:'Both placements reference one mesh. A shared-mesh change can affect its uses; a component material override changes the appearance of that placement. Watch the cube whose material changes and compare its neighbors. Where should our operation act if the other placements must stay unchanged?',
24:'This complete example reads Content Browser selection. It prints each loaded asset’s name, class and object path. Select a texture and a mesh, then predict their class names. Which selection will supply textures to the material assistant?',
27:'This Karol course capture shows a normal-map image with Masks compression. Compare the visible setting with the prepared Normalmap requirement. The suffix and image are clues; inspect the actual property before reporting a mismatch. What should the validator tell the artist to inspect next?',
29:'The example keeps Texture2D objects, counts skipped selections and reads compression and sRGB. Select a normal map, then a base-color texture. Predict which values differ. We are inspecting shared texture assets, so this script makes no repairs or saves.',
31:'The captured T_Crate_Normal selection produced one Texture2D, its object path, Normalmap compression and sRGB False. Compare the output with the texture’s controls. The selection and log are separate crops from the recorded run. How would a mixed texture-and-mesh selection change the counts?',
32:'The shown loop is an excerpt. The complete UE06 file initializes the selected textures, expected compression and counters, then prints the totals. A name ending in _Normal makes a texture eligible for this rule. Zero checked textures is inconclusive. Why would a success-looking empty report be misleading?',
35:'A disk path identifies a location in the filesystem. An Unreal object path identifies an engine object. Loading the Cube asset does not place a cube in the level. Which path would pathlib inspect, and which would unreal.load_asset use?',
37:'This open-source script editor brings files, temporary scripts and familiar editing controls together. An artist tool may need a simpler entry point for one repeated task. A Qt window is also different from a native Slate tab. Which part of your own workflow needs to be saved and repeatable?',
41:'AYON separates loading, publishing and scene inventory within a larger production pipeline. Follow the input, the handoff and the result. You do not need to recreate the platform to apply that idea: what does your tool receive, and who uses its output?',
53:'The Project Titan ivy tool divides generation into artist-controllable shape, branch growth and leaf placement. It is a Houdini digital asset used in Unreal. Compared with our fixed VFX placements, this example constructs organic content. Which choices should remain exposed for art direction? Name one repetitive art task and three controls that would support it.',
54:'The Project Titan train tool connects modular construction with automatic rig creation. Its screenshot shows the rigged result and part of the Houdini network. Identify the handoff from modeling to animation. Which relationship would you inspect before trusting the next stage? A useful student tool could automate one small part of that transition.',
55:'Follow the environment from blockout to a finished production-tech-demo scene. Repeated structures and procedural tools support it, while composition, lighting and other art choices remain deliberate. The clip does not show a single tool generating the whole level. Which decisions would you preserve for the artist?',
61:'The artist wants to preview a material on a selected prop. The implementation finds Actors, inspects components and assigns a material. The interface should represent the task through target, material choice, preview and commit. It should not require the artist to reconstruct every implementation step. What would the artist expect this control to do?',
62:'Find the inputs, scope, preview and primary action in this practice interface. Spacing and alignment imply which decisions belong together. Simplifying the layout must preserve necessary feedback. Which controls belong to the same step, and which should be separated?',
63:'Compare Blender’s before and after examples. Find Affect Only, then identify which labels belong to it. The revised grouping and alignment make those relationships more explicit. These shipped design changes do not by themselves establish a measured speed gain. Which cluster in your tool would you test with the same question?',
64:'Recall how composition guided attention in our earlier art discussion. The scene guides a player through space; the tool guides an artist through decisions. These are separate examples, not a matched before and after. Where do you look first, and how quickly can you find the affected target and the next action?',
65:'The game image uses a restricted palette and strong red emphasis. In a tool, color also needs a stable operational meaning. Pair a warning hue with text or another cue, and distinguish selected, available and completed states. What would remain understandable if you removed the hue?',
66:'NN/g’s redesign used repeated testing to compare alternatives, including a grid and a list. Reported preference for one version does not make lists universally better. Transfer the method to an artist task: use comparable inputs, observe the attempt, then ask about preference. What evidence would make you revise your preferred layout?',
67:'Assess the whole task. Before acting, can the artist identify scope? During the operation, can they tell whether it is working or blocked? Afterward, can they inspect the result and recover? Include keyboard use and repeated entry. A tidy first screen is only one part of the experience.',
68:'PowerRename shows original and proposed Windows filenames before Apply. Transfer the preview pattern to asset names, affected scope and conflicts. For Unreal assets, use engine-aware operations; this is not an instruction to rename uasset files in Explorer. What information would you need before trusting a batch change?',
69:'The controls on the left filter which material parameters appear. Follow the relationship between the two areas. Would a first-time user recognize the active filter and understand why a parameter disappeared? Grouping is useful only when its meaning remains clear.',
70:'A click is an input, and the counter gives immediate evidence that something happened. Name the corresponding visible state in your tool. What should appear while a longer action is running, and what should appear when it is blocked?',
71:'These two captures use sample data. The warning asks for review and acknowledgment; the blocker requires an input correction. Acknowledgment cannot make an invalid operation valid. What can the artist do next in each state?',
72:'Compare the baseline, applied material and recovered assignment. In the recorded rehearsal, Undo restored the component assignment while the newly created material asset remained. Recovery has a specific scope. What should the interface promise, and what would you inspect afterward?',
74:'This is hypothetical feedback. Separate what the tester observed from the possible explanation and the proposed change. The revision is a hypothesis to test. Compare the example with “I do not like the layout.” Which one gives the owner a concrete next experiment?',
})
case_numbers={10,20,37,41,50,51,52,53,54,55,63,66,68,69,70,73}
result={}
for s in inv['slides']:
 n=s['number']; raw=s['notes'].replace('\r\n','\n').replace('\r','\n')
 urls=list(dict.fromkeys(re.findall(r'https?://[^\s|]+',raw)))
 if n in case_numbers:raw=raw.replace(boiler,'')
 # Keep provenance separately; remove inherited notes-page numbers and editorial metadata.
 lines=raw.splitlines();clean=[];skip_next=False;skip_block=False
 for line in lines:
  st=line.strip()
  if st in ('PACING','TRANSITION','RETURN CUE','BRIDGE TO THE LAB','CASE STUDY DISCUSSION'):
   if st=='PACING':skip_next=True
   continue
  if skip_next:skip_next=False;continue
  if not st or st.isdigit():continue
  if st.startswith(('Source insight','Facilitation','Sources:','Source:','Visual:','Review anchor:','Placement rationale:','Credit:','Original capture:','Source lesson:','Playback:','Context:','Discussion:')):
   break
  if st.startswith(('https://','http://','C:/','C:\\','Course/','Week07UnrealPython/')):continue
  if skip_block:continue
  clean.append(st)
 narration=' '.join(clean)
 if n in custom:narration=custom[n]
 # Case clips had unrelated notes inherited from the shared-asset slide.
 if n in {10,20,47,73}:
  # Keep the final authored clip-specific paragraph when present.
  starts={10:'Before we discuss individual API calls',20:'Watch',47:'This is our rehearsal sequence',68:'Look',69:'Look',70:'Watch',73:'Track where information appears'}
  marker=starts[n]
  if marker in raw:
   tail=raw[raw.index(marker):].split('Discussion:')[0].strip()
   narration=tail+' '+({10:'What input is driving the visible change?',47:'What changed after republish, and what stayed independent?',73:'How much spatial context can the artist keep while inspecting a region?'}.get(n,'What visible cue would help a new user understand this action?'))
 if not narration:narration='Identify the task, the affected objects and the evidence shown. What would you need to inspect next?'
 result[str(n)]={'narration':narration,'sources':urls,'original_notes':s['notes']}
result['2']['facilitation']='3:30–3:35 introduction; 3:35–3:50 setup; 3:50–4:10 API examples; 4:10–4:40 reliability, bridge and instructor demos; 4:40–4:55 colleagues; 4:55–5:10 break; 5:10–5:18 Lab 1; 5:18–5:30 UX mantras; 5:30–6:00 peer review. Protect the activity times. Use the named custom show and the linked route guide.'
result['59']['facilitation']='Eight-minute investigation first; twelve-minute mantra route follows. Prediction before reveal. Do not expose the instructor answer page to students in advance.'
(OUT/'source-notes.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Prepared slide-specific narration and separated provenance for 76 source slides.')
