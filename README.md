# Week 7 Unreal Tooling and class materials

**Current assessment snapshot: 15 October 2026.**

Start with [StudentMaterials](StudentMaterials/README.md): the class section guide, Lab 1 batch-renaming handout and Lab 2 peer-review packet are available as PDFs.

- [Current project quick start](Week07UnrealPython/README.md)
- [Runnable Unreal and Blender examples](Week07UnrealPython/lesson_materials/week_07_api_checkpoints/README.md)
- [Current slides: Ordered Lessons v9.1](Course/Slides/Week07/LiveCleanup20261015/output/Week%207%20-%20Ordered%20Lessons%20v9.1.pptx)
- [Current instructor class pack](Course/Slides/Week07/LiveCleanup20261015/index.html) (open locally after cloning)

Use Unreal 5.7.4. Run `git lfs install` before cloning and `git lfs pull` afterward. Local Python environments and PySide dependencies are excluded; follow the project quick start to install them. The missing-mesh starter remains an optional draft, not a finalized or graded assignment.

The native and live PySide tools have recorded Unreal rehearsal evidence in the current class pack. The checkpoint guide distinguishes offline checks from real-host verification. This private assessment archive also contains instructor materials and older drafts; `StudentMaterials` is the current handout entry point.

Full Week07UnrealPython working project and Week 7 teaching WIP, including the
Maya/Blender FBX + JSON bridge. Binary Unreal assets, source scenes, decks and
packages use Git LFS. Run `git lfs install` before cloning/pulling.

- Start: Week07UnrealPython/README.md
- Archived bridge notes: Course/InstructorArchive/Week07/20261015/Docs/Bridge/README.md
- Previous checkpoint deck: Course/Slides/Week07/CheckpointDeck20261013/output/Week_7_Runnable_API_Checkpoints_v8.pptx
- Archived Maya/Blender comparison: Course/InstructorArchive/Week07/20261015/Docs/Bridge/parity.html
- Companion comparison slide: Course/Slides/Week07/BridgeRehearsal20261013/output/Maya_Blender_Bridge_Parity_v2.pptx
- Small self-contained bridge: Week07UnrealPython/Deliverables/Week07_Bridge_Student_Pack.zip
- Actual UI captures, slide draft and Karol review: Course/Slides/Week07/BridgeRehearsal20261013/index.html

This is an instructor WIP archive. Northwood preserves its Isaac Oster course
provenance and includes third-party assets; this private backup is not a public
redistribution license. Karol download archives are reference material, not copied
into this repository. Generated caches, installed dependencies, local editor
state, lock/backup files and generated intermediate slide renders/decks are omitted.
Editable `.build` scripts and small supporting JSON are retained. Shared course
readers, visuals, wiki sources and references are included to support teaching links.
The Android
file-server local security token is blanked in this backup.

The active authoring workspace remains in Perforce. This repository is a separate
Git snapshot at C:/Users/antho/git/Week07-Unreal-Tooling; subsequent Perforce edits
must be synced and committed explicitly. Run `python sync_from_workspace.py <workspace>`
to update this snapshot, review `git diff`, then commit/push. It never deletes or
publishes files. `snapshot-inventory.json` records scope and exclusions.
No unrelated student folders are copied.

Superseded project guides are preserved under `Course/InstructorArchive/Week07`.
Review source removals separately because the sync script does not delete them.
Run `python build_student_materials.py` with ReportLab installed to refresh the
student PDFs from the current reviewed handout exports and section guide source.

The full project includes native plugin source; build the Week07Tools plugin with
the matching UE 5.7 development tools if the editor requests missing binaries.
The small bridge student package has no custom C++ plugin dependency.
