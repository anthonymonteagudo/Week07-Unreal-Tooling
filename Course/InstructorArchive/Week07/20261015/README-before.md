# Week 7 · Unreal Python Tooling

**Maya / Blender bridge:** [working publishers, source scenes and comparison guide](Docs/Bridge/README.md).
Open `/Game/Week07/Bridge/W07_BridgeComparison` for the FBX + JSON handoff demo.
Both hosts use the same publisher core and Unreal receiver; start the receiver explicitly.

**Live teaching:** [rehearsed Unreal demo, recovery and offline fallback](../Course/Slides/Week07/FinalClass20261013/live-demo.html). Launch `Scripts/launch_live_demo.ps1` for the prepared W07_MaterialVFXLab fixture.

**Start with [Material & VFX Tools: student practice](Docs/Students/START_HERE.md).**
Open [Week07PythonTools.code-workspace](Week07PythonTools.code-workspace) in VS Code.
Use **UI OFFLINE — Week 7: Material and VFX assistants** to open the PySide tool
when ready to rehearse. Practice mode uses fictional data and never contacts Unreal.

**Instructor route:** [demo sequence and compatibility boundaries](Docs/DEMO_SEQUENCE.md).
The current classroom timing and read-aloud sequence are in the live teaching run sheet linked above. The older demo sequence preserves practice-mode context. [The presentation checklist](Docs/UI/PRESENTATION_CHECKLIST.md) contains
captures and the outstanding manual/live checks.

| Role | Entry point | Status |
| --- | --- | --- |
| Primary demo: Material Setup → VFX Placement | [Student tasks](Docs/Students/START_HERE.md), `Scripts/assistants.py` | Practice mode plus live PySide and native Slate workflows rehearsed in UE 5.7.4. |
| Optional Python foundation | [Checkpoints 01–08](lesson_materials/week_07_unreal_python/README.md), `Scripts/lessons.py` | 01–07 run offline; 08 is reading only. These use prop cleanup. |
| Main UI/UX progression | [Material/VFX stages 1–3](lesson_materials/week_07_unreal_python/stage_05_ui_progression/README.md), `Scripts/assistants.py --stage 1` | Same two tools evolve from text review to tables to guided actions, with shared safeguards. |
| Existing editor fallback | Five `w7.run_example(...)` examples below | Six-prop console backend has earlier engine evidence; Material/VFX PySide hosting is now rehearsed. |
| Required native Unreal UI | [EUW specification and bridge](Docs/UI/UNREAL_NATIVE_UI.md) | Implemented C++ Slate editor tab in Plugins/Week07Tools; Preview/Apply and recovery rehearsed. |

The PySide tool is Qt Widgets. A Qt window parented to Unreal is not a native
dockable editor tab. Material/VFX functionality is bounded to prepared assets;
see [scope and guardrails](Docs/UI/MATERIAL_VFX_SCOPE.md).

## Development and earlier prop-demo reference

The sections below retain the established APIs and setup. `w7.preview()`,
`w7.apply(plan)`, `w7.check()` and `w7.reset_demo()` operate on the **prop fixture**,
not the Material/VFX workflows. `w7.show_assistants()` opens the new live PySide
panel once Unreal preparation is complete. `w7.show_ui()` / `show_pyside_ui()`
continue to open the old Prop Inspector for compatibility.

In Unreal, both panels share one window host: opening another stage/tool replaces
the current panel. `reload_tools()` and every `run_example()` close that panel and
expire native sessions/previews. Finish a demonstration before switching; reopen
and make a fresh preview after reload. Neither action saves the map.

For offline code checks, run `Scripts/dev.py check`, `Scripts/dev.py test`, and
`Scripts/ui_quality.py --stage 3` with `.venv/Scripts/python.exe`. Engine tests and
stub generation below explicitly launch Unreal; they are separate preparation.
If VS Code reports Restricted Mode, review Workspace Trust before enabling tasks.

## The edit / run loop

1. In VS Code, edit a file under `Content/Python/week07_tooling` and save it.
2. In Unreal, open **Output Log** and choose **Python** beside the command field.
3. Run the following **in Unreal**, one line at a time:

```python
import week07_tools as w7
w7.reload_tools()
w7.list_examples()
w7.run_example('01_hello_editor')
```

`run_example()` reloads the implementation and loaded examples before running one lesson. Importing the package and reloading it never modifies the scene. If you edit `week07_tools.py` itself (including its example list), reload that entry module first:

