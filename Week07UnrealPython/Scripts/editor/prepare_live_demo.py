"""One-time live fixture construction. Never overwrites an existing classroom map."""
import json
from pathlib import Path
import unreal

root=Path(unreal.Paths.project_dir()).resolve()
assert root.name=='Week07UnrealPython'
MAP='/Game/Week07/Maps/W07_MaterialVFXLab'
BASE='/Game/Week07/LiveDemo'
assets=unreal.EditorAssetLibrary
tools=unreal.AssetToolsHelpers.get_asset_tools()
level=unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
sub=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
assert not assets.does_asset_exist(MAP), 'Prepared map exists. Open it; do not rebuild it.'
textures={}
for role in ['BaseColor','Normal','ORM']:
 path=f'{BASE}/Textures/T_Crate_{role}'
 if not assets.does_asset_exist(path):
  task=unreal.AssetImportTask();task.filename=str(root/f'Source/LiveDemo/T_Crate_{role}.tga');task.destination_path=BASE+'/Textures';task.destination_name='T_Crate_'+role;task.automated=True;task.save=False
  tools.import_asset_tasks([task])
 tex=unreal.load_asset(path);assert isinstance(tex,unreal.Texture2D),path
 tex.set_editor_property('srgb',role=='BaseColor')
 tex.set_editor_property('compression_settings',unreal.TextureCompressionSettings.TC_NORMALMAP if role=='Normal' else unreal.TextureCompressionSettings.TC_DEFAULT if role=='BaseColor' else unreal.TextureCompressionSettings.TC_MASKS)
 assets.save_loaded_asset(tex);textures[role]=tex
