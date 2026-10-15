"""Student-facing PySide tools: choose, preview, apply, check."""
from pathlib import Path
from PySide6 import QtCore, QtWidgets
from week07_tooling.workflows import WorkflowSession
from week07_tooling.workflow_presentation import describe_plan
from week07_tooling.ui.assistant_views import STAGES, make_review
from week07_tooling.ui.window import STYLE
from week07_tooling.ui.assistant_style import ASSISTANT_STYLE


class AssistantWindow(QtWidgets.QWidget):
    closed = QtCore.Signal()
    stage = 'workflows'

    def __init__(self, backend, ui_stage=3):
        if ui_stage not in STAGES:
            raise ValueError('UI stage must be 1, 2, or 3.')
        super().__init__()
        self.ui_stage = ui_stage
        self.session = WorkflowSession(backend)
        self.setWindowTitle(f'Week 7 · Material & VFX Tools · {STAGES[ui_stage]}')
        self.resize(1120, 900)
        self.setMinimumSize(800, 700)
        icons = (Path(__file__).resolve().parent / 'icons').as_posix()
        self.setStyleSheet(STYLE + ASSISTANT_STYLE + '''
            QComboBox, QSpinBox, QDoubleSpinBox { background: #202c3c; padding: 7px;
                border: 1px solid #61748e; border-radius: 4px; min-height: 20px; }
            QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus { border: 2px solid #9ccaff; }
            QLabel#steps { color: #bcd3f5; font-weight: 600; }
            QCheckBox::indicator { width: 18px; height: 18px; background: #202c3c; border: 1px solid #9bb4d2; border-radius: 3px; }
            QCheckBox::indicator:checked { background: #a9cfff; image: url("ICON_ROOT/check.svg"); }
            QCheckBox::indicator:focus { border: 2px solid #ffffff; }
            QSpinBox::up-arrow, QDoubleSpinBox::up-arrow { image: url("ICON_ROOT/up.svg"); width: 10px; height: 6px; }
            QSpinBox::down-arrow, QDoubleSpinBox::down-arrow, QComboBox::down-arrow { image: url("ICON_ROOT/down.svg"); width: 10px; height: 6px; }
        '''.replace('ICON_ROOT', icons))
        # Earlier stages retain legibility, keyboard focus and all safety feedback.
        # Stage 3 adds emphasis; color is never the sole signal.
        if ui_stage < 3:
            self.setStyleSheet(self.styleSheet() + 'QPushButton#apply { background: #303e53; color: #eef2f8; font-weight: 400; }')
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)
        title = QtWidgets.QLabel('Material & VFX Tools')
        title.setObjectName('title')
        layout.addWidget(title)
        self.mode = QtWidgets.QLabel('UNREAL EDITOR · uses your current selection' if backend.is_live
            else 'PRACTICE MODE · sample data')
        self.mode.setObjectName('mode')
        self.mode.setWordWrap(True)
        self.mode.setText(self.mode.text() + f' · Stage {ui_stage}: {STAGES[ui_stage]}')
        layout.addWidget(self.mode)
        self.steps = QtWidgets.QLabel('Choose inputs    →    Preview    →    Apply    →    Check')
        self.steps.setObjectName('steps')
        self.steps.setWordWrap(True)
        self.steps.setVisible(ui_stage == 3)
        layout.addWidget(self.steps)
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setAccessibleName('Choose Material Setup or VFX Placement')
        self.master = QtWidgets.QComboBox()
        self.preset = QtWidgets.QComboBox()
        self.setup_error = ''
        self.load_options()
        self.name = QtWidgets.QLineEdit('MI_Crate_Demo')
        self.name.setClearButtonEnabled(True)
        self.slot = QtWidgets.QSpinBox()
        self.slot.setRange(0, 31)
        self.scale = QtWidgets.QDoubleSpinBox()
        self.scale.setRange(0.25, 1.0)
        self.scale.setSingleStep(0.1)
        self.scale.setValue(1.0)
        self.scale.setSuffix(' ×')
        material = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout(material)
        form.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.field(form, 'Parent material', self.master, 'A prepared material supplied by your instructor.')
        self.field(form, 'New instance name', self.name, 'Start with MI_. Use letters, digits and underscores.')
        self.field(form, 'Material slot', self.slot, 'Slot numbers start at 0. Only the chosen component slot changes.')
        text = ('Practice selection: 3 textures and 1 mesh Actor are already supplied.' if not backend.is_live else
                'Select 3 textures in the Content Browser and mesh Actors in the viewport or Outliner.')
        self.material_help = self.label(text)
        self.material_help.setToolTip('Texture suffixes: _BaseColor, _Normal, _ORM. ORM = occlusion, roughness, metallic.')
        self.material_help.setVisible(ui_stage >= 2)
        form.addRow(self.material_help)
        self.tabs.addTab(material, '&Material Setup')
        effects = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout(effects)
        self.field(form, 'Effect preset', self.preset, 'Only instructor-reviewed presets appear. Each has its own placement limit.')
        self.field(form, 'Effect scale', self.scale, 'Uniform size multiplier, limited to 0.25–1.0. This does not set particle count.')
        text = ('Practice selection: 3 placement markers are already supplied.' if not backend.is_live else
                'Select placement markers in the Outliner. Your instructor tags them W07_VFXAnchor.')
        self.vfx_help = self.label(text)
        self.vfx_help.setToolTip('One effect per marker, using its position and rotation.')
        self.vfx_help.setVisible(ui_stage >= 2)
        form.addRow(self.vfx_help)
        self.tabs.addTab(effects, '&VFX Placement')
        layout.addWidget(self.tabs)
        self.status = self.label('')
        self.status.setObjectName('status')
        self.status.setAccessibleName('Tool status and next step')
        layout.addWidget(self.status)
        self.summary = self.label('')
        self.summary.setAccessibleName('Number and scope of proposed changes')
        self.summary.setVisible(ui_stage >= 2)
        layout.addWidget(self.summary)
        self.review_view = make_review(ui_stage)
        self.review = self.review_view.widget
        self.review.setMinimumHeight(145)
        layout.addWidget(self.review, 1)
        self.ack = QtWidgets.QCheckBox('I reviewed the density warning')
        self.ack.setAccessibleName('Acknowledge the effect density warning')
        self.ack.hide()
        self.ack.toggled.connect(self.update_apply)
        layout.addWidget(self.ack)
        buttons = QtWidgets.QHBoxLayout()
        self.reset_button = QtWidgets.QPushButton('Reset &practice data')
        self.reset_button.setToolTip('Reset both sample workflows. This button never changes an Unreal scene.')
        self.reset_button.setVisible(not backend.is_live)
        self.reset_button.clicked.connect(self.reset_practice)
        buttons.addWidget(self.reset_button)
        buttons.addStretch()
        self.preview_button = QtWidgets.QPushButton('&Preview')
        self.preview_button.setObjectName('preview')
        self.apply_button = QtWidgets.QPushButton('&Apply')
        self.apply_button.setObjectName('apply')
        for button in (self.preview_button, self.apply_button, self.reset_button):
            button.setAutoDefault(False)
        self.preview_button.clicked.connect(self.preview)
        self.apply_button.clicked.connect(self.apply)
        buttons.addWidget(self.preview_button)
        buttons.addWidget(self.apply_button)
        layout.addLayout(buttons)
        self.note = self.label('')
        layout.addWidget(self.note)
        # The review remains read-only, but stays in the keyboard route for inspection.
        focus_order = [self.tabs, self.master, self.name, self.slot, self.preset,
                       self.scale, self.review, self.ack, self.preview_button,
                       self.apply_button, self.reset_button]
        for current, following in zip(focus_order, focus_order[1:]):
            QtWidgets.QWidget.setTabOrder(current, following)
        for combo in (self.master, self.preset):
            combo.currentIndexChanged.connect(self.invalidate)
        self.name.textChanged.connect(self.invalidate)
        for spin in (self.slot, self.scale):
            spin.valueChanged.connect(self.invalidate)
        self.tabs.currentChanged.connect(self.invalidate)
        self.invalidate()

    @staticmethod
    def label(text):
        label = QtWidgets.QLabel(text)
        label.setWordWrap(True)
        label.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        return label

    @staticmethod
    def field(form, title, widget, help_text):
        widget.setAccessibleName(title)
        widget.setToolTip(help_text)
        form.addRow(title, widget)

    def load_options(self):
        try:
            options = self.session.backend.options()
        except Exception as error:
            options = {}
            self.setup_error = f'Instructor setup needed: could not read the preset catalogue. {error}'
        for combo, key in ((self.master, 'materials'), (self.preset, 'vfx')):
            for option in options.get(key, []):
                combo.addItem(option['label'], option['value'])
            if combo.count() == 0:
                combo.addItem('Not configured: ask your instructor', None)

    def invalidate(self, *_):
        self.result_present = False
        self.session.clear()
        self.ack.setChecked(False)
        self.ack.hide()
        self.review_view.clear()
        material = self.tabs.currentIndex() == 0
        available = bool((self.master if material else self.preset).currentData())
        self.preview_button.setEnabled(available)
        self.summary.setText('Input editing does not undo applied changes.')
        self.steps.setText('CHOOSE INPUTS    →    Preview    →    Apply    →    Check')
        self.note.setText('Sample data only. No Unreal changes.' if not self.session.backend.is_live else 'Selected components only. Save changes yourself.' if material else
                          'Placement limits are not a performance test.')
        self.message('Choose inputs, then Preview.' if available else
                     self.setup_error or 'No preset available. Ask your instructor.',
                     tone='info' if available else 'warning')
        self.update_apply()

    def message(self, text, tone='info'):
        self.status.setText(text)
        self.status.setToolTip(text)
        self.status.setProperty('tone', tone)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def preview(self):
        self.result_present = False
        self.ack.setChecked(False)
        self.ack.hide()
        self.review_view.clear()
        try:
            if self.tabs.currentIndex() == 0:
                plan = self.session.preview('material', {'master': self.master.currentData(),
                    'name': self.name.text().strip(), 'slot': self.slot.value()})
            else:
                plan = self.session.preview('vfx', {'preset': self.preset.currentData(), 'scale': self.scale.value()})
            presentation = describe_plan(plan)
            self.review_view.render(presentation)
            self.summary.setText(presentation['summary'])
            warnings = plan.get('warnings', [])
            self.ack.setVisible(bool(warnings))
            self.steps.setText('Choose inputs    →    REVIEW PREVIEW    →    Apply    →    Check')
            self.message(('Review needed: ' + ' '.join(warnings)) if warnings else
                         'Review the changes, then Apply.', 'warning' if warnings else 'info')
        except Exception as error:
            self.session.clear()
            self.review_view.clear()
            self.steps.setText('CHECK INPUTS    →    Preview    →    Apply    →    Check')
            self.summary.setText('No changes made. Fix the input, then Preview.')
            self.message(f'Needs attention: {error}', 'error')
        self.update_apply()

    def update_apply(self, *_):
        pending = self.session.pending
        ready = bool(pending) and (not pending[3].get('warnings') or self.ack.isChecked())
        self.apply_button.setEnabled(ready)
        action = (describe_plan(pending[3])['action'] if pending and self.ui_stage == 3
                  else 'Apply')
        self.apply_button.setText('&' + action)
        self.apply_button.setAccessibleName(action.replace('&&', 'and'))
        if ready:
            apply_help = 'Applies this preview after rechecking the current selection and tool limits.'
        elif self.result_present:
            apply_help = 'This preview was already applied. Inspect the result before starting another operation.'
        elif pending:
            apply_help = 'Review and acknowledge the visible warning before applying this preview.'
        else:
            apply_help = 'Create a valid preview before applying changes.'
        self.apply_button.setToolTip(apply_help)
        # Emphasis follows the available next action. A warning keeps attention on
        # review rather than encouraging another Preview or an unavailable Apply.
        primary = (self.apply_button if ready else self.preview_button
                   if not pending and not self.result_present and self.preview_button.isEnabled() else None)
        for button in (self.preview_button, self.apply_button):
            button.setProperty('emphasis', 'primary' if self.ui_stage == 3 and button is primary else 'secondary')
            button.style().unpolish(button)
            button.style().polish(button)

    def apply(self):
        self.apply_button.setEnabled(False)
        try:
            result = self.session.apply(warnings_reviewed=self.ack.isChecked())
            self.result_present = True
            self.review_view.complete()
            self.steps.setText('Choose inputs    →    Preview    →    Applied    →    CHECK RESULT')
            self.message('Completed. Check the result in Unreal.' if self.session.backend.is_live else 'Completed in sample data.', 'success')
            self.status.setToolTip(result)
            self.summary.setText(('Undo restores the assignment; the new asset remains.'
                                  if self.tabs.currentIndex() == 0 else
                                  'Undo removes this batch. Save changes yourself.')
                                 if self.session.backend.is_live else
                                 'Preview again to test duplicates, or reset sample data.')
        except Exception as error:
            self.result_present = False
            self.review_view.clear()
            self.steps.setText('Choose inputs    →    Preview    →    APPLY STOPPED    →    Check')
            self.message(f'Apply stopped: {error}', 'error')
            self.summary.setText('Resolve the issue, then create a new preview.')
        self.ack.hide()
        self.update_apply()

    def reset_practice(self):
        if self.session.backend.is_live:
            return
        self.session.clear()
        self.session.backend.reset_practice()
        self.invalidate()
        self.message('Sample data reset. Choose either task.')

    def closeEvent(self, event):
        self.session.clear()
        self.closed.emit()
        super().closeEvent(event)

