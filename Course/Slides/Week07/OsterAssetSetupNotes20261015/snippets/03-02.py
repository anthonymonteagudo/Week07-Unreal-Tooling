import unreal

def configure_instance(instance, parent, bindings):
    if not isinstance(instance, unreal.MaterialInstanceConstant):
        raise TypeError("Expected a MaterialInstanceConstant")
    if not isinstance(parent, unreal.MaterialInterface):
        raise TypeError("Expected a material parent")

    library = unreal.MaterialEditingLibrary
    available = {str(name) for name in library.get_texture_parameter_names(parent)}
    for parameter, texture in bindings.items():
        if parameter not in available or not isinstance(texture, unreal.Texture):
            raise ValueError(f"Invalid texture binding: {parameter}")

    library.set_material_instance_parent(instance, parent)
    for parameter, texture in bindings.items():
        setter_result = library.set_material_instance_texture_parameter_value(
            instance, parameter, texture
        )
        actual = library.get_material_instance_texture_parameter_value(
            instance, parameter
        )
        if actual != texture:
            raise RuntimeError(
                f"Texture readback mismatch: {parameter}; setter={setter_result}"
            )
    library.update_material_instance(instance)
