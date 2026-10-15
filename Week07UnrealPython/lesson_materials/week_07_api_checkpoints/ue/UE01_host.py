"""UE01: run inside Unreal's Python editor console or Execute Python Script."""

# Section: setup
import unreal

# Section: focus
unreal.log("Hello from Unreal")
print(unreal.SystemLibrary.get_engine_version())
print(unreal.Paths.project_dir())
