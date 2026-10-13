"""Disposable offline rehearsal of the two selected tools, not editor simulation."""
from copy import deepcopy
from week07_tooling.workflows import TEXTURES, require


class SampleBackend:
    is_live = False

    def options(self):
        return {'materials': [{'label': 'Prepared surface · practice', 'value': 'sample://PreparedSurface'}],
                'vfx': [{'label': 'Steam · practice', 'value': 'steam_demo'}]}

    def reset_practice(self):
        self.__init__()

    def __init__(self):
        self.created = set()
        self.effects = []
        self.materials = {
            'world': 'sample://world', 'master_valid': True, 'target_exists': False,
            'mixed_selection': False, 'parameters': list(TEXTURES.values()),
            'textures': [{'path': f'sample://T_Crate_{role}', 'name': f'T_Crate_{role}',
                          'is_texture': True, 'srgb': role == 'BaseColor', 'normal_compression': role == 'Normal'}
                         for role in TEXTURES],
            'targets': [{'path': 'sample://crate', 'component': 'Mesh', 'slot': 0, 'material': 'sample://old'}]}
        self.vfx = {'world': 'sample://world', 'system_valid': True, 'has_effect_type': True,
                    'mixed_selection': False,
                    'profile': {'system': 'sample://Steam', 'reviewed_for_demo': True,
                                'review_note': 'Fictional offline preset only.', 'max_new': 4},
                    'anchors': [{'path': f'sample://vent-{i}', 'location': [i * 300, 0, 0],
                                 'rotation': [0, 0, 0]} for i in range(3)], 'existing': self.effects}

    def snapshot(self, kind, request):
        require(kind in ('material', 'vfx'), 'Unknown workflow.')
        snapshot = deepcopy(self.materials if kind == 'material' else self.vfx)
        if kind == 'material':
            require(request.get('master') == self.options()['materials'][0]['value'],
                    'Choose Prepared surface from the practice parent list.')
            require(type(request.get('slot')) is int and request['slot'] == 0,
                    'The practice crate has only material slot 0. Choose slot 0 and preview again.')
            snapshot['target_exists'] = request['name'] in self.created
        else:
            require(request.get('preset') == self.options()['vfx'][0]['value'],
                    'Choose Steam from the practice effect list.')
        return snapshot

    def execute(self, kind, plan):
        if kind == 'material':
            self.created.add(plan['output'].rsplit('/', 1)[1])
            self.materials['targets'][0]['material'] = plan['output']
            return 'Offline: created one instance and assigned the sample component. No Unreal connection.'
        for anchor in plan['anchors']:
            self.effects.append({'system': plan['system'], 'source': anchor['path'], 'location': anchor['location']})
        return f"Offline: placed {len(plan['anchors'])} effects. Repeating the same anchors is blocked."
