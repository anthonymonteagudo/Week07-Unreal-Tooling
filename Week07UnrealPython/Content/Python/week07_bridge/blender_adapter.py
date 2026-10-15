"""Only Blender-specific scene access and export. No transport or JSON policy."""
from pathlib import Path


class BlenderAdapter:
    def environment(self):
        import bpy
        return {'name': 'Blender', 'version': bpy.app.version_string}

    def _source(self):
        import bpy
        if bpy.context.mode != 'OBJECT':
            raise ValueError('Switch to Object Mode, then select one mesh.')
        selected = bpy.context.selected_objects
        if len(selected) != 1 or selected[0].type != 'MESH':
            raise ValueError('Select exactly one polygon mesh in Object Mode.')
        obj = selected[0]
        if obj.find_armature() or obj.data.shape_keys:
            raise ValueError('This static-mesh lesson excludes armatures and shape keys.')
        if obj.matrix_world.determinant() <= 0:
            raise ValueError('Resolve mirrored/zero scale before publishing this teaching asset.')
        return obj

    def inspect_selection(self):
        import bpy
        obj = self._source()
        evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
        mesh = evaluated.to_mesh()
        try:
            unit_cm = bpy.context.scene.unit_settings.scale_length * 100
            points = [evaluated.matrix_world.to_3x3() @ v.co for v in mesh.vertices]
            dims = [(max(p[i] for p in points) - min(p[i] for p in points)) * unit_cm
                    for i in range(3)] if points else [0, 0, 0]
            return dict(host='blender', source_file=bpy.data.filepath, object_name=obj.name,
                        mesh_count=1, face_count=len(mesh.polygons), dimensions_cm=dims)
        finally:
            evaluated.to_mesh_clear()

    def export_fbx(self, path):
        import bpy
        from mathutils import Matrix
        source = self._source()
        scene = bpy.context.scene
        selection = list(bpy.context.selected_objects)
        active = bpy.context.view_layer.objects.active
        unit_system, unit_scale = scene.unit_settings.system, scene.unit_settings.scale_length
        temporary = mesh = None
        try:
            # Evaluate modifiers on a disposable copy. The source mesh is never applied/frozen.
            graph = bpy.context.evaluated_depsgraph_get()
            evaluated = source.evaluated_get(graph)
            mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=graph)
            # Bake rotation/scale and metres-to-centimetres into geometry, keeping the origin.
            transform = Matrix.Scale(unit_scale * 100, 4) @ source.matrix_world.to_3x3().to_4x4()
            mesh.transform(transform)
            temporary = bpy.data.objects.new('__BridgeExport', mesh)
            scene.collection.objects.link(temporary)
            for obj in selection:
                obj.select_set(False)
            temporary.select_set(True)
            bpy.context.view_layer.objects.active = temporary
            scene.unit_settings.system = 'METRIC'
            scene.unit_settings.scale_length = 0.01
            result = bpy.ops.export_scene.fbx(
                filepath=str(Path(path)), check_existing=False, use_selection=True,
                object_types={'MESH'}, use_mesh_modifiers=True, bake_anim=False,
                add_leaf_bones=False, global_scale=1.0, apply_unit_scale=True,
                apply_scale_options='FBX_SCALE_UNITS', axis_forward='-Y', axis_up='Z',
                mesh_smooth_type='FACE', use_triangles=True)
            if result != {'FINISHED'}:
                raise RuntimeError('Blender FBX exporter cancelled: ' + str(result))
        finally:
            scene.unit_settings.system = unit_system
            scene.unit_settings.scale_length = unit_scale
            if temporary is not None:
                bpy.data.objects.remove(temporary, do_unlink=True)
            if mesh is not None:
                bpy.data.meshes.remove(mesh)
            for obj in selection:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = active
