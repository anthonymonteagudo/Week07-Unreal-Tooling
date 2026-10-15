import unreal

def import_prepared_files(file_names, destination):
    data = unreal.AutomatedAssetImportData()
    data.set_editor_property("filenames", list(file_names))
    data.set_editor_property("destination_path", destination)
    data.set_editor_property("replace_existing", False)

    tools = unreal.AssetToolsHelpers.get_asset_tools()
    imported = tools.import_assets_automated(data)
    meshes = [obj for obj in imported
              if isinstance(obj, unreal.StaticMesh)]
    textures = [obj for obj in imported
                if isinstance(obj, unreal.Texture)]
    return meshes, textures
