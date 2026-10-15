"""UE04: Content Browser selection is independent of the Outliner selection."""

# Section: setup
import unreal

# Section: focus
assets = unreal.EditorUtilityLibrary.get_selected_assets()
print("Selected assets:", len(assets))
for asset in assets:
    print(asset.get_name(), asset.get_class().get_name())
    print(asset.get_path_name())
