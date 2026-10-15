"""Exercise the real live adapter with an in-memory Unreal API double."""
from pathlib import Path
import importlib.util
import sys
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
from contextlib import nullcontext

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'Content/Python'))
from week07_tooling.workflows import WorkflowSession, OUTPUT
from week07_tooling.editor import native_bridge, native_panel
import week07_tooling.editor as editor

class Material:
    def __init__(self, path): self.path, self.parameters = path, {}
    def get_path_name(self): return self.path

class Texture:
    def __init__(self, role, folder='/Game/Textures', prefix='T_Crate'):
        self.name = prefix + '_' + role
        self.path = folder + '/' + self.name + '.' + self.name
        self.srgb = role == 'BaseColor'
        self.compression = 'normal' if role == 'Normal' else 'default'
    def get_name(self): return self.name
    def get_path_name(self): return self.path
    def get_editor_property(self, key):
        return {'srgb': self.srgb, 'compression_settings': self.compression}[key]

class Component:
    def __init__(self): self.material = Material('/Engine/BasicShapeMaterial')
    def get_name(self): return 'Mesh'
    def get_num_materials(self): return 1
    def get_material(self, slot): return self.material
    def modify(self): pass
    def set_material(self, slot, value): self.material = value

class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.textures = [Texture(r) for r in ('BaseColor', 'Normal', 'ORM')]
        self.assets = {t.path.split('.')[0]: t for t in self.textures}
        self.parent = Material('/Game/Parent')
        self.assets[self.parent.path] = self.parent
        self.selected = [self.textures[0]]
        self.component = Component()
        self.actor = NS(get_path_name=lambda: '/Game/Map.Cube', get_actor_label=lambda: 'Cube',
                        get_components_by_class=lambda cls: [self.component])
        world = NS(get_path_name=lambda: '/Game/Week07/Maps/W07_MaterialVFXLab.Map')
        demo = NS(world=lambda: world, DEMO_MAP='/Game/Other',
                  actors=lambda: NS(get_selected_level_actors=lambda: [self.actor]))
        def create(name, folder, cls, factory):
            instance = Material(folder + '/' + name)
            self.assets[instance.path] = instance
            return instance
        host = NS(Texture2D=Texture, MaterialInterface=Material, StaticMeshComponent=Component,
                  MaterialInstanceConstant=Material, MaterialInstanceConstantFactoryNew=lambda: None,
                  LevelEditorSubsystem=object(), get_editor_subsystem=lambda cls: NS(is_in_play_in_editor=lambda: False),
                  load_asset=lambda path: self.assets.get(path.split('.')[0]),
                  EditorUtilityLibrary=NS(get_selected_assets=lambda: list(self.selected)),
                  EditorAssetLibrary=NS(does_asset_exist=lambda path: path.split('.')[0] in self.assets),
                  TextureCompressionSettings=NS(TC_NORMALMAP='normal'),
                  AssetToolsHelpers=NS(get_asset_tools=lambda: NS(create_asset=create)),
                  ScopedEditorTransaction=lambda label: nullcontext(),
                  MaterialEditingLibrary=NS(
                      get_texture_parameter_names=lambda master: ['BaseColorTexture', 'NormalTexture', 'ORMTexture'],
                      set_material_instance_parent=lambda instance, parent: None,
                      set_material_instance_texture_parameter_value=lambda inst, key, value: inst.parameters.update({key: value}),
                      get_material_instance_texture_parameter_value=lambda inst, key: inst.parameters[key],
                      update_material_instance=lambda instance: None))
        spec = importlib.util.spec_from_file_location('workflow_adapter_under_test',
                ROOT / 'Content/Python/week07_tooling/editor/workflow_backend.py')
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'unreal': host, 'week07_tooling.editor.demo': demo}), patch.object(editor, 'demo', demo, create=True):
            spec.loader.exec_module(self.module)
        self.backend = self.module.EditorWorkflowBackend()
        self.backend.options = lambda: {'materials': [{'value': '/Game/Parent'}], 'vfx': []}
        self.request = {'master': '/Game/Parent', 'name': 'MI_Regression', 'slot': 0}
        self.session = WorkflowSession(self.backend)

    def tearDown(self): native_bridge.close_all()

    def test_one_selected_texture_previews_and_applies_all_three(self):
        import json
        identity = native_bridge.open_workflow_session(self.backend)
        def dispatch(action):
            return json.loads(native_panel.dispatch(json.dumps(dict(self.request, action=action,
                              session=identity, kind='material'))))
        result = dispatch('preview')
        self.assertTrue(result['can_apply'], result)
        self.assertEqual(len(result['plan']['mapping']), 3)
        self.assertEqual(self.component.material.path, '/Engine/BasicShapeMaterial')
        self.assertTrue(dispatch('apply')['ok'])
        self.assertEqual(self.component.material.path, OUTPUT + '/MI_Regression')
        self.assertEqual(set(self.component.material.parameters.values()), set(self.textures))
        self.assertEqual(self.selected, [self.textures[0]])

    def test_any_single_role_resolves_same_exact_set(self):
        for texture in self.textures:
            self.selected = [texture]
            self.assertEqual(len(self.session.preview('material', self.request)['mapping']), 3)

    def test_missing_sibling_blocks_with_exact_path(self):
        del self.assets['/Game/Textures/T_Crate_Normal']
        with self.assertRaisesRegex(ValueError, 'Missing Normal texture: /Game/Textures/T_Crate_Normal'):
            self.session.preview('material', self.request)
        self.assertIsNone(self.session.pending)

    def test_no_cross_folder_guessing_or_mixed_set(self):
        self.selected.append(Texture('Normal', folder='/Game/Other'))
        with self.assertRaisesRegex(ValueError, 'same folder'):
            self.session.preview('material', self.request)

    def test_auto_resolved_texture_settings_are_still_validated(self):
        self.textures[1].srgb = True
        with self.assertRaisesRegex(ValueError, 'Normal: review'):
            self.session.preview('material', self.request)

    def test_change_to_discovered_texture_after_preview_blocks_apply(self):
        self.session.preview('material', self.request)
        self.textures[1].compression = 'default'
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.session.apply()
        self.assertNotIn(OUTPUT + '/MI_Regression', self.assets)

    def test_changed_seed_selection_blocks_old_plan(self):
        self.session.preview('material', self.request)
        self.selected = [self.textures[1]]
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.session.apply()

    def test_invalid_slot_reports_zero_and_keeps_cube_visible(self):
        request = dict(self.request, slot=1)
        snapshot = self.backend.snapshot('material', request)
        self.assertEqual(snapshot['selection_rows'][0][0], 'Cube')
        with self.assertRaisesRegex(ValueError, 'Available slots: 0'):
            self.session.preview('material', request)
