"""JSON boundary for the native Slate panel, using the same workflow session."""
import json
from week07_tooling.editor import native_bridge

def dispatch(payload):
    data = json.loads(payload)
    action = data.get('action')
    identity = data.get('session', '')
    if action == 'connect':
        return json.dumps({'session': native_bridge.open_workflow_session(), 'can_apply': False,
                           'message': 'Choose inputs, then Preview.'})
    if action == 'close':
        native_bridge.close_session(identity)
        return json.dumps({'can_apply': False, 'message': 'Closed.'})
    try:
        session = native_bridge._workflow_sessions.get(identity)
        if session is None:
            raise ValueError('Session expired. Reconnect and preview again.')
        kind = data.get('kind', 'material')
        if action == 'preview':
            options = session.backend.options()
            if kind == 'material':
                if not options['materials']:
                    raise ValueError('Instructor setup needed: no prepared parent.')
                request = {'master': options['materials'][0]['value'], 'name': data['name'], 'slot': int(data['slot'])}
            elif kind == 'vfx':
                if not options['vfx']:
                    raise ValueError('Instructor setup needed: no reviewed effect.')
                request = {'preset': options['vfx'][0]['value'], 'scale': float(data['scale'])}
            else:
                raise ValueError('Unknown workflow.')
            result = json.loads(native_bridge.dispatch_workflow(identity,action,kind,json.dumps(request)))
            if result['ok']:
                warnings=result['plan'].get('warnings',[])
                result['message']=('Review needed: '+' '.join(warnings)) if warnings else 'Review the changes, then Apply.'
            return json.dumps(result)
        return native_bridge.dispatch_workflow(identity,action,warnings_reviewed=data.get('ack') is True)
    except Exception as error:
        session = native_bridge._workflow_sessions.get(identity)
        if session:
            session.clear()
        return json.dumps({'can_apply': False, 'ok': False, 'message': str(error)})
