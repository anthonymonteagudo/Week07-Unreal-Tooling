"""BL03: read evaluated geometry and release the temporary mesh even on failure."""
# %% setup
import bpy
objects = list(bpy.context.selected_objects)
if bpy.context.mode != "OBJECT" or len(objects) != 1 or objects[0].type != "MESH":
    raise RuntimeError("In Object Mode, select exactly one mesh object.")
obj = objects[0]

# %% focus
graph = bpy.context.evaluated_depsgraph_get()
evaluated = obj.evaluated_get(graph)
mesh = evaluated.to_mesh()
try:
    print("Source polygons:", len(obj.data.polygons))
    print("Evaluated polygons:", len(mesh.polygons))
finally:
    evaluated.to_mesh_clear()
