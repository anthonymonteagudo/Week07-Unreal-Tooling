"""Locate project-local Qt without modifying the engine's Python installation."""
from pathlib import Path
import os
import sys


def enable_qt():
    dependency_root = Path(__file__).resolve().parents[4] / '.deps' / 'ui'
    if dependency_root.is_dir() and str(dependency_root) not in sys.path:
        sys.path.insert(0, str(dependency_root))
    try:
        from PySide6 import QtCore, QtWidgets
    except ImportError as error:
        raise RuntimeError(
            'Qt is not installed for this project. In a VS Code terminal run: '
            './.venv/Scripts/python.exe -m pip install --target .deps/ui -r requirements-ui.txt'
        ) from error
    return QtCore, QtWidgets


def configure_headless_fonts(app):
    """Qt's offscreen Windows backend needs fonts explicitly registered for renders."""
    if os.environ.get('QT_QPA_PLATFORM') != 'offscreen' or sys.platform != 'win32':
        return
    from PySide6 import QtGui
    fonts = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    for filename in ('segoeui.ttf', 'segoeuib.ttf', 'seguisb.ttf'):
        path = fonts / filename
        if path.exists():
            QtGui.QFontDatabase.addApplicationFont(str(path))
    app.setFont(QtGui.QFont('Segoe UI', 10))
    if not QtGui.QFontMetrics(app.font()).inFontUcs4(ord('A')):
        raise RuntimeError('Headless render font is unavailable; do not accept blank-glyph captures.')
