from pathlib import Path
import shutil
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
PROJECT=ROOT/'Week07UnrealPython'
DOC=PROJECT/'Docs'
pack='../../Course/Slides/Week07/Refinement20261015/index.html'
(DOC/'DEMO_SEQUENCE.md').write_text('''# Material and VFX classroom demonstration

Use the [current Week 7 class pack](../../Course/Slides/Week07/Refinement20261015/index.html) and its revised live-demo run sheet. The ten-minute instructor allocation is five minutes for Material Setup, four for VFX Placement and one for questions. The Blender bridge has a separate allocation. Colleague demonstrations retain their fifteen-minute block.

## Choose the teaching mode

The native C++ Slate tab and live PySide window were rehearsed in Unreal 5.7.4 on the prepared `W07_MaterialVFXLab` fixture. The [recorded report](../../Course/Slides/Week07/FinalClass20261013/live-captures/rehearsal.json) and [capture fallback](../../Course/Slides/Week07/FinalClass20261013/live-demo.html) document that run. The 15 October copy and action-tooltip refinement was checked offline; it is not a fresh engine rehearsal.

For a prepared live run, use `Scripts/launch_live_demo.ps1` from the project. If the project is already open, use its current editor and Tools → Material & VFX Tools. `import week07_tools as w7; w7.show_assistants()` opens the separate PySide window. Use one interface for the task, then compare captures of the other.

For practice, run `./.venv/Scripts/python.exe Scripts/assistants.py`. Keep PRACTICE MODE visible. Inputs are fictional sample data; Unreal selection does not change them. See the [student tasks](Students/START_HERE.md).

## Ten-minute route

| Elapsed | Action and evidence |
| --- | --- |
| 0:00–0:30 | Show the target and protected cube. Ask what changes and what stays shared. |
| 0:30–1:30 | Select Material Setup, slot 0 and a fresh MI_ name. Preview destination, parent, three texture bindings and component assignment. |
| 1:30–2:30 | Apply once. Inspect the blue target and unchanged protected cube; read back the instance parameters. |
| 2:30–3:00 | Preview the same name again. Existing output must block creation. |
| 3:00–4:00 | Undo only the known material-assignment transaction. Inspect the target; the new instance remains as a separate asset. |
| 4:00–5:00 | Ask for input, action, expected result and protected scope. Leave the draft for later inspection. |
| 5:00–5:45 | Select the three tagged VFX anchors and Classroom fountain at scale 1.0. Predict count and positions. |
| 5:45–6:30 | Preview transforms, then Apply once. Inspect exactly three placements. |
| 6:30–7:15 | Preview the same anchors again. Occupied anchors must block duplication. |
| 7:15–8:00 | Undo the known VFX placement. Verify all three effects disappear and pedestals remain. |
| 8:00–9:00 | Separate placement safeguards from performance measurement. State the current evidence and limits. |
| 9:00–10:00 | Questions and transition. Switch to captures after one short recovery attempt if needed. |

Do not save the modified demonstration map. Restore the saved baseline after class; inspect any new material instance separately. Reopening a map does not remove a created asset. Never use broad asset deletion as a reset.

## State language shared with the slides

Choose → Preview → Apply → Check. Changing inputs expires the preview; it does not undo prior edits. A completed plan cannot be applied twice. Warnings require acknowledgment; hard blockers require correction. Apply rechecks selection and state in the backend even when the button was enabled. A successful call and a visible success message both require a result check.

The sample reset restores both fictional workflows and retains input fields. Engine Undo restores the documented transaction scope. Material assignment Undo retains the new asset; VFX placement Undo removes that batch. Effect counts do not establish frame cost.

## Read the implementation

1. `Content/Python/week07_tooling/workflow_sample.py`: sample inputs and reset.
2. `workflows.py`: plan rules, preview expiration and guarded Apply.
3. `workflow_presentation.py`: counts, rows and operation names.
4. `ui/assistants.py` and `ui/assistant_style.py`: state, action emphasis and copy.
5. `editor/workflow_backend.py`: actual editor reads, mutation, verification and cleanup.
6. `Plugins/Week07Tools`: the native Slate presentation.

Compare the same task across stages 1, 2 and 3 using `Scripts/assistants.py --stage N`. The [style sheet](UI/UX_STYLE_SHEET.md) records the rules; the [presentation checklist](UI/PRESENTATION_CHECKLIST.md) separates automated evidence from manual host checks.
''',encoding='utf-8')
(DOC/'UI/PRESENTATION_CHECKLIST.md').write_text('''# Material and VFX presentation checks

Use the [current class pack](../../../Course/Slides/Week07/Refinement20261015/index.html), [ten-minute demo route](../DEMO_SEQUENCE.md) and [student tasks](../Students/START_HERE.md). The product is Material & VFX Tools; tabs are Material Setup and VFX Placement.

## Recorded evidence and current checks

| Area | Evidence and scope |
| --- | --- |
| Unreal 5.7.4 prepared fixture | Recorded material creation/readback, protected cube/shared mesh unchanged, assignment Undo with asset retained, three VFX placements, duplicate block and VFX Undo. |
| Native Slate and live PySide | Both used Preview/Apply in the recorded rehearsal. PySide reopen was also checked. Native is a C++ editor tab; PySide is a separate window. |
| 15 October refinement | 88 offline tests and 18 assistant UI gates passed. Input-change copy, state-specific tooltips and completed-result guidance were refined. |
| Current visuals | Nine fresh sample-data captures cover start, preview, completed, blocked, warning and narrow states. These are practice captures. |
| Manual review | Keyboard operation, classroom projection/Windows scaling and accessibility with real users remain separate checks. No new live engine run was made during the overnight refinement. |

The [recorded report](../../../Course/Slides/Week07/FinalClass20261013/live-captures/rehearsal.json) establishes the fixture checks, not arbitrary assets or target-device performance.

## Before a live showcase

Open the saved baseline with two plain cubes and three empty pedestals. Confirm UE 5.7.4, the intended project and the native plugin build. Preflight the fixture; select target and textures separately; inspect the active preset catalogue. Open the [capture fallback](../../../Course/Slides/Week07/FinalClass20261013/live-demo.html) before beginning.

Use a fresh MI_ output name, slot 0 and Classroom fountain at scale 1.0. The catalogue already supplies `/Game/Week07/LiveDemo/Materials/M_PreparedSurface` and `/Game/Week07/LiveDemo/FX/NS_ClassroomFountain`. Reopen the panel after changing that catalogue. Preview and Apply recheck the live state.

Check Tab/Shift+Tab, combo and spin controls, Preview/Apply and warning acknowledgment on the presentation machine. Keep focus visible. At narrow widths the table scrolls; essential controls must remain reachable. The automated gates do not establish screen-reader or native desktop usability.

## During the demonstration

Ask for a prediction before Apply. Inspect target and protected scope afterward. Explain that changing input expires a plan without undoing existing edits. Distinguish a warning from a hard block, and a completed operation from an unmeasured performance claim. Show only the reset and Undo behavior actually supported by the current mode.

Allow one short recovery attempt. Then use the labeled captures within the same ten-minute allocation. Preserve the break, colleague demos and peer-review time.

## Keeping future edits consistent

Read [UX_STYLE_SHEET.md](UX_STYLE_SHEET.md), run `Scripts/dev.py test`, `Scripts/dev.py check` and `Scripts/ui_quality.py --stage 3`, then render the affected states with `Scripts/assistants.py --render <directory>`. Use the same inputs for comparisons. Recheck host integration when an edit changes host behavior. Do not treat a practice screenshot as live engine evidence.
''',encoding='utf-8')
native=DOC/'UI/UNREAL_NATIVE_UI.md'
archive=DOC/'UI/UNREAL_NATIVE_UI_EUW_PROPOSAL_ARCHIVE.md'
if not archive.exists():archive.write_text('# Archived EUW design proposal\n\nSuperseded by the implemented C++ Slate tab. Retained for architectural reference. Use [the current interface guide](UNREAL_NATIVE_UI.md) for teaching.\n\n'+native.read_text(encoding='utf-8'),encoding='utf-8')
native.write_text('''# Native Slate and PySide interfaces

The current classroom tool has two presentations over the same Python planner and Unreal backend. **Tools → Material & VFX Tools** opens the native C++ Slate editor tab in `Plugins/Week07Tools`. **`w7.show_assistants()`** opens a separate PySide6 Qt Widgets window. A Qt window parented to Unreal is still a Qt window; it is not native Slate docking.

| Surface | Implementation | Classroom use |
| --- | --- | --- |
| Native Unreal | C++ Slate `SDockTab` and native controls call the Python bridge | Prepared editor-integrated showcase |
| Live PySide | Python Qt Widgets call the shared live backend | Compare portable DCC UI patterns |
| Practice PySide | Same staged UI with sample backend | Repeatable, engine-free interaction exercise |
| Editor Utility Widget | UMG/Blueprint editor interface | An alternative architecture, not this tool’s current implementation |

The [recorded UE 5.7.4 rehearsal](../../../Course/Slides/Week07/FinalClass20261013/live-captures/rehearsal.json) checked native Material/VFX Apply and repeat-placement blocking, plus live PySide workflows. The [capture fallback](../../../Course/Slides/Week07/FinalClass20261013/live-demo.html) contains the actual native and PySide captures. The older [EUW assembly proposal](UNREAL_NATIVE_UI_EUW_PROPOSAL_ARCHIVE.md) is archived.

## Shared behavior

Both live interfaces identify scope, preview before mutation, expire stale plans, require acknowledgment for reviewable warnings, reject hard blockers and consume Apply. Backend validation is the boundary; enabling a button is only feedback. `workflow_presentation.describe_plan()` supplies common labels, counts and rows. `editor/native_bridge.py` owns Qt-free sessions for the native tab.

## Lifecycle and recovery

Reopening or reloading invalidates old sessions and plans. Reconnect or reopen the appropriate interface, then preview again. Do not keep a stale plan while stepping through console examples. Native plugin binaries match the recorded Windows UE 5.7.4 build; another engine build requires a rebuild. Use the current [run sheet and mode boundaries](../DEMO_SEQUENCE.md).

## References

- [Epic Slate editor-window quickstart](https://dev.epicgames.com/documentation/en-us/unreal-engine/slate-editor-window-quickstart-guide-for-unreal-engine)
- [Epic Editor Utility Widgets](https://dev.epicgames.com/documentation/en-us/unreal-engine/editor-utility-widgets-in-unreal-engine?application_version=5.7)
- [Epic editor Python scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python?application_version=5.7)

API reference pages explain the architecture. The project code and dated rehearsal establish what this classroom implementation does.
''',encoding='utf-8')
p=DOC/'UI/UX_STYLE_SHEET.md';t=p.read_text(encoding='utf-8').replace('Version 1 ·','Version 2 ·').replace('It records the existing dark course-tool palette and the new action-emphasis refinement.','It records the dark course-tool palette, action emphasis and state wording.')
t=t.replace('- Inputs or task change: invalidate the plan and return to Preview.','- Inputs or task change: invalidate the plan and return to Preview. Say explicitly that this does not undo earlier applied changes; never imply that the scene or sample has been restored.')
t=t.replace('- Apply completed: keep the result inspectable, disable repeat Apply, explain the next verification step.','- Apply completed: keep the result inspectable, disable repeat Apply, explain the next verification step. Name the recovery scope: material assignment Undo retains the created asset; VFX Undo removes its placed batch; neither workflow automatically saves the map.\n- Apply tooltip: explain the actual state—fresh preview required, warning acknowledgment required, ready to recheck and apply, or already completed. Do not show an active-operation promise on a disabled completed button.')
p.write_text(t,encoding='utf-8')
p=DOC/'UI/MATERIAL_VFX_SCOPE.md';t=p.read_text(encoding='utf-8').replace('Source prepared; **not yet run or verified inside Unreal**.','Rehearsed on the prepared UE 5.7.4 fixture; see [recorded evidence](../../../Course/Slides/Week07/FinalClass20261013/live-captures/rehearsal.json).').replace('A Qt-free native-widget Python bridge for the same workflows. The native EUW\n  asset and its Blueprint wiring remain pending.','A Qt-free Python bridge used by the implemented C++ Slate tab in `Plugins/Week07Tools`. EUW remains an alternative architecture.')
t=t.replace('The live catalogue is unconfigured; no prepared material asset is implied.\nPrepare and register a matching parent during the later editor rehearsal.','The live catalogue contains the prepared classroom blue-surface parent under `/Game/Week07/LiveDemo/Materials`. Its three texture bindings were checked in the recorded fixture rehearsal.')
p.write_text(t,encoding='utf-8')
p=PROJECT/'README.md';t=p.read_text(encoding='utf-8').replace('Material/VFX Unreal adapter; live rehearsal pending.','Material/VFX Unreal adapter; prepared UE 5.7.4 fixture rehearsed. See Docs/DEMO_SEQUENCE.md for scope.')
p.write_text(t,encoding='utf-8')
p=DOC/'Students/START_HERE.md';t=p.read_text(encoding='utf-8');anchor='## Task 1'
if 'Changing inputs clears' not in t:t=t.replace(anchor,'Changing inputs clears the current preview; it does not undo work already applied. Use the appropriate reset or recovery action for the current mode.\n\n'+anchor,1)
p.write_text(t,encoding='utf-8')
# Fresh practice images replace only their matching UI captures; preserve all originals in the overnight package.
for image in (OUT/'assets/practice').glob('*.png'):
    target=DOC/'UI/captures'/image.name
    if target.exists():
        old=OUT/'assets/practice-before'/image.name;old.parent.mkdir(exist_ok=True)
        if not old.exists():shutil.copy2(target,old)
    shutil.copy2(image,target)
print('Updated canonical demo documentation, preserved historical EUW proposal and refreshed nine practice captures.')
