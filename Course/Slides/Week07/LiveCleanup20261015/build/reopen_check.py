from week07_tooling.ui import host
qt=host.show('workflows')
available=qt.screen().availableGeometry()
frame=qt.frameGeometry()
print('Qt frame:',frame,'Screen:',available)
assert available.contains(frame), 'Qt panel extends off screen'
assert not unreal.EditorAssetLibrary.does_asset_exist('/Game/Week07/LiveDemo/Materials/MI_Crate_Live')
assert not unreal.EditorAssetLibrary.does_asset_exist('/Game/Week07/LiveDemo/Materials/MI_Crate_Final')
record('Clean restart; Qt panel fits screen; rehearsal assets discarded')
print('Dirty maps:',unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages())
