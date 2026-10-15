"""Editable slide-content manifest. IDs are v15 anchors, not new slide numbers."""
P=[]
def add(id,mantra,title,body,notes,visual,edit,why,sources=(),old=None):
    P.append(dict(id=str(id),mantra=mantra,title=title,body=body,notes=notes,visual=visual,edit=edit,rationale=why,sources=list(sources),old=old if old is not None else (id if isinstance(id,int) else None)))

add(39,'M1','Know the task',
 ['UI/UX for artist tools','What is the artist trying to accomplish?'],
 'Keep your first judgment from the batch-renamer exercise. We will revisit it through five practical reminders. First, know the task. A tool exists within a workflow: someone arrives with particular inputs, makes a decision, and needs a result they can trust. What did the renamer’s success message fail to tell us?',
 'Reuse v15’s purple UX section divider. Use the mantra as the main title, UI/UX as the subtitle; no new decorative theme.',
 'Replace the title and subtitle. Preserve the UX section color and the agenda’s block boundary. Move timing/editorial text to notes.',
 'Introduces the requested structure while recalling the investigation instead of restarting with definitions.',('tasks',))
add(40,'M1','Interface and experience',
 ['UI communicates the available decisions','UX includes reaching and checking the result','What must change, and what must remain unchanged?'],
 'The interface is what the artist sees and operates: labels, controls, layout and feedback. The experience includes preparing data, finding the tool, completing the operation, inspecting the result and recovering when necessary. A polished window can still fail the task. Which part of your own tool’s workflow happens before its window opens?',
 'Keep the existing simple text composition; pair one short phrase with a small current-tool crop if space permits.',
 'Keep the title and distinction. Replace the bullet block with concise task language. Preserve the protected-scope question.',
 'Preserves the current deck’s stronger workflow framing.',('tasks',))
add(41,'M1','A user story names an outcome',
 ['As an environment artist…','I want to preview a material assignment on selected props…','So I can compare a look without changing other placements.','Which assumption would you check with the artist?'],
 'This is a proposed classroom story, not a requirement we have validated with a production team. The role identifies whose work matters; the goal names an outcome; the benefit explains why it matters. Ask about the current workaround, frequency, inputs and consequence of failure. A request for a blue button chooses a solution before establishing the problem.',
 'Three editable text lines with role, goal and benefit visually aligned; the same target crate appears in the next example.',
 'Keep the original slide number and role/goal/benefit structure. Replace the importer example with the recurring material example; preserve the importer story in notes.',
 'Connects the abstract story to a visible task students can test.',('stories','mapping'))
add('41A','M1','Make success observable',
 ['Preview names the target, slot and mapping','Apply changes only the reviewed components','Changed input requires a fresh preview','What evidence would disprove success?'],
 'A story gives us direction; acceptance checks make the intended behavior inspectable. Given these textures and a target crate, creating a preview should show the mapping without changing the scene. If the selection changes afterward, the old plan must not apply. The protected crate gives us a visible check of scope. These are behavioral checks; they do not prescribe a particular widget.',
 'Use the actual material preview capture alongside a short editable acceptance-check list. Point to target and slot, not internal class names.',
 'Insert after 41. Keep the existing 41 note about acceptance checks, but teach the expanded example here.',
 'Gives user stories enough substance to guide implementation and testing.',('stories','tasks'))
add('41B','M1','Outline the whole task',
 ['Choose inputs → inspect scope → review → apply → check','Include the blocked path and recovery','Which small slice delivers a useful result?'],
 'Map the work from the artist’s perspective. A small useful slice takes someone all the way from prepared inputs to a checked result. Include the point where the tool can refuse an operation and what happens next. A story map helps us see missing steps; it is different from a list of backend functions. Where does your tool hand responsibility back to the artist?',
 'One editable sequence of short text labels, or a paper story-map capture prepared from this exact example. No generic dashboard.',
 'Insert after 41A. Keep the full story-writing guide in the companion notes.',
 'Makes the user-story discussion actionable while preventing a detour into project-management ceremony.',('mapping',))
add(46,'M1','Use the artist’s model',
 ['Implementation: spawn and kill events','Artist’s decision: VFX duration','Which details support the next decision?'],
 'The production example shows a mismatch between internal events and the way an artist reasons about an effect. An artist can think about its duration while the software handles separate events underneath. This is not a rule to hide all technical detail. Expose the detail when it helps the user decide. What implementation term in your own tool could be expressed more clearly?',
 'Keep the existing Jeff Stewart / Vicarious Visions visual and attribution. Retain the original source-page link.',
 'Move current 46 into the task subsection after 41B. Shorten the title; preserve the production example and its source.',
 'Uses an already strong game-production example instead of duplicating it with web examples.')
