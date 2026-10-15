"""BL01: run in Blender's Text Editor. Read selection without changing it."""

# Section: setup
import bpy

# Section: focus
print("Blender:", bpy.app.version_string)
print("Mode:", bpy.context.mode)
objects = list(bpy.context.selected_objects)
print("Selected objects:", len(objects))
for obj in objects:
    print(obj.name, obj.type)
