"""BL02: Object owns the transform; mesh data can be shared by several Objects."""
# %% setup
import bpy
objects = list(bpy.context.selected_objects)
meshes = [obj for obj in objects if obj.type == "MESH"]
print("Selected mesh objects:", len(meshes))

# %% focus
for obj in meshes:
    print("Object:", obj.name, "location:", tuple(obj.location))
    print("Mesh:", obj.data.name, "users:", obj.data.users)
    print("Source polygons:", len(obj.data.polygons))