add(42,'M2','Guide the eye',
 ['Visual hierarchy supports the task','Where should the artist look first?'],
 'Now consider how the interface makes that task visible. We can use the same principles that organize an artwork: balance, rhythm, emphasis and relationships between shapes. The difference is that the artist must also act. The most prominent area should support the current decision, not merely decorate the tool.',
 'Reuse the existing layout/hierarchy divider. Keep the approved UX colors and type treatment.',
 'Replace divider title and subtitle. Preserve its section-transition role.',
 'Creates a clear art-to-interface bridge.',('principles',))
add('42A','M2','Art principles become interface decisions',
 ['Balance: distribute visual weight','Rhythm and alignment: establish a pattern','Proximity: show what belongs together','What carries over from composing a game scene?'],
 'In a composition, you arrange weight, repetition and emphasis so the viewer can read what matters. In a tool, repeated field spacing and aligned labels help establish a pattern, while larger gaps separate decisions. Balance does not require symmetry. The course lenses still apply: constraints shape the design, systems connect the parts, a repeated improvement offers leverage, and the workflow affects throughput.',
 'Use a verified Week 1 lens reference and one current tool image. Keep art analogy labels editable; do not claim every term was on a specific Week 1 slide.',
 'Insert after 42. Preserve Week 1 lens meanings and palette; no fifth lens.',
 'Connects to earlier course learning without inventing a historical slide attribution.',('art','principles'))
add(44,'M2','Layout follows the task',
 ['Inputs belong together','The preview explains scope and consequences','Which information belongs beside the action?'],
 'Look at the material tool as one task. First identify the inputs, then the target and proposed changes, then the available action. The preview should help you decide whether to apply. A heading or colored area does not compensate for missing scope. Before I point anything out, where would you look to confirm which crate and material slot will change?',
 'Replace the narrow old crop with a legible current capture, then use a second close crop only for the target/slot detail. Matched sample state required.',
 'Keep title and task question. Replace stale screenshot after the UI alignment pass and retain practice-mode provenance in notes.',
 'Keeps the lecture accountable to the actual demo.')
add(45,'M2','Group related decisions',
 ['Repeat the spacing inside a group','Use larger gaps between different decisions','Keep labels with their fields','Which grouping do you perceive first?'],
 'Rhythm comes from a pattern we can recognize. Proximity tells us which things are related. Neither requires a border around every group. Compare the gaps inside the input area with the gaps around the preview and actions. A consistent visual treatment should mean something consistent. What would you move closer, and what would you separate?',
 'Keep the existing NN/g comparison as a brief reference; make the current tool the main application. Add the source lesson 18 alignment capture in the review, not a replacement theme.',
 'Keep current 45 anchor. Expand the wording to include rhythm and alignment; retain the existing source attribution.',
 'Consolidates related concepts rather than giving each a disconnected definition.',('principles',))
add('45A','M2','Value makes the light and dark structure visible',
 ['Value: lightness and darkness in art','Contrast: a difference between elements','HSV Value is not perceived lightness','What survives when the hues disappear?'],
 'In art, value is how light or dark something appears. Contrast describes a difference, and value is one way to create it. Hue, size and shape can also create contrast. A software HSV Value field is not a measurement of perceived lightness. Two vivid colors may still have similar lightness, which is why a colorful interface can become hard to read in grayscale.',
 'Use the original and grayscale view of the SAME current-tool capture in the diagnostic review. For final slides, export a clearly labeled diagnostic copy through the approved visual workflow.',
 'Insert after 45. Move the brief HSV definition from current 55 into the qualified discussion here; preserve 55’s rendering-context connection.',
 'Corrects an ambiguity in v15 and adds the requested art concept.',('art','contrast'))
