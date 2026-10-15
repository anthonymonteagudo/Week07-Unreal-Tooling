# Week 7 teaching tool style sheet

Version 2 · 15 October 2026. Applies to the Material Setup and VFX Placement PySide assistants. It records the dark course-tool palette, action emphasis and state wording. It does not replace GOLF+ design rules or certify the native Slate and Blender/Maya surfaces.

## Purpose and task

An artist chooses inputs, inspects a proposed change, applies that reviewed operation, and checks the result. The interface must expose scope and recovery. A successful API return is not proof that the artistic goal was achieved.

## Visual roles

The existing palette lives in `Content/Python/week07_tooling/ui/window.py`. The assistant action roles live in `ui/assistant_style.py` and are the source for the new emphasis states. Migration of all legacy literals to tokens remains a separate cleanup; do not claim it is complete.

| Role | Treatment | Meaning |
| --- | --- | --- |
| Canvas | Existing dark neutral `#171d27` | Tool workspace |
| Main text | `#eef2f8` | Readable content and labels |
| Primary action | `#a9cfff`, text `#142033` | Available forward action in the refined stage |
| Secondary action | `#303e53`, text `#eef2f8` | Supporting operation, still recognizable as a button |
| Focus | `#9ccaff`, visible outline | Keyboard destination; distinct from selection and availability |
| Disabled | `#252d39`, text `#8793a6` | Unavailable operation; explanation is also provided |
| Warning/error/success | Existing tinted status surface plus explicit message | State information; never hue alone |

Preserve Segoe UI, the current scale and the 24-pixel outer margins. These are implementation choices for this tool, not universal design laws. Use the host’s layout managers. Essential labels must remain readable at supported window sizes; distinguish hierarchy with weight, spacing and grouping before reducing text contrast.

## State contract

- No pending plan: Preview is the emphasized action when available. Apply is disabled.
- Valid plan, no unacknowledged warning: Apply becomes emphasized. Its label names the operation.
- Warning awaiting review: neither forward button receives primary emphasis. Keep the warning and acknowledgment visible; acknowledgment does not bypass hard limits.
- Inputs or task change: invalidate the plan and return to Preview. Say explicitly that this does not undo earlier applied changes; never imply that the scene or sample has been restored.
- Apply completed: keep the result inspectable, disable repeat Apply, explain the next verification step. Name the recovery scope: material assignment Undo retains the created asset; VFX Undo removes its placed batch; neither workflow automatically saves the map.
- Apply tooltip: explain the actual state—fresh preview required, warning acknowledgment required, ready to recheck and apply, or already completed. Do not show an active-operation promise on a disabled completed button.
- Error: name the problem and next action. Keep scope and unchanged-work claims accurate for the actual failure.

`WorkflowSession` continues to validate at execution. UI enablement is never the safety boundary.

## Layout and controls

Keep inputs together, then state/scope, then the read-only review, then forward actions. Keep Reset separated from Preview/Apply. Use the same column order and labels across material and VFX reviews. A disabled control still looks like a control; a heading must not look like a clickable button. Full-width actions, borders, and text links are context-dependent choices, not prohibited styles.

Keyboard order follows the task: task tabs, active inputs, review, acknowledgment when present, Preview, Apply, then practice reset. Hidden controls should be skipped by Qt. Test the actual focus sequence with keyboard input; code order alone is not proof. Keep focus visible on the review table as well as buttons and fields.

## Review procedure

Render starting, preview, warning, blocked, applied and narrow-window states with `Scripts/assistants.py --render <directory>`. Use functional, guided and refined stages with the same backend. Run the existing workflow/widget gates. Check grayscale hierarchy, a squint/blur approximation, and actual foreground/background contrast separately. Neither grayscale nor squinting substitutes for color-vision, keyboard, text-size, screen-reader or user testing.

Capture before/after from the same input and state. A practice capture must say it uses sample data. Do not label offscreen tests as live engine validation. Before a new showcase, revalidate the native Slate panel and host integration separately, then replace stale slide crops and code excerpts.

## Maintaining the rules with AI

Give the agent the current version of this sheet, token file, representative captures and the requested scope. Ask it to identify which existing pattern applies before changing UI. Require a before/after capture and a list of deliberate exceptions. Accept a rule change explicitly, update the source, then recapture affected states. An agent’s claim of compliance is not the verification step.

For a classroom skill example, see `Course/Slides/Week07/UXMantras20261015/style-skill/SKILL.md` in the course workspace. It is a local teaching example, not a globally installed skill.
