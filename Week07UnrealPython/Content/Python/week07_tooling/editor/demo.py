"""Week 7: inspect, check, preview, apply, verify. Run inside Unreal Editor.

No work runs on import. Mutations are confined to the six tagged demo Actors.
The Static Mesh assets and original Northwood map are never edited.
"""
import json
from pathlib import Path
import unreal

from week07_tooling.config import DEMO_MAP, TAG, FOLDER, BASELINE, KINDS
from week07_tooling import rules


def actors():
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem)


def world():
    return unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()


def _guard():
    if world().get_path_name().split('.')[0] != DEMO_MAP:
        raise RuntimeError('Open W07_PythonLab before changing the demo.')
    if unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).is_in_play_in_editor():
        raise RuntimeError('Stop Play in Editor first.')


def _id(actor):
    ids = [str(t).split('=')[1] for t in actor.tags if str(t).startswith('W07_ID=')]
    return int(ids[0]) if len(ids) == 1 else -1


def fixture():
    _guard()
    found = [a for a in actors().get_all_level_actors() if TAG in [str(t) for t in a.tags]]
    if len(found) != 6 or sorted(_id(a) for a in found) != list(range(6)):
        raise RuntimeError('Expected six uniquely tagged demo props. Reopen the saved baseline map.')
    return sorted(found, key=_id)


def select_demo():
    found = fixture()
    actors().set_selected_level_actors(found)
    unreal.log('W07: Selected six demo props. Content Browser selection is separate.')
    return found


def inspect_selection():
    """Read-only: show Actor -> Component -> shared asset for current selection."""
    rows = []
    selected = actors().get_selected_level_actors()
    for actor in selected:
        components = actor.get_components_by_class(unreal.StaticMeshComponent)
        rows.append({'actor': actor.get_actor_label(), 'path': actor.get_path_name(),
                     'class': actor.get_class().get_name(),
                     'components': [{'name': c.get_name(),
                                     'mesh_asset': c.static_mesh.get_path_name() if c.static_mesh else None,
                                     'material_slots': c.get_num_materials()} for c in components]})
    unreal.log(json.dumps(rows, indent=2))
    unreal.log(f'W07: {len(rows)} level Actors; {len(unreal.EditorUtilityLibrary.get_selected_assets())} Content Browser assets selected.')
    if not rows:
        unreal.log_warning('W07: Nothing selected. Select level Actors in the viewport or Outliner.')
    return rows


def _state(actor):
    p = actor.get_actor_location()
    return {'path': actor.get_path_name(), 'id': _id(actor),
            'label': actor.get_actor_label(), 'location': [p.x, p.y, p.z]}


def preview():
    """Return a reviewable plan; no scene changes. Keep it as plan = w7.preview()."""
    _guard()
    selected = list(actors().get_selected_level_actors())
    valid = fixture()
    if not selected:
        unreal.log_warning('W07: No selection; no plan created.')
        return None
    if any(a not in valid for a in selected):
        raise ValueError('Select only tagged Week 7 props. Mixed selections are rejected, not silently expanded.')
    plan = rules.make_plan(world().get_path_name(), [_state(a) for a in selected])
    unreal.log('W07 PREVIEW (centimeters; Actor labels, not asset names):\n' + json.dumps(plan, indent=2))
    return plan


def apply(plan):
    """Apply only a fresh, unmodified preview as one Undo transaction. Does not save."""
    _guard()
    if not plan:
        unreal.log_warning('W07: No plan to apply.')
        return 0
    # Recompute before mutating: changed selection, transforms, labels, or plan refuse the entire edit.
    current = preview()
    if plan != current:
        raise RuntimeError('Preview is stale or edited. Run preview() again and review it.')
    by_path = {a.get_path_name(): a for a in fixture()}
    targets = {item['before']['path'] for item in plan['items']}
    other_labels = {a.get_actor_label() for a in actors().get_all_level_actors() if a.get_path_name() not in targets}
    if any(item['after']['label'] in other_labels for item in plan['items']):
        raise RuntimeError('A proposed label is already used outside the selection.')
    changed = 0
    with unreal.ScopedEditorTransaction('Week 7: organize selected props'):
        for item in plan['items']:
            actor = by_path[item['before']['path']]
            dest = item['after']
            if item['before']['label'] == dest['label'] and item['before']['location'] == dest['location']:
                continue
            actor.modify()
            actor.root_component.modify()
            actor.set_actor_location(unreal.Vector(*dest['location']), False, True)
            actor.set_actor_label(dest['label'])
            changed += 1
    unreal.log(f'W07: Changed {changed} Actors. Verify with check(); Ctrl+Z undoes this batch. Map not saved.')
    return changed


def check():
    """Read-only fixture-specific rules; this is not a production asset validator."""
    rows = []
    for actor in fixture():
        i = _id(actor)
        mesh = actor.get_component_by_class(unreal.StaticMeshComponent)
        issues = rules.issues_for(_state(actor), bool(mesh and mesh.static_mesh))
        rows.append({'actor': actor.get_actor_label(), 'id': i,
                     'status': 'FAIL' if issues else 'PASS', 'issues': issues})
    unreal.log('W07 CHECK:\n' + json.dumps(rows, indent=2))
    unreal.log(f'W07: {sum(r["status"] == "PASS" for r in rows)}/6 props pass the demo rules.')
    return rows


def reset_demo():
    """Restore seeded labels/locations only, as one Undo step; never saves."""
    with unreal.ScopedEditorTransaction('Week 7: reset demo baseline'):
        for actor in fixture():
            actor.modify()
            actor.root_component.modify()
            i = _id(actor)
            actor.set_actor_location(unreal.Vector(*BASELINE[i]), False, True)
            actor.set_actor_label(f'prop_temp_{i+1}')
    unreal.log('W07: Baseline restored. Use select_demo(), inspect_selection(), check(), preview().')


def camera_view():
    _guard()
    cam = next(a for a in actors().get_all_level_actors() if a.get_actor_label() == 'W07_Camera_Overview')
    unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).set_level_viewport_camera_info(
        cam.get_actor_location(), cam.get_actor_rotation())


def capture_view(enabled=True):
    """Pilot the saved 16:9 camera for captures. Do not fly/navigate while piloting."""
    _guard()
    level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    if enabled:
        cam = next(a for a in actors().get_all_level_actors() if a.get_actor_label() == 'W07_Camera_Overview')
        level.pilot_level_actor(cam)
        level.set_exact_camera_view(True)
        level.editor_set_game_view(True)
    else:
        level.eject_pilot_level_actor()
        level.editor_set_game_view(False)


def export_report():
    """Write a local evidence file; no assets or maps are saved."""
    from datetime import datetime
    out = Path(unreal.Paths.project_saved_dir()) / 'Week07' / 'Reports'
    out.mkdir(parents=True, exist_ok=True)
    path = out / ('selection_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.json')
    path.write_text(json.dumps({'map': world().get_path_name(), 'selection': inspect_selection()}, indent=2), encoding='utf-8')
    unreal.log(f'W07: Report written to {path}')
    return str(path)
