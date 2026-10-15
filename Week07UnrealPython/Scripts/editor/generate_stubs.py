"""Wait for Unreal Developer Mode to generate project-specific autocomplete data."""
import json
import os
from pathlib import Path
import time
import unreal

stub = Path(unreal.Paths.project_intermediate_dir()) / 'PythonStub/unreal.py'
result_path = Path(os.environ['WEEK07_RESULT_PATH'])
started = time.monotonic()
unreal.EditorPythonScripting.set_keep_python_script_alive(True)
handle = None


def tick(delta):
    if not stub.exists() and time.monotonic() - started < 90:
        return
    result_path.write_text(json.dumps({'status': 'PASS' if stub.exists() else 'FAIL',
                                       'stub': str(stub.resolve())}, indent=2), encoding='utf-8')
    unreal.unregister_slate_post_tick_callback(handle)
    unreal.EditorPythonScripting.set_keep_python_script_alive(False)


handle = unreal.register_slate_post_tick_callback(tick)
