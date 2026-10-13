"""Presentation checkpoints for the SAME Material/VFX plans and session.

Functional: readable linear review. Guided: compare structured before/after rows.
Refined: retain that review and add workflow cues in AssistantWindow.
No view decides whether a request is safe or performs a mutation.
"""
from PySide6 import QtWidgets
from week07_tooling.ui.views import table, fill


class FunctionalReview:
    """A complete, read-only review without a comparison table."""
    def __init__(self):
        self.widget = QtWidgets.QPlainTextEdit()
        self.widget.setReadOnly(True)
        self.widget.setAccessibleName('Material or VFX change review')
        self.presentation = None

    def clear(self):
        self.presentation = None
        self.widget.clear()

    def render(self, presentation, applied=False):
        self.presentation = presentation
        phase = 'Applied change' if applied else 'After Apply'
        lines = [('APPLIED RESULT' if applied else 'PROPOSED CHANGES'), presentation['summary']]
        for item, before, after in presentation['rows']:
            lines.append(f'{item}\n  Before: {before}\n  {phase}: {after}')
        self.widget.setPlainText('\n\n'.join(lines))

    def complete(self):
        if self.presentation:
            self.render(self.presentation, applied=True)


class GuidedReview:
    """The same information becomes a side-by-side comparison."""
    def __init__(self):
        self.widget = table(['Item or target', 'Before', 'After Apply'])
        self.widget.setAccessibleName('Read-only before and after preview')

    def clear(self):
        fill(self.widget, [])
        self.widget.setHorizontalHeaderLabels(['Item or target', 'Before', 'After Apply'])

    def render(self, presentation):
        self.clear()
        fill(self.widget, presentation['rows'])

    def complete(self):
        self.widget.setHorizontalHeaderLabels(['Item or target', 'Before', 'Applied change'])


STAGES = {1: 'Functional', 2: 'Guided', 3: 'Refined'}


def make_review(stage):
    return FunctionalReview() if stage == 1 else GuidedReview()
