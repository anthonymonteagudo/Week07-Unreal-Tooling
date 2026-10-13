"""Shared action wiring and final styling. Launch explicitly; no import side effects."""
import json
import traceback
from PySide6 import QtCore, QtWidgets
from week07_tooling.ui.controller import ToolController
from week07_tooling.ui.views import FunctionalView, GuidedView, RefinedView

STAGES = {1: ('Functional', FunctionalView), 2: ('Guided', GuidedView), 3: ('Refined', RefinedView)}

STYLE = '''
QWidget { background: #171d27; color: #eef2f8; font-family: "Segoe UI"; font-size: 13px; }
QLabel#title { font-size: 25px; font-weight: 600; }
QLabel#mode { color: #bcd3f5; font-weight: 600; }
QLabel#status { background: #263347; padding: 12px; border-radius: 5px; }
QLabel#status[tone="warning"] { background: #493b22; color: #fff0ce; }
QLabel#status[tone="error"] { background: #502b34; color: #ffe4e8; }
QLabel#status[tone="success"] { background: #213f37; color: #d8fff0; }
QPushButton { background: #303e53; border: 1px solid #61748e; border-radius: 4px; padding: 9px 13px; }
QPushButton:hover { background: #3b5070; }
QPushButton:focus, QLineEdit:focus { border: 2px solid #9ccaff; }
QPushButton#apply { background: #a9cfff; color: #142033; font-weight: 600; }
QPushButton:disabled, QPushButton#apply:disabled { background: #252d39; color: #8793a6; border-color: #3b485c; }
QTableWidget, QPlainTextEdit { background: #1c2532; alternate-background-color: #253143; gridline-color: #3c4c63; }
QTableWidget::item { padding: 8px; }
QTableWidget::item:selected { background: #47698d; color: #ffffff; }
QHeaderView::section { background: #303e53; padding: 10px; border: none; font-weight: 600; }
QLineEdit { background: #202c3c; padding: 9px; border: 1px solid #61748e; border-radius: 4px; }
QTabWidget::pane { border: 1px solid #4c5e76; }
QTabBar::tab { background: #252f40; padding: 10px 14px; }
QTabBar::tab:selected { background: #3a4d68; border-bottom: 2px solid #a9cfff; }
'''


