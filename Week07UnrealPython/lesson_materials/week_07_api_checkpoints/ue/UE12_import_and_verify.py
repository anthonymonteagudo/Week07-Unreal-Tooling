"""UE12: independent full checkpoint; repeats UE11's task preparation.

Creates one unsaved StaticMesh in /Game/Week07/APILessons. Refuses an existing
destination. Uses the prepared FBX and pins the legacy importer while it runs.
"""
# %% setup
import unreal
from pathlib import Path
root = Path(unreal.Paths.project_dir())
fbx = root / "Samples/Bridge/Handoffs/blender/baseline/SM_Compare_Blender.fbx"
destination = "/Game/Week07/APILessons"
asset_name = "SM_API_Wedge"
if not fbx.is_file():
    raise RuntimeError("Open the Week07UnrealPython project with Samples included.")

# %% options
options = unreal.FbxImportUI()
options.set_editor_property("import_mesh", True)
options.set_editor_property("import_as_skeletal", False)
options.set_editor_property("import_materials", False)
options.set_editor_property("import_textures", False)
options.set_editor_property("automated_import_should_detect_type", False)
options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)

# %% task
task = unreal.AssetImportTask()
task.set_editor_property("filename", str(fbx))
task.set_editor_property("destination_path", destination)
task.set_editor_property("destination_name", asset_name)
task.set_editor_property("automated", True)
task.set_editor_property("replace_existing", False)
task.set_editor_property("save", False)
task.set_editor_property("options", options)
task.set_editor_property("factory", unreal.FbxFactory())

# %% eligibility
package = destination + "/" + asset_name
level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
if level.is_in_play_in_editor():
    raise RuntimeError("Stop Play in Editor before importing.")
if unreal.EditorAssetLibrary.does_asset_exist(package):
    raise RuntimeError("Lesson destination already exists. Inspect it; do not overwrite.")

# %% focus
flag = "Interchange.FeatureFlags.Import.FBX"
previous = unreal.SystemLibrary.get_console_variable_int_value(flag)
try:
    unreal.SystemLibrary.execute_console_command(None, flag + " 0")
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    tools.import_asset_tasks([task])
finally:
    unreal.SystemLibrary.execute_console_command(None, flag + " " + str(previous))

# %% check
paths = list(task.get_editor_property("imported_object_paths"))
mesh = unreal.load_asset(package)
if package + "." + asset_name not in paths or not isinstance(mesh, unreal.StaticMesh):
    raise RuntimeError("Expected mesh missing. Inspect importer output and Content Browser.")
print("Imported:", paths)
print("Bounds:", mesh.get_bounding_box())
print("Not saved. Inspect size, axes and pivot. Import is not a general Undo transaction.")


