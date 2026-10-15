"""UE02: read the level selection; selecting nothing is a valid empty result."""

# Section: setup
import unreal
editor = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# Section: focus
actors = editor.get_selected_level_actors()
print("Selected Actors:", len(actors))
for actor in actors:
    print(actor.get_actor_label(), actor.get_class().get_name())
