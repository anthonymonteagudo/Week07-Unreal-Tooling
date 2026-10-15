assert not unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()
assert len(unreal.EditorUtilityLibrary.get_selected_assets())==3
record('Ready for instructor: clean map, material target and textures selected')
import sys
unreal.unregister_slate_post_tick_callback(sys._getframe(1).f_globals['handle'])
print('Local rehearsal callback stopped. Editor stays open on the prepared map.')
