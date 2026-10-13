"""UE07: distinguish a host disk path from an Unreal object path."""
# %% setup
import unreal
from pathlib import Path

# %% focus
disk_folder = Path(unreal.Paths.project_dir()) / "Content"
object_path = "/Engine/BasicShapes/Cube.Cube"
mesh = unreal.load_asset(object_path)
print("Disk folder:", disk_folder)
print("Loaded object:", mesh.get_path_name() if mesh else None)
print("Content directory exists:", disk_folder.is_dir())
