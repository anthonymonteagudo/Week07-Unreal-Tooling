"""UE03: repeat the setup, then inspect components without changing the level."""

# %% setup
import unreal
editor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
actors = editor.get_selected_level_actors()
print("Selected Actors:", len(actors))

# %% focus
for actor in actors:
    components = actor.get_components_by_class(unreal.StaticMeshComponent)
    print(actor.get_actor_label(), "mesh components:", len(components))
    for component in components:
        mesh = component.get_editor_property("static_mesh")
        print(component.get_name(), mesh.get_path_name() if mesh else None)
