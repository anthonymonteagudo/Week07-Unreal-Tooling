"""Explicit Unreal entry point. Slate pumps Qt without blocking the editor."""
_window = None
_app = None
_tick = None
_shutdown = None


def close():
    global _window, _tick, _shutdown
    import unreal
    if _tick is not None:
        unreal.unregister_slate_post_tick_callback(_tick)
        _tick = None
    if _shutdown is not None:
        unreal.unregister_python_shutdown_callback(_shutdown)
        _shutdown = None
    window, _window = _window, None
    if window is not None:
        window.close()
        window.deleteLater()


def show(stage=3):
    global _window, _app, _tick, _shutdown
    import unreal
    from week07_tooling.ui.dependencies import enable_qt
    enable_qt()
    from PySide6 import QtWidgets
    from week07_tooling.ui.window import ToolWindow
    from week07_tooling.editor.ui_backend import UnrealBackend
    if stage not in (1, 2, 3, 'workflows'):
        raise ValueError('UI stage must be 1, 2, 3, or workflows.')
    if _window is not None and _window.stage == stage:
        _window.show()
        _window.raise_()
        return _window
    close()
    _app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    _app.setQuitOnLastWindowClosed(False)
    try:
        if stage == 'workflows':
            from week07_tooling.editor.workflow_backend import EditorWorkflowBackend
            from week07_tooling.ui.assistants import AssistantWindow
            _window = AssistantWindow(EditorWorkflowBackend())
        else:
            _window = ToolWindow(UnrealBackend(), stage)
        _window.closed.connect(close)
        _window.show()
        unreal.parent_external_window_to_slate(int(_window.winId()))
        # Keep the complete teaching panel inside the current screen.
        available = _window.screen().availableGeometry()
        _window.resize(min(_window.width(), available.width() - 60),
                       min(_window.height(), available.height() - 100))
        frame = _window.frameGeometry()
        frame.moveCenter(available.center())
        _window.move(frame.topLeft())
        _tick = unreal.register_slate_post_tick_callback(lambda delta: _app.processEvents())
        _shutdown = unreal.register_python_shutdown_callback(close)
    except Exception:
        close()
        raise
    return _window
