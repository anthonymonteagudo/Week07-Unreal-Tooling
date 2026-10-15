# Material and VFX presentation checks

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
