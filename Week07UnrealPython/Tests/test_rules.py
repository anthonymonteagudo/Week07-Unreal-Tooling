"""Run in ordinary Python: python -m unittest discover -s Tests -v."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Content/Python'))
from week07_tooling import rules


def state(i=0):
    return {'path': f'/Demo.Actor{i}', 'id': i, 'label': 'temporary', 'location': [10, 20, 30]}


class RuleTests(unittest.TestCase):
    def test_empty_selection_has_no_plan(self):
        self.assertIsNone(rules.make_plan('/Demo', []))

    def test_selection_order_does_not_change_plan(self):
        self.assertEqual(rules.make_plan('/Demo', [state(2), state(0)]),
                         rules.make_plan('/Demo', [state(0), state(2)]))

    def test_preview_is_independent_of_later_input_mutation(self):
        row = state()
        plan = rules.make_plan('/Demo', [row])
        row['location'][0] = 999
        self.assertEqual(plan['items'][0]['before']['location'], [10, 20, 30])

    def test_duplicate_actor_is_rejected(self):
        with self.assertRaises(ValueError):
            rules.make_plan('/Demo', [state(), state()])

    def test_unknown_id_is_rejected(self):
        for bad in (-1, 6, True, '0'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                rules.target_for(bad)

    def test_missing_mesh_is_distinct_from_placement(self):
        row = state()
        row.update(rules.target_for(0))
        self.assertEqual(rules.issues_for(row, False), ['MISSING_MESH'])

    def test_tolerance_avoids_float_noise(self):
        row = state()
        row.update(rules.target_for(0))
        row['location'][0] += 0.05
        self.assertEqual(rules.issues_for(row, True), [])
        row['location'][0] += 0.2
        self.assertEqual(rules.issues_for(row, True), ['PLACEMENT'])

    def test_nonfinite_position_rejected(self):
        for bad in (float('nan'), float('inf')):
            row = state()
            row['location'][0] = bad
            with self.assertRaises(ValueError):
                rules.make_plan('/Demo', [row])


if __name__ == '__main__':
    unittest.main()
