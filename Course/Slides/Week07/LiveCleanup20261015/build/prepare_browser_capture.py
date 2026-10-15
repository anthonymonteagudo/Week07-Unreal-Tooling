host.close()
normal=unreal.load_asset('/Game/Week07/LiveDemo/Textures/T_Crate_Normal')
unreal.EditorAssetLibrary.sync_browser_to_objects([normal.get_path_name()])
print('Normal readback:',normal.get_name(),normal.get_editor_property('compression_settings'),normal.get_editor_property('srgb'))
