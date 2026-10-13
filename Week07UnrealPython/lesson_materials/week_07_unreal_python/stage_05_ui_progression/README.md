# Material & VFX Tools · functional → guided → refined

The **same two tools** evolve through all three PySide stages. Inputs, sample data,
plans, validation and mutation behavior stay constant. The teaching variable is the
presentation: how easily can someone understand, review and recover from a task?
This progression is Python/PySide only. Unreal UI cohesion is a later pass.

## Run one checkpoint at a time

From the project root, when ready to open a practice window:

```powershell
./.venv/Scripts/python.exe Scripts/assistants.py --stage 1
./.venv/Scripts/python.exe Scripts/assistants.py --stage 2
./.venv/Scripts/python.exe Scripts/assistants.py --stage 3
```

Close each stage before opening the next. Each launch starts fresh sample data;
there is no editor connection or transfer of a pending preview between stages.
The default is stage 3. VS Code's **UI OFFLINE — Week 7: open teaching stage** task
and **Debug Material and VFX assistants (practice mode)** configuration ask for a
stage. The main student quick-start still opens the refined stage by default.

## Compare the same task, not different tools

First compare **Material Setup across 1 → 2 → 3**, then **VFX Placement across
1 → 2 → 3**. Keep the window size and inputs identical. Use the default name
`MI_Crate_Demo`, slot `0`, Steam preset and scale `1.00×`.

For each comparison: preview, identify the exact change, apply, preview the same
request again to see the blocker, then reset practice data. In early stages the
button says **Apply reviewed changes**; stage 3 names the operation and count.

| Stage | What changes | Why it changes | Quality gate before advancing |
| --- | --- | --- | --- |
| 1 · Functional | Labeled inputs, read-only linear review, explicit Preview/Apply, status and recovery messages. | Establish the complete task first. The user can inspect every proposed value, but may have to scroll and compare it mentally. | Both tasks complete; repeat operations are blocked; stale inputs cannot apply; warnings need acknowledgement. |
| 2 · Guided | Before/after table, persistent scope summary, inline selection and input guidance. | Reduce memory and interpretation effort. Identify affected objects and compare values in aligned columns. | Table contains the same data as stage 1; distinguish proposed from applied rows; find the target and count without decoding text. |
| 3 · Refined | Progress cues, operation-specific Apply label with count, stronger primary-action emphasis. | Make the current step and consequence of the next action easier to predict. | Progress follows state; labels match the reviewed operation; keyboard focus and controls remain usable at the minimum window size. |

All stages retain readable text, accessible control names, keyboard access,
read-only review, empty-state feedback, input invalidation, warning acknowledgement,
hard limits, consumed previews and reset. Safety and accessibility are not rewards
reserved for the final stage. The shared color theme keeps comparisons focused on
information structure and interaction rather than on a cosmetic reskin.

## Capture pairs for slide preparation

These are screenshots of actual offscreen Qt widgets, using the same fictional
inputs. Keep the practice banner and stage label visible. No slides were edited.

| Stage | Material Setup | VFX Placement |
| --- | --- | --- |
| 1 · Functional | [Text preview](../../../Docs/UI/captures/assistants_stage_1_material_preview.png) | [Text preview](../../../Docs/UI/captures/assistants_stage_1_vfx_preview.png) |
| 2 · Guided | [Table preview](../../../Docs/UI/captures/assistants_stage_2_material_preview.png) | [Table preview](../../../Docs/UI/captures/assistants_stage_2_vfx_preview.png) |
| 3 · Refined | [Guided action](../../../Docs/UI/captures/material_preview.png) | [Guided action](../../../Docs/UI/captures/vfx_preview.png) |

Ask the same questions at each stage: “What will change?”, “How many objects?”,
“What do I do next?”, and “How do I recover?” At stage 2 point to the table and
summary; at stage 3 point to the progress cue and the counted Apply action.

Each stage also has start, complete, blocked, warning and narrow-warning captures.
The density-warning fixture has six existing effects plus three proposed effects;
it is a separate scenario from the default empty-world task. Count limits are not
performance measurements.

To render without opening a desktop window, repeat for N = 1, 2, 3:

```powershell
./.venv/Scripts/python.exe Scripts/assistants.py --stage 1 --render Docs/UI/captures
```

Stages 1 and 2 use `assistants_stage_N_` filename prefixes. Stage 3 retains the
existing `material_preview.png` / `vfx_preview.png` names for guide compatibility.

## Code checkpoints and quality gates

Read [assistant_views.py](../../../Content/Python/week07_tooling/ui/assistant_views.py):
`FunctionalReview` formats a linear review, then `GuidedReview` displays the same
rows in columns. Both consume `describe_plan()` and never execute changes.
Then read [AssistantWindow](../../../Content/Python/week07_tooling/ui/assistants.py):
`ui_stage` controls the presentation; the same `WorkflowSession` handles every
Preview and Apply. Stage 3 builds on the guided table rather than duplicating rules.

Run cumulative automated gates, using stage 1, then 2, then 3:

```powershell
./.venv/Scripts/python.exe Scripts/ui_quality.py --stage 1
./.venv/Scripts/python.exe Scripts/ui_quality.py --stage 2
./.venv/Scripts/python.exe Scripts/ui_quality.py --stage 3
```

The default gate target is now Material/VFX. Tests compare plans/results across
stages, enforce stale/invalid-input and warning behavior, and check presentation
contracts. Missing Qt fails the mandatory gate. Separately review keyboard-only
use, projection scaling and screen-reader behavior on the teaching machine.
Offline gates do not establish live Unreal readiness.

Earlier Prop Inspector code remains a reference only: `Scripts/ui.py --stage N`,
and its retained gates use `Scripts/ui_quality.py --tool props --stage N`.
It is no longer part of this UI/UX demonstration. Stable foundation IDs 01–08
remain available without renumbering the current demo or slides.
