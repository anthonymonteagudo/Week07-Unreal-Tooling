# Week 7 UI/UX integration handoff

Prepared 15 October 2026. Open `index.html` first. This package prepares the direct edit; it is not a modified PowerPoint.

## Updated delivery direction

Use the supplied Course Generator screenshot and fuller visible teaching content. `slide_explanations.py` revises the proposal records and adds `visible_detail` tables, worked examples and an exact code excerpt. Put this material on the projected slides; notes elaborate it. Use the worked example as the main visual and remove redundant bullets rather than fitting both at reduced type size. Live execution is optional reinforcement after rehearsal. Preserve the colleagues’ demo time and the existing schedule.

## Source and scope

Baseline: `../DesktopIntegrated20261014/output/Week_7_Python_in_Unreal_v15.pptx`. Its SHA-256 is recorded in `source-manifest.json` and `slide-proposals.json`. Verify that hash before applying this plan. If it changed, compare the new deck and reconcile the anchors; do not overwrite later edits.

`slide-proposals.json` has proposed copy, read-aloud notes, visual instructions, field-level edits, rationale, source links, the exact current text and notes, and actual current preview paths. IDs refer to the v15 anchors. Lettered IDs are insertions, not final numbers. The `proposed_order` includes the unchanged preparation divider 61 before 62. Preserve 1–38 and 63–134, including existing references and hidden-slide status.

## Integration procedure

1. Re-read `Course/AGENTS.md`, the slide review preferences and the presentations skill. Reuse the v15 theme, compositions, typography and source treatments. Do not turn this review website into the slide theme.
2. Resolve delivery depth. The source schedule has 16 minutes for concepts and 4 for task preparation. The earlier full proposal estimate was 28–35 minutes; the fuller visible explanation now needs rehearsal. Keep the fuller material prepared. Do not change the break, peer rounds or course schedule silently. The integration plan describes an overview route and the complete sequence.
3. Make a new versioned output deck. Retain the original. Apply `proposed_order`, preserving every required topic. Use the field-level `edit` value to determine replacements and moves. Keep 61 as a four-minute boundary.
4. Use the prepared slide body and read-aloud notes. Preserve existing production attribution and useful supplemental examples from `current.notes`; specifically retain the original import/reimport story from current 41 as the second story example. Keep editorial decisions, estimated timing and implementation instructions out of read-aloud notes.
5. Use actual evidence from `after/` for updated PySide states. These are sample data, not engine captures. Label historical GOLF+ images and source pages accurately. The GOLF+ images do not yet form a matched before/after pair. The newly supplied Course Generator screenshot is the primary visual for 52A and 53C. It is sufficient for the visual lesson; acquire additional captures only for behavior or before/after claims. Do not infer enabled/completed state from colors alone.
6. Add the requested art/values bridge, user-story expansion, Figma, color tools, squint/blockout/grayscale checks, and style-sheet/AI workflow. Sources are in the JSON and `sources.html`. Preserve the distinction between art value, HSV Value and relative luminance. Do not reintroduce the unqualified claims identified in the refined notes.
7. Ground one principle in the existing PySide implementation. `assistant_style.py` and the updated `AssistantWindow.update_apply` are the current code references. Keep the native C++ Slate panel and Editor Utility Widgets conceptually distinct. A host integration claim requires host evidence.
8. Follow the presentations skill’s supported editing/export path. Render all edited and inserted slides. Check text fit, diagram/source readability, screenshot size, notes and attribution, hidden status, final slide numbering, and order around the task-preparation boundary. Refresh the slide map and review index for the final deck.
9. Rebuild course readers with `Course/Tools/build_readers.mjs` after final HTML links are authored. Preserve editable sources. Distinguish readiness for a prepared visual explanation from readiness for a live tool run. Host, scaling and behavioral checks still govern any live demonstration.

## Authored material

- `build.py`: refined note generation. The captured source JSON is preserved under `sources/`; original vault notes remain the authority.
- `slide_explanations.py`: follow-up content revision and visible worked examples.
- `proposals.py`: editable proposal records; `slide-proposals.json` is their review manifest.
- `prepare_review.py`: HTML comparison, source register, demo audit and diagnostic companion. Uses the preserved source files and local evidence; it does not launch an editor.
- `render_plan.mjs`: renders `integration-plan.md` with the bundled Markdown runtime.
- `style-skill/SKILL.md`: local teaching example; not globally installed. It references the project style sheet and does not authorize agents or host execution.
- `verification.json`: source preservation, coverage, contrast and browser verification record. Offline results have limited scope.

## Changes made to the demo

`Week07UnrealPython/Content/Python/week07_tooling/ui/assistants.py`, the new `assistant_style.py`, and `Week07UnrealPython/Docs/UI/UX_STYLE_SHEET.md` implement and document the focused action-hierarchy update. The existing 87 tests passed after the change; nine practice states were rendered. No GOLF+ production code, native Slate panel or live engine session was changed in this pass.

The demo audit is deliberately candid about remaining surfaces. The standard in the lecture is a review method, not an assertion that every existing interface has already passed it.
