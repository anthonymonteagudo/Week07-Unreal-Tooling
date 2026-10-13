"""UE11: prepare an import task. This checkpoint does NOT execute an import."""
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

# %% check
print("Prepared only:", task.filename, "to", destination + "/" + asset_name)
print("No import call has run. UE12 contains the execution checkpoint.")