class ToolWindow(QtWidgets.QWidget):
    closed = QtCore.Signal()

    def __init__(self, backend, stage=3):
        super().__init__()
        if stage not in STAGES:
            raise ValueError('UI stage must be 1, 2, or 3.')
        self.stage = stage
        self.controller = ToolController(backend)
        self.setWindowTitle(f'Week 7 · Prop Inspector · {STAGES[stage][0]}')
        self.resize(1100, 860) if stage == 3 else self.resize(1050, 720)
        self.setMinimumSize(760, 570)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 22)
        layout.setSpacing(14)
        title = QtWidgets.QLabel('Prop Inspector')
        title.setObjectName('title')
        layout.addWidget(title)
        mode = QtWidgets.QLabel(('UNREAL EDITOR' if backend.is_live else 'OFFLINE REHEARSAL · fictional data')
                               + f'   /   Stage {stage}: {STAGES[stage][0]}')
        mode.setObjectName('mode')
        mode.setWordWrap(True)
        layout.addWidget(mode)
        self.scope = QtWidgets.QLabel()
        self.scope.setWordWrap(True)
        self.scope.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.scope)
        self.status = QtWidgets.QLabel()
        self.status.setObjectName('status')
        self.status.setWordWrap(True)
        self.status.setAccessibleName('Tool status and next action')
        layout.addWidget(self.status)
        actions = QtWidgets.QHBoxLayout()
        self.select_button = self.button('Select &demo props', self.controller.select_demo, actions)
        self.refresh_button = self.button('&Refresh', self.controller.refresh, actions)
        self.validate_button = self.button('&Validate fixture', self.controller.validate, actions)
        actions.addStretch()
        layout.addLayout(actions)
        self.view = STAGES[stage][1]()
        layout.addWidget(self.view, 1)
        if stage == 3:
            utilities = QtWidgets.QHBoxLayout()
            self.copy_button = self.button('Copy report', self.copy_report, utilities)
            self.reset_button = self.button('Reset fixture…', self.confirm_reset, utilities)
            utilities.addStretch()
            layout.addLayout(utilities)
        footer = QtWidgets.QHBoxLayout()
        footer.addStretch()
        self.preview_button = self.button('&Preview changes', self.controller.preview, footer)
        self.apply_button = self.button('&Apply reviewed changes', self.controller.apply, footer)
        self.apply_button.setObjectName('apply')
        layout.addLayout(footer)
        note = QtWidgets.QLabel('Apply changes Actor labels and positions only. Mesh assets are not changed. '
                                + ('One Undo step; map is not saved.' if backend.is_live
                                   else 'No connection to Unreal; resettable in-memory sample.'))
        note.setWordWrap(True)
        layout.addWidget(note)
        if stage == 3:
            self.setStyleSheet(STYLE)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(750)
        self.timer.timeout.connect(self.poll)
        self.invoke(self.controller.refresh)
        self.timer.start()

    def button(self, label, callback, layout):
        button = QtWidgets.QPushButton(label)
        button.setAutoDefault(False)
        button.clicked.connect(lambda checked=False: self.invoke(callback))
        button.setAccessibleName(label.replace('&', '').replace('…', ''))
        layout.addWidget(button)
        return button

    def invoke(self, callback):
        try:
            callback()
        except Exception as error:
            traceback.print_exc()
            self.controller.invalidate(str(error), 'error')
        self.render()

    def poll(self):
        try:
            changed = self.controller.refresh()
        except Exception as error:
            # Inline, nonmodal recovery; do not flood logs every timer tick.
            self.controller.invalidate(str(error), 'error')
            changed = True
        if changed:
            self.render()

    def render(self):
        c = self.controller
        selected = len(c.snapshot['selected']) if c.snapshot else 0
        context = c.snapshot['world'] if c.snapshot else 'Context unavailable'
        self.scope.setText(f'{selected} selected Actors  ·  validation scope: entire six-prop fixture\n{context}')
        prefix = {'info': 'Ready', 'warning': 'Attention', 'error': 'Action needed', 'success': 'Complete'}[c.tone]
        self.status.setText(f'{prefix} — {c.message}')
        self.status.setProperty('tone', c.tone)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)
        self.apply_button.setEnabled(c.can_apply)
        self.apply_button.setText(f'&Apply {c.change_count} reviewed changes' if c.can_apply else '&Apply reviewed changes')
        self.apply_button.setToolTip('Apply the displayed plan; the backend rechecks it before changing anything.'
                                    if c.can_apply else 'Preview changes first. Stale or empty plans cannot be applied.')
        self.preview_button.setEnabled(c.snapshot is not None)
        if self.stage == 3:
            self.copy_button.setEnabled(bool(c.report))
        self.view.render(c)

    def copy_report(self):
        QtWidgets.QApplication.clipboard().setText(json.dumps({
            'mode': 'unreal' if self.controller.backend.is_live else 'offline',
            'scope': 'entire fixture', 'validation': self.controller.report}, indent=2))
        self.controller.message = 'Fixture validation report copied to the clipboard.'
        self.controller.tone = 'info'

    def confirm_reset(self):
        answer = QtWidgets.QMessageBox.question(
            self, 'Reset demo fixture?',
            'Restore baseline labels and positions for all six props? Mesh references are unchanged. '
            + ('This is one Undo step and does not save the map.' if self.controller.backend.is_live
               else 'This changes only the offline sample.'),
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel,
            QtWidgets.QMessageBox.StandardButton.Cancel)
        if answer == QtWidgets.QMessageBox.StandardButton.Yes:
            self.controller.reset()

    def closeEvent(self, event):
        self.timer.stop()
        self.closed.emit()
        super().closeEvent(event)
