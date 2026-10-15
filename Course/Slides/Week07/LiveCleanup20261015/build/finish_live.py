assert unreal.Week07EditorLibrary.undo_demo()
record('Final clean demo state after all rehearsals')
assert not EVIDENCE['steps'][-1]['effects']
assert all(v['material'].startswith('/Engine/BasicShapes/') for v in EVIDENCE['steps'][-1]['cubes'].values())
print(live_demo.preflight())
print('Dirty maps:',[p.get_path_name() for p in unreal.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
w7.close_ui()
