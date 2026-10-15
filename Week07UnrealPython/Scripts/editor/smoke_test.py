"""Regression checks in a separate full editor. Does not save any maps or assets."""
import json
import os
from pathlib import Path
import traceback
import unreal
import week07_tools as w7

result_path = Path(os.environ['WEEK07_RESULT_PATH'])
result = {'status': 'FAIL', 'checks': {}}
try:
    assert Path(unreal.Paths.project_dir()).resolve().name == 'Week07UnrealPython'
    level = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    assert level.load_level(w7.DEMO_MAP)
    w7.reload_tools()
    sub = w7.actors()
    checks = result['checks']
    checks['hello_example'] = bool(w7.run_example('01_hello_editor')['engine'])
    checks['saved_baseline'] = all(r['status'] == 'FAIL' for r in w7.check())
    sub.clear_actor_selection_set()
    checks['empty_selection'] = w7.preview() is None and w7.apply(None) == 0
    floor = next(a for a in sub.get_all_level_actors() if a.get_actor_label() == 'W07_Stage')
    sub.set_selected_level_actors([floor])
    try:
        w7.preview()
        raise AssertionError('Unrelated Actor accepted')
    except ValueError:
        checks['unrelated_actor_rejected'] = True
    w7.select_demo()
    rows = w7.run_example('02_inspect_selection')
    by_label = {r['actor']: r for r in rows}
    checks['shared_asset'] = by_label['prop_temp_1']['components'][0]['mesh_asset'] == by_label['prop_temp_3']['components'][0]['mesh_asset']
    plan = w7.run_example('03_preview_changes')
    checks['preview_no_mutation'] = all(r['status'] == 'FAIL' for r in w7.check())
    sub.set_selected_level_actors(w7.fixture()[:2])
    try:
        w7.apply(plan)
        raise AssertionError('Stale preview accepted')
    except RuntimeError:
        checks['stale_preview_rejected'] = True
    w7.select_demo()
    plan = w7.run_example('03_preview_changes')
    checks['apply_six'] = w7.run_example('04_apply_reviewed_plan', plan=plan) == 6
    checks['all_pass'] = all(r['status'] == 'PASS' for r in w7.run_example('05_validate_fixture'))
    checks['repeat_noop'] = w7.apply(w7.preview()) == 0
    w7.reset_demo()
    checks['reset_baseline'] = all(r['status'] == 'FAIL' for r in w7.check())
    # Confirm reload revisits dependencies, not only the facade module.
    from week07_tooling import rules
    rules.KINDS = ['Broken']
    w7.reload_tools()
    checks['reload_dependencies'] = rules.target_for(5)['label'] == 'W07_Chair_06'
    assert all(checks.values()), checks
    result['status'] = 'PASS'
    result['engine'] = unreal.SystemLibrary.get_engine_version()
except Exception:
    result['error'] = traceback.format_exc()
    unreal.log_error(result['error'])
finally:
    result_path.write_text(json.dumps(result, indent=2), encoding='utf-8')
    unreal.log('WEEK07_TOOLING_TEST_' + result['status'])
