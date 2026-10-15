# Week 7: Python tools in Unreal

Open `Week07UnrealPython.uproject` in **Unreal 5.7.4**. The prepared Material and
VFX map is `/Game/Week07/Maps/W07_MaterialVFXLab`.

## Try the tools

1. Open **Window > Output Log**, choose **Python**, and run:
   ```python
   from week07_tooling.editor import live_demo
   print(live_demo.preflight())
   ```
   This checks the clean scene and selects the target crate and three textures.
2. Open **Tools > Material & VFX Tools**. In **Material Setup**, enter an unused
   `MI_` name and keep slot **0**. Click **Preview**.
3. Compare **Before** with **After Apply**. Hover an asset name for its full path.
   Click **Apply: create instance**. The column becomes **Result**.
4. Check the target crate. The protected crate and shared Cube mesh stay unchanged.
5. In Output Log > Python, run `live_demo.select_vfx()`. In the tool, choose
   **VFX Placement**, leave scale at **1**, then **Preview** and **Apply: place 3 effects**.
   Inspect the three fountains in the scene.

Preview again to see duplicate protection. If inputs or selection change, make a
fresh preview. A density warning needs review; it does not bypass a hard limit.
Placement checks do not measure frame cost. The tools do not save automatically.

## Recover and repeat

Check **Edit > Undo** before using it. The expected operation is
**Week 7: assign prepared material instance** or **Week 7: place reviewed VFX**.
Undoing the assignment leaves the new material asset; use another unused name.
Undoing placement removes that batch. Camera piloting can add a separate Undo entry.
To return to the saved fixture, close and reopen without saving rehearsal changes.
Do not discard unrelated work.

## Compare the PySide interface

In Unreal's Python console:
```python
import week07_tools as w7
w7.show_assistants()
```
This external Qt window uses the same live workflow. **UNREAL EDITOR** in its
header identifies live mode. Native Slate remains the menu-based interface above.

For sample data without Unreal, from the project folder:
```powershell
./.venv/Scripts/python.exe Scripts/assistants.py
```
The header says **PRACTICE MODE**. **Reset practice data** restores both sample
workflows. Add `--stage 1` or `--stage 2` to compare the earlier UI stages.

## Follow the lesson

Use the numbered files in `lesson_materials/week_07_api_checkpoints` when directed
by the slides. Each file identifies its host: Unreal, Blender or ordinary Python.
The lab starter is in `lesson_materials/week_07_unreal_python/stage_04_lab_starter`.
The optional Maya/Blender bridge has one quick start inside
`Deliverables/Week07_Bridge_Student_Pack.zip`.

## Environment setup

The native menu requires the included **Week07Tools** plugin. If another machine
asks to rebuild it, use a compatible Unreal C++ toolchain. PySide additionally needs
Python 3.11 and the pinned packages in `requirements-ui.txt` installed in `.deps/ui`.
With the prepared project interpreter:
```powershell
./.venv/Scripts/python.exe -m pip install --target .deps/ui -r requirements-ui.txt
```
Unreal discovers `Content/Python` automatically. `Intermediate/PythonStub/unreal.py`
is for autocomplete only; never put the stub on the runtime Python path.

## Attribution

This classroom project grew from Prof. Monteagudo's Northwood work following
Isaac Oster's public Unreal Python course. The current fixtures, tools and tests
were developed for Week 7.