```python
import importlib
importlib.reload(w7)
w7.reload_tools()
```

**The terminal's Python is for pure code and tests.** Unreal supplies the real `unreal` module inside the editor. VS Code's green “Run Python File” button cannot run editor scripts against the open project. There is no remote-execution service or automatic code watcher in this setup.

## Start with these files

| Path | Purpose |
| --- | --- |
| `Content/Python/week07_tooling/ui/` | UI workflow, three presentations, offline backend and explicit Unreal window lifecycle. |
| `Content/Python/week07_tooling/editor/ui_backend.py` | Live UI adapter to the existing guarded demo functions. |
| `Docs/DEMO_SEQUENCE.md` | Canonical Material/VFX demo order and compatibility boundaries. |
| `Docs/UI/README.md` | Earlier Prop Inspector reference and shared dependency setup. |
| `Content/Python/week07_tooling/workflows.py` | Primary Material/VFX pure rules and preview/apply session. |
| `Content/Python/week07_tooling/editor/workflow_backend.py` | Material/VFX Unreal adapter; prepared UE 5.7.4 fixture rehearsed. See Docs/DEMO_SEQUENCE.md for scope. |
| `lesson_materials/week_07_unreal_python/` | Optional prop foundations: stages, checkpoints, expected observations and lab starter. |
| `Scripts/lessons.py` | List/run ordinary Python checkpoints; refuses the reading-only editor handoff. |
| `Content/Python/week07_tools.py` | Stable entry point, example list and dependency-aware reload. Existing slide/demo commands still work. |
| `Content/Python/week07_tooling/examples/` | Five integrated editor examples with explicit `run()` functions; separate from the draft checkpoint numbering. |
| `Content/Python/week07_tooling/editor/demo.py` | Unreal selection, scene reads, changes, transactions and reports. |
| `Content/Python/week07_tooling/rules.py` | Pure calculations and validation of ordinary Python data. No Unreal imports. |
| `Content/Python/week07_tooling/config.py` | Demo map, tags, fixture IDs and baseline values. |
| `Tests/test_rules.py` | Tests runnable directly in VS Code. |
| `Scripts/editor/smoke_test.py` | Integration checks in an isolated full editor process; no map saves. |
| `Scripts/dev.py` | Setup, syntax, tests, autocomplete and environment checks. |
| `Scripts/templates/editor_example.py` | A read-only starting point for another lesson. |
| `Scripts/build_week07.py` | One-time fixture builder; refuses to overwrite the existing map. |
| `Scripts/capture_week07.py` | Existing full-editor capture automation. |
| `Reference/LegacyPython/` | Original study scripts, retained with disabled extensions. |

Keep application-independent calculations in `rules.py` (or another pure module as the tools grow). Let an editor adapter collect scene data and apply approved changes. Keep examples small and call the same implementation the demo uses.

Unreal automatically discovers `Content/Python`. Do not put this code under a second source root or add machine-specific paths to classroom examples. There is deliberately no `init_unreal.py` that changes a scene at startup.

## The five integrated editor examples

| Example | What to show |
| --- | --- |
| `01_hello_editor` | Unreal's engine and project context; a simple log message. |
| `02_inspect_selection` | Actor → Component → mesh asset; level vs Content Browser selection. |
| `03_preview_changes` | Return an inspectable change plan without editing. |
| `04_apply_reviewed_plan` | Require an explicit plan and group changes into one Undo action. |
| `05_validate_fixture` | Verify against fixture-specific rules and report failures. |

On `/Game/Week07/Maps/W07_PythonLab`, use this rehearsal sequence:

```python
w7.select_demo()
w7.run_example('02_inspect_selection')
plan = w7.run_example('03_preview_changes')
# Read the before/after output before continuing.
w7.run_example('04_apply_reviewed_plan', plan=plan)
w7.run_example('05_validate_fixture')
```

Use **Edit → Undo Week 7: organize selected props** to recover in one step. `w7.reset_demo()` restores the seed arrangement for another rehearsal. Neither Apply nor Reset saves the map. `w7.capture_view()` pilots the saved camera; `w7.capture_view(False)` returns to ordinary navigation. Do not fly the camera while piloting if you want repeatable framing.

Old commands such as `w7.preview()`, `w7.apply(plan)` and `w7.check()` remain available. After changing rules or selection, make and review a fresh preview.

## VS Code tasks and debugging

Use **Terminal → Run Task**:

- **Week 7 Python: check Python syntax** — also the default build task (`Ctrl+Shift+B`).
- **Week 7 Python: list draft checkpoints** — prints the provisional order and file paths.
- **Week 7 Python: run draft checkpoint** — choose 01–07; runs on sample data without Unreal.
- **Week 7 Python: test pure Python rules** — production rules plus offline checkpoint tests, no editor required.
- **Week 7 Python: check development setup** — reports interpreter, engine and stub availability.
- **ENGINE — Week 7: test in separate Unreal editor** — launches a full editor process; not part of code-only preparation.
- **ENGINE — Week 7: refresh Unreal autocomplete** — launches a full editor to generate the stub; not part of code-only preparation.

The **Testing** panel discovers the files under `Tests/`. For step-by-step teaching, choose **Debug draft checkpoint (ordinary Python)** in Run and Debug, select a step, and set a breakpoint in its file. **Debug pure Python rule tests (outside Unreal)** runs the full offline suite. Attaching a debugger to the embedded Unreal interpreter is optional future work; these launch configurations do not imply such an attachment.

The local `.venv` uses Unreal's Python **3.11.8**. Core rules and console examples require no third-party dependencies. The UI uses pinned PySide6 Essentials and Shiboken in ignored `.deps/ui`; pip has now been enabled in the local venv to install those project-local packages. See the UI guide for reproducible setup. Python, Pylance and Python Debugger were already installed in VS Code. If VS Code shows a different interpreter, run **Python: Select Interpreter** and select `.venv/Scripts/python.exe`.

Autocomplete points to `Intermediate/PythonStub/unreal.py`, generated from this project's enabled plugins. Developer Mode is enabled for this tooling project. The stub is analysis-only: never add its directory to runtime `PYTHONPATH` or copy it into `Content/Python`. Regenerate it after engine/plugin changes. The Explorer hides generated directories and binary Unreal assets to keep code browsing clear; these files still exist and remain visible in Unreal.

## Add an example

1. Copy `Scripts/templates/editor_example.py` to `Content/Python/week07_tooling/examples/e06_my_example.py`.
2. Keep work in `run()`; importing a module should not perform the lesson's action.
3. Add `'06_my_example': 'A short scope/behavior description.'` to `_EXAMPLES` in `week07_tools.py`.
4. Reload the entry module as shown above, then run `w7.run_example('06_my_example')` in Unreal.
5. Put reusable rules in a pure module and test them outside Unreal. Add editor regression coverage when the tool changes scene behavior.

When adding a new shared module, add it to the dependency order in `reload_tools()` so it reloads before its consumers. Reloading does not refresh local variables imported with `from ... import ...` in your console; prefer `import week07_tools as w7` and call through `w7`.

## Setup on another machine

From the project root with a compatible installed Python:

```powershell
python Scripts/dev.py setup --engine-root 'C:/Program Files/Epic Games/UE_5.7'
./.venv/Scripts/python.exe Scripts/dev.py stubs
./.venv/Scripts/python.exe Scripts/dev.py doctor
```

The engine path is recorded only in ignored `.vscode/unreal.local.json`. The workspace and examples use relative paths. If you move the project or change Python installations, recreate the local `.venv` rather than copying it between machines.

Keep `.venv`, `Intermediate`, `Saved`, caches, logs and bytecode out of Perforce. The project contains local ignore rules; the parent workspace also ignores Unreal generated folders. No changelist has been submitted.

## Provenance and teaching context

Prof. Monteagudo confirmed on **10 October 2026** that the original **Northwood** project resulted from working through Isaac Oster's public online course, **Utilizing Python for Editor Scripting in Unreal Engine**. The compiled notes cover sources he had already reviewed. **Week07UnrealPython** is the subsequent classroom-preparation spinoff. Its fixture, controlled-edit tools, tests, VS Code workspace and captures were added during Week 7 preparation.

- [Compiled Week 7 prep notes](../Course/Slides/Week07/PrepNotes/index.html)
- [Earlier prop-fixture run sheet and captures](../Course/Slides/Week07/UnrealPythonDemo/index.html)
- [Project quick start](START_HERE.txt)

Batch FBX import, the final student lab and in-editor debugger attachment are still future examples. The current validator checks this teaching fixture, not all assets in Northwood.

API/setup references: [Epic Python autocomplete](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-autocomplete-for-editor-python-scripting-in-unreal-engine), [VS Code Python settings](https://code.visualstudio.com/docs/python/settings-reference), and [VS Code Python testing](https://code.visualstudio.com/docs/python/testing).

