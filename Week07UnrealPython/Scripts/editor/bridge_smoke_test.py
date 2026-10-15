"""Real UE import/reimport verification on a new, unsaved test map."""
from pathlib import Path
import json
import os
import traceback
import unreal
from week07_bridge import core, unreal_receiver

root = Path(unreal.Paths.project_dir()).resolve()
exchange = root / 'Saved/BridgeRehearsal'
result_path = Path(os.environ.get('WEEK07_RESULT_PATH', str(exchange / 'engine_result.json')))
report = {'status': 'FAIL', 'engine': unreal.SystemLibrary.get_engine_version(), 'hosts': []}
try:
    # This script runs in its own editor process; no existing map is modified.
    level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    level.new_level('/Temp/BridgeRehearsal')
    actor_system = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    for host in ('blender', 'maya'):
        sample = core.read_json(exchange / (host + '_samples.json'))
        first = unreal_receiver.import_manifest(sample['baseline'], exchange)
        mesh = unreal.load_asset(first['asset_path'])
        original_path = mesh.get_path_name()
        actors = [actor_system.spawn_actor_from_object(mesh, unreal.Vector(i * 250, 0, 0)) for i in range(2)]
        components = [a.static_mesh_component for a in actors]
        material = unreal.load_asset('/Engine/BasicShapes/BasicShapeMaterial')
        components[0].set_material(0, material)
        second = unreal_receiver.import_manifest(sample['revised'], exchange)
        assert second['asset_path'] == original_path
        assert second['updated_existing']
        assert all(c.static_mesh.get_path_name() == original_path for c in components)
        assert components[0].get_material(0) == material
        assert abs(components[1].static_mesh.get_bounding_box().max.z - 220) < .1
        report['hosts'].append({'host': host, 'first': first, 'second': second,
                                'two_instances_updated': True, 'component_material_preserved': True})
    report['status'] = 'PASS'
except Exception:
    report['error'] = traceback.format_exc()
finally:
    core.atomic_json(result_path, report)
    unreal.log(json.dumps(report, indent=2))
