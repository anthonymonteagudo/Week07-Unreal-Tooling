def buildSelectedAssets(folderPath,fileNames):
    """
    Sets up static mesh, material instances, and textures.  Args passed in by import script.
    """
    # lists to hold new assets
    textures = []
    geo = []
    materialInstances = []
    # create asset tools instance
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    EAL = unreal.EditorAssetLibrary()
    # hard coded path to parent material
    materialParent = EAL.load_asset('/Game/Meshes/ImportTest/M_parent')
    # get all assets in folder path
    for assetPath in EAL.list_assets(folderPath):
        # clean up asset path
        assetPath = assetPath.split('.')[0]
        # identify newly import assets
        # load assets, located file import path, and compare to file import paths passed in from import script.
        asset = EAL.load_asset(assetPath)
        try:
            assetImportData = asset.get_editor_property('asset_import_data')
            importfilePath = assetImportData.get_first_filename()
            if importfilePath in fileNames:
                if isinstance(asset, unreal.StaticMesh):
                    geo.append(asset)
                if isinstance(asset, unreal.Texture):
                    textures.append(asset)
        except AttributeError: # not all assets have asset import data
            pass
    for staticMesh in geo:
        # get asset name from static mesh to find textures later
        assetName = staticMesh.get_name().split('_')[1]
        # iterate over all static materials associated with mesh
        for staticMaterial in staticMesh.static_materials:
            # get the index of the current static material for later
            index = staticMesh.static_materials.index(staticMaterial)
            # locate and delete the default material created on import
            matPath = staticMaterial.material_interface.get_path_name()
            unreal.EditorAssetLibrary.delete_asset(matPath)
            # create new material instance
            materialInstance = assetTools.create_asset(
                staticMaterial.material_slot_name,
                folderPath,
                unreal.MaterialInstanceConstant,
                unreal.MaterialInstanceConstantFactoryNew(),
            )
            materialInstances.append(materialInstance)
            # set parent material
            materialInstance.set_editor_property('parent', materialParent)
            # assign new material instance to correct material slot
            staticMesh.set_material(index, materialInstance)
            # iterate over textures
            for texture in textures:
                # identify textures associated with asset by naming convention
                if assetName in texture.get_name():
                    # get parameter name from texture name - i.e. T_Airconditioner_BC -> BC
                    parameterName = texture.get_name().split('_')[-1]
                    # set up material instance parameter
                    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(
                        materialInstance,
                        parameterName,
                        texture
                )
    # save all new assets
    newAssets = [geo,textures,materialInstances]
    for list in newAssets:
        for asset in list:
            unreal.EditorAssetLibrary.save_asset(asset.get_path_name())