"""Required automated UI gates; missing Qt is a failure here, never a skipped pass."""
import os
import argparse
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
sys.path[:0] = [str(ROOT / 'Content/Python'), str(ROOT / 'Tests')]
from week07_tooling.ui.dependencies import enable_qt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', type=int, choices=(1, 2, 3), default=3,
                        help='Run cumulative automated gates through this stage.')
    parser.add_argument('--tool', choices=('assistants', 'props'), default='assistants',
                        help='Material/VFX progression by default; props retains the earlier gates.')
    args = parser.parse_args()
    enable_qt()
    tests = ['test_ui_controller', 'test_ui_widgets.WidgetGates.test_gate_1_functional_all_stages',
             'test_ui_widgets.WidgetGates.test_close_stops_polling']
    if args.stage >= 2:
        tests += ['test_ui_widgets.WidgetGates.test_gate_2_review_tables_and_stale_recovery']
    if args.stage >= 3:
        tests += ['test_workflows', 'test_ui_widgets.WidgetGates.test_assistants_review_apply_and_input_invalidation',
                  'test_ui_widgets.WidgetGates.test_assistants_invalid_practice_slot_blocks_apply_and_recovers',
                  'test_ui_widgets.WidgetGates.test_assistants_practice_reset_and_warning_gate',
                  'test_ui_widgets.WidgetGates.test_assistants_unconfigured_choices_and_keyboard_layout',
                  'test_ui_widgets.WidgetGates.test_gate_3_filter_does_not_change_apply_scope',
                  'test_ui_widgets.WidgetGates.test_gate_3_reset_cancel_is_non_destructive',
                  'test_ui_widgets.WidgetGates.test_gate_3_keyboard_controls_and_minimum_size']
    if args.tool == 'assistants':
        tests = ['test_workflows']
        from test_assistant_stages import AssistantStageGates
        tests += [f'test_assistant_stages.AssistantStageGates.{name}'
                  for name in unittest.defaultTestLoader.getTestCaseNames(AssistantStageGates)
                  if int(name.split('_')[2]) <= args.stage]
        if args.stage == 3:
            tests += ['test_ui_widgets.WidgetGates.test_assistants_unconfigured_choices_and_keyboard_layout']
    suite = unittest.defaultTestLoader.loadTestsFromNames(tests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful() or result.skipped:
        return 1
    print(f'Automated {args.tool} UI gates through stage {args.stage} passed. Visual review and live Unreal rehearsal remain separate gates.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
