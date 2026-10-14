"""Maya PySide publisher. Uses the same actions/status as the Blender sidebar."""
from .client import Publisher
from .maya_adapter import MayaAdapter
from .core import default_exchange

_window = None


def show():
    from PySide6 import QtCore, QtWidgets
    from shiboken6 import wrapInstance
    import maya.OpenMayaUI as omui
    from .fixture import create_maya
    global _window
    if _window:
        _window.close()
    pointer = omui.MQtUtil.mainWindow()
    parent = wrapInstance(int(pointer), QtWidgets.QWidget) if pointer else None

    class Window(QtWidgets.QDialog):
        def __init__(self):
            super().__init__(parent)
            self.setWindowTitle('Week 7: Maya / Blender to Unreal')
            self.setMinimumWidth(520)
            self.publisher = Publisher(MayaAdapter())
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel('One static mesh | source pivot | centimeters'))
            self.exchange = QtWidgets.QLineEdit(str(default_exchange()))
            self.name = QtWidgets.QLineEdit('SM_Compare_Maya')
            form = QtWidgets.QFormLayout()
            form.addRow('Exchange folder', self.exchange)
            form.addRow('Unreal asset name', self.name)
            layout.addLayout(form)
            layout.addWidget(QtWidgets.QLabel('/Game/Week07/Bridge'))
            self.connection = QtWidgets.QLabel()
            layout.addWidget(self.connection)
            for label, callback in (
                ('Publish FBX + JSON', lambda: self.publish(False)),
                ('Publish & Send to Unreal', lambda: self.publish(True)),
                ('Send Published Revision', lambda: self.publisher.send()),
                ('Create Comparison Prop', lambda: create_maya(False)),
                ('Create Revised Prop (+40 cm)', lambda: create_maya(True)),
            ):
                button = QtWidgets.QPushButton(label)
                button.clicked.connect(lambda checked=False, fn=callback: self.action(fn))
                layout.addWidget(button)
            self.message = QtWidgets.QLabel(self.publisher.message)
            self.message.setWordWrap(True)
            self.message.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            layout.addWidget(self.message)
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.poll)
            self.timer.start(1000)
            self.poll()

        def action(self, callback):
            try:
                self.publisher.set_exchange(self.exchange.text())
                callback()
            except Exception as error:
                self.publisher.message = str(error)
            self.message.setText(self.publisher.message)

        def publish(self, send):
            self.publisher.set_exchange(self.exchange.text())
            self.publisher.publish(self.name.text(), send=send)

        def poll(self):
            self.publisher.set_exchange(self.exchange.text())
            self.publisher.poll()
            self.connection.setText('Unreal: ' + ('Connected' if self.publisher.connected else 'Offline'))
            self.message.setText(self.publisher.message)

        def closeEvent(self, event):
            self.timer.stop()
            super().closeEvent(event)

    _window = Window()
    _window.show()
    return _window
