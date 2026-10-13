"""Read-only evidence collection after the manual Blender UI rehearsal."""
import json
from pathlib import Path
import unreal

root = Path(unreal.Paths.project_dir()).resolve()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
records = []
for actor in actors:
    if actor.get_actor_label().startswith(('Blender -', 'Maya -')):
        component = actor.static_mesh_component
        mesh = component.static_mesh
        box = mesh.get_bounding_box()
        size = box.max - box.min
        records.append(dict(actor=actor.get_actor_label(), actor_path=actor.get_path_name(),
                            mesh=mesh.get_path_name(), dimensions_cm=[size.x,size.y,size.z],
                            location=str(actor.get_actor_location()), scale=str(actor.get_actor_scale3d()),
                            material=component.get_material(0).get_path_name()))
blender = [r for r in records if r['actor'].startswith('Blender -')]
assert len(blender) == 2
assert len({r['mesh'] for r in blender}) == 1
assert all(abs(r['dimensions_cm'][2] - 220) < .1 for r in blender)
responses = [json.loads(p.read_text()) for p in (root/'Saved/BridgeExchange/responses').glob('*.json')]
result = dict(method='Actual Blender UI vertex edit and Publish & Send buttons; read-only Unreal evidence',
              expected_height_change_cm=[180,220], actors=records, responses=responses)
path = root/'Docs/Bridge/UI-Rehearsal/verification.json'
path.write_text(json.dumps(result,indent=2),encoding='utf8')
unreal.log('UI rehearsal verified: two existing Blender actors reference the same 220 cm mesh.')
