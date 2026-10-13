"""UI state and workflow, independent of both Qt and Unreal.

The backend supplies snapshot/select_demo/preview/apply/check/reset_demo.
A snapshot contains world, selected paths, and fixture records (including has_mesh).
"""
from copy import deepcopy


class ToolController:
    def __init__(self, backend):
        self.backend = backend
        self.snapshot = None
        self.plan = None
        self.report = []
        self.message = 'Select demo props, then preview their changes.'
        self.tone = 'info'

    @property
    def change_count(self):
        if not self.plan:
            return 0
        return sum(any(item['before'][key] != item['after'][key]
                       for key in ('label', 'location')) for item in self.plan['items'])

    @property
    def can_apply(self):
        return self.change_count > 0

    def invalidate(self, message, tone='warning'):
        self.plan = None
        self.report = []
        self.message, self.tone = message, tone

    def refresh(self):
        try:
            current = self.backend.snapshot()
        except Exception:
            self.snapshot = None
            self.invalidate('Context unavailable. Open W07_PythonLab and stop Play in Editor.')
            raise
        changed = current != self.snapshot
        if changed:
            had_plan = self.plan is not None
            self.snapshot = deepcopy(current)
            self.invalidate('Selection or scene changed. Preview again before Apply.' if had_plan
                            else 'Ready. Select demo props and preview changes.', 'info')
        return changed

    def select_demo(self):
        self.invalidate('Selecting demo props…', 'info')
        self.backend.select_demo()
        self.refresh()

    def preview(self):
        self.invalidate('Building preview…', 'info')
        self.refresh()
        self.plan = deepcopy(self.backend.preview())
        if not self.plan:
            self.message, self.tone = 'Nothing selected. Use Select demo props, then Preview.', 'warning'
        elif not self.change_count:
            self.message, self.tone = 'No label or placement changes needed. Validate to check mesh references.', 'info'
        else:
            self.message = f'Review {self.change_count} proposed Actor changes. Nothing has been applied.'
            self.tone = 'info'

    def validate(self):
        self.refresh()
        self.report = self.backend.check()
        failures = sum(row['status'] != 'PASS' for row in self.report)
        self.message = f'Entire fixture: {len(self.report) - failures}/{len(self.report)} pass. '
        self.message += 'Review the reported issues.' if failures else 'All fixture checks pass.'
        self.tone = 'warning' if failures else 'success'

    def apply(self):
        self.refresh()  # UI state is advisory; backend also rechecks at mutation time.
        if not self.can_apply:
            raise ValueError('No fresh changes to apply. Preview and review first.')
        reviewed = deepcopy(self.plan)
        self.plan = None  # Consumed even when the backend refuses or fails.
        try:
            count = self.backend.apply(reviewed)
        except Exception:
            self.invalidate('Apply did not complete. Inspect the scene, then preview again.', 'error')
            raise
        try:
            self.refresh()
            self.report = self.backend.check()
        except Exception as error:
            self.invalidate(f'Applied {count} changes, but verification failed: {error}. Inspect before retrying.', 'error')
            return count
        failures = sum(row['status'] != 'PASS' for row in self.report)
        recovery = 'Use Edit → Undo in Unreal. Map not saved.' if self.backend.is_live else 'Offline data only; Reset restores the sample.'
        result = ('1 fixture prop still has issues.' if failures == 1 else
                  f'{failures} fixture props still have issues.' if failures else 'All fixture checks pass.')
        self.message = f'Applied {count} changes. {result} {recovery}'
        self.tone = 'warning' if failures else 'success'
        return count

    def reset(self):
        self.invalidate('Resetting fixture…', 'info')
        self.backend.reset_demo()
        self.refresh()
        self.message = 'Baseline labels and positions restored. Preview again. Mesh references were not repaired.'
        self.tone = 'info'
