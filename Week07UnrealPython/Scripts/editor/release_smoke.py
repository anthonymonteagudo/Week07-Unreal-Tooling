"""Verify a disposable extracted release in a separate editor; never save assets.

Run only with WEEK07_RELEASE_RESULT set. The process exits after verification.
"""
import json
import os
from pathlib import Path
import time
import traceback
import unreal
from week07_tooling.editor import live_demo, native_panel
import week07_lessons

output = Path(os.environ['WEEK07_RELEASE_RESULT'])
root = Path(unreal.Paths.project_dir()).resolve()
assert not (root/'Content/Northwood').exists(), 'Verify the small extracted package, not an authoring project.'
checks = {}
stage = 0
deadline = time.monotonic() + 150
next_tick = 0
identity = None


def finish(error=None):
    unreal.unregister_slate_post_tick_callback(handle)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'status': 'FAIL' if error else 'PASS', 'checks':checks,
        'error':error,'engine':unreal.SystemLibrary.get_engine_version()},indent=2),encoding='utf8')
    unreal.SystemLibrary.quit_editor()


def call(action, **kwargs):
    result=json.loads(native_panel.dispatch(json.dumps(dict(action=action,session=identity,**kwargs))))
    return result


def tick(delta):
    global stage,next_tick,identity
    try:
        if time.monotonic()>deadline: raise TimeoutError('Timed out waiting for prepared selection.')
        if time.monotonic()<next_tick: return
        next_tick=time.monotonic()+1
        actors=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
        if stage==0:
            level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
            assert level.load_level('/Game/Week07/Maps/W07_MaterialVFXLab')
            checks['native_module']=hasattr(unreal,'Week07EditorLibrary')
            assert checks['native_module']
            registry=unreal.AssetRegistryHelpers.get_asset_registry()
            registry.scan_paths_synchronous(['/Game/Week07'],force_rescan=True)
            missing=[]
            for asset in registry.get_assets_by_path('/Game/Week07',recursive=True):
                for dep in registry.get_dependencies(asset.package_name,unreal.AssetRegistryDependencyOptions()):
                    name=str(dep)
                    if name.startswith('/Game/') and not unreal.EditorAssetLibrary.does_asset_exist(name): missing.append(name)
            assert not missing,missing
            checks['project_dependencies_resolve']=True
            live_demo.preflight()
            identity=call('connect')['session']
            unreal.Week07EditorLibrary.open_tools()
            stage=1
        elif stage==1:
            if len(unreal.EditorUtilityLibrary.get_selected_assets())!=3: return
            for step in ['UE01','UE02','UE03','UE04','UE05','UE06','UE07','UE11','UE12']:
                week07_lessons.run(step)
            checks['unreal_checkpoints']=True
            result=call('preview',kind='material',name='MI_ReleaseCheck',slot=0)
            assert result['ok'],result
            assert call('apply')['ok']
            by_label={a.get_actor_label():a for a in actors.get_all_level_actors()}
            target=by_label['W07_Crate_Target'].get_component_by_class(unreal.StaticMeshComponent)
            protected=by_label['W07_Crate_Protected'].get_component_by_class(unreal.StaticMeshComponent)
            assert target.get_material(0).get_name()=='MI_ReleaseCheck'
            assert protected.get_material(0).get_name()=='BasicShapeMaterial'
            checks['material_apply_scope']=True
            assert unreal.Week07EditorLibrary.undo_demo()
            assert target.get_material(0).get_name()=='BasicShapeMaterial'
            checks['material_undo']=True
            live_demo.select_vfx()
            stage=2
        elif stage==2:
            result=call('preview',kind='vfx',scale=1)
            assert result['ok'],result
            assert call('apply')['ok']
            fx=[a for a in actors.get_all_level_actors() if 'W07_PlacedVFX' in map(str,a.tags)]
            assert len(fx)==3
            checks['vfx_apply']=True
            blocked=call('preview',kind='vfx',scale=1)
            assert not blocked['ok']
            checks['duplicate_blocked']=True
            assert unreal.Week07EditorLibrary.undo_demo()
            assert not [a for a in actors.get_all_level_actors() if 'W07_PlacedVFX' in map(str,a.tags)]
            checks['vfx_undo']=True
            checks['clean_baseline']=bool(live_demo.preflight())
            stage=3
        elif stage==3:
            level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
            assert level.load_level('/Game/Week07/Bridge/W07_BridgeComparison')
            meshes=[a for a in actors.get_all_level_actors() if a.get_actor_label().startswith(('Blender -','Maya -'))]
            assert len(meshes)==4
            checks['bridge_map_loads']=True
            finish()
    except Exception:
        finish(traceback.format_exc())


handle=unreal.register_slate_post_tick_callback(tick)