parent_path=BASE+'/Materials/M_PreparedSurface'
parent=unreal.load_asset(parent_path) if assets.does_asset_exist(parent_path) else None
if parent is None:
 parent=tools.create_asset('M_PreparedSurface',BASE+'/Materials',unreal.Material,unreal.MaterialFactoryNew())
 lib=unreal.MaterialEditingLibrary
 for i,role in enumerate(['BaseColor','Normal','ORM']):
  node=lib.create_material_expression(parent,unreal.MaterialExpressionTextureSampleParameter2D,-500,i*240)
  node.set_editor_property('parameter_name',role+'Texture')
  node.set_editor_property('texture',textures[role])
  node.set_editor_property('sampler_type',unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL if role=='Normal' else unreal.MaterialSamplerType.SAMPLERTYPE_COLOR if role=='BaseColor' else unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
  if role=='BaseColor':lib.connect_material_property(node,'RGB',unreal.MaterialProperty.MP_BASE_COLOR)
  elif role=='Normal':lib.connect_material_property(node,'RGB',unreal.MaterialProperty.MP_NORMAL)
  else:
   for channel,prop in [('R',unreal.MaterialProperty.MP_AMBIENT_OCCLUSION),('G',unreal.MaterialProperty.MP_ROUGHNESS),('B',unreal.MaterialProperty.MP_METALLIC)]:lib.connect_material_property(node,channel,prop)
 lib.recompile_material(parent);assets.save_loaded_asset(parent)
fx_path=BASE+'/FX/NS_ClassroomFountain'
fx=unreal.load_asset(fx_path) if assets.does_asset_exist(fx_path) else assets.duplicate_asset('/Niagara/DefaultAssets/Templates/Systems/FountainLightweight',fx_path)
assert isinstance(fx,unreal.NiagaraSystem)
effect_path=BASE+'/FX/NET_Classroom'
effect=unreal.load_asset(effect_path) if assets.does_asset_exist(effect_path) else tools.create_asset('NET_Classroom',BASE+'/FX',unreal.NiagaraEffectType,unreal.NiagaraEffectTypeFactoryNew())
settings=unreal.NiagaraSystemScalabilitySettings()
settings.set_editor_property('cull_by_distance',True);settings.set_editor_property('max_distance',5000.)
settings.set_editor_property('cull_max_instance_count',True);settings.set_editor_property('max_instances',8)
settings.set_editor_property('cull_per_system_max_instance_count',True);settings.set_editor_property('max_system_instances',4)
scalability=unreal.NiagaraSystemScalabilitySettingsArray()
scalability.set_editor_property('settings',[settings])
effect.set_editor_property('system_scalability_settings',scalability)
effect.set_editor_property('cull_reaction',unreal.NiagaraCullReaction.DEACTIVATE_RESUME)
assets.save_loaded_asset(effect)
fx.set_editor_property('effect_type',effect);assets.save_loaded_asset(fx)
assert level.new_level(MAP)
def spawn(cls,label,pos,rot=(0,0,0)):
 a=sub.spawn_actor_from_class(cls,unreal.Vector(*pos),unreal.Rotator(*rot));assert a
 a.set_actor_label(label);a.set_folder_path('Week07/LiveDemo');return a
cube=unreal.load_asset('/Engine/BasicShapes/Cube')
baseline=unreal.load_asset('/Engine/BasicShapes/BasicShapeMaterial')
def mesh(label,pos,scale):
 a=spawn(unreal.StaticMeshActor,label,pos);a.static_mesh_component.set_static_mesh(cube);a.set_actor_scale3d(unreal.Vector(*scale));a.static_mesh_component.set_material(0,baseline);return a
floor=mesh('W07_Stage',(150,0,-25),(18,18,.4))
target=mesh('W07_Crate_Target',(-150,-220,65),(1.3,1.3,1.3));target.tags=['W07_MaterialTarget']
protected=mesh('W07_Crate_Protected',(-150,220,65),(1.3,1.3,1.3));protected.tags=['W07_Protected']
for i,y in enumerate([-300,0,300],1):
 a=spawn(unreal.TargetPoint,f'W07_VFXAnchor_{i}',(300,y,20));a.tags=['W07_VFXAnchor']
 mesh(f'W07_Marker_Base_{i}',(300,y,0),(.7,.7,.12))
sun=spawn(unreal.DirectionalLight,'W07_KeyLight',(-500,-300,850),(-45,-30,0));sun.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);sun.light_component.set_intensity(5.)
sky=spawn(unreal.SkyLight,'W07_FillLight',(0,0,600));sky.light_component.set_mobility(unreal.ComponentMobility.MOVABLE);sky.light_component.set_editor_property('real_time_capture',True)
spawn(unreal.SkyAtmosphere,'W07_Sky',(0,0,0))
post=spawn(unreal.PostProcessVolume,'W07_Exposure',(0,0,0));post.unbound=True
s=post.settings;s.override_auto_exposure_min_brightness=True;s.override_auto_exposure_max_brightness=True;s.auto_exposure_min_brightness=1.;s.auto_exposure_max_brightness=1.;post.settings=s
position=unreal.Vector(-1100,-1050,900);rotation=unreal.MathLibrary.find_look_at_rotation(position,unreal.Vector(80,0,100))
camera=sub.spawn_actor_from_class(unreal.CameraActor,position,rotation);camera.set_actor_label('W07_LiveDemo_Camera');camera.camera_component.set_field_of_view(55)
unreal.EditorLevelLibrary.set_level_viewport_camera_info(position,rotation)
sub.set_selected_level_actors([target]);unreal.EditorAssetLibrary.sync_browser_to_objects([t.get_path_name() for t in textures.values()])
assert level.save_current_level()
catalogue={'schema_version':1,'materials':{'prepared_surface':{'label':'Classroom blue surface','parent':parent_path}},'vfx':{'classroom_fountain':{'label':'Classroom fountain','system':fx_path,'reviewed_for_demo':False,'review_note':'Pending live preset review.','max_new':3}}}
(root/'Config/Week07ToolPresets.json').write_text(json.dumps(catalogue,indent=2)+'\n',encoding='utf-8')
(root/'Saved/LiveRehearsal/setup.json').write_text(json.dumps({'map':MAP,'parent':parent_path,'textures':{k:v.get_path_name() for k,v in textures.items()},'fx':fx_path,'source_fx':'/Niagara/DefaultAssets/Templates/Systems/FountainLightweight','baseline_saved':True},indent=2),encoding='utf-8')
print('PREPARED',MAP)
