import unreal,json
from pathlib import Path
from week07_tooling.editor import live_demo
print('ENGINE',unreal.SystemLibrary.get_engine_version())
print('WORLD',unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world().get_path_name())
print('DIRTY_MAPS',[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
print(live_demo.preflight())