add(54,'M2','Color reinforces meaning',
 ['Keep color roles consistent','Pair status with labels or shape','Check the actual foreground and background','Could you still identify the warning without hue?'],
 'Color can support identity and state, but it should not carry the entire message. A warning needs words that name the issue; focus and selection also need distinguishable cues. Palette tools such as Coolors can help explore combinations. Assign the roles first, then check the colors in context. A palette that looks good together can still produce unreadable text.',
 'Keep the Adobe Spectrum comparison and attribution. Add Coolors as a small Explore further link, not a product-tour slide.',
 'Move current 54 into M2. Preserve the source visual, revise the title, and add the tool pointer in notes.',
 'Adds practical exploration without replacing accessibility checks with palette selection.',('color','coolors','coolors-contrast'))
add(55,'M2','Color changes with context',
 ['UI: inspect text, state and surface contrast','Game art: inspect lighting, exposure and background','Would identical RGB values look identical?'],
 'The same numeric color can appear different depending on its surroundings and rendering pipeline. For interface work, inspect the actual foreground and surface. For materials and VFX, also consider color space, lighting and exposure. Today we are using this as a connection to the next block, not treating a color-picker setting as proof that the result will be readable.',
 'Keep the historical Epic color-picker control, source label and game-art connection. The value distinction is now explicit on 45A.',
 'Keep title purpose and visual. Replace the bullet defining Value as if it were the art concept. Preserve the later-rendering bridge.',
 'Retains existing useful coverage while resolving terminology.')
add('45B','M2','Block out, grayscale, squint',
 ['Shapes reveal layout','Grayscale reveals value relationships','Squinting reveals dominant masses','Restore detail and test the real interface'],
 'Try three quick diagnostic views of the same tool. Reduce it to shapes to inspect grouping. Remove hue to inspect its light and dark structure. Briefly squint or step back to see which masses dominate. A blurred preview approximates that last exercise. None of these proves accessibility or correct behavior. Restore the original, read the labels, measure contrast, and try the task.',
 'Use the included interactive diagnostic view for the current capture. The blockout example comes from the source lesson capture; it is not falsely labeled as a generated analysis of our tool.',
 'Insert after 55. Keep all three checks together and label their limits on the slide itself.',
 'Adds the requested practical art method without overstating what it establishes.',('contrast',))
add('45C','M2','Show the data needed for a decision',
 ['Name the affected item','Compare before and proposed result','Distinguish skipped, blocked and untested','What can this summary prove?'],
 'The preview table is a decision aid. It needs enough identity and context to let the artist recognize the affected objects. A summary count can help, but it must not hide which items were skipped or blocked. Zero changes, a failed operation and an untested state are different. Remove decoration when it competes with the data, but keep the labels and units needed to interpret it.',
 'Use the tool’s before/after table. Optional production comparison: attached talk pp.35–37 asset overview. Show a table for exact lookup; do not manufacture measured charts.',
 'Insert after the diagnostic checks. Tie the new data lessons directly to the renamer and material preview.',
 'Distills lessons 43–46 into a game-tool decision rather than a chart-design survey.')
add('46B','M3','Make actions clear',
 ['Information, controls and state need distinct cues','Can you predict what happens before clicking?'],
 'A clean interface is still confusing if a heading looks like a button or if a status color looks like a command. Our next question is what the user thinks they can do. Watch how the available action changes with the tool state, and check whether the interface tells the same story as the operation underneath.',
 'Use the existing transition layout. Keep this a short divider, not a checklist.',
 'Insert before current 47; current 47’s feedback content remains a separate slide.',
 'Establishes a distinct subsection for interaction rather than mixing it into visual polish.')
add(47,'M3','State determines the next action',
 ['Choose inputs: Preview','Valid reviewed plan: Apply','Completed: inspect the result','What becomes unavailable after Apply?'],
 'At the start, Preview is the useful next action, so that is where the refined tool puts its emphasis. A valid plan makes Apply available. An unreviewed warning keeps attention on the review. After applying, inspect the changed target and the protected scope; the completion message alone is not enough. What happens to the plan when we change an input?',
 'Use matched before/after state captures from the updated PySide tool. Include the action row and the status, not just a decorative button close-up.',
 'Keep the state/feedback topic and anchor. Replace stale captures and narration with the current action-emphasis behavior.',
 'Makes the demo embody the lecture’s central hierarchy claim.')
