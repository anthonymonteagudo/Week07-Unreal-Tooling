"""In-memory rehearsal, visibly marked OFFLINE; no Unreal imports or IPC."""
from copy import deepcopy
from week07_tooling import config, rules


class OfflineBackend:
    is_live = False

    def __init__(self):
        self.records = [
            {'path': f'sample://prop-{i}', 'id': i, 'label': f'prop_temp_{i+1}',
             'location': list(config.BASELINE[i]), 'has_mesh': i != 1}
            for i in range(6)
        ]
        self.selected = []

    def snapshot(self):
        return deepcopy({'world': 'OFFLINE / fictional six-prop fixture',
                         'selected': sorted(self.selected), 'records': self.records})

    def select_demo(self):
        self.selected = [r['path'] for r in self.records]

    def preview(self):
        known = {r['path'] for r in self.records}
        if any(path not in known for path in self.selected):
            raise ValueError('Select only tagged Week 7 props; mixed selections are rejected.')
        states = [{k: r[k] for k in ('path', 'id', 'label', 'location')}
                  for r in self.records if r['path'] in self.selected]
        return rules.make_plan(self.snapshot()['world'], states)

    def apply(self, plan):
        if not plan or plan != self.preview():
            raise ValueError('Preview is stale. Preview again before applying.')
        changed = 0
        by_path = {r['path']: r for r in self.records}
        for item in plan['items']:
            if any(item['before'][k] != item['after'][k] for k in ('label', 'location')):
                by_path[item['before']['path']].update(deepcopy(item['after']))
                changed += 1
        return changed

    def check(self):
        result = []
        for record in self.records:
            issues = rules.issues_for(record, record['has_mesh'])
            result.append({'actor': record['label'], 'id': record['id'],
                           'status': 'FAIL' if issues else 'PASS', 'issues': issues})
        return result

    def reset_demo(self):
        for record in self.records:
            i = record['id']
            record.update(label=f'prop_temp_{i+1}', location=list(config.BASELINE[i]))
