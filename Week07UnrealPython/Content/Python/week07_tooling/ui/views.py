"""Three teaching checkpoints: readable output → structured review → focused review.

These are the actual presentation implementations, not screenshot mockups.
All stages share the controller so usability changes cannot bypass its safeguards.
"""
import json
from PySide6 import QtCore, QtWidgets

ISSUE_TEXT = {'LABEL': 'Label does not match the naming rule.',
              'PLACEMENT': 'Position does not match the layout.',
              'MISSING_MESH': 'Missing mesh reference. Assign a mesh manually.'}


class FunctionalView(QtWidgets.QPlainTextEdit):
    """Gate 1: read-only results, visible scope and working actions."""
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setAccessibleName('Preview and validation results')

    def render(self, controller):
        self.setPlainText(json.dumps({'preview_selected_actors': controller.plan,
                                     'validation_entire_fixture': controller.report}, indent=2))


def table(headers):
    widget = QtWidgets.QTableWidget(0, len(headers))
    widget.setHorizontalHeaderLabels(headers)
    widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
    widget.setAlternatingRowColors(True)
    widget.setWordWrap(True)
    widget.verticalHeader().hide()
    widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
    return widget


def fill(widget, rows):
    widget.setRowCount(len(rows))
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            item = QtWidgets.QTableWidgetItem(str(value))
            item.setToolTip(str(value))
            widget.setItem(r, c, item)
    widget.resizeRowsToContents()


def position(values):
    return ', '.join(f'{value:g}' for value in values)


class GuidedView(QtWidgets.QWidget):
    """Gate 2: compare before/after and distinguish selected scope from fixture scope."""
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.hint = QtWidgets.QLabel('1  Select props    →    2  Preview and review    →    3  Apply and verify')
        self.hint.setWordWrap(True)
        self.layout.addWidget(self.hint)
        self.tabs = QtWidgets.QTabWidget()
        self.preview = table(['Current Actor label', 'Proposed label', 'Position in cm · before → after'])
        self.preview.setAccessibleName('Selected Actors change preview')
        self.validation = table(['Actor', 'Result', 'Issues'])
        self.validation.setAccessibleName('Entire fixture validation')
        self.tabs.addTab(self.preview, 'Change preview · selected Actors')
        self.tabs.addTab(self.validation, 'Validation · entire fixture')
        self.layout.addWidget(self.tabs)

    def render(self, controller):
        rows = []
        if controller.plan:
            for item in controller.plan['items']:
                before, after = item['before'], item['after']
                rows.append([before['label'], after['label'],
                             f"{position(before['location'])} → {position(after['location'])}"])
        fill(self.preview, rows)
        fill(self.validation, [[r['actor'], r['status'], ' '.join(ISSUE_TEXT.get(i, i) for i in r['issues']) or 'No issues']
                               for r in controller.report])
        if controller.report:
            self.tabs.setCurrentIndex(1)
        elif controller.plan:
            self.tabs.setCurrentIndex(0)
        self.hint.setText('Validation checks the entire fixture. Label and position fixes do not repair mesh references.'
                          if controller.report else
                          'Review the proposed labels and positions below. Units: centimeters.' if rows else
                          'Select demo props, then Preview changes. Validation checks all six props.')


class RefinedView(GuidedView):
    """Gate 3: help users focus on findings and carry results into a bug/report."""
    def __init__(self):
        super().__init__()
        self.filter = QtWidgets.QLineEdit()
        self.filter.setPlaceholderText('Filter displayed rows by Actor, result, or issue…')
        self.filter.setAccessibleName('Filter displayed results')
        self.filter.setClearButtonEnabled(True)
        self.filter.setToolTip('Display filter only. Does not change selection or the Apply scope.')
        self.layout.insertWidget(1, self.filter)
        self.counts = QtWidgets.QLabel()
        self.counts.setWordWrap(True)
        self.layout.addWidget(self.counts)
        self.filter.textChanged.connect(self.filter_rows)
        self.tabs.currentChanged.connect(self.filter_rows)

    def render(self, controller):
        super().render(controller)
        self.filter_rows()

    def filter_rows(self, *_):
        query = self.filter.text().casefold()
        for widget in (self.preview, self.validation):
            for row in range(widget.rowCount()):
                text = ' '.join(widget.item(row, col).text() for col in range(widget.columnCount()))
                widget.setRowHidden(row, query not in text.casefold())
        current = self.tabs.currentWidget()
        visible = sum(not current.isRowHidden(row) for row in range(current.rowCount()))
        self.counts.setText(f'{visible} of {current.rowCount()} rows shown. Filtering does not change what Apply affects.')
