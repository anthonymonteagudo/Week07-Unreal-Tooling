"""Policy tests for the two classroom tools; no Qt/Unreal or scene mutation."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Content/Python'))
from week07_tooling.workflows import WorkflowSession, material_plan, vfx_plan
from week07_tooling.workflow_sample import SampleBackend

MATERIAL = {'master': 'sample://PreparedSurface', 'name': 'MI_Test', 'slot': 0}
VFX = {'preset': 'steam_demo', 'scale': 1.0}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.backend = SampleBackend()
        self.session = WorkflowSession(self.backend)

    def test_material_preview_read_only_and_no_overwrite(self):
        before = deepcopy(self.backend.materials)
        plan = self.session.preview('material', MATERIAL)
        self.assertEqual(self.backend.materials, before)
        self.assertEqual(len(plan['mapping']), 3)
        self.session.apply()
        with self.assertRaisesRegex(ValueError, 'already exists'):
            self.session.preview('material', MATERIAL)

    def test_practice_rejects_unavailable_inputs_and_clears_previous_preview(self):
        cases = [('material', dict(MATERIAL, slot=1), 'slot 0'),
                 ('material', dict(MATERIAL, slot=-1), 'slot 0'),
                 ('material', dict(MATERIAL, slot=True), 'slot 0'),
                 ('material', dict(MATERIAL, master='sample://Unknown'), 'parent list'),
                 ('vfx', dict(VFX, preset='unknown'), 'effect list')]
        for kind, request, message in cases:
            with self.subTest(request=request):
                self.session.preview('material', MATERIAL)
                with self.assertRaisesRegex(ValueError, message):
                    self.session.preview(kind, request)
                with self.assertRaisesRegex(ValueError, 'Preview'):
                    self.session.apply()
                self.assertFalse(self.backend.created)
                self.assertFalse(self.backend.effects)

    def test_material_requires_complete_unambiguous_matching_set(self):
        for change in ('missing', 'duplicate', 'prefix'):
            data = self.backend.snapshot('material', MATERIAL)
            if change == 'missing':
                data['textures'].pop()
            elif change == 'duplicate':
                data['textures'].append(deepcopy(data['textures'][0]))
            else:
                data['textures'][0]['name'] = 'Different_BaseColor'
            with self.subTest(change=change), self.assertRaises(ValueError):
                material_plan(MATERIAL, data)

    def test_material_rejects_invalid_parent_slot_selection_and_texture_settings(self):
        mutations = [lambda d: d.update(master_valid=False), lambda d: d.update(parameters=[]),
                     lambda d: d.update(mixed_selection=True), lambda d: d.update(targets=[]),
                     lambda d: d['textures'][1].update(srgb=True),
                     lambda d: d['textures'][1].update(normal_compression=False)]
        for change in mutations:
            data = self.backend.snapshot('material', MATERIAL)
            change(data)
            with self.subTest(change=change), self.assertRaises(ValueError):
                material_plan(MATERIAL, data)

    def test_vfx_blocks_unreviewed_missing_scalability_and_mixed_selection(self):
        mutations = [lambda d: d['profile'].update(reviewed_for_demo=False),
                     lambda d: d['profile'].update(review_note=''),
                     lambda d: d.update(has_effect_type=False),
                     lambda d: d.update(system_valid=False), lambda d: d.update(mixed_selection=True)]
        for change in mutations:
            data = self.backend.snapshot('vfx', VFX)
            change(data)
            with self.subTest(change=change), self.assertRaises(ValueError):
                vfx_plan(VFX, data)

    def test_scale_rejects_nonfinite_and_out_of_range(self):
        for scale in (float('nan'), float('inf'), -1, 0, 1.1, True):
            with self.subTest(scale=scale), self.assertRaises(ValueError):
                vfx_plan(dict(VFX, scale=scale), self.backend.snapshot('vfx', VFX))

    def test_spacing_and_repeated_anchor_are_blocked(self):
        data = self.backend.snapshot('vfx', VFX)
        data['anchors'][1]['location'] = [20, 0, 0]
        with self.assertRaisesRegex(ValueError, '100 cm'):
            vfx_plan(VFX, data)
        self.session.preview('vfx', VFX)
        self.session.apply()
        with self.assertRaisesRegex(ValueError, 'already occupies'):
            self.session.preview('vfx', VFX)

    def test_count_limits_include_unowned_effects(self):
        for count, system, message in ((30, 'sample://Other', '32'), (14, 'sample://Steam', '16')):
            data = self.backend.snapshot('vfx', VFX)
            data['existing'] = [{'system': system, 'source': '', 'location': [10000 + i * 200, 0, 0]}
                                for i in range(count)]
            with self.assertRaisesRegex(ValueError, message):
                vfx_plan(VFX, data)
        data = self.backend.snapshot('vfx', VFX)
        data['profile']['max_new'] = 9
        with self.assertRaises(ValueError):
            vfx_plan(VFX, data)

    def test_preset_lower_limit_is_enforced(self):
        self.backend.vfx['profile']['max_new'] = 2
        with self.assertRaisesRegex(ValueError, 'Batch limit: 2'):
            self.session.preview('vfx', VFX)

    def test_density_warning_needs_explicit_acknowledgement(self):
        self.backend.effects.extend({'system': 'sample://Other', 'source': '', 'location': [10000 + i * 200, 0, 0]}
                                    for i in range(6))
        plan = self.session.preview('vfx', VFX)
        self.assertTrue(plan['warnings'])
        with self.assertRaisesRegex(ValueError, 'acknowledge'):
            self.session.apply()
        self.assertEqual(len(self.backend.effects), 6)
        self.session.preview('vfx', VFX)
        self.session.apply(warnings_reviewed=True)
        self.assertEqual(len(self.backend.effects), 9)

    def test_scene_preset_and_request_changes_cannot_mutate_reviewed_plan(self):
        request = deepcopy(VFX)
        public_plan = self.session.preview('vfx', request)
        public_plan['scale'] = 100
        request['scale'] = 100
        self.backend.vfx['profile']['max_new'] = 1
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.session.apply()
        self.assertEqual(self.backend.effects, [])
        with self.assertRaisesRegex(ValueError, 'Preview'):
            self.session.apply()


if __name__ == '__main__':
    unittest.main()
