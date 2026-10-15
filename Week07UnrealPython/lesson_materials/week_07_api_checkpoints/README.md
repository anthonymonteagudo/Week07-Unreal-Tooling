# Week 7 numbered examples

Use the IDs named in the slides. Start with UE01-UE07; use the other examples when directed or for optional practice.

- Unreal: Tools > Execute Python Script. For UE08, open W07_MaterialVFXLab first.
- Blender: open the saved file in its Text Editor and Run Script (Alt+P).
- PY01: ordinary Python; no application modules required.

Each complete file includes its imports. Within a file, run blocks in order. The `# %%` markers are labels, not native Unreal cells. Re-run setup after changing the selection.

## UE01 Unreal host and project

[Open source](ue/UE01_host.py) | Host: unreal

Prepare: Unreal editor open, Python Script Plugin enabled.

Check: Hello from Unreal, the engine version and the actual project directory.

Repeat or recover: Read only. Rerun freely.

## UE02 Level selection

[Open source](ue/UE02_level_selection.py) | Host: unreal

Prepare: Select the target cube, then try an empty selection.

Check: Selected Actor count, labels and class names. Empty selection prints zero.

Repeat or recover: Read only. Selection is manual.

## UE03 Actor, component and mesh

[Open source](ue/UE03_components.py) | Host: unreal

Prepare: Select a mesh Actor; repeat with a camera or light.

Check: Component count and shared mesh path. Actors without mesh components print zero.

Repeat or recover: Read only. No dependency on UE02's variables.

## UE04 Content Browser selection

[Open source](ue/UE04_asset_selection.py) | Host: unreal

Prepare: Select assets in the Content Browser, independently of the Outliner.

Check: Asset count, names, class names and object paths.

Repeat or recover: Read only. Rerun after changing asset selection.

## UE05 Texture editor properties

[Open source](ue/UE05_texture_properties.py) | Host: unreal

Prepare: Select textures; include a non-texture to test eligibility.

Check: Texture/skipped counts, compression and sRGB values.

Repeat or recover: Read only. Shared texture assets remain unchanged.

## UE06 Read-only validation

[Open source](ue/UE06_validation_report.py) | Host: unreal

Prepare: Select textures. The prepared material tool uses the suffix _Normal.

Check: Every mismatching _Normal texture and final checked/mismatch counts. Zero checked is explicitly inconclusive.

Repeat or recover: Read only. No repair or saving.

## UE07 Disk paths and asset paths

[Open source](ue/UE07_paths.py) | Host: unreal

Prepare: Any Unreal project with the built-in BasicShapes cube available.

Check: Project Content disk folder and loaded /Engine object path.

Repeat or recover: Read only. Loading the cube does not place an Actor.

## BL01 Blender host and selection

[Open source](blender/BL01_host_selection.py) | Host: blender

Prepare: Blender Text Editor, preferably the prepared BridgeCompare.blend.

Check: Blender version, mode, selection count, object names/types.

Repeat or recover: Read only. Rerun freely.

## BL02 Object and mesh data

[Open source](blender/BL02_object_mesh.py) | Host: blender

Prepare: Select at least one mesh object.

Check: Object location, mesh datablock name/users and source polygon count.

Repeat or recover: Read only. No dependency on BL01's variables.

## BL03 Evaluated geometry

[Open source](blender/BL03_evaluated_mesh.py) | Host: blender

Prepare: Object Mode with exactly one mesh selected. A modifier can make the contrast visible.

Check: Source and evaluated polygon counts. They can be equal without a topology-changing modifier.

Repeat or recover: Read only. Temporary mesh released in finally; modifier is not applied.

## BL04 One FBX export

[Open source](blender/BL04_export_fbx.py) | Host: blender

Prepare: Object Mode, one unrigged mesh, no shape keys. FBX exporter available.

Check: A nonempty FBX in a new temporary folder; exact path prints.

Repeat or recover: Writes a new temporary folder each run. Remove only the printed lesson folder afterward. No scene save.

## UE11 Prepare an import task

[Open source](ue/UE11_import_task.py) | Host: unreal

Prepare: Week07UnrealPython project with Samples/Bridge/Handoffs included.

Check: Prepared source and destination. No new Unreal asset.

Repeat or recover: Read only. Constructs task/options objects but does not execute an import.

## UE12 Import and inspect

[Open source](ue/UE12_import_and_verify.py) | Host: unreal

Prepare: Same project, PIE stopped, /Game/Week07/APILessons/SM_API_Wedge absent.

Check: One unsaved StaticMesh at the exact lesson path, returned paths and bounds.

Repeat or recover: Creates an unsaved lesson asset. Refuses repeat overwrite. After inspection manually remove only that lesson asset, or use a fresh disposable project copy. Do not assume Undo reverses import.

## UE08 One material override

[Open source](ue/UE08_material_override.py) | Host: unreal

Prepare: W07_MaterialVFXLab, PIE stopped. Select only tagged W07_Crate_Target and one existing material/instance.

Check: Target slot zero changes; old/new materials print. Protected cube remains unchanged.

Repeat or recover: One viewport Undo restores the assignment. No new asset or save. Already assigned material creates no new Undo entry.

## UE09 Material parameter readback

[Open source](ue/UE09_material_readback.py) | Host: unreal

Prepare: Select exactly one MaterialInstanceConstant in the Content Browser.

Check: Texture parameter names and resolved texture paths, or None. Zero parameters prints zero.

Repeat or recover: Read only. Use the instance from the prepared Material/VFX demo.

## UE10 Niagara component inspection

[Open source](ue/UE10_niagara_components.py) | Host: unreal

Prepare: Select the effects produced by the prepared VFX tool, or compare a non-effect Actor.

Check: Niagara component counts and referenced system paths. No effects are spawned.

Repeat or recover: Read only. Use the prepared tool for placement and its demonstrated Undo.

## PY01 A preview snapshot

[Open source](python/PY01_preview_snapshot.py) | Host: python

Prepare: Ordinary Python, Unreal Python or Blender Python; no host module required.

Check: The changed target differs from the reviewed copy, so BLOCKED prints.

Repeat or recover: Only local teaching dictionaries change. Rerun resets them.

## Optional Blueprint snippet

[UE13](ue/UE13_blueprint_map.py) is a short snippet for an editor utility Blueprint's Execute Python Script node. Its docstring names the output pin and expected values. It is separate from the 17 complete-file checkpoints and the launcher.

The pure Python checks do not prove every host example works in every engine or Blender version. Use the stated host and prepared inputs. The Material/VFX tool rehearsal is separate from these examples.
