# Karol integration — copyable teaching proposals

13 October 2026. Review only: the deck and demo code have not been edited. See the adjacent HTML review for current slide images, original wording, detailed feature acceptance criteria and all 44 note comparisons.

## Recommended direction

Use existing validation, scope inspection and Undo behavior more explicitly. The best new feature is a read-only texture validation report that shows every relevant mismatch while leaving shared assets unchanged. Reuse the same backend results in PySide and the native Slate panel.

## Keep the current schedule

Opening/Python 32 minutes; contributors 35; break 15; Lab 1 eight; UX concepts 16; task preparation four; peer-test briefing/rotations 35; synthesis five. Total: 150 minutes.

## Note audit result

44 notes reviewed; 26 updated; 585 image embeds preserved. The notes are now 75.1% shorter than the original text instead of 80.3%. Original notes are unchanged. Examples were syntax-checked, not executed in Unreal. A ZIP of the previous refined notes is included in history/.

## Slide 7 / 03 — Explain the editor host, then show its execution control

Route: live. Karol lessons: 1, 2, 6, 7.

### Field-level edits

Keep the title and plugin screenshot. Add a one-line host reminder beneath the existing setup instruction. Keep the visible question; do not turn this into a package-installation exercise.

### Proposed slide copy

Run editor scripts inside Unreal.
IDE autocomplete describes the API; it does not provide a running editor.
Is this input field running Python or console commands?

### Read-aloud narration

The language is still Python, but Unreal supplies the objects and editor functions. Our IDE can describe that API without running the editor. Before I execute anything, check this input field: is it in Python mode or console-command mode? What is unclear about where this code runs?

### Editorial rationale

Prevents the common mistake of running an editor example in a normal terminal or putting the autocomplete stub on the runtime path.

### Timing and preparation

Within anchor 03’s existing 2:45. Replace 20 seconds of setup narration; keep the setup question.

## Slide 8 / 04 — Make saved-file execution reproducible

Route: live. Karol lessons: 6, 7, 8.

### Field-level edits

Keep the Hello Unreal code and title. Replace the version-specific “File > Execute Python Script” instruction with “Saved file: editor Execute Python Script command.” In preparation, verify the menu location in the actual classroom build; Karol’s screenshot shows Tools.

### Proposed slide copy

Output Log: choose Python
Saved file: editor Execute Python Script command
A second import does not rerun a cached module.
Which execution route would you use for a repeatable script?

### Read-aloud narration

This short command confirms that we are talking to Unreal. The same operation can live in a saved file. During development, importing a module again is not the same as rerunning the file: Python may use its cached module. What would you like clarified about the two execution routes?

### Editorial rationale

Adds the missing practical execution detail without introducing debugger installation during class.

### Timing and preparation

Existing 2 minutes. Use a prepared file, not live typing of a path.

## Slide 10 / 06A — Preserve the shared-asset versus placement distinction

Route: live. Karol lessons: 10, 11, 40.

### Field-level edits

Keep the title, diagram and prediction. Add “This demo assigns a component override” to narration; keep Karol’s shared-mesh action as optional contrast.

### Proposed slide copy

One shared mesh; two actor placements.
This demo changes one component’s material override.
Where would you make a change that affects only Actor A?

### Read-aloud narration

These placements refer to the same mesh asset. Today we assign an override to the selected actor’s component. Karol’s Blueprint action instead changes material slots on the mesh asset itself, which can affect its other uses. Point to the place we should change if Actor B must remain untouched. What questions do you have about that scope?

### Editorial rationale

Avoids transplanting a superficially similar material script that violates the demo’s protected-scope promise.

### Timing and preparation

Existing 3 minutes, including the existing 45-second prediction pause.

## Slide 11 / 07 — Show that there are two independent selections

Route: live. Karol lessons: 10, 11, 40.

### Field-level edits

Keep the actor-subsystem example. Add a compact second line naming EditorUtilityLibrary.get_selected_assets(), labeled Content Browser. Keep selected actors and selected assets visually separate.

### Proposed slide copy

Level selection → target actor components
Content Browser selection → input textures
Do both selections belong to the same tool operation?
Questions about selection or paths?

### Read-aloud narration

The Outliner selection tells us which placements may change. The Content Browser selection supplies the three textures. Those are separate collections. We already have loaded objects, so we do not need to load them again just to inspect them. Which collection would you check if the tool reported a missing normal map?

### Editorial rationale

Connects the simple selection snippet directly to the two-input Material Setup workflow.

### Timing and preparation

Existing 3 minutes. Use the existing 45-second question pause for this check.

