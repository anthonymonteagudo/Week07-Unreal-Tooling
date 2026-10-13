import {S,slides as old} from '../../TeachingDeck20261013/.build/content.mjs';
export {S};
export const hiddenChanges={
'02A':['S1','Fold the outcomes into the section opening.'],
'02B':['11','Production motivation is already demonstrated by contributor tools and the retained GDC cases.'],
'05':['S1','Carry the same-language/new-host explanation in the opening notes.'],
'06':['06A','Explain Actors, Components and shared assets on the existing relationship diagram.'],
'07A':['10','Explain source-file and Unreal destination paths during the handoff.'],
'10A':['10','Keep raw importer setup as reference; use the prepared handoff during class.'],
'09F':['09','State the stale-preview rule during the actual operation; backend implementation stays available.'],
'08':['08A','Use the architecture diagram for the brief Blueprint tie-in.'],
'09A':['09','Use the actual fixture during the demo; keep this capture as fallback.'],
'09B':['09','Verify the live result during the demo; keep this capture as fallback.'],
'14E':['14B','Discuss upstream and downstream workflow in the user-story example.'],
'14C':['14D','Teach sketching and Figma with the two-layout visual rather than two consecutive explanations.'],
'14A':['14F','Keep the production mental-model example live; menu findability becomes optional depth.'],
'16B':['16C','Introduce Mission Kontrol briefly on the QA iteration slide.'],
'16':['16E','Use the testing loop to distinguish observation, explanation and retest.']};
export const slots={
'01':[.5,'Opening','Welcome; name the editor-tooling and user-testing goals.'],
'02':[.5,'Opening','Show the route. No round-robin discussion here.'],
'S1':[.25,'Python','Same Python language, new host API.'],
'03':[2.75,'Python','Show the prepared editor. Plugin setup is a demonstration, not an installation workshop.'],
'04':[2,'Python','One log statement and its output. Allow one short clarification.'],
'06A':[3,'Python','Asset versus Actor versus Component. Include a 45-second scope prediction.'],
'07':[3,'Python','Inspect selected Actors. Reserve 45 seconds for questions about selection.'],
'10':[7,'Python demo','1 min handoff diagram and paths; 5 min prepared export/import and one revision; 1 min inspection/questions.'],
'09':[7,'Python demo','1 min recipe; 4 min inspect/preview/apply; 2 min verify affected and protected scope.'],
'08A':[2,'Python','One shared operation behind Qt or an Editor Utility Widget. No Blueprint construction.'],
'09D':[4,'Python','2 min Undo and result check; 2 min questions or demo recovery reserve. End this block at elapsed 32:00.'],
'11':[35,'Contributor demos','Co-teacher 15 min, TA 20 min. Questions, introductions and transitions are inside those slots.'],
'13':[15,'Break','Full break; resume at elapsed 82:00.'],
'S3':[.25,'Assessment','Orient groups to the sheet.'],
'12':[4.75,'Assessment','45 sec roles/instructions; 3 min individual prediction and group comparison; 1 min record trust judgment.'],
'12A':[3,'Assessment','Reveal and inspect for 1 min; discuss evidence for 1 min; record first priority for 1 min.'],
'S4':[.25,'UX','Transition from their assessment.'],
'14':[.75,'UX','Success count versus successful task. Revisit one initial judgment.'],
'14B':[1.5,'UX','Role, goal, benefit and observable success. Include before/after workflow.'],
'14D':[1.5,'UX','Compare two sketches; briefly identify paper/Figma as prototype methods.'],
'15':[1.5,'UX','Scope, preview and action grouping. One short student prediction.'],
'14F':[1.5,'UX','Artist-facing duration versus internal spawn/kill events. One production example.'],
'15A':[1,'UX','State and next action. Explain the unavailable Apply control.'],
'15G':[1,'UX','Point to enabled-state logic. No Qt syntax walkthrough.'],
'15D':[1,'UX','Ask for the next recovery action, then take one answer.'],
'15B':[1,'UX','Keyboard, focus, labels and recovery. One accessible name is only a starting point.'],
'16C':[1.5,'UX','Brief Mission Kontrol context; QA feedback changed adjacent controls.'],
'16E':[3.5,'UX','90 sec observation/hypothesis/retest example, then 2 min student questions or recovery reserve.'],
'16A':[4,'Task preparation','Protected writing time. Start by elapsed 106:00. Check goal, input, result and reset.'],
'S5':[.25,'Peer briefing','Introduce observer and participant roles.'],
'17':[1,'Peer briefing','Use author machine; observe before coaching; declare fallback mode.'],
'18':[1,'Peer briefing','Explain the reciprocal ten-minute round.'],
'19':[32.75,'Peer testing','45 sec assign A–D; round 1 at 113:00, switch 123:00–124:00, round 2 124:00–134:00, switch to 135:00, round 3 to 145:00.'],
'20':[5,'Synthesis','2 min compare evidence, 2 min choose one change and retest, 1 min record unresolved questions.']};
export const slides=old.map((s,i)=>{const d=structuredClone(s);d.oldIndex=i+2;if(hiddenChanges[d.id]){d.hidden=true;d.rationale='Hide from the normal slideshow. '+hiddenChanges[d.id][1]+' Live destination: '+hiddenChanges[d.id][0]+'.';d.facilitation='Optional reference only. Do not insert this as an additional explanation during the 150-minute route. '+d.facilitation;}return d;});
const m=new Map(slides.map(s=>[s.id,s]));
const add=(id,t)=>m.get(id).notes+=' '+t;
add('S1','The general Python language carries over from Maya. The host objects and API change. Keep asking what the tool affects and how the artist will verify it.');
add('06A','An Actor is a placement in the level. Its Static Mesh Component references the shared mesh asset and may carry an override. Moving one Actor differs from editing the shared asset.');
add('10','The disk file names the exported source, while /Game/Props names an Unreal destination folder. Watch one prepared revision and check that the intended asset updates. What questions do you have about this handoff?');
add('09','Apply recomputes the preview before editing. A stale or edited plan must be reviewed again. Predict the affected Actors, then inspect the result and one object that should remain unchanged.');
add('08A','An Editor Utility Widget can pass inputs to editor-only Python execution. That connection does not make Python a runtime gameplay language.');
add('14B','Include what the artist does before opening the tool and what they need to inspect afterwards. The tool window is one part of that workflow.');
add('14D','Sketch a starting state, a result and a failure. Paper or linked Figma frames can test interpretation and flow. A running Unreal tool is still needed to test the actual operation.');
add('16C','Mission Kontrol is NetherRealm’s Unreal-based developer tool for repeatable character actions. It uses Slate and game automation rather than our Python editor recipe.');
add('16E','For example, the tester chose the wrong destination. That is the observation. An unclear label is a possible explanation. Showing the full path is a proposed change, and a new tester’s attempt is the retest. What questions do you have before writing your own task?');
m.get('16E').question='What questions remain before you write the peer-test task?';
m.get('07').question='What questions do you have about selection and scope?';
m.get('09D').question='What questions remain about verification and recovery?';
let elapsed=0;export const timing=[];
for(const d of [{id:'01',title:'Review & specialization'},...slides]){if(d.hidden)continue;const slot=slots[d.id];if(!slot)throw Error('Missing time '+d.id);const row={id:d.id,title:d.title,minutes:slot[0],start:elapsed,end:elapsed+slot[0],block:slot[1],cue:slot[2]};timing.push(row);elapsed+=slot[0];if(d.id!=='01'){d.pacing=row;d.facilitation='TIME BUDGET: '+slot[0]+' min. Elapsed '+row.start+'–'+row.end+'. '+slot[2]+' '+(d.facilitation||'');}}
if(elapsed!==150)throw Error('Timing total '+elapsed);
