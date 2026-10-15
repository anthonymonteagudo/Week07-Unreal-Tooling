import unreal

def describe_material_slots(mesh):
    if not isinstance(mesh, unreal.StaticMesh):
        raise TypeError("Expected a StaticMesh asset")

    slots = mesh.get_editor_property("static_materials")
    for index, slot in enumerate(slots):
        material = slot.get_editor_property("material_interface")
        name = str(slot.get_editor_property("material_slot_name"))
        path = material.get_path_name() if material else "<unassigned>"
        print(index, name, path)
