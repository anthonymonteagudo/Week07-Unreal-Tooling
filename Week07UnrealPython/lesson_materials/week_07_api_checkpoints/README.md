# Week 7: runnable API checkpoints

Open the [copyable source guide](../../../Course/Slides/Week07/MaterialsWalkthrough20261013/checkpoints.html) and [latest slide review](../../../Course/Slides/Week07/MaterialsWalkthrough20261013/index.html).

Each complete `.py` file is independent: imports, setup, one topic, and an observable result. Run the file in its named host. Blocks marked `# %%` are teaching segments, not automatic Unreal cells. Within a file, run blocks in order; they share variables. The guide can copy a complete file, one block, or all prerequisites through a block. Re-run setup after changing the selection.

## Teaching order

| Stage | Checkpoints | Concept |
|---|---|---|
| 01 Unreal objects | UE01–UE03 | Host → Actor selection → components |
| 02 Asset inspection | UE04–UE07 | Asset selection → properties → validation → paths |
| 03 Blender comparison | BL01–BL04 | Selection → Object/data → evaluated geometry → FBX |
| 04 Import tasks | UE11–UE12 | Prepare options/task → execute → verify |
| 05 Controlled edits | UE08–UE10 | Eligibility → material override → readback → Niagara inspection |
| 06 Full-tool reasoning | PY01 | Reviewed data becomes stale when inputs change |

Predict the result, run one prepared file, inspect the evidence, then change one input and rerun. As in Week 3, introduce one new API idea at a named run point. The live deck runs selected checkpoints and traces the others; optional deeper examples follow the live sequence.

## Run

- Unreal: open `Week07UnrealPython.uproject`, enable Python Script Plugin, then use Tools → Execute Python Script. Optional Python launcher: `import week07_lessons; week07_lessons.run("UE02")`. It executes the actual source file in a fresh namespace.
- Blender: open a `blender/` source in the Text Editor and Run Script (Alt+P). Read printed output in the system console. Use Object Mode where required.
- PY01: ordinary Python. It illustrates the preview contract with a small dictionary, not the complete production validator.
- Offline inspection: `python Scripts/api_lessons.py list`, `show UE02`, or `check`. These commands do not start a host.

UE08 edits one prepared target’s material override and supports Undo. UE12 refuses an existing destination, imports an unsaved asset, and restores the importer setting even on failure. BL04 writes a new temporary folder. Read each guide entry’s prerequisites, expected evidence and recovery before running.

## Source and verification

`sequence.json` is built by `Scripts/build_api_lesson_catalog.py`. Slide code is extracted from the real marked source blocks by the deck’s `.build/content.mjs`; it is not a separately maintained example. `bindings.json` records the correspondence.

Offline syntax checks and 82 project tests passed, including 13 checkpoint tests with explicit host doubles. New checkpoints have not been executed in Unreal or Blender in this revision. Rehearse in the actual hosts before teaching; these tests do not establish integration behavior. Existing production-demo host evidence is documented separately in the instructor run sheet and the slide demo review.

The original `week_07_unreal_python` sequence remains an ordinary-Python foundations recap with stable IDs. Production implementations remain in `Content/Python`; these files isolate the visible API operations for teaching.

