# Foundation sequence assessment — updated 13 October 2026

Main demo: **Material Setup → VFX Placement**, using [the canonical route](../../Docs/DEMO_SEQUENCE.md).
The numbered prop checkpoints below are optional foundations. Their stable IDs are
retained; they do not number the main demo or the slides.

## Why this order

Week 3 already introduced values, collections, loops, functions and an asset report
before host-specific operations. Steps 01–04 reactivate those ideas with
Actor-shaped dictionaries. They can be compressed into a recap if students retain
the Week 3 material. Keep scope selection explicit: a mixed selection is a common
reason a seemingly simple batch operation becomes dangerous or confusing.

Steps 05–06 separate a report (what is wrong), a plan (what we propose to change),
and application (what changes). Students can inspect each value and use VS Code
breakpoints without needing an editor session. A missing mesh deliberately survives
the rename operation: a successful fix is not proof that everything is valid.

Step 07 replaces repeated teaching functions with the project's tested pure rules.
It adds placement and fixture IDs, then makes the boundary with Unreal visible.
Step 08 is where selection, Actor/Component/asset distinctions, transactions and
manual reload belong when the slides and the live demo are ready.

## Differences worth discussing

- Step 02 filters mixed data and reports exclusions. The live adapter deliberately
  rejects mixed selections before applying changes. Filtering is an introductory
  exercise, not a promise of identical production behavior.
- Steps 03–06 derive names from trusted sample `kind` values. Production rules map
  known fixture IDs to kinds and validate IDs, paths and coordinates.
- Step 06 checks the proposed rename list against a fresh list. It is an in-memory
  exercise, not full scene concurrency protection. The editor adapter also checks
  world, selection, full states, collisions and editor mode.
- A deep copy is not an Unreal transaction. Editor Undo must be taught separately.
- Production plans include all selected records, even already-correct ones. The
  introductory rename plan lists only changes. Inspect this difference in Step 07.

## Decisions waiting on the slides

| Decision | Current placeholder | Consequence for sequence |
| --- | --- | --- |
| How much Python recap? | Four tiny checkpoints | Compress 01–04 without deleting reference files. |
| Main tool scope (decided) | Material Setup and VFX Placement | Prop cleanup is a supporting example; batch import is outside this demo. |
| Where to introduce placement? | Step 07 only | Split it into another pure checkpoint if vectors need teaching time. |
| Student lab deliverable? | Reporting a missing mesh | Finalize inputs and acceptance criteria before numbering the lab. |
| Required UI progression | Material/VFX implement functional / guided / refined stages | Compare identical inputs and operations across text review, structured review and guided actions. |
| Exact slide positions? | Demo beats D1–D6 are defined in the canonical route | Map these beats to slide numbers when the deck settles. |

No lecture timings, slide numbers, lab grading rules, or capture claims are final.
The new checkpoints have not been rehearsed inside Unreal; they are offline Python.

The instructor subsequently confirmed that a clean UI is mandatory. See
[the staged UI progression](stage_05_ui_progression/README.md) and its separate
automated, visual, and live-hosting gates. Console-only is no longer the intended
finished tool experience.

## Organization references and provenance

- Week 3: `D:/Personal Projects/Week3_StudentMaterial/week03_student_materials/week03_student_materials/lesson_materials/week_03_python_and_maya`.
  The staged Python → UI → host progression and expected-result instructions informed this draft.
- SimonDev: `C:/Users/antho/Downloads/project-source`, especially its numbered topic
  folders, Blank/example checkpoints, `START-HERE.txt` and workspace. Organization only.
- Original Northwood: instructor's work through Isaac Oster's public **Utilizing
  Python for Editor Scripting in Unreal Engine** course. Week07UnrealPython is the
  later classroom-preparation spinoff. The new sequence is a draft for this class,
  not a reconstruction or attribution of these steps to Oster or SimonDev.
