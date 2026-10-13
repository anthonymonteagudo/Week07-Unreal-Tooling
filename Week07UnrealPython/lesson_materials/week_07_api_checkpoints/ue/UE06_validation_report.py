"""UE06: _N is an illustrative project convention, not proof of image content."""
# %% setup
import unreal
assets = unreal.EditorUtilityLibrary.get_selected_assets()
textures = [a for a in assets if isinstance(a, unreal.Texture2D)]
expected = unreal.TextureCompressionSettings.TC_NORMALMAP
checked, mismatches = 0, 0

# %% focus
for texture in textures:
    if not texture.get_name().endswith("_N"):
        continue
    checked += 1
    actual = texture.get_editor_property("compression_settings")
    if actual != expected:
        mismatches += 1
        print("MISMATCH", texture.get_path_name(), actual, expected)

# %% check
print("Checked:", checked, "mismatches:", mismatches)
if checked == 0:
    print("No matching _N textures. This is not a passing validation.")
