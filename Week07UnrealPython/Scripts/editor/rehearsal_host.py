"""Explicitly launched, local-file rehearsal harness. No network endpoint or startup hook."""
from pathlib import Path
import contextlib
import io
import json
import time
import traceback
import unreal

ROOT = Path(unreal.Paths.project_dir()).resolve()
assert ROOT.name == 'Week07UnrealPython'
OUT = ROOT / 'Saved/LiveRehearsal'
OUT.mkdir(parents=True, exist_ok=True)
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
state = {'last': None, 'poll': 0.0}
if (OUT / 'request.json').exists():
    try:
        state['last'] = json.loads((OUT / 'request.json').read_text(encoding='utf-8'))['id']
    except (OSError, ValueError, KeyError):
        pass
scope = {'unreal': unreal, 'ROOT': ROOT, 'OUT': OUT}

def tick(delta):
    if time.monotonic() - state['poll'] < .2:
        return
    state['poll'] = time.monotonic()
    request = OUT / 'request.json'
    if not request.exists():
        return
    try:
        data = json.loads(request.read_text(encoding='utf-8'))
    except (ValueError, OSError):
        return
    if data['id'] == state['last']:
        return
    state['last'] = data['id']
    output = io.StringIO()
    result = {'id': data['id'], 'ok': False}
    try:
        with contextlib.redirect_stdout(output):
            exec(compile(data['code'], '<explicit local rehearsal>', 'exec'), scope)
        result['ok'] = True
    except Exception:
        result['error'] = traceback.format_exc()
    result['stdout'] = output.getvalue()
    (OUT / ('response-' + data['id'] + '.json')).write_text(json.dumps(result, indent=2), encoding='utf-8')

handle = unreal.register_slate_post_tick_callback(tick)
(OUT / 'ready.json').write_text(json.dumps({'engine': unreal.SystemLibrary.get_engine_version(), 'project': str(ROOT)}), encoding='utf-8')
