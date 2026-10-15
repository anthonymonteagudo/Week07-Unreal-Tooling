"""Instructor convenience functions for the prepared Material & VFX classroom map."""
import unreal
from week07_tooling.editor.workflow_backend import guard, WORKFLOW_MAP, EditorWorkflowBackend

def select_material():
    guard()
    sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    matches = [a for a in sub.get_all_level_actors() if a.get_actor_label() == 'W07_Crate_Target']
    if len(matches) != 1:
        raise RuntimeError('Expected exactly one W07_Crate_Target. Inspect the map.')
    sub.set_selected_level_actors(matches)
    unreal.EditorAssetLibrary.sync_browser_to_objects([
        '/Game/Week07/LiveDemo/Textures/T_Crate_' + suffix for suffix in ('BaseColor','Normal','ORM')])
    return 'Target and textures selected. Wait for Content Browser to update, then Preview.'

def select_vfx():
    guard()
    sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    matches = [a for a in sub.get_all_level_actors() if 'W07_VFXAnchor' in [str(t) for t in a.tags]]
    if len(matches) != 3:
        raise RuntimeError('Expected exactly three tagged anchors. Inspect the map.')
    sub.set_selected_level_actors(matches)
    return 'Three anchors selected. Preview before Apply.'

def preflight():
    guard()
    sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = sub.get_all_level_actors()
    by_label = {a.get_actor_label(): a for a in actors}
    required = ['W07_Crate_Target','W07_Crate_Protected','W07_LiveDemo_Camera']
    missing = [label for label in required if label not in by_label]
    if missing:
        raise RuntimeError('Missing fixture Actors: ' + ', '.join(missing))
    if any('W07_PlacedVFX' in [str(t) for t in a.tags] for a in actors):
        raise RuntimeError('Previous effects remain. Undo the known placement or reopen the clean map without saving rehearsal edits.')
    for label in required[:2]:
        comp = by_label[label].get_component_by_class(unreal.StaticMeshComponent)
        if not comp or comp.get_material(0).get_path_name() != '/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial':
            raise RuntimeError(label + ' is not at the baseline material. Inspect or reopen the clean map.')
    options = EditorWorkflowBackend().options()
    if not options['materials'] or not options['vfx']:
        raise RuntimeError('Prepared parent or reviewed VFX preset is unavailable.')
    for suffix in ('BaseColor','Normal','ORM'):
        if not unreal.load_asset('/Game/Week07/LiveDemo/Textures/T_Crate_' + suffix):
            raise RuntimeError('Missing prepared texture: ' + suffix)
    camera = by_label['W07_LiveDemo_Camera']
    editor = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    editor.set_level_viewport_camera_info(camera.get_actor_location(), camera.get_actor_rotation())
    select_material()
    return ('Material & VFX: ready. Target and textures selected. '
            'Open Tools > Material & VFX Tools. Enter a new MI_ name, then Preview. '
            'This check does not test the Maya/Blender bridge.')
