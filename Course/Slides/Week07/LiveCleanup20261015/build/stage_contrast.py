# Improve the actual classroom stage so white VFX are legible against the ground.
assert not EVIDENCE['steps'][-1]['effects']
for a in actor_sub.get_all_level_actors():
 if a.get_actor_label() in ('W07_Crate_Target','W07_Crate_Protected'):
  assert a.get_component_by_class(unreal.StaticMeshComponent).get_material(0).get_path_name().startswith('/Engine/BasicShapes/')
p='/Game/Week07/LiveDemo/Materials/M_StageBackdrop'
assert not unreal.EditorAssetLibrary.does_asset_exist(p)
m=unreal.AssetToolsHelpers.get_asset_tools().create_asset('M_StageBackdrop','/Game/Week07/LiveDemo/Materials',unreal.Material,unreal.MaterialFactoryNew())
lib=unreal.MaterialEditingLibrary
color=lib.create_material_expression(m,unreal.MaterialExpressionConstant3Vector,-250,0)
color.set_editor_property('constant',unreal.LinearColor(.035,.045,.06,1))
assert lib.connect_material_property(color,'',unreal.MaterialProperty.MP_BASE_COLOR)
rough=lib.create_material_expression(m,unreal.MaterialExpressionConstant,-250,150)
rough.set_editor_property('r',1.)
assert lib.connect_material_property(rough,'',unreal.MaterialProperty.MP_ROUGHNESS)
lib.recompile_material(m)
floor=next(a for a in actor_sub.get_all_level_actors() if a.get_actor_label()=='W07_Stage')
floor.get_component_by_class(unreal.StaticMeshComponent).set_material(0,m)
assert unreal.EditorAssetLibrary.save_loaded_asset(m)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
print('Saved only stage material and baseline classroom map; no tool results saved.')
record('Improved stage contrast: clean fixture saved')
print(qt.windowTitle(),qt.isVisible())
