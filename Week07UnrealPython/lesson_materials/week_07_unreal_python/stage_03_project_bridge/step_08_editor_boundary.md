# 08 · Read the editor boundary: manual demo later

Open these project-relative paths in VS Code in this order:

| File / function | Responsibility | Earlier checkpoint |
| --- | --- | --- |
| `Content/Python/week07_tooling/rules.py` | Calculate expected states and return issues/plans from data. | 03–07 |
| `Content/Python/week07_tooling/editor/demo.py`: `inspect_selection`, `preview` | Collect actual selected Actor state; guard demo world and selection. | 01–02, 05 |
| Same file: `apply` | Recheck plan, reject conflicts, transact actual editor changes. | 06 is only the data analogy. |
| Same file: `check` | Validate the fixture after a change. | 04, 07 |
| `Content/Python/week07_tools.py` | Public calls and explicit dependency-aware reload. | Instructor's manual editor entry point. |

Trace how a selected Actor becomes ordinary data and where the real engine calls
begin. An Actor is a level instance; its components can reference shared mesh
assets. Renaming or moving an Actor does not rename or rewrite the shared asset.

This source-reading exercise uses the older prop demo. Its W07_PythonLab map and
Northwood assets belong to the full archive and are omitted from the small download.
For a runnable editor exercise, follow the project README's Material/VFX demo.
Do not execute Unreal calls from the VS Code terminal. A stub provides autocomplete
only; it is not a connection to Unreal.

Discussion prompts: What becomes stale when selection changes? Why recheck before
Apply? Why can a rename succeed while validation still reports a missing mesh?
Why does engine Undo need more than a Python deep copy?
