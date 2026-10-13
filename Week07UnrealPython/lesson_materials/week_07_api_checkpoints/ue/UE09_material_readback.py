"""UE09: inspect one selected material instance after the prepared tool demo."""
# %% setup
import unreal
assets = unreal.EditorUtilityLibrary.get_selected_assets()
if len(assets) != 1 or not isinstance(assets[0], unreal.MaterialInstanceConstant):
    raise RuntimeError("Select one material instance in the Content Browser.")
instance = assets[0]
library = unreal.MaterialEditingLibrary

# %% focus
names = library.get_texture_parameter_names(instance)
print("Texture parameters:", len(names))
for name in names:
    texture = library.get_material_instance_texture_parameter_value(
        instance, name)
    print(name, texture.get_path_name() if texture else None)
