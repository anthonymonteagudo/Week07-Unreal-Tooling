# Week 7 Material and VFX demo

**Windows + Unreal 5.7.4.** The two classroom labs can be completed without installing this demo. Use this project when you want to run the tools shown in the slides.

## First setup

1. Install Unreal **5.7.4** through Epic Games Launcher. Extract the entire demo ZIP to a writable folder outside the ZIP viewer.
2. Open PowerShell in this folder and run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\Setup.ps1
   ```
   If Unreal is installed elsewhere, add `-EngineRoot 'D:\Epic Games\UE_5.7'`.
3. Open `Week07UnrealPython.uproject`. The prepared **W07_MaterialVFXLab** map opens automatically. If you opened another map, find `Content/Week07/Maps/W07_MaterialVFXLab` in the Content Browser and double-click it.

Setup uses Unreal's bundled Python and the included native plugin. No separate Python or Visual Studio installation is needed. Success ends with **Setup complete**. If the module build does not match, use the exact engine version above; instructor rebuild instructions are in the repository's `Instructor` folder.

## Try the two tools

1. Open **Window > Output Log**, choose **Python**, and run:
   ```python
   from week07_tooling.editor import live_demo
   print(live_demo.preflight())
   ```
   Expect **Material & VFX: ready**. The target crate and three textures are selected. Keep Play in Editor stopped.
2. Open **Tools > Material & VFX Tools**. Choose **Material Setup**, enter a new name such as `MI_Student_01` and keep slot **0**. Click **Preview**.
3. Inspect **Before** and **After Apply**, then click **Apply: create instance**. The target changes; the protected crate and shared Cube mesh stay unchanged.
4. Run `live_demo.select_vfx()` in the Python log. In the panel, choose **VFX Placement**, keep scale **1**, then Preview and **Apply: place 3 effects**. Inspect the three fountains.

Selecting any one of the matching BaseColor, Normal or ORM textures is sufficient.
The tool finds the other members by exact name in the same folder and shows all three
in Preview. Missing textures and invalid settings block Apply with a specific reason.
**Refresh selection** lists current inputs; **Preview** validates and enables Apply.

For Python-only updates in a running editor, run
`import week07_tools as w7; w7.reload_tools()`, then **Reconnect > Preview**.
For native plugin updates, close Unreal, pull the update and rerun `Setup.ps1` before reopening.

Preview again to see duplicate protection. Changed inputs need a fresh preview. Placement checks do not measure frame cost. The tools do not save automatically.

## Reset

Check **Edit > Undo** before using it. The expected operation is **Week 7: assign prepared material instance** or **Week 7: place reviewed VFX**. Undoing assignment leaves the new material asset; use another unused name. Undoing placement removes that batch. Camera piloting may add a separate Undo entry.

For a clean start, close and reopen this demo without saving rehearsal changes. Keep unrelated work in a separate project. If you saved a changed fixture, extract a fresh copy of the demo ZIP to a new folder.

## Optional PySide comparison

Run setup again with `-WithQt` to install the pinned Qt packages (internet required):
```powershell
powershell -ExecutionPolicy Bypass -File .\Setup.ps1 -WithQt
.\.venv\Scripts\python.exe Scripts/assistants.py
```
This opens **PRACTICE MODE** with sample data and a reset button. Add `--stage 1` or `--stage 2` to compare the earlier UI stages. Close the practice window when finished.

For the live external Qt window, run inside Unreal:
```python
import week07_tools as w7
w7.show_assistants()
```
Its header says **UNREAL EDITOR**. Native Slate remains the menu panel above.

## Examples and optional bridge

[Numbered examples](lesson_materials/week_07_api_checkpoints/README.md) keep the lesson IDs used by the slides. Run each in its named host. The [bridge quick start](BRIDGE.md) covers the optional Maya/Blender comparison. The earlier prop-based Python recap remains optional; it is not Lab 1.

This classroom project grew from Prof. Monteagudo's Northwood study following Isaac Oster's public Unreal Python course. The prepared Week 7 download does not include the older Northwood environment.


## Walk from the tool to its code

Start with the workflow, then open the Unreal adapter when explaining engine calls.
The native and PySide interfaces use the same workflow; they are not two implementations
of the material/VFX rules. Use the editor's Go to Symbol to jump to the names below.

| Tool action or behavior | Code to open | Function to explain |
| --- | --- | --- |
| Preview: capture inputs and build a plan | [workflows.py](Content/Python/week07_tooling/workflows.py) | `WorkflowSession.preview` |
| Material validation and proposed assignments | [workflows.py](Content/Python/week07_tooling/workflows.py) | `material_plan` |
| VFX placement checks and proposed transforms | [workflows.py](Content/Python/week07_tooling/workflows.py) | `vfx_plan` |
| Read selected Actors, components and textures | [workflow_backend.py](Content/Python/week07_tooling/editor/workflow_backend.py) | `EditorWorkflowBackend.snapshot` |
| Find matching textures from one selected member | [workflow_backend.py](Content/Python/week07_tooling/editor/workflow_backend.py) | `resolve_texture_assets` |
| Apply: reject a stale preview before editing | [workflows.py](Content/Python/week07_tooling/workflows.py) | `WorkflowSession.apply` |
| Create an instance, set textures and assign overrides | [workflow_backend.py](Content/Python/week07_tooling/editor/workflow_backend.py) | `EditorWorkflowBackend._material` |
| Spawn effects at the reviewed anchor transforms | [workflow_backend.py](Content/Python/week07_tooling/editor/workflow_backend.py) | `EditorWorkflowBackend._vfx` |
| Fill Before / After Apply rows | [workflow_presentation.py](Content/Python/week07_tooling/workflow_presentation.py) | `describe_plan` |
| Route native buttons to Python | [native_panel.py](Content/Python/week07_tooling/editor/native_panel.py) | `dispatch` |
| Wire the native buttons and enabled state | [Week07Tools.cpp](Plugins/Week07Tools/Source/Week07Tools/Private/Week07Tools.cpp) | `SWeek07Tools::Action`, `Construct` |
| Wire the equivalent PySide buttons | [assistants.py](Content/Python/week07_tooling/ui/assistants.py) | `AssistantWindow.preview`, `apply` |

For a short walkthrough: Preview -> snapshot -> material_plan or vfx_plan -> Apply ->
_material or _vfx. Show the UI wiring afterward. Each numbered checkpoint remains a
standalone example for explaining an individual API operation before the full tool.
The `# Section:` comments name teaching sections; the loader uses those names to extract
examples. They are ordinary Python comments, with no editor-cell percent markers.
