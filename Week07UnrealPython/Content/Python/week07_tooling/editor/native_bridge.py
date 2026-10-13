"""Qt-free Python boundary shared by the native Slate panel and possible EUWs.

No widget asset is created here. Blueprint calls these functions through Execute
Python Script pins. Each widget instance owns a session; plans stay in Python.
Importing this module requires neither PySide nor Unreal.
"""
import json
from uuid import uuid4
from week07_tooling.ui.controller import ToolController

_sessions = {}
_workflow_sessions = {}
_actions = {'refresh', 'select_demo', 'preview', 'validate', 'apply', 'reset'}


def open_session(backend=None):
    if backend is None:
        from week07_tooling.editor.ui_backend import UnrealBackend
        backend = UnrealBackend()
    session_id = uuid4().hex
    _sessions[session_id] = ToolController(backend)
    return session_id


def close_session(session_id):
    _sessions.pop(session_id, None)
    _workflow_sessions.pop(session_id, None)


def close_all():
    """Reload invalidates all native UI sessions; old widgets must reconnect."""
    _sessions.clear()
    _workflow_sessions.clear()


def open_workflow_session(backend=None):
    """A separate session for Material Setup/VFX; no Qt dependency."""
    from week07_tooling.workflows import WorkflowSession
    if backend is None:
        from week07_tooling.editor.workflow_backend import EditorWorkflowBackend
        backend = EditorWorkflowBackend()
    session_id = uuid4().hex
    _workflow_sessions[session_id] = WorkflowSession(backend)
    return session_id


def dispatch_workflow(session_id, action, kind='', request_json='{}', warnings_reviewed=False):
    """Return JSON for the native interface; no dynamic code evaluation."""
    session = _workflow_sessions.get(session_id)
    if session is None:
        return json.dumps({'ok': False, 'can_apply': False, 'message': 'Session expired. Reconnect.'})
    try:
        if action == 'preview':
            plan = session.preview(kind, json.loads(request_json))
            from week07_tooling.workflow_presentation import describe_plan
            return json.dumps({'ok': True, 'can_apply': True, 'plan': plan,
                               'presentation': describe_plan(plan),
                               'warning_ack_required': bool(plan.get('warnings'))})
        if action == 'apply':
            message = session.apply(warnings_reviewed=warnings_reviewed)
        elif action == 'clear':
            session.clear()
            message = 'Preview cleared.'
        else:
            raise ValueError('Unknown workflow action.')
        return json.dumps({'ok': True, 'can_apply': False, 'message': message})
    except Exception as error:
        session.clear()
        return json.dumps({'ok': False, 'can_apply': False, 'message': str(error)})


def dispatch(session_id, action, reset_confirmed=False):
    """Return pin-friendly state. Never execute arbitrary command strings."""
    controller = _sessions.get(session_id)
    if controller is None:
        return {'ok': False, 'session_valid': False, 'status_text': 'Session expired. Reconnect the tool.',
                'tone': 'error', 'can_apply': False, 'change_count': 0, 'selection_count': 0,
                'preview_text': '', 'validation_text': '', 'world_text': '', 'report_json': '[]'}
    ok = True
    try:
        if action not in _actions:
            raise ValueError('Unknown tool action.')
        if action == 'reset' and reset_confirmed is not True:
            raise ValueError('Confirm Reset in the widget before restoring the fixture.')
        getattr(controller, action)()
    except Exception as error:
        controller.invalidate(str(error), 'error')
        ok = False
    plan = controller.plan or {'items': []}
    preview_lines = []
    for item in plan['items']:
        before, after = item['before'], item['after']
        preview_lines.append(f"{before['label']} → {after['label']}\n"
                             f"  cm: {before['location']} → {after['location']}")
    issues = {'LABEL': 'Naming rule mismatch', 'PLACEMENT': 'Layout position mismatch',
              'MISSING_MESH': 'Missing mesh reference; assign a mesh manually'}
    validation_lines = [f"{row['actor']} · {row['status']} · "
                        + ('; '.join(issues.get(i, i) for i in row['issues']) or 'No issues')
                        for row in controller.report]
    return {'ok': ok and controller.tone != 'error', 'session_valid': True,
            'status_text': controller.message, 'tone': controller.tone,
            'can_apply': controller.can_apply, 'change_count': controller.change_count,
            'selection_count': len(controller.snapshot['selected']) if controller.snapshot else 0,
            'world_text': controller.snapshot['world'] if controller.snapshot else '',
            'preview_text': '\n\n'.join(preview_lines),
            'validation_text': '\n'.join(validation_lines),
            'report_json': json.dumps(controller.report, indent=2)}
