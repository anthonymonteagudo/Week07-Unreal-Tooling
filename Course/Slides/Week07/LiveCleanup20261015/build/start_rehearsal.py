import unreal,json,datetime
from pathlib import Path
from week07_tooling.editor import live_demo
REHEARSAL=Path(unreal.Paths.project_dir()).resolve().parent/'Course/Slides/Week07/LiveCleanup20261015'
EVIDENCE={'engine':unreal.SystemLibrary.get_engine_version(),'started':datetime.datetime.now().astimezone().isoformat(),'steps':[]}
if (REHEARSAL/'qa/live-rehearsal.json').exists(): EVIDENCE=json.loads((REHEARSAL/'qa/live-rehearsal.json').read_text(encoding='utf-8'))
actor_sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
def record(label):
    aa=actor_sub.get_all_level_actors(); cubes={}
    for a in aa:
        if a.get_actor_label() in ['W07_Crate_Target','W07_Crate_Protected']:
            c=a.get_component_by_class(unreal.StaticMeshComponent)
            cubes[a.get_actor_label()]={'material':c.get_material(0).get_path_name(),'mesh_default':c.static_mesh.get_material(0).get_path_name(),'mesh':c.static_mesh.get_path_name()}
    effects=[{'name':a.get_actor_label(),'location':str(a.get_actor_location()),'scale':str(a.get_actor_scale3d()),'tags':[str(t) for t in a.tags]} for a in aa if 'W07_PlacedVFX' in [str(t) for t in a.tags]]
    data={'label':label,'time':datetime.datetime.now().astimezone().isoformat(),'cubes':cubes,'effects':effects,'selected':[a.get_actor_label() for a in actor_sub.get_selected_level_actors()],'selected_assets':[a.get_name() for a in unreal.EditorUtilityLibrary.get_selected_assets()]}
    EVIDENCE['steps'].append(data);(REHEARSAL/'qa/live-rehearsal.json').write_text(json.dumps(EVIDENCE,indent=2),encoding='utf-8');print(json.dumps(data))
record('Clean baseline before UI rehearsal')
print(live_demo.preflight())