## Slide 13 / 10 — Give the handoff an explicit reimport prediction

Route: live. Karol lessons: 19, 20.

### Field-level edits

Keep the Maya-to-Unreal schematic and title. Make the source filename, destination and expected replacement behavior explicit in the prepared demonstration. Do not describe the Material/VFX assistant as having an importer.

### Proposed slide copy

Source file → import settings → Unreal asset
Predict the destination and replacement behavior.
After a revision, inspect the result and check for unintended duplicates.
What must survive the reimport?

### Read-aloud narration

An import needs more than a filename. We choose where it goes and what happens if the asset is already there. Before the revision, predict which asset should change and what must remain. After the import, inspect the returned asset path and the result in the editor. What questions do you have about the handoff?

### Editorial rationale

Karol provides the missing task/options vocabulary. The current assistant does not expose this workflow, so it belongs to the separate prepared handoff.

### Timing and preparation

Keep the existing 7 minutes: 1-minute schematic, 5-minute prepared handoff/revision, 1-minute questions. If the importer has not been rehearsed, use labeled existing material rather than improvise a new feature.

## Slide 15 / 09 — Use one blocked input to explain the existing validation

Route: live. Karol lessons: 12, 13, 14, 21, 34, 40.

### Field-level edits

Keep title, blue-cube result and protected-cube comparison. Replace the three bullets with the proposed sequence below. Replace the live duplicate-name attempt with a missing-texture attempt; keep duplicate-name behavior in optional study material. Do not modify texture settings during the demonstration.

### Proposed slide copy

Preview checks the texture set and target slot.
Apply creates one instance and changes one component.
Undo restores the assignment; the new asset remains.
What changes? What must stay unchanged?

### Read-aloud narration

First I have left one texture out. The tool blocks the operation before changing the scene. I will select the complete set and preview again. Check the destination, the texture mapping, the target and slot. After Apply, the blue cube changes and the protected cube stays plain. We inspect the actual parameter state as well as the message. Undo restores the assignment, but it does not remove the new instance asset. What questions do you have about those two results?

### Editorial rationale

Uses an existing failure path to teach validation, state inspection and recovery. Karol’s texture fixer is not copied into an actor-only tool that promises to leave shared inputs unchanged.

### Timing and preparation

Same 7 minutes / 3:49–3:56: 0:00–0:45 prediction; 0:45–1:30 missing-input block and correction; 1:30–3:00 Preview/Apply; 3:00–4:15 result/protected scope; 4:15–5:15 Undo and retained asset; 5:15–7:00 questions and recovery buffer.

## Slide 16 / 09F — Replace the older backend excerpt with the current workflow

Route: optional. Karol lessons: 13, 34, 37.

### Field-level edits

Keep the optional backend-check topic. Replace the older propdemo.py excerpt and source label with WorkflowSession.apply from workflows.py. Show a short exact excerpt, with omitted surrounding code labeled.

### Proposed slide copy

require(self.backend.snapshot(kind, request) == snapshot,
        "Selection, scene, preset or destination changed. Preview again.")

Changed input invalidates the reviewed plan.
Then rerun rules, acknowledge warnings and execute.
What else could make a preview stale?

### Read-aloud narration

Disabling a button is useful feedback, but it is not the final check. Apply compares a fresh snapshot with the reviewed one, reruns the rules, and only then calls the backend. The live material backend also reads the texture parameter back after setting it. A return flag alone was not enough in the recorded rehearsal.

### Editorial rationale

Aligns the code being taught with the current Material/VFX implementation and a real recorded bug, rather than an older prop workflow.

### Timing and preparation

Optional study replacement; adds zero live minutes. Link from slide 15.

## Slide 18 / 08A — Name the actual native implementation

Route: live. Karol lessons: 29, 32, 39, 40.

### Field-level edits

Keep title and shared-backend structure. For a slide describing the current demo, replace the lower box “Editor Utility / Blueprint UI” with “Native Slate / editor panel.” Keep Blueprint/EUW as an optional alternative on slide 17 / anchor 08, not a claim about the current panel.

### Proposed slide copy

PySide UI + native Slate editor panel → shared Python rules → Unreal editor API
Same operation and validation; different interfaces.
Which logic should survive a complete UI redesign?

### Read-aloud narration

Both interfaces call the same workflow. The current native panel is built with Slate; the other view uses PySide. Karol’s Asset Action Utility shows another possible entry point, but changing the interface should not duplicate our validation rules. Which parts would you keep if the interface were redesigned? What questions do you have about where the logic belongs?

### Editorial rationale

