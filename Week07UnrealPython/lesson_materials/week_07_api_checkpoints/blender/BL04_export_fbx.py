"""BL04: basic FBX export from the prepared bridge scene.

Exports one selected static mesh to a new temporary folder. Does not modify the
source geometry or promise the production adapter's transform/pivot guarantees.
Every run creates a new folder, printed below. Remove only that folder when done.
"""
# %% setup
import bpy
from pathlib import Path
import tempfile
objects = list(bpy.context.selected_objects)
if bpy.context.mode != "OBJECT" or len(objects) != 1 or objects[0].type != "MESH":
    raise RuntimeError("In Object Mode, select exactly one mesh object.")
if objects[0].find_armature() or objects[0].data.shape_keys:
    raise RuntimeError("This exercise uses an unrigged mesh without shape keys.")
output = Path(tempfile.mkdtemp(prefix="week07-api-")) / "lesson_mesh.fbx"

# %% focus
result = bpy.ops.export_scene.fbx(
    filepath=str(output), use_selection=True,
    object_types={"MESH"}, use_mesh_modifiers=True,
    bake_anim=False, add_leaf_bones=False,
    axis_forward="-Y", axis_up="Z")

# %% check
if result != {"FINISHED"} or not output.is_file() or output.stat().st_size == 0:
    raise RuntimeError("No nonempty FBX produced: " + str(output))
print("Exported:", output)
print("This proves a file exists. Inspect the imported result in Unreal.")
