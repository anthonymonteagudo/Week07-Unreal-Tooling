"""Capture actual editor-rendered baseline / apply / reset states. Never save edits."""
import json
from pathlib import Path
import time
import traceback
import unreal
import week07_tools as w7

root = Path(unreal.Paths.project_dir()).resolve()
assert root.name == 'Week07UnrealPython'
out = root / 'Saved/Week07/Captures'
out.mkdir(parents=True, exist_ok=True)
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
assert unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(w7.DEMO_MAP)
w7.select_demo()
w7.camera_view()
camera = next(a for a in w7.actors().get_all_level_actors() if a.get_actor_label() == 'W07_Camera_Overview')
names = ['01_baseline', '02_organized', '03_reset']
report = {'map': w7.DEMO_MAP, 'engine': unreal.SystemLibrary.get_engine_version(),
          'kind': 'Actual Unreal Editor renders; discrete tool states, not live screen recording', 'captures': []}
state = {'index': 0, 'task': None, 'since': time.monotonic(), 'start': time.monotonic(), 'prepared': False}
handle = None


def finish():
    (out / 'capture_manifest.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    unreal.unregister_slate_post_tick_callback(handle)
    unreal.EditorPythonScripting.set_keep_python_script_alive(False)


def tick(delta):
    try:
        now = time.monotonic()
        if now - state['start'] > 240:
            raise TimeoutError('Capture exceeded four minutes.')
        if state['task']:
            if not state['task'].is_task_done():
                return
            file = out / (names[state['index']] + '.png')
            if not file.exists():
                raise RuntimeError(f'Capture missing: {file}')
            report['captures'].append({'file': file.name, 'camera': camera.get_actor_label(),
                                       'location': str(camera.get_actor_location()), 'rotation': str(camera.get_actor_rotation())})
            state.update(index=state['index'] + 1, task=None, since=now, prepared=False)
        if state['index'] == len(names):
            report['status'] = 'COMPLETE'
            unreal.log('W07_CAPTURE_OK')
            finish()
            return
        if not state['prepared']:
            if state['index'] == 0:
                w7.reset_demo()
            elif state['index'] == 1:
                w7.apply(w7.preview())
            else:
                w7.reset_demo()
            w7.actors().clear_actor_selection_set()
            state.update(prepared=True, since=now)
            unreal.AutomationLibrary.finish_loading_before_screenshot()
            return
        if now - state['since'] < 5:
            return
        # Selection was cleared to keep renders free of editor outlines; reselect only for next tool action.
        if state['index'] < 2:
            w7.select_demo()
        state['task'] = unreal.AutomationLibrary.take_high_res_screenshot(
            1600, 900, str(out / (names[state['index']] + '.png')),
            camera=camera, delay=0.5, force_game_view=True)
    except Exception:
        report.update(status='FAILED', error=traceback.format_exc())
        unreal.log_error(report['error'])
        finish()


handle = unreal.register_slate_post_tick_callback(tick)
