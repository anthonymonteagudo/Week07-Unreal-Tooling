# Week 7 Python tooling — draft checkpoints

For the main student-facing Material Setup and VFX Placement activities, use
[the student quick-start](../../Docs/Students/START_HERE.md). The small prop-based
checkpoints below are an optional code recap, with stable IDs retained for reference.

Use these for an **optional VS Code foundations recap**. Steps 01–07 operate on invented records in
memory. They do not read, connect to, save, or change the open Unreal project.
Step 08 is a reading guide for a later manual editor demo.

The structure follows Week 3's `lesson_materials` → numbered stages → small steps,
and SimonDev's separate lesson checkpoints. This is an organizational reference;
no SimonDev shader implementation was copied. Each step starts fresh, so open the
current file and compare it to the preceding checkpoint without running them all.
Short naming functions intentionally repeat to keep checkpoints readable. Step 07
then shows where reusable production code belongs.

## Run and debug

From the project root in the VS Code terminal:

```powershell
./.venv/Scripts/python.exe Scripts/lessons.py list
./.venv/Scripts/python.exe Scripts/lessons.py run 01
```

Use **Terminal → Run Task → Week 7 Python: run draft checkpoint** to choose a step.
Use **Run and Debug → Debug draft checkpoint (ordinary Python)** and set a breakpoint
in the selected step. The runner supplies the shared sample-data and project import
paths. Run checkpoints through this runner, rather than the file's green Run button;
each file defines `main()` and leaves execution to the runner.

Output is JSON in the terminal. No generated files or dependencies are needed.
The data source is [sample_data.py](sample_data.py), explicitly fictional and smaller
than the six-prop Unreal fixture. Paths beginning `sample://` are identifiers only.

## Open one stage at a time

| Stage | Steps | Check before moving on |
| --- | --- | --- |
| [00 · Data and scope](stage_00_data_and_scope/README.md) | 01–02 | Four records; only three tagged props belong to this tool. |
| [01 · Rules and reports](stage_01_rules_and_reports/README.md) | 03–04 | Two label issues and one missing mesh; nothing changes. |
| [02 · Preview and apply](stage_02_preview_and_apply/README.md) | 05–06 | Two proposed renames; corrected copy, unchanged original; missing mesh remains. |
| [03 · Project bridge](stage_03_project_bridge/README.md) | 07–08 | Real pure rules add placement; host access lives in the editor adapter. |
| [04 · Lab starter](stage_04_lab_starter/README.md) | unnumbered | Optional exercise to shape after lecture/lab scope is settled. |
| [05 · UI progression](stage_05_ui_progression/README.md) | UI 1–3 | Material/VFX functional → guided → refined; same tools and safeguards, Qt captures and gates. |

For the main demo, follow [the canonical route](../../Docs/DEMO_SEQUENCE.md).
Read [SEQUENCING.md](SEQUENCING.md) for the teaching rationale and open decisions.
Step IDs identify checkpoints, **not slides**. The earlier five `w7.run_example()`
commands remain the integrated editor demo; they are not this new step numbering.

## Add or reorder a checkpoint

1. Copy the nearest small checkpoint into the appropriate stage. Keep its action in
   `main()` and its inputs ordinary Python data.
2. Add a unique stable ID, title, runtime and relative file to `sequence.json`.
   List order controls teaching order; keep IDs stable when slides move.
3. For a runnable offline step use `runtime: "python"`. Use `reading` for the host
   handoff. Never add an engine launcher to this offline runner.
4. Update the stage's expected observations and the VS Code pick lists in
   `.vscode/tasks.json` and `.vscode/launch.json`.
5. Run `Scripts/dev.py check` and `Scripts/dev.py test` with the local interpreter.

The pure checkpoints teach label repair first. The separate UI progression evolves the Material/VFX tools through three
presentations; it does not require continuing the prop-cleanup task. Generic asset validation,
FBX import and remote execution remain outside this draft. The live adapter uses
the existing Unreal transaction behavior; its new UI hosting still needs rehearsal.
