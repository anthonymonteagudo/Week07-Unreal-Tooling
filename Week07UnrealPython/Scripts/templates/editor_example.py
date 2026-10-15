"""06: Replace this summary with the small task your lesson demonstrates.

Copy into week07_tooling/examples/e06_my_example.py; register 06_my_example
in week07_tools._EXAMPLES, then run from Unreal with w7.run_example().
"""
import unreal


def run():
    # First lesson step: make scope visible before introducing any changes.
    subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    selected = subsystem.get_selected_level_actors()
    labels = [actor.get_actor_label() for actor in selected]
    if not labels:
        unreal.log_warning('Select one or more level Actors first.')
        return []
    unreal.log(f'Example scope: {len(labels)} selected Actors: {labels}')
    return labels
