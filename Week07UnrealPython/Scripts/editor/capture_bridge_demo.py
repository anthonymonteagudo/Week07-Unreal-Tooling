"""Capture the saved comparison map in a separate editor process."""
from pathlib import Path
import time
import traceback
import unreal
from week07_bridge import core

root = Path(unreal.Paths.project_dir()).resolve()
out = root / 'Docs/Bridge'
out.mkdir(parents=True, exist_ok=True)
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level('/Game/Week07/Bridge/W07_BridgeComparison')
from week07_bridge.unreal_demo import style
style()
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
camera = next(a for a in actors.get_all_level_actors() if a.get_actor_label() == 'Bridge comparison camera')
actors.clear_actor_selection_set()
started = time.monotonic()
state = {'task': None}


def tick(delta):
    try:
        if time.monotonic() - started > 90:
            raise TimeoutError('Screenshot timed out')
        if state['task']:
            if not state['task'].is_task_done():
                return
            assert (out / 'unreal-comparison.png').is_file()
            core.atomic_json(out / 'capture-evidence.json', {'status': 'PASS',
                'kind': 'Actual Unreal 5.7.4 editor render of the saved bridge comparison map',
                'image': 'unreal-comparison.png'})
            unreal.unregister_slate_post_tick_callback(handle)
            unreal.SystemLibrary.quit_editor()
        elif time.monotonic() - started > 6:
            unreal.AutomationLibrary.finish_loading_before_screenshot()
            state['task'] = unreal.AutomationLibrary.take_high_res_screenshot(
                1280, 720, str(out / 'unreal-comparison.png'), camera=camera,
                delay=.5, force_game_view=True)
    except Exception:
        core.atomic_json(out / 'capture-evidence.json', {'status': 'FAIL', 'error': traceback.format_exc()})
        unreal.unregister_slate_post_tick_callback(handle)
        unreal.SystemLibrary.quit_editor()


handle = unreal.register_slate_post_tick_callback(tick)
