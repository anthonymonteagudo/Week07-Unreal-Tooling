# Instructor presentation pass · Material & VFX Tools

> Current classroom route, 13 October 2026: Material/VFX workflows were rehearsed in Unreal 5.7.4 with both live PySide and the native C++ Slate tab in `Plugins/Week07Tools`. Prepared assets and `W07_MaterialVFXLab` now exist. Use the [live run sheet and actual capture fallback](../../../Course/Slides/Week07/FinalClass20261013/live-demo.html). Pending statements below describe the earlier plan, not current Material/VFX readiness. The separate Maya bridge is outside this rehearsal.


The student entry point is [Docs/Students/START_HERE.md](../Students/START_HERE.md).
The product title is **Material & VFX Tools**; its tabs are **Material Setup** and
**VFX Placement**. Use these names in narration, screenshots and later native UI.

## Current readiness

| Area | Evidence / state |
| --- | --- |
| PySide practice workflow | Implemented; fictional sample data, resettable, no Unreal connection. |
| Automated offline checks | See the current `Scripts/dev.py test` output for the test total, including warning acknowledgement, stale previews and input invalidation. |
| Syntax | Run `Scripts/dev.py check` for the current syntax result. |
| Visual review | Actual Qt renders cover start, preview, completed, blocked and density-warning states; narrow 800×700 capture included. |
| Native desktop usability | Manual keyboard, screen-reader and display-scaling review still needed. Offscreen checks do not establish this. |
| Live Unreal material/VFX adapters | Source prepared; real assets, Undo/failure handling and host integration not yet rehearsed. |
| Native Unreal tab | Python bridge prepared; EUW asset, wiring and native captures still pending. |

Do not present the live integration as verified based on practice-mode tests.
The existing Northwood/Oster study provenance remains in the root README.

## Before students use the workspace

- Open the practice runner on the teaching machine when convenient and confirm the
  **PRACTICE MODE** header. Verify Qt setup using the existing UI dependency guide.
- Perform each student task exactly as written. Expect one material instance and
  three effects. Repeat the preview to demonstrate overwrite/duplicate rejection.
- Confirm Reset practice data resets both operations. Fields retain their values.
- Test keyboard-only operation: Tab/Shift+Tab, combo selection, spin controls,
  Preview and Apply shortcuts, warning acknowledgement. Verify focus is visible.
- Check the UI at classroom projection resolution and Windows scaling settings.
  At smaller widths, the table scrolls; action buttons must remain accessible.
- Use the student guide for instructions; keep implementation-status documents
  and preset configuration in the instructor preparation material.

## Live preset preparation — still pending

Configure `Config/Week07ToolPresets.json`. The student UI uses named dropdowns:

```json
{
  "materials": {
    "prepared_surface": {
      "label": "Prepared surface",
      "parent": "/Game/Week07/Materials/M_PreparedSurface"
    }
  },
  "vfx": {
    "steam_demo": {
      "label": "Steam",
      "system": "/Game/Week07/FX/NS_Steam",
      "reviewed_for_demo": false,
      "review_note": "",
      "max_new": 4
    }
  }
}
```

Paths above are illustrative, **not assets created by this pass**. Retain the
catalogue's `schema_version` field. Set the real prepared parent path and verify its
three texture parameters. Select a real Niagara System, complete the bounded-effect
review in [the functionality guide](MATERIAL_VFX_SCOPE.md), then record the review
and enable that preset. Missing parents and unreviewed effects are omitted from
student choices. If no choices exist, Preview remains disabled with an instructor
setup message. Reopen the panel after changing the catalogue; live snapshots still
recheck the preset on Preview/Apply.

Before a live class demo, check successful operations, stale/empty/mixed selections,
existing destination handling, Undo, failure cleanup, duplicate placement, map/PIE
guards, close/reopen and reload. Confirm results by inspecting the real editor,
including component material slots, the generated instance and Niagara Actors.
Do not use an effect-count threshold as a performance claim.

## Canonical presentation sequence

Follow [demo beats D1–D6](../DEMO_SEQUENCE.md), including the compatibility and reset
boundaries. The principles below support that route; they are not a second sequence.

1. Show the repetitive task: texture assignment, then placing an effect at markers.
2. Ask students to predict what each operation will change and what stays shared.
3. Run **Choose → Preview → Apply → Check**, pointing to the scope count and rows.
4. Introduce one deliberate problem: duplicate output name or repeated markers.
   Ask students to read the message and recover before explaining the implementation.
5. Compare UI quality using the task: can a new user identify the inputs, affected
   objects, next action and recovery? A consistent color scheme is only one part.
6. Read the code in the student guide's order: inputs → rules → presentation → UI
   events → Unreal boundary. Revisit the preview after seeing the implementation.

No timings, slide numbers or assessment requirements are assigned by this draft.
The UI stages now use Material Setup and VFX Placement themselves. Use [the UI progression](../../lesson_materials/week_07_unreal_python/stage_05_ui_progression/README.md)
to compare the same task across functional, guided and refined presentations.
Use `Scripts/assistants.py --stage N` and its matching stage capture set.

## Screenshot set and what to discuss

All images are generated from actual PySide widgets with offscreen sample data.
Keep the practice-mode banner visible when using them in slides.

| Capture | Teaching use |
| --- | --- |
| [Material start](captures/material_start.png) | Empty state and disabled Apply. |
| [Material preview](captures/material_preview.png) | Texture mapping, destination, component override and scope count. |
| [Material complete](captures/material_complete.png) | Result feedback; the preview is consumed. |
| [Material blocked](captures/material_blocked.png) | Recover from a duplicate asset name. |
| [VFX preview](captures/vfx_preview.png) | One marker → one effect; before/after loaded count. |
| [VFX complete](captures/vfx_complete.png) | Operation completed without claiming performance certification. |
| [VFX blocked](captures/vfx_blocked.png) | Repeating a placement should not multiply effects. |
| [VFX warning](captures/vfx_warning.png) | Distinguish a reviewable warning from a hard blocker. |
| [VFX warning, narrow](captures/vfx_warning_narrow.png) | Table scrolling while controls remain reachable. |

Regenerate with `Scripts/assistants.py --render Docs/UI/captures` using the project
interpreter. This does not open desktop windows. Run `Scripts/ui_quality.py --stage 3`
for the mandatory Qt gate; missing dependencies must fail rather than count as a pass.

## Consistency contract for the future native widget

Reuse `workflow_presentation.describe_plan()` (also returned by the native bridge)
for counts, rows and action labels. Keep the same terms and four-step workflow.
On input changes clear the plan; on warnings require acknowledgement; on completion
show a result; on failure give a recovery action. Preserve the distinction between
practice data, actual Unreal operations and performance measurement. This keeps
student tasks stable when the presentation changes from PySide to an Unreal tab.
