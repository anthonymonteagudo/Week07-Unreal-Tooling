"""Live adapters for prepared assets; only invoked explicitly inside Unreal.

No asset saves, graph edits, simulation-rate overrides or automatic scene clearing.
Rehearsed on the prepared UE 5.7.4 classroom fixture; other assets require their own checks.
"""
import json
from pathlib import Path
import unreal
from week07_tooling.editor import demo
from week07_tooling.workflows import OUTPUT, require

WORKFLOW_MAP = '/Game/Week07/Maps/W07_MaterialVFXLab'

def guard():
    if demo.world().get_path_name().split('.')[0] not in (demo.DEMO_MAP, WORKFLOW_MAP):
        raise RuntimeError('Open W07_MaterialVFXLab before using Material & VFX Tools.')
    if unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).is_in_play_in_editor():
        raise RuntimeError('Stop Play in Editor first.')


class EditorWorkflowBackend:
    is_live = True

    def options(self):
        catalogue = json.loads((Path(unreal.Paths.project_dir()) / 'Config/Week07ToolPresets.json').read_text(encoding='utf-8'))
        return {
            'materials': [{'label': p.get('label', key), 'value': p['parent']}
                          for key, p in catalogue.get('materials', {}).items() if p.get('parent')],
            'vfx': [{'label': p.get('label', key), 'value': key}
                    for key, p in catalogue.get('vfx', {}).items()
                    if p.get('system') and p.get('reviewed_for_demo') is True and p.get('review_note')],
        }

    def snapshot(self, kind, request):
        guard()
        selected = sorted(demo.actors().get_selected_level_actors(), key=lambda a: a.get_path_name())
        base = {'world': demo.world().get_path_name(), 'mixed_selection': False}
        if kind == 'material':
            require(type(request['slot']) is int and request['slot'] >= 0, 'Material slot must be a nonnegative integer.')
            master = unreal.load_asset(request['master'])
            valid = isinstance(master, unreal.MaterialInterface)
            base.update(master_valid=valid,
                        parameters=sorted(str(p) for p in unreal.MaterialEditingLibrary.get_texture_parameter_names(master)) if valid else [],
                        target_exists=unreal.EditorAssetLibrary.does_asset_exist(f"{OUTPUT}/{request['name']}"),
                        textures=[], targets=[])
            for asset in sorted(unreal.EditorUtilityLibrary.get_selected_assets(), key=lambda a: a.get_path_name()):
                texture = isinstance(asset, unreal.Texture2D)
                base['textures'].append({'path': asset.get_path_name(), 'name': asset.get_name(),
                    'is_texture': texture, 'srgb': bool(asset.get_editor_property('srgb')) if texture else False,
                    'normal_compression': texture and asset.get_editor_property('compression_settings') == unreal.TextureCompressionSettings.TC_NORMALMAP})
            for actor in selected:
                components = actor.get_components_by_class(unreal.StaticMeshComponent)
                if len(components) != 1 or request['slot'] >= components[0].get_num_materials():
                    base['mixed_selection'] = True
                    continue
                component = components[0]
                old = component.get_material(request['slot'])
                base['targets'].append({'path': actor.get_path_name(), 'label': actor.get_actor_label(), 'component': component.get_name(),
                                        'slot': request['slot'], 'material': old.get_path_name() if old else None})
            return base
        require(kind == 'vfx', 'Unknown workflow.')
        presets = Path(unreal.Paths.project_dir()) / 'Config/Week07ToolPresets.json'
        catalogue = json.loads(presets.read_text(encoding='utf-8'))
        profile = catalogue['vfx'].get(request['preset'])
        system = unreal.load_asset(profile['system']) if profile and profile['system'] else None
        valid = isinstance(system, unreal.NiagaraSystem)
        base.update(profile=profile, system_valid=valid,
                    has_effect_type=bool(system.get_editor_property('effect_type')) if valid else False,
                    anchors=[], existing=[])
        for actor in selected:
            if 'W07_VFXAnchor' not in [str(tag) for tag in actor.tags]:
                base['mixed_selection'] = True
                continue
            p, r = actor.get_actor_location(), actor.get_actor_rotation()
            base['anchors'].append({'path': actor.get_path_name(), 'label': actor.get_actor_label(), 'location': [p.x, p.y, p.z],
                                    'rotation': [r.pitch, r.yaw, r.roll]})
        for actor in sorted(demo.actors().get_all_level_actors(), key=lambda a: a.get_path_name()):
            source = next((str(t).removeprefix('W07_Source=') for t in actor.tags if str(t).startswith('W07_Source=')), '')
            for component in sorted(actor.get_components_by_class(unreal.NiagaraComponent), key=lambda c: c.get_name()):
                p = component.get_world_location()
                asset = component.get_editor_property('asset')
                base['existing'].append({'path': component.get_path_name(), 'source': source,
                                         'system': asset.get_path_name().split('.')[0] if asset else '',
                                         'location': [p.x, p.y, p.z]})
        return base

    def execute(self, kind, plan):
        guard()
        if kind == 'material':
            return self._material(plan)
        return self._vfx(plan)

    def _material(self, plan):
        require(not unreal.EditorAssetLibrary.does_asset_exist(plan['output']), 'Destination exists; overwrite refused.')
        actors = {a.get_path_name(): a for a in demo.actors().get_selected_level_actors()}
        targets = []
        for target in plan['targets']:
            component = next(c for c in actors[target['path']].get_components_by_class(unreal.StaticMeshComponent)
                             if c.get_name() == target['component'])
            targets.append((component, target['slot'], component.get_material(target['slot'])))
        instance = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            plan['output'].rsplit('/', 1)[1], OUTPUT, unreal.MaterialInstanceConstant,
            unreal.MaterialInstanceConstantFactoryNew())
        require(instance is not None, 'Could not create the material instance.')
        try:
            unreal.MaterialEditingLibrary.set_material_instance_parent(instance, unreal.load_asset(plan['parent']))
            for parameter, path in plan['mapping'].items():
                texture = unreal.load_asset(path)
                # UE 5.7 returns false even after setting this value. Verify the actual state.
                unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(instance, parameter, texture)
                require(unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(
                    instance, parameter) == texture, f'Could not verify parameter {parameter}.')
            unreal.MaterialEditingLibrary.update_material_instance(instance)
            with unreal.ScopedEditorTransaction('Week 7: assign prepared material instance'):
                for component, slot, old in targets:
                    component.modify()
                    component.set_material(slot, instance)
                    require(component.get_material(slot) == instance, 'Material assignment verification failed.')
        except Exception as error:
            for component, slot, old in targets:
                component.set_material(slot, old)
            raise RuntimeError(f'Assignments restored after failure. Inspect the new draft asset {plan["output"]}; '
                               f'it was not automatically deleted or saved. Details: {error}') from error
        return (f'Created {plan["output"]}; assigned {len(targets)} component overrides. '
                'Nothing automatically saved. Undo reverts assignments; new asset cleanup is separate.')

    def _vfx(self, plan):
        system = unreal.load_asset(plan['system'])
        created = []
        try:
            with unreal.ScopedEditorTransaction('Week 7: place reviewed VFX'):
                for anchor in plan['anchors']:
                    actor = demo.actors().spawn_actor_from_class(unreal.NiagaraActor,
                        unreal.Vector(*anchor['location']), unreal.Rotator(*anchor['rotation']))
                    require(actor is not None, 'Could not create the Niagara Actor.')
                    created.append(actor)
                    actor.modify()
                    component = actor.get_component_by_class(unreal.NiagaraComponent)
                    require(component is not None, 'Spawned Actor has no Niagara Component.')
                    component.modify()
                    component.set_asset(system)
                    require(component.get_editor_property('asset') == system, 'Effect assignment verification failed.')
                    actor.set_actor_scale3d(unreal.Vector(plan['scale'], plan['scale'], plan['scale']))
                    actor.set_actor_label('W07_FX_' + anchor['path'].rsplit('.', 1)[-1])
                    actor.set_folder_path('Week07/VFXPlacements')
                    actor.set_editor_property('tags', [unreal.Name('W07_PlacedVFX'),
                        unreal.Name('W07_Source=' + anchor['path'])])
        except Exception as error:
            remaining = [a.get_path_name() for a in created if not demo.actors().destroy_actor(a)]
            raise RuntimeError(f'Placement failed; cleanup attempted only for this batch. '
                               f'Actors requiring inspection: {remaining}. Details: {error}') from error
        return (f'Placed {len(created)} effects. Undo removes this batch; map not saved. '
                'Placement limits passed, but runtime performance has not been measured.')
