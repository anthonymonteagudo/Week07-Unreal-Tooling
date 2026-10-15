record('Material Undo verified')
assert EVIDENCE['steps'][-1]['cubes']['W07_Crate_Target']['material'].startswith('/Engine/BasicShapes/BasicShapeMaterial')
assert unreal.EditorAssetLibrary.does_asset_exist('/Game/Week07/Generated/Materials/MI_Crate_Live')
print('Undo restored component and retained created asset, as expected.')
