"""Launch offline PySide assistants, or render them offscreen without desktop UI."""
import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render', type=Path)
    parser.add_argument('--stage', type=int, choices=(1, 2, 3), default=3,
                        help='Same tools: 1 functional, 2 guided, 3 refined.')
    args = parser.parse_args()
    if args.render:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    sys.path.insert(0, str(ROOT / 'Content/Python'))
    from week07_tooling.ui.dependencies import enable_qt, configure_headless_fonts
    enable_qt()
    from PySide6 import QtWidgets
    from week07_tooling.ui.assistants import AssistantWindow
    from week07_tooling.workflow_sample import SampleBackend
    app = QtWidgets.QApplication([])
    configure_headless_fonts(app)
    window = AssistantWindow(SampleBackend(), ui_stage=args.stage)
    window.show()
    if not args.render:
        return app.exec()
    args.render.mkdir(parents=True, exist_ok=True)
    def capture(name):
        app.processEvents()
        # Keep existing stage-3 filenames compatible with student guides.
        prefix = f'assistants_stage_{args.stage}_' if args.stage != 3 else ''
        require_path = args.render / f'{prefix}{name}.png'
        if not window.grab().save(str(require_path)):
            raise RuntimeError(f'Could not save {require_path}')
        print(require_path.resolve())
    capture('material_start')
    for index, name in enumerate(('material', 'vfx')):
        window.tabs.setCurrentIndex(index)
        window.preview()
        capture(f'{name}_preview')
        window.apply()
        capture(f'{name}_complete')
        window.preview()
        capture(f'{name}_blocked')
        window.reset_practice()
    window.session.backend.effects.extend(
        {'system': 'sample://Other', 'source': '', 'location': [10000 + i * 200, 0, 0]} for i in range(6))
    window.preview()
    capture('vfx_warning')
    window.resize(800, 700)
    capture('vfx_warning_narrow')
    window.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
