"""UE10: inspect already placed effects; this script creates no effects."""
# %% setup
import unreal
editor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = editor.get_selected_level_actors()
print("Selected Actors:", len(actors))

# %% focus
for actor in actors:
    parts = actor.get_components_by_class(unreal.NiagaraComponent)
    print(actor.get_actor_label(), "Niagara components:", len(parts))
    for part in parts:
        system = part.get_editor_property("asset")
        print(system.get_path_name() if system else None)
