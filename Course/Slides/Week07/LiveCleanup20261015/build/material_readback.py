record('Native Material Apply through button')
i=unreal.load_asset('/Game/Week07/Generated/Materials/MI_Crate_Live')
readback={n:unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(i,n).get_path_name() for n in ['BaseColorTexture','NormalTexture','ORMTexture']}
EVIDENCE['material_texture_readback']=readback
(REHEARSAL/'qa/live-rehearsal.json').write_text(json.dumps(EVIDENCE,indent=2),encoding='utf-8')
print(readback)
