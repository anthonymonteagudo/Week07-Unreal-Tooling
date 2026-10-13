"""One-time prep in the isolated Week07UnrealPython project. Never run in the source project."""
import json
from pathlib import Path
import unreal
import week07_tools as w7

root = Path(unreal.Paths.project_dir()).resolve()
assert root.name == 'Week07UnrealPython', 'Only run in the Week 7 spinoff.'
assert not unreal.EditorAssetLibrary.does_asset_exist(w7.DEMO_MAP), 'Baseline already exists; refusing overwrite.'
out = root / 'Saved/Week07'
out.mkdir(parents=True, exist_ok=True)
level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
assert level.new_level(w7.DEMO_MAP)
sub = w7.actors()


def spawn(cls, label, pos, rot=(0, 0, 0), folder='Week07/02_Stage'):
    a = sub.spawn_actor_from_class(cls, unreal.Vector(*pos), unreal.Rotator(*rot))
    assert a, label
    a.set_actor_label(label)
    a.set_folder_path(folder)
    return a


floor = spawn(unreal.StaticMeshActor, 'W07_Stage', (0, 0, -20))
floor.static_mesh_component.set_static_mesh(unreal.load_asset('/Engine/BasicShapes/Cube'))
floor.set_actor_scale3d(unreal.Vector(22, 22, 0.4))
floor.static_mesh_component.set_material(0, unreal.load_asset('/Engine/BasicShapes/BasicShapeMaterial'))
sun = spawn(unreal.DirectionalLight, 'W07_KeyLight', (-600, -400, 900), (-45, -35, 0))
sun.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
sun.light_component.set_intensity(5.0)
sky = spawn(unreal.SkyLight, 'W07_FillLight', (0, 0, 600))
sky.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
sky.light_component.set_editor_property('real_time_capture', True)
spawn(unreal.SkyAtmosphere, 'W07_Sky', (0, 0, 0))
post = spawn(unreal.PostProcessVolume, 'W07_Exposure', (0, 0, 0))
post.set_editor_property('unbound', True)
settings = post.get_editor_property('settings')
settings.set_editor_property('override_auto_exposure_min_brightness', True)
settings.set_editor_property('override_auto_exposure_max_brightness', True)
settings.set_editor_property('auto_exposure_min_brightness', 1.0)
settings.set_editor_property('auto_exposure_max_brightness', 1.0)
post.set_editor_property('settings', settings)

base = '/Game/Northwood/EpicContent/Megascans/3D_Assets/'
paths = [
    base + 'Wooden_Crate_udribbjqx/Wooden_Crate_LOD0_udribbjqx',
    base + 'Wooden_Barrel_udlmcdhqx/Wooden_Barrel_LOD0_udlmcdhqx',
    base + 'Wooden_Crate_udribbjqx/Wooden_Crate_LOD0_udribbjqx',
    base + 'Wooden_Ammo_Crate_uehqdivfa/Wooden_Ammo_Crate_LOD0_uehqdivfa',
    base + 'Old_Wooden_Bench_ueigebjfa/Old_Wooden_Bench_LOD0_ueigebjfa',
    base + 'Wooden_Chair_ukipagtbw_00/Wooden_Chair_LOD0_ukipagtbw']
manifest = []
for i, path in enumerate(paths):
    mesh = unreal.load_asset(path)
    assert isinstance(mesh, unreal.StaticMesh), path
    actor = spawn(unreal.StaticMeshActor, f'prop_temp_{i+1}', w7.BASELINE[i], folder=w7.FOLDER)
    comp = actor.static_mesh_component
    comp.set_mobility(unreal.ComponentMobility.MOVABLE)
    comp.set_static_mesh(mesh)
    lo, hi = comp.get_local_bounds()
    scale = 115.0 / max(hi.x-lo.x, hi.y-lo.y, hi.z-lo.z)
    actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))
    # These source props have approximately ground-level pivots (record bounds below).
    actor.set_editor_property('tags', [w7.TAG, f'W07_ID={i}'])
    manifest.append({'id': i, 'asset': path, 'bounds_min': [lo.x, lo.y, lo.z], 'scale': scale})

pos = unreal.Vector(-1150, -680, 780)
rot = unreal.MathLibrary.find_look_at_rotation(pos, unreal.Vector(0, 0, 30))
cam = sub.spawn_actor_from_class(unreal.CameraActor, pos, rot)
cam.set_actor_label('W07_Camera_Overview')
cam.set_folder_path('Week07/03_Capture')
cam.camera_component.set_field_of_view(55)
w7.camera_view()
w7.select_demo()
assert level.save_current_level()
(out / 'fixture_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

# Exercise real Unreal behavior, including empty/mixed/stale selection and idempotence.
checks = {}
sub.clear_actor_selection_set()
checks['empty_selection'] = w7.preview() is None and w7.apply(None) == 0
sub.set_selected_level_actors([floor])
try:
    w7.preview()
    raise AssertionError('Mixed selection accepted')
except ValueError:
    checks['unrelated_actor_rejected'] = True
w7.select_demo()
checks['baseline_fails'] = all(r['status'] == 'FAIL' for r in w7.check())
rows = w7.inspect_selection()
checks['shared_asset_example'] = rows[0]['components'][0]['mesh_asset'] == rows[2]['components'][0]['mesh_asset']
plan = w7.preview()
selected = w7.fixture()
sub.set_selected_level_actors(selected[:2])
try:
    w7.apply(plan)
    raise AssertionError('Stale selection accepted')
except RuntimeError:
    checks['stale_selection_rejected'] = True
w7.select_demo()
checks['six_changed'] = w7.apply(w7.preview()) == 6
checks['all_pass_after_apply'] = all(r['status'] == 'PASS' for r in w7.check())
checks['second_apply_noop'] = w7.apply(w7.preview()) == 0
w7.reset_demo()
checks['reset_restores_baseline'] = all(r['status'] == 'FAIL' for r in w7.check())
assert all(checks.values()), checks
assert level.save_current_level()
(out / 'validation.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
unreal.log('W07_BUILD_AND_TEST_OK')
