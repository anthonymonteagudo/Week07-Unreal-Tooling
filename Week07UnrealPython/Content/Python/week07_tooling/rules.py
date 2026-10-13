"""Pure Python: plan data and validate it without starting Unreal."""
from copy import deepcopy
from math import dist, isfinite
from .config import KINDS


def target_for(prop_id):
    """Return the fixture rule for an Actor ID. Units are centimeters."""
    if type(prop_id) is not int or not 0 <= prop_id < len(KINDS):
        raise ValueError(f'Unknown fixture ID: {prop_id!r}')
    return {'label': f'W07_{KINDS[prop_id]}_{prop_id+1:02d}',
            'location': [0, -450 + prop_id * 180, 0]}


def _validate_location(location):
    if len(location) != 3 or not all(isinstance(v, (int, float)) and isfinite(v) for v in location):
        raise ValueError('Expected three finite position coordinates.')


def make_plan(world_path, states):
    """Copy the input snapshot so later edits cannot silently rewrite the preview."""
    if not states:
        return None
    ids, paths = set(), set()
    items = []
    for state in sorted(states, key=lambda row: row['id']):
        target = target_for(state['id'])
        _validate_location(state['location'])
        if state['id'] in ids or state['path'] in paths:
            raise ValueError('Duplicate Actor ID or path in selection.')
        ids.add(state['id'])
        paths.add(state['path'])
        items.append({'before': deepcopy(state), 'after': target})
    return {'world': world_path, 'items': items}


def issues_for(state, has_mesh):
    target = target_for(state['id'])
    _validate_location(state['location'])
    issues = []
    if state['label'] != target['label']:
        issues.append('LABEL')
    if dist(state['location'], target['location']) > 0.1:
        issues.append('PLACEMENT')
    if not has_mesh:
        issues.append('MISSING_MESH')
    return issues
