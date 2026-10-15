assert unreal.Week07EditorLibrary.capture_tools(str(REHEARSAL/'captures/native-material-applied.png'))
record('Updated native Material Apply')
s=EVIDENCE['steps'][-1]
assert s['cubes']['W07_Crate_Target']['material'].endswith('MI_Crate_Live.MI_Crate_Live')
assert s['cubes']['W07_Crate_Protected']['material'].startswith('/Engine/BasicShapes/')
assert all(v['mesh_default'].startswith('/Engine/EngineMaterials/WorldGridMaterial') for v in s['cubes'].values())
i=unreal.load_asset('/Game/Week07/Generated/Materials/MI_Crate_Live')
for parameter,suffix in [('BaseColorTexture','BaseColor'),('NormalTexture','Normal'),('ORMTexture','ORM')]:
 assert unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(i,parameter).get_name()=='T_Crate_'+suffix
# Capture the current viewport without piloting a camera or adding an Undo entry.
cap=unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(REHEARSAL/'captures/material-result.png'),delay=.2,force_game_view=True)
