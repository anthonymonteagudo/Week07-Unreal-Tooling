"""Validate an extracted student project, including a material-preserving reimport."""
from pathlib import Path
import json
import shutil
import traceback
import unreal
import week07_bridge
from week07_bridge import core, unreal_receiver

root = Path(unreal.Paths.project_dir()).resolve()
report = {'status': 'FAIL', 'project': str(root)}
try:
    assert Path(week07_bridge.__file__).resolve().is_relative_to(root)
    level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    assert level.load_level('/Game/Week07/Bridge/W07_BridgeComparison')
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    placed = [a for a in actors.get_all_level_actors() if 'shared mesh instance' in a.get_actor_label()]
    assert len(placed) == 4
    results = []
    for host in ('Blender', 'Maya'):
        mesh = unreal.load_asset('/Game/Week07/Bridge/SM_Compare_' + host)
        material = mesh.get_material(0)
        assert material.get_path_name().startswith('/Game/Week07/Bridge/M_Bridge' + host)
        original_path = mesh.get_path_name()
        source = root / 'Samples/Bridge/Handoffs' / host.lower() / 'revised'
        manifest = core.read_json(source / 'manifest.json')
        target = core.default_exchange() / 'publishes' / manifest['asset_name'] / manifest['revision']
        target.mkdir(parents=True, exist_ok=True)
        for name in ('manifest.json', manifest['filename']):
            shutil.copy2(source / name, target / name)
        result = unreal_receiver.import_manifest(target / 'manifest.json')
        assert result['updated_existing'] and result['asset_path'] == original_path
        assert mesh.get_material(0) == material
        matching = [a for a in placed if a.get_actor_label().startswith(host)]
        assert len(matching) == 2
        assert all(abs(a.static_mesh_component.static_mesh.get_bounding_box().max.z - 220) < .1
                   for a in matching)
        results.append(result)
    unreal_receiver.install_menu()
    unreal_receiver.start()
    unreal_receiver.stop()
    report.update(status='PASS', placed_instances=4, mesh_materials_preserved=True,
                  source_loaded_from_extracted_project=True, imports=results)
except Exception:
    report['error'] = traceback.format_exc()
finally:
    core.atomic_json(root / 'Saved/portable_result.json', report)
    unreal.log(json.dumps(report, indent=2))
