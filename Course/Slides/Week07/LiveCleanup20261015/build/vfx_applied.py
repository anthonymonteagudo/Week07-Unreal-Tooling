assert unreal.Week07EditorLibrary.capture_tools(str(REHEARSAL/'captures/native-vfx-applied.png'))
record('Native VFX Apply: 3 effects')
assert len(EVIDENCE['steps'][-1]['effects'])==3
for a in actor_sub.get_all_level_actors():
 if 'W07_PlacedVFX' in [str(t) for t in a.tags]:
  assert a.get_component_by_class(unreal.NiagaraComponent).get_asset().get_name()=='NS_ClassroomFountain'
  assert a.get_actor_scale3d()==unreal.Vector(1,1,1)
cap=unreal.AutomationLibrary.take_high_res_screenshot(1600,900,str(REHEARSAL/'captures/vfx-result.png'),delay=1,force_game_view=True)
