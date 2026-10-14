"""UE06: _Normal is an illustrative project convention, not proof of image content."""

# %% setup
import unreal
assets = unreal.EditorUtilityLibrary.get_selected_assets()
textures = [asset for asset in assets
            if isinstance(asset, unreal.Texture2D)]
expected = unreal.TextureCompressionSettings.TC_NORMALMAP
checked = 0
mismatches = 0

# %% focus
for texture in textures:
    if not texture.get_name().endswith("_Normal"):
        continue
    checked += 1
    actual = texture.get_editor_property("compression_settings")
    if actual != expected:
        mismatches += 1
        print("MISMATCH", texture.get_path_name(), actual, expected)

# %% check
print("Checked:", checked, "mismatches:", mismatches)
if checked == 0:
    print("No matching _Normal textures. This is not a passing validation.")
