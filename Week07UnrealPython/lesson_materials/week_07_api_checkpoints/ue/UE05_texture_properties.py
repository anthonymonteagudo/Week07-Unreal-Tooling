"""UE05: read properties of selected textures; skip other asset classes."""
# %% setup
import unreal
assets = unreal.EditorUtilityLibrary.get_selected_assets()
textures = [a for a in assets if isinstance(a, unreal.Texture2D)]
print("Textures:", len(textures), "skipped:", len(assets) - len(textures))

# %% focus
for texture in textures:
    compression = texture.get_editor_property("compression_settings")
    srgb = texture.get_editor_property("srgb")
    print(texture.get_name(), compression, "sRGB:", srgb)
