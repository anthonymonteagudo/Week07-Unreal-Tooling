camera=next(a for a in actor_sub.get_all_level_actors() if a.get_actor_label()=='W07_LiveDemo_Camera')
cap=unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(REHEARSAL/'captures/material-result.png'),camera=camera,delay=.5,force_game_view=True)
print('Material scene capture requested')
