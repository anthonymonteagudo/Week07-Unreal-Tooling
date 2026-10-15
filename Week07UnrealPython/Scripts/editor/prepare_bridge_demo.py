"""Create the bridge comparison map once, using the published baseline assets.

Run in an isolated editor, after build_samples.py for both hosts. Refuses to
overwrite the map. Receiver never places actors: this is explicit fixture setup.
"""
from pathlib import Path
import json
import os
import traceback
import unreal
from week07_bridge import core, unreal_receiver

root = Path(unreal.Paths.project_dir()).resolve()
exchange = root / 'Saved/BridgeRehearsal'
result_path = Path(os.environ.get('WEEK07_RESULT_PATH', str(exchange / 'prepared_map.json')))
map_path = '/Game/Week07/Bridge/W07_BridgeComparison'
report = {'status': 'FAIL'}
try:
    if unreal.EditorAssetLibrary.does_asset_exist(map_path):
        raise RuntimeError('Comparison map already exists. Open it; this builder does not overwrite it.')
    level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    level.new_level(map_path)
    for host, y in [('blender', -160), ('maya', 160)]:
        sample = core.read_json(exchange / (host + '_samples.json'))
        result = unreal_receiver.import_manifest(sample['baseline'], exchange)
        mesh = unreal.load_asset(result['asset_path'])
        for index, x in enumerate([-130, 130]):
            actor = actors.spawn_actor_from_object(mesh, unreal.Vector(x, y, 0))
            actor.set_actor_label(host.title() + ' - shared mesh instance ' + str(index + 1))
        text = actors.spawn_actor_from_class(unreal.TextRenderActor, unreal.Vector(20, y - 55, 250), unreal.Rotator(0, 0, 0))
        text.set_actor_label(host.title() + ' label')
        text.text_render.set_text(host.title() + '  |  2 instances')
        text.text_render.set_world_size(24)
    floor = actors.spawn_actor_from_object(unreal.load_asset('/Engine/BasicShapes/Cube'), unreal.Vector(0, 0, -10))
    floor.set_actor_scale3d(unreal.Vector(9, 9, .2))
    floor.set_actor_label('Bridge comparison floor')
    light = actors.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 500), unreal.Rotator(-45, -35, 0))
    light.set_actor_label('Bridge key light')
    actors.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 400))
    camera = actors.spawn_actor_from_class(unreal.CameraActor, unreal.Vector(800, -900, 650))
    rotation = unreal.MathLibrary.find_look_at_rotation(camera.get_actor_location(), unreal.Vector(0, 0, 100))
    camera.set_actor_rotation(rotation, False)
    camera.set_actor_label('Bridge comparison camera')
    unreal.EditorLevelLibrary.set_level_viewport_camera_info(camera.get_actor_location(), rotation)
    from week07_bridge.unreal_demo import style
    style()
    assert level.save_current_level()
    report.update(status='PASS', map=map_path, instances=4, baseline_dimensions_cm=[120, 60, 180])
except Exception:
    report['error'] = traceback.format_exc()
finally:
    core.atomic_json(result_path, report)
    unreal.log(json.dumps(report, indent=2))
