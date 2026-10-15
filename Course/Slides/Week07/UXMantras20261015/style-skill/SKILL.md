---
name: week7-tool-ui-style
description: Maintain visual and interaction consistency in the Week 7 Material and VFX PySide teaching assistants. Use for changes to those interfaces; not for GOLF+ branding, unrelated tools, or Unreal engine execution.
---

# Week 7 tool UI style

Find `Week07UnrealPython/Docs/UI/UX_STYLE_SHEET.md` in the course workspace and read it before editing the assistants. Use `Content/Python/week07_tooling/ui/assistant_style.py` for action roles and the existing `ui/window.py` palette for the shared legacy surface. Do not introduce a second palette silently.

Preserve the separation between presentation and `WorkflowSession` validation. Refined-stage emphasis follows the next available action; functional and guided stages retain their instructional purpose and all safety feedback.

Keep the current task and state identifiable without color. Preserve accessible names, keyboard navigation, visible focus and the read-only preview. An input change invalidates a pending plan. Do not make cosmetic edits that bypass these behaviors.

Compare matching starting, preview, warning, blocked and completed states before and after a change. Render offscreen using the project’s `--render` route and run the relevant existing tests. The project AGENTS.md governs engine use. Do not launch a live editor to obtain proof during code-only work.

Report intentional departures from the style sheet and update the sheet when the user asks to change its rules. If multiple agents are already authorized for a task, give each the same sheet/version and assign one shared review; this skill does not independently authorize spawning agents.
