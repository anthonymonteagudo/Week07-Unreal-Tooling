# Material and VFX classroom demonstration

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
