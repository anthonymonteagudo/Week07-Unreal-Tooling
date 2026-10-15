print('MATERIAL_CAPTURE_DONE',cap.is_task_done())
assert cap.is_task_done()
assert unreal.Week07EditorLibrary.undo_demo()
record('Material assignment Undo')
assert EVIDENCE['steps'][-1]['cubes']==EVIDENCE['steps'][0]['cubes']
EVIDENCE['material_undo_retained_asset']=unreal.EditorAssetLibrary.does_asset_exist('/Game/Week07/Generated/Materials/MI_Crate_Live')
cap=unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(REHEARSAL/'captures/baseline-recovered.png'),camera=camera,delay=.5,force_game_view=True)
print(live_demo.select_vfx())
