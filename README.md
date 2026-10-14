# Week 7 Unreal Tooling — private WIP archive

Full Week07UnrealPython working project and Week 7 teaching WIP, including the
Maya/Blender FBX + JSON bridge. Binary Unreal assets, source scenes, decks and
packages use Git LFS. Run `git lfs install` before cloning/pulling.

- Start: Week07UnrealPython/README.md
- Bridge: Week07UnrealPython/Docs/Bridge/README.md
- Current deck: Course/Slides/Week07/CheckpointDeck20261013/output/Week_7_Runnable_API_Checkpoints_v8.pptx
- Maya/Blender implementation comparison: Week07UnrealPython/Docs/Bridge/parity.html
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

The full project includes native plugin source; build the Week07Tools plugin with
the matching UE 5.7 development tools if the editor requests missing binaries.
The small bridge student package has no custom C++ plugin dependency.
