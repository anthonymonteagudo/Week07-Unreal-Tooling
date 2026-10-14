"""UE08: assign an existing material to the prepared target, then inspect Undo."""

# %% setup
import unreal
editor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
map_path = world.get_editor_world().get_path_name().split(".")[0]
teaching_map = "/Game/Week07/Maps/W07_MaterialVFXLab"
if level.is_in_play_in_editor() or map_path != teaching_map:
    raise RuntimeError("Stop PIE and open W07_MaterialVFXLab.")
actors = editor.get_selected_level_actors()
assets = unreal.EditorUtilityLibrary.get_selected_assets()

# %% eligibility
if len(actors) != 1 or "W07_MaterialTarget" not in map(str, actors[0].tags):
    raise RuntimeError("Select only the tagged W07_Crate_Target Actor.")
if len(assets) != 1 or not isinstance(assets[0], unreal.MaterialInterface):
    raise RuntimeError("Select one material in the Content Browser.")
components = actors[0].get_components_by_class(unreal.StaticMeshComponent)
if len(components) != 1 or components[0].get_num_materials() < 1:
    raise RuntimeError("Need one mesh component with slot zero.")
component = components[0]
material = assets[0]
before = component.get_material(0)

# %% focus
if before == material:
    print("Already assigned. No change and no new Undo entry.")
else:
    with unreal.ScopedEditorTransaction("API lesson: material override"):
        component.modify()  # Record the previous state for Undo.
        component.set_material(0, material)

# %% check
actual = component.get_material(0)
print("Before:", before, "after:", actual)
if actual != material:
    raise RuntimeError("Assignment check failed. Inspect the target and Undo.")
print("Check the protected cube, then Undo once over the viewport.")
