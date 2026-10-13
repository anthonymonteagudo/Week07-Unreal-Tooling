# Material & VFX Tools · canonical demo route

> Current classroom route, 13 October 2026: Material/VFX workflows were rehearsed in Unreal 5.7.4 with both live PySide and the native C++ Slate tab in `Plugins/Week07Tools`. Prepared assets and `W07_MaterialVFXLab` now exist. Use the [live run sheet and actual capture fallback](../../Course/Slides/Week07/FinalClass20261013/live-demo.html). Pending statements below describe the earlier plan, not current Material/VFX readiness. The separate Maya bridge is outside this rehearsal.


Updated 13 October 2026. This is the demo project's rehearsal order and capture
map. D1–D6 identify demonstration beats, not slide numbers. No deck was edited,
timings assigned or lab requirements finalized by this cleanup.

**Student route:** [Choose → Preview → Apply → Check](Students/START_HERE.md).
**Instructor readiness:** [presentation checklist](UI/PRESENTATION_CHECKLIST.md).
The two tasks use the same interaction pattern, with different domain rules.
Teach one task fully before transferring that pattern to the second.

## Rehearse the primary route

From the project root, manually run:

```powershell
./.venv/Scripts/python.exe Scripts/assistants.py
```

Keep **PRACTICE MODE** visible. The sample supplies textures, a crate and three
markers; clicking in Unreal does not change these inputs. Begin with fresh practice
data, name `MI_Crate_Demo`, slot `0`, and effect scale `1.00×`.

| Beat / purpose | Demonstrate | Expected result / gate to continue | Capture |
| --- | --- | --- | --- |
| D1 · Define the task and scope | Open Material Setup; identify the parent, output name and slot. Ask what should change. | Students distinguish a component assignment from shared mesh or parent-graph changes. Apply is disabled until preview. | [Material start](UI/captures/material_start.png) |
| D2 · Review before mutation | Preview the default material request. Read texture mapping and before/after assignment. | Exactly one new instance and one component assignment. Slot 0 is the sample crate's only slot. | [Material preview](UI/captures/material_preview.png) |
| D3 · Apply, check and recover | Apply once. Preview the same name again; read the rejection. Reset practice data for the next task. | Completion consumes the plan. Existing names cannot be overwritten. Reset clears both sample workflows, retaining input fields. | [Completed](UI/captures/material_complete.png), [blocked](UI/captures/material_blocked.png) |
| D4 · Transfer the workflow | Open VFX Placement; preview Steam at the three supplied markers. Review transforms, then apply. | Three markers produce three effects. Loaded component count changes from 0 to 3. No scatter or Niagara graph edits. | [VFX preview](UI/captures/vfx_preview.png), [completed](UI/captures/vfx_complete.png) |
| D5 · Explain the placement limits | Preview the same markers again. Explain the duplicate rejection. Optionally show the separate density-warning capture. | Students distinguish a hard blocker from a reviewable warning. Acknowledging a warning cannot bypass a hard limit. Counts do not establish frame cost. | [Duplicate blocked](UI/captures/vfx_blocked.png), [warning](UI/captures/vfx_warning.png) |
| D6 · Explain the code and host boundary | Trace sample → rules/session → presentation → UI → Unreal adapter using the files below. | Students identify where proposed data becomes a real editor mutation. End with the pending live/native work, not a claim of a completed Unreal demo. | Reuse the preview alongside the relevant code; no native capture exists yet. |

The warning capture uses a separately seeded sample with existing effects. The
default three-marker task does not produce that warning. Do not invent a live
failure or repeatedly apply batches just to reach a screenshot's count.

Use these short explanations while showing the corresponding state:

- **D2:** “This table is our proposed change. We can review the destination and
  component assignment before creating anything.”
- **D3:** “The preview has been used. Repeating the name is blocked, so we need a
  new name or a fresh practice sample.”
- **D4:** “We reuse the same interaction pattern. The rules now describe markers
  and effect placement instead of textures and material slots.”
- **D5:** “Placement checks passed does not mean the effect is cheap. Rendering
  and optimization work will measure what these count checks cannot.”
- **D6:** “The sample lets us study behavior without an editor. The adapter is
  where we will need to verify real assets, transactions and editor behavior.”

## Trace the implementation in this order