add(48,'M3','A UI decision becomes code',
 ['A layout associates labels and fields','Input changes invalidate the preview','Enabled state reflects readiness','The backend rechecks before changing anything'],
 'Here are two small implementation decisions behind the behavior you just saw. A layout manager keeps labels and fields associated as the panel resizes. Input-change signals invalidate the old plan. The interface reflects readiness, but the session validates again when Apply runs. Styling an enabled button is not the same as making an operation safe. What should happen if the selection changes outside the window?',
 'Use code copied from current assistants.py: signal-to-invalidate and update_apply. Label excerpts with the required widget/session context. Pair with the exact state capture.',
 'Keep this slide and its technical purpose. Refresh the code excerpt from the changed source; do not paste an outdated version from v15.',
 'Grounds the principles with a bounded implementation example.',('qt',))
add('48A','M3','The same task across toolkits',
 ['PySide: Python widgets and layouts','Editor Utility Widget: UMG and Blueprint','Current native panel: C++ Slate','Which behavior should stay consistent?'],
 'These are different ways to present an editor workflow. The existing native panel uses Slate; it is not the PySide window docked inside Unreal. An Editor Utility Widget is another option using UMG and Blueprint. The important shared contract is the task: inputs, preview, guarded apply and inspectable results. Each host still needs its own keyboard, sizing and recovery checks.',
 'Use actual PySide and native captures from the same task where available. Keep the EUW example labeled as an implementation option, not an already-built course asset.',
 'Insert after 48. Keep detailed implementation as linked study, not a second toolkit workshop.',
 'Answers the request for in-engine grounding accurately.',('euw','qt'))
add(49,'M3','An error should support recovery',
 ['Name the problem and affected input','Give a useful next action','Keep diagnostics available','Could a peer continue without reading the code?'],
 'Read this message as someone who did not build the tool. What went wrong, what does it affect, and what can you do next? The programmer may need a detailed diagnostic record, but the artist needs a route forward. A stopped operation is not automatically proof that nothing changed; the message must match the actual behavior.',
 'Use an actual blocked-state capture; keep the bridge’s Copy diagnostics as a separate concrete example when discussed.',
 'Keep the topic and question. Replace the stale blocked crop only after reproducing the corresponding state.',
 'Retains the existing strength in error and recovery teaching.')
add(50,'M3','An actionable error message',
 ['Problem','Relevant cause','Next action','What would you change in your own message?'],
 'This older Windows example is useful because it separates the problem, the reason and the next action. We do not need to copy its visual style into our tool. Apply the communication structure to an asset name collision or a missing texture. Which part of the message would let an artist recover independently?',
 'Keep the existing Microsoft historical screenshot and attribution.',
 'Keep title, screenshot and source. Use as a quick comparison after 49; preserve it as prepared material rather than silently removing it for time.',
 'Uses a familiar non-game example for a directly transferable behavior.')
add(51,'M3','Recovery and accessibility',
 ['Visible focus and readable labels','Meaning beyond color','A tested recovery path','Can a classmate finish without a mouse?'],
 'Try the task with the keyboard and keep track of focus. Read every label at the supported size and check that state does not depend on hue alone. Then test the recovery we actually offer. Undo for a property edit is different from restoring a generated file or reimporting an asset. One accessible name or one contrast calculation is only a starting point.',
 'Replace the single accessible-name code block with a current focus-state crop. Keep the code fragment in notes as one implementation example.',
 'Keep current title and recovery distinction. Strengthen the visible test rather than implying one Qt property proves accessibility.',
 'Maintains behavior-based evaluation alongside visual checks.',('contrast','color'))
add(52,'M3','Visible commands and shortcuts',
 ['Visible commands help people learn','Shortcuts support repeated work','Host shortcuts and focus still matter','What should this key affect?'],
 'Your command should be discoverable before someone memorizes its shortcut. Shortcuts also share space with the host editor. In the GOLF+ notes, modifier handling interfered with viewport and selection commands. That feedback concerns the whole workflow, even when the tool window looks fine. Test shortcuts with the correct focus and selection context.',
 'Keep the Microsoft reference, then link the GOLF+ feedback/capture as an instructor example. Do not show personal conversation metadata.',
 'Keep title and existing source. Add the concrete GOLF+ host-interaction case to narration.',
 'Brings a real game-tool failure mode into the general principle.')
add('52A','M3','GOLF+ overlay: a tool in the artist’s workspace',
 ['Commands remain close to the work','Compact icons need discoverable meaning','The surrounding editor is part of the test','What would a first-time user need explained?'],
 'This is an existing annotated capture from my course-overlay work. It shows how close the controls sit to the scene, but compactness also creates a discoverability question. The notes ask for clearer access and record shortcut conflicts. Treat this as process evidence: a design can be useful and still need targeted refinement. This capture is not a measured before-and-after result.',
 'Use assets/golf-overlay.png at its native aspect ratio, with its August capture date in instructor notes. A new full overlay walkthrough is a preparation item.',
 'Insert after 52. Keep existing annotation visible and label it as an instructor source capture.',
 'Uses the instructor’s own tools and process without inventing performance gains.')
