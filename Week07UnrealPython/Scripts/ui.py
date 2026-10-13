"""Offline UI rehearsal or headless renders. Never imports or starts Unreal."""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', type=int, choices=(1, 2, 3), default=3)
    parser.add_argument('--render', type=Path, help='Render PNG states offscreen to this folder; no desktop window.')
    args = parser.parse_args()
    if args.render:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    sys.path.insert(0, str(ROOT / 'Content/Python'))
    from week07_tooling.ui.dependencies import enable_qt, configure_headless_fonts
    enable_qt()
    from PySide6 import QtWidgets
    from week07_tooling.ui.offline_backend import OfflineBackend
    from week07_tooling.ui.window import ToolWindow
    app = QtWidgets.QApplication([])
    configure_headless_fonts(app)
    window = ToolWindow(OfflineBackend(), args.stage)
    window.show()
    if not args.render:
        return app.exec()
    window.timer.stop()
    args.render.mkdir(parents=True, exist_ok=True)

    def capture(name):
        window.render()
        app.processEvents()
        target = args.render / f'stage_{args.stage}_{name}.png'
        if not window.grab().save(str(target)):
            raise RuntimeError(f'Could not save {target}')
        print(target.resolve())

    capture('empty')
    window.controller.select_demo()
    window.controller.preview()
    capture('preview')
    window.controller.apply()
    capture('verified')
    window.close()
    app.processEvents()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