| Read | Focus | Question for the demo |
| --- | --- | --- |
| [workflow_sample.py](../Content/Python/week07_tooling/workflow_sample.py) | `SampleBackend.snapshot` | Which inputs and state are fictional? Why does slot 1 fail? |
| [workflows.py](../Content/Python/week07_tooling/workflows.py) | `material_plan`, then `vfx_plan` | What must be true before proposing this operation? |
| [workflows.py](../Content/Python/week07_tooling/workflows.py) | `WorkflowSession.preview/apply` | Why clear old plans, recheck the snapshot and consume Apply? |
| [workflow_presentation.py](../Content/Python/week07_tooling/workflow_presentation.py) | `describe_plan` | How do structured data become useful rows, counts and action labels? |
| [assistants.py](../Content/Python/week07_tooling/ui/assistants.py) | `AssistantWindow` | How do input changes, feedback and disabled actions guide the user? |
| [workflow_backend.py](../Content/Python/week07_tooling/editor/workflow_backend.py) | `EditorWorkflowBackend` | Where are actual editor reads, mutations and cleanup handled? |

This is a reading route through the working implementation. It does not replace
the small, independent [Python foundations 01–08](../lesson_materials/week_07_unreal_python/README.md).
Use those only when a concept needs a smaller example. Their prop data, naming
rules and reset behavior differ from these two workflows.

## UI/UX progression: the same Material/VFX tools

Use [the three assistant stages](../lesson_materials/week_07_unreal_python/stage_05_ui_progression/README.md).
Compare Material Setup across stages 1 → 2 → 3, then VFX Placement across 1 → 2 → 3.
Keep inputs and window size constant; each stage begins with fresh practice data.
Use D2 and D4 as the preview comparison beats, and D3/D5 to compare recovery.

| Stage | Observe | Quality question |
| --- | --- | --- |
| 1 · Functional | Linear text review and explicit actions | Can the user inspect and complete the entire task? |
| 2 · Guided | Before/after table, scope summary and inline input guidance | Can the user find the exact target and compare values without holding them in memory? |
| 3 · Refined | Progress cues, counted Apply labels and primary-action emphasis | Can the user identify the current step and predict the next action? |

Run `Scripts/assistants.py --stage N` manually, or add `--render Docs/UI/captures`
for offscreen captures. `Scripts/ui_quality.py --stage N` now gates these assistant
stages. The shared session retains all safeguards at every stage. Prop Inspector
is retained only as an earlier reference; the UI lesson no longer switches tools.
Unreal-facing cohesion remains a later pass.

## Compatibility and reset boundaries

| Established entry point | Still means | Do not confuse it with |
| --- | --- | --- |
| `Scripts/lessons.py run 01` through `07`; reading `08` | Optional pure-Python prop foundations | D1–D6, slide numbers, or the five editor examples |
| `Scripts/assistants.py --stage 1/2/3` | Main Material/VFX UI progression, offline | The unchanged live panel API |
| `Scripts/ui.py --stage 1/2/3` | Earlier Prop Inspector reference, offline | The main UI/UX lesson |
| `w7.show_ui()` / `w7.show_pyside_ui(stage=3)` | Live Prop Inspector Qt panel | The main assistants or a native dockable tab |
| `w7.show_assistants()` | Live Material/VFX Qt panel, pending rehearsal | Standalone practice data or a finished native widget |
| `w7.preview()`, `apply(plan)`, `check()`, `reset_demo()` | Six-prop fixture operations | Material asset cleanup or removal of placed effects |
| **Reset practice data** | Restore both fictional assistant workflows; retain inputs | Undo, map reset, asset deletion or saving in Unreal |
| `w7.reload_tools()` / `w7.run_example(...)` | Reload implementation; close shared Qt window and expire native sessions/plans | A way to keep the current UI preview while stepping console examples |

The live Qt host owns one panel. Opening another stage/tool replaces it. Finish
the current demo before switching, then reopen and preview again after reload.
The native bridge has separate session entry points for props and workflows;
`close_all()` expires both. The original commands and stable IDs are retained.

For future live material rehearsal, restoring component assignments and handling
the newly created material asset are separate steps. For VFX, inspect the actual
placed Actors and Undo behavior. Neither workflow automatically saves. Follow
the [live acceptance checklist](UI/PRESENTATION_CHECKLIST.md) before presenting
these as verified editor operations.

## What this cleanup resolved

- Competing “start here” instructions now converge on Material Setup → VFX
  Placement. Prop examples remain optional foundations or fallback. The UI progression now uses Material/VFX themselves.
- The outdated “cleanup or batch import?” decision is resolved to the user's
  selected tools. Advanced graph editing and scattering remain outside scope.
- Practice mode now rejects unavailable material slots, parents and presets;
  previously a changed slot could silently preview the sample's slot 0.
- Reload, reset and single-window behavior are explicit, rather than implied to
  apply uniformly to both tool families.

Original Northwood was the instructor's work through Isaac Oster's public UE
Python course. This project is the classroom-preparation spinoff. Earlier
[prop-fixture screenshots and GIFs](../../Course/Slides/Week07/UnrealPythonDemo/index.html)
document that earlier demo; they are not evidence of Material/VFX integration.
Current Material/VFX images are actual offscreen PySide practice captures.
The live presets, Unreal rehearsal and native EUW asset remain pending.
