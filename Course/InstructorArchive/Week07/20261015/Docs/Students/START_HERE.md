# Week 7 · Material & VFX Tools

**Your workflow: Choose → Preview → Apply → Check.**

Use two small tools to automate repeated work. Material Setup creates and assigns
a material instance. VFX Placement places a prepared effect at selected markers.
Both show the proposed changes before you apply them.

## Start in practice mode

Open `Week07PythonTools.code-workspace` in VS Code. Choose **Terminal → Run Task →
UI OFFLINE — Week 7: Material and VFX assistants**.

Alternatively, from the project folder:

```powershell
./.venv/Scripts/python.exe Scripts/assistants.py
```

The window must say **PRACTICE MODE**. This is a real PySide interface using sample
data. No Unreal session is needed, and no files or Actors are created by the sample.
Selections are supplied for you; clicking in Unreal will not affect practice mode.
If the window cannot start, ask your instructor to check the project environment.

**Reset practice data** restores both sample workflows. Your input fields remain
as you entered them; the current preview is cleared. Closing/reopening also starts
with a fresh sample.

Changing inputs clears the current preview; it does not undo work already applied. Use the appropriate reset or recovery action for the current mode.

## Task 1 · Set up a material instance

**Goal:** assign one prepared surface to the sample crate.

1. Open **Material Setup**. Leave **Parent material** on *Prepared surface · practice*.
2. Use **MI_Crate_Demo** as the new instance name and material slot **0**.
   This practice crate has only slot 0; choosing another slot produces a message
   asking you to return to slot 0 and preview again.
3. Select **Preview changes**. Read the summary: **1 new material instance · 1 component assignment**.
4. In the table, identify the parent, the three textures and the component receiving
   the assignment. Check the **Before** and **After Apply** columns.
5. Select **Apply: create 1 instance**. The status becomes **Completed**, and the
   table changes to **Applied change**. Apply is disabled because that preview has
   already been used.
6. Select **Preview changes** again with the same name. Creation should be blocked
   because the instance already exists. Choose a different name or reset the sample.

**Check your understanding:** did this task create a new material graph, change the
parent, change the shared mesh asset, or assign a component override?

![Material Setup preview in practice mode](../UI/captures/material_preview.png)

## Task 2 · Place prepared VFX

**Goal:** place one prepared steam effect at each of three sample markers.

1. Open **VFX Placement**. Choose *Steam · practice* and leave **Effect scale** at **1.00×**.
2. Select **Preview changes**. Expect **3 anchors → 3 new effects** and a loaded
   component count changing from **0 to 3**.
3. Review each marker's position in centimeters and rotation in degrees.
4. Select **Apply: place 3 effects**. Check the completion message and applied rows.
5. Preview again using the same markers. Duplicate placement should be blocked.
6. Select **Reset practice data** to repeat the task.

**Check your understanding:** scale changes the effect's size. Does that tell you
its particle count, screen coverage or frame cost? Why should a placement tool
refuse to pile repeated effects onto the same marker?

![VFX Placement preview in practice mode](../UI/captures/vfx_preview.png)

## See the same tools evolve

The default practice tool is **Stage 3 · Refined**. For the UI/UX comparison, use
**UI OFFLINE — Week 7: open teaching stage** and choose 1, 2 or 3. Stage 1 shows a
text review, stage 2 adds comparison tables and guidance, and stage 3 adds progress
cues and counted actions. Both tasks and their safeguards remain the same.
Earlier stages use the button **Apply reviewed changes**. Each launch starts with
fresh practice data. Follow [the stage guide](../../lesson_materials/week_07_unreal_python/stage_05_ui_progression/README.md)
when your instructor demonstrates the progression.

## Read feedback before retrying

| Message | Meaning | Your next action |
| --- | --- | --- |
| Ready to preview | There is no reviewed plan yet. | Choose inputs and preview. |
| Ready to apply | The proposed changes passed the current checks. | Review the table before applying. |
| Review needed | A density warning needs attention. | Read the placement count; reduce the live selection if appropriate. Acknowledge only after reviewing. |
| Needs attention | Preview could not produce an acceptable plan. | Fix the named problem and preview again. |
| Completed | The operation returned successfully. | Inspect the applied result; don't repeat Apply. |
| Apply stopped | The operation refused or failed. | Read the message and inspect any reported partial result before making a fresh preview. |
| Instructor setup needed | A prepared parent or reviewed effect is unavailable. | Ask your instructor; do not guess asset paths or bypass checks. |

Changing a field or switching tools clears the preview. Apply rechecks the current
selection and scene. A checked warning box never overrides a hard placement limit.

## Words used in the tools

| Term | Meaning here |
| --- | --- |
| Parent material | An existing material that exposes parameters. The tool does not edit its graph. |
| Material instance | An asset using that parent with particular parameter values, such as texture references. |
| Material slot | A numbered assignment on a mesh component. The first slot is 0. |
| Component override | A material assignment for that Actor's component; the shared mesh asset is unchanged. |
| ORM | One texture carrying occlusion, roughness and metallic data in separate channels. |
| Anchor / marker | A selected Actor whose position and rotation define where an effect goes. |
| Effect preset | An instructor-reviewed Niagara System plus placement policy. |
| Preview | A proposed operation; reading it does not apply it. |

## When your instructor demonstrates the Unreal version

The header says **UNREAL EDITOR**. Material Setup reads texture selection from the
Content Browser and Actor selection from the viewport/Outliner. These are different
selections. VFX Placement reads the instructor's tagged markers. The prepared
choices come from the project catalogue, not from student-entered paths.

Check the actual result in the editor: material assignments on the intended slots,
and effect placement/orientation at the intended markers. The tool does not save
automatically. Assignment Undo and new material-asset cleanup are separate concerns;
follow your instructor's save/reset instructions. The practice reset button is not
available in the live tool.

The native dockable Unreal interface is still being prepared. Current screenshots
show **PySide practice mode**, not a completed native Unreal tab.

## What passing validation means

The tool checks things it can establish: known inputs, counts, spacing, duplicate
placements and whether the reviewed plan is still current. Its VFX policy is a
classroom guardrail, not a measured performance budget. Fewer effects can still be
expensive. Learn to say **“placement checks passed”**, then measure performance in
the appropriate rendering/optimization exercise.

## Follow the code after trying the task

Read only the current step; you do not need to understand the whole project at once.

| Step | File | Question to answer |
| --- | --- | --- |
| 1 · Inputs | [workflow_sample.py](../../Content/Python/week07_tooling/workflow_sample.py) | What data describes a texture, target or marker? |
| 2 · Rules | [workflows.py](../../Content/Python/week07_tooling/workflows.py) | What must be true before a plan can be created? |
| 3 · Review | [workflow_presentation.py](../../Content/Python/week07_tooling/workflow_presentation.py) | How does plan data become readable before/after rows? |
| 4 · Interaction | [assistants.py](../../Content/Python/week07_tooling/ui/assistants.py) | Which events invalidate a preview or enable Apply? |
| 5 · Host boundary | [workflow_backend.py](../../Content/Python/week07_tooling/editor/workflow_backend.py) | Where do data operations become actual Unreal API calls? |

Optional Python recap: [the numbered checkpoints](../../lesson_materials/week_07_unreal_python/README.md).
Those checkpoints introduce the same read → plan → apply distinction with a smaller
prop-cleanup example. They are reference exercises, not additional required tasks.