Corrects the mismatch between the generic Blueprint diagram and the current demo while preserving the valuable separation of UI and operation.

### Timing and preparation

Existing 2 minutes / 3:56–3:58. Compare interfaces briefly; do not run the whole workflow twice.

## Slide 21 / 09D — Treat repeat blocking and Undo as observable results

Route: live. Karol lessons: 15, 25, 34.

### Field-level edits

Keep the three-effects capture, title and repeat/Undo sequence. Keep the performance boundary explicit; do not add procedural scattering, graph editing or cost inspection.

### Proposed slide copy

Three tagged anchors → three prepared effects.
A repeat is blocked. Undo removes this batch.
Placement checks do not measure frame cost.
What would you inspect before claiming performance?

### Read-aloud narration

We expect one effect at each of these three anchors. A second attempt should be blocked because those anchors are occupied. After Undo, inspect the Outliner and the scene. These checks establish bounded placement and recovery. They do not tell us the frame cost on target hardware. What questions do you have about what this result proves?

### Editorial rationale

Transfers Karol’s duplicate detection and transaction concepts without expanding the agreed VFX scope.

### Timing and preparation

Keep 4 minutes / 3:58–4:02, including 2 minutes for questions/recovery as scheduled.

## Slide 25 / 12 — Keep the prefix lab, strengthen its technical evidence

Route: live. Karol lessons: 21, 22, 35, 37.

### Field-level edits

Keep the exact-one-SM_ rule and existing lab structure. Add the expected untouched set to the instructor answer guide, not another student implementation task. A success-count message is insufficient evidence.

### Proposed slide copy

Rule: exactly one SM_ prefix on selected assets. Leave all others unchanged.
Predict the resulting names and identify what must remain untouched.
What evidence would distinguish success from “the script ran”?

### Read-aloud narration

Write the expected names before running anything. Include an already-prefixed asset and something outside the selected set. If the tool reports four updates, that count does not tell us whether the naming rule or protected scope was respected. What would you inspect next?

### Editorial rationale

Connects automated validation to the existing observation lab without replacing the UX assessment or changing assignment requirements.

### Timing and preparation

Keep the combined 8-minute Lab 1 block across anchors 12 and 12A.

## Slide 43 / 16E — Turn a confirmed defect into a regression check

Route: live. Karol lessons: 35, 36, 37, 38.

### Field-level edits

Keep title, Observe → Interpret → Revise → Retest loop and peer-test question. Add an optional study pointer, “Explore further: from a confirmed defect to a regression test.” Do not replace peer testing with an automation lecture.

### Proposed slide copy

Observe the attempt → investigate the cause → revise → retest.
A confirmed defect can become a repeatable regression check.
What questions remain before you write the peer-test task?

### Read-aloud narration

A useful observation names the input, action, expected result and what actually happened. Once we confirm a defect, we can turn the repeatable part into a regression check. For example, an incomplete texture set must not create an asset. That automated check still cannot tell us whether a new artist understands the error message. What questions remain before you write your peer-test task?

### Editorial rationale

Separates correctness evidence from usability evidence while giving student observations a practical engineering destination.

### Timing and preparation

Use 30–40 seconds inside anchor 16E’s existing 3:30; retain the final question pause and all peer-testing time.

## Slide 59 / A1 — Update the appendix that still calls material automation “later”

Route: optional. Karol lessons: 12, 13, 14, 39.

### Field-level edits

Replace “Material automation: a later connection” with “Material Setup: implementation details.” Keep this optional; label practice captures as practice and point to the current live run sheet for editor evidence.

### Proposed slide copy

Material Setup: implementation details
Read inputs → validate → preview → apply → inspect.
Texture rules and exact parent parameter names are project contracts.
Explore further: a read-only texture validation report.

### Read-aloud narration

The material workflow is already part of today’s live demonstration. This appendix explains its implementation and a possible extension: reporting every texture-setting mismatch in one readable table while leaving the inputs unchanged.

### Editorial rationale

Removes stale framing and gives Karol’s deeper texture/material content a clear optional home.

### Timing and preparation

Zero live minutes; optional appendix replacement.

## Future functionality, in order

1. Read-only texture validation report: property, actual/expected values, reason and recovery; aggregate issues; invalidate stale plans; both interfaces.
2. Optional failure-to-regression walkthrough using existing tests before building a new runner.
3. Separate explicit import/reimport preview, only after engine/importer rehearsal.
4. Progress/cancel and truthful partial-completion summary when a real larger batch requires it.

Preserve the project’s Isaac Oster / Northwood attribution and credit Karol / Tech Art Corner for the supplemental material.
