"""Stable classroom entry point. Existing slides and capture scripts keep working.

In Unreal's Python console:
    import week07_tools as w7
    w7.reload_tools()             # Save in VS Code, then reload here.
    w7.list_examples()
    w7.run_example('02_inspect_selection')
"""
import importlib
import sys

from week07_tooling import config, rules
from week07_tooling.editor import demo
# Explicit exports keep VS Code navigation/completion useful as well as runtime compatibility.
from week07_tooling.config import DEMO_MAP, TAG, FOLDER, BASELINE, KINDS
from week07_tooling.editor.demo import (
    actors, world, fixture, select_demo, inspect_selection, preview, apply,
    check, reset_demo, camera_view, capture_view, export_report,
)

_PUBLIC = ('actors', 'world', 'fixture', 'select_demo', 'inspect_selection',
           'preview', 'apply', 'check', 'reset_demo', 'camera_view',
           'capture_view', 'export_report')
_CONSTANTS = ('DEMO_MAP', 'TAG', 'FOLDER', 'BASELINE', 'KINDS')
_EXAMPLES = {
    '01_hello_editor': 'Read engine and project context; no edits.',
    '02_inspect_selection': 'Actor -> Component -> asset for the current selection.',
    '03_preview_changes': 'Return a plan for the selected fixture props; no edits.',
    '04_apply_reviewed_plan': 'Apply an explicitly supplied plan; one Undo step.',
    '05_validate_fixture': 'Read the six-prop rule report.',
}


def _bind():
    for name in _PUBLIC:
        globals()[name] = getattr(demo, name)
    for name in _CONSTANTS:
        globals()[name] = getattr(config, name)


def reload_tools():
    """Close the shared Qt panel, expire native plans, then reload. No scene edits."""
    importlib.invalidate_caches()
    # Close UI before replacing code, so old callbacks/plans cannot survive reload.
    host = sys.modules.get('week07_tooling.ui.host')
    if host is not None:
        host.close()
    bridge = sys.modules.get('week07_tooling.editor.native_bridge')
    if bridge is not None:
        bridge.close_all()
    for module in (config, rules, demo):
        importlib.reload(module)
    for name in ('week07_tooling.ui.controller', 'week07_tooling.ui.offline_backend',
                 'week07_tooling.workflows', 'week07_tooling.workflow_presentation', 'week07_tooling.workflow_sample',
                 'week07_tooling.editor.workflow_backend',
                 'week07_tooling.editor.ui_backend', 'week07_tooling.editor.native_bridge',
                 'week07_tooling.editor.native_panel',
                 'week07_tooling.ui.views',
                 'week07_tooling.ui.window', 'week07_tooling.ui.assistants', 'week07_tooling.ui.host'):
        if name in sys.modules:
            importlib.reload(sys.modules[name])
    for name in sorted(sys.modules.copy()):
        if name.startswith('week07_tooling.examples.'):
            importlib.reload(sys.modules[name])
    _bind()
    print('W07: Tools reloaded. Review a fresh plan before Apply.')


def list_examples():
    for name, description in _EXAMPLES.items():
        print(f'{name}: {description}')
    return dict(_EXAMPLES)


def show_pyside_ui(stage=3):
    """Open Prop Inspector's external Qt comparison UI; stages 1/2/3."""
    from week07_tooling.ui import host
    return host.show(stage)


def show_ui(stage=3):
    """Compatibility alias for show_pyside_ui. Native EUW is a separate interface."""
    return show_pyside_ui(stage)


def show_assistants():
    """Open PySide Material Setup and VFX Placement; prepared assets still required."""
    from week07_tooling.ui import host
    return host.show('workflows')


def close_ui():
    """Close the panel and remove its Slate callback."""
    host = sys.modules.get('week07_tooling.ui.host')
    if host is not None:
        host.close()


def run_example(name, **kwargs):
    """Reload (closing UI/expiring native plans), then run a prop-fixture lesson."""
    if name not in _EXAMPLES:
        raise ValueError(f'Unknown example {name!r}. Run list_examples().')
    reload_tools()
    module = importlib.import_module('week07_tooling.examples.e' + name)
    return module.run(**kwargs)


_bind()
