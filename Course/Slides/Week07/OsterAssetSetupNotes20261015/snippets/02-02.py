import unreal

def create_empty_instance(asset_name, destination):
    target = f"{destination.rstrip('/')}/{asset_name}"
    if unreal.EditorAssetLibrary.does_asset_exist(target):
        raise ValueError(f"Destination already exists: {target}")

    instance = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name,
        destination,
        unreal.MaterialInstanceConstant,
        unreal.MaterialInstanceConstantFactoryNew(),
    )
    if not isinstance(instance, unreal.MaterialInstanceConstant):
        raise RuntimeError(f"Material-instance creation failed: {target}")
    return instance