add(53,'M4','Keep a shared visual language',
 ['Record the rules so the next tool stays coherent','Who decides when a pattern should change?'],
 'A consistent tool suite needs more than someone remembering the right shade of blue. Record the visual and interaction decisions, reuse them, and decide how they change. This matters when several developers or AI agents work on different parts of the same system.',
 'Reuse the current color-section divider layout with the new mantra title. Color content remains live under M2.',
 'Replace divider title and subtitle; move the existing color teaching slides into M2 rather than deleting them.',
 'Creates space for the requested style-sheet and AI-workflow material.')
add('53A','M4','A style sheet records decisions',
 ['Type, spacing, color roles and icons','Control states and wording','Examples, exceptions and ownership','A stylesheet file implements only part of this'],
 'A style sheet is the team’s maintained reference for how the interface communicates. It should say what a color means, how controls behave, and why a pattern exists. Tokens give recurring decisions names; components apply those decisions repeatedly. Larger teams commonly use shared systems to coordinate work, though no universal rule says every organization does it well or uses the same format.',
 'Show the included Week 7 style-sheet excerpt beside its actual action states. Keep specification and QSS clearly distinguished.',
 'Insert after 53. Use a concrete rule instead of a wall of brand tokens.',
 'Explains what the document does and why it matters at scale.',('system',))
add('53B','M4','Use the style sheet with AI',
 ['Provide the current rules and examples','Reuse tokens and existing components','Compare matching states before and after','How would you detect design drift?'],
 'In my workflow, I keep the agreed design decisions in a style-sheet skill and require the agents working on the interface to refer to it. That makes the reference reusable; it does not make the output automatically correct. I still compare screenshots, test behavior and record deliberate exceptions. If I decide to change the design, I update the shared rules so the next pass does not restore an old decision.',
 'Show a short excerpt from the local teaching skill and the corresponding before/after PySide captures. Label the instructor workflow as personal practice.',
 'Insert after 53A. Keep tool/platform specifics in notes; focus the slide on the process.',
 'Uses the requested personal AI example while retaining a real verification step.')
add('53C','M4','GOLF+ design rules in practice',
 ['A repeated workflow across tools','Shared color and icon meanings','Feedback becomes a maintained rule','Which rule needs an explicit exception?'],
 'The GOLF+ UI Quality Playbook turns feedback into reusable rules: a short main workflow, consistent terminology, shared visual roles and screenshot review. It also records decisions still being consolidated. Notice that its full-width primary buttons are a sensible counterexample to treating a web-course example as a universal prohibition. The goal is a coherent working system for these artists.',
 'Use the local playbook as readable excerpt and the GUI feedback capture as process evidence. Do not imply an August image is the current October build.',
 'Insert after 53B. Keep GOLF+ brand choices separate from the course tool’s palette.',
 'Demonstrates contextual judgment and the maintenance process with the instructor’s work.')
add(56,'M5','Test the whole workflow',
 ['Choose a question the prototype can answer','Observe the attempt and inspect the result','What remains untested?'],
 'Our last reminder is to test the whole workflow. A sketch can answer whether people understand the sequence. A running tool can answer whether the intended asset changed. A production workflow also includes setup, finding the tool, recovery and maintenance. Choose the evidence that fits the question.',
 'Keep the existing testing divider composition.',
 'Replace title/subtitle while preserving the section boundary.',
 'Connects the design principles to the existing peer-test method.',('tasks','figma'))
add(43,'M5','Prototype the question',
 ['Paper or Figma: interpretation and flow','Running tool: behavior and host integration','Prepare start, preview, blocked and complete states','Which uncertainty can this prototype resolve?'],
 'These two sketches describe the same task. Before building the operation, ask a peer to explain what they would do and what they expect to happen. Paper or connected Figma frames can test that interpretation. They cannot verify actual imports, stale selection, undo or latency. When those are the uncertainty, use the running tool. What would you test before spending time polishing the final screen?',
 'Keep both existing sketches and their illustrative label. Add a four-state storyboard reference in the companion; a linked Figma prototype is not claimed to exist.',
 'Move current 43 into M5. Keep the visual comparison; expand the caption and narration to identify Figma and fidelity limits.',
 'Makes prototyping explicit without requiring students to learn another application.',('figma','tasks'))
add(57,'M5','Feedback changes the interface',
 ['Observe a real task','Separate a finding from an explanation','What did the original feature list miss?'],
 'This production example reminds us that a feature list does not predict every usability problem. Record what the person actually did and the help they needed. Then propose an explanation. Keep the observation separate from your guess about its cause, and choose a change that can be retested.',
 'Keep the existing NetherRealm / Mission Kontrol source image and attribution.',
 'Keep title, visual and source; connect the narration to the GOLF+ feedback process and the next lab.',
 'Preserves an existing game-production connection.')
add(58,'M5','A test produces the next question',
 ['Record expected and observed behavior','Choose one change','Repeat the task and compare','What questions remain?'],
 'A useful finding describes the starting situation, the action and what you observed. “Confusing” is a reaction; “I expected this row to change, but an unselected object changed too” is evidence you can investigate. Choose one revision and repeat a comparable task. What would you need to see before calling the revision successful?',
 'Keep the existing testing-loop visual and its distinction between observation and explanation.',
 'Keep the current title, diagram and audience question. Avoid adding a second generic design-process diagram.',
 'Links the new visual principles back to the established evidence standard.',('tasks',))
add(59,'M5','Telemetry and observation',
 ['Events show recorded outcomes','Observation shows hesitation and workarounds','Low usage has more than one explanation','What would you investigate next?'],
 'An event log can show that an operation finished or was blocked. Observation can reveal hesitation, misunderstanding or a workaround. Neither alone tells the entire story. Low Apply use might mean confusion, a deliberate cancellation or little need for the task. Inspect the actual result and ask about context before redesigning the interface.',
 'Keep current concise text or one existing event example; do not invent a chart of collected behavior.',
 'Keep the telemetry topic and uncertainty. Preserve its current status as an illustrative plan.',
 'Prevents stronger visual-design language from weakening the measurement caveats.')
add(60,'M5','A small event plan',
 ['Preview finished: target count and elapsed time','Apply blocked: reason','Apply finished: reported outcome and changes','Recovery used: which route'],
 'These are proposed events, not measurements collected from our class. Choose fields that answer a concrete question about the workflow. Keep actual task success separate from the event name. An apply-finished event may tell us the operation returned, but we still need to inspect what it changed.',
 'Keep the existing editable event table and its explicit illustrative label.',
 'Keep current table/source and example status. Retain in the comprehensive sequence; do not add telemetry implementation to this preparation task.',
 'Preserves useful existing content and limits the scope of demo changes.')
add('60A','M5','Production case: less manual handling',
 ['A small team needs repeatable asset ingestion','The interface exposes a bounded batch','Review remains part of the workflow','What would you verify after import?'],
 'Marcus White’s Unit 2 Games talk presents a small-team ingestion workflow and a compact batch-import interface. The useful connection is how automation removes repeated setup while leaving a recognizable artist task. Treat the talk’s no-error language as an aspiration, not a guarantee. Its Python setup is from an older Unreal ecosystem; this is workflow evidence, not current setup code.',
 'Use attached PDF p.26 for the interface, p.33 for the workflow, or pp.35–37 for the asset overview. Prefer one clear page per teaching use.',
 'Insert before peer preparation as a prepared production example, or cross-reference it from 45C. Retain clear source-page attribution.',
 'Uses the attached material to connect the section to game production without importing obsolete APIs.')
add(62,'M5','Prepare a task a peer can attempt',
 ['Goal and prepared inputs','Visible success and protected scope','Reset or declared fallback','Can a peer attempt it without a click script?'],
 'Use your story to prepare the task, but give the reviewer a goal rather than a sequence of button presses. State the starting inputs, what should change and what must remain unchanged. Decide how you will reset the task between reviewers. If execution is unavailable, label the review as recorded or conceptual so the evidence is interpreted accurately.',
 'Keep the current preparation sheet and the existing four-minute block. Add the material story as a worked example in the companion only.',
 'Keep current slide and task-preparation timing. Strengthen the connection to story/criteria; add no new grading or submission requirements.',
 'Makes the richer lecture directly useful to the existing lab.',('tasks',))

from slide_explanations import apply_revision
apply_revision(P)
ORDER=[p['id'] for p in P]
