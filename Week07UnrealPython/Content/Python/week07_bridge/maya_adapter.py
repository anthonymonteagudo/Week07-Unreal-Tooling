"""Maya selection and FBX export for the shared Publisher."""


class MayaAdapter:
    def environment(self):
        import maya.cmds as cmds
        return {'name': 'Maya', 'version': cmds.about(version=True)}

    def _source(self):
        import maya.cmds as cmds
        selected = cmds.ls(selection=True, long=True) or []
        if len(selected) != 1 or cmds.nodeType(selected[0]) != 'transform':
            raise ValueError('Select exactly one polygon mesh transform (no components).')
        mesh_transform = selected[0]
        shapes = cmds.listRelatives(
            mesh_transform, shapes=True, noIntermediate=True, fullPath=True
        ) or []
        if len(shapes) != 1 or cmds.nodeType(shapes[0]) != 'mesh':
            raise ValueError('Select a transform containing exactly one polygon mesh.')
        if cmds.listRelatives(mesh_transform, children=True, type='transform'):
            raise ValueError('Select a single mesh without child transforms.')
        history = cmds.listHistory(mesh_transform) or []
        if any(cmds.nodeType(node) in ('skinCluster', 'blendShape') for node in history):
            raise ValueError('This static-mesh lesson excludes skin and blend shapes.')
        if cmds.currentUnit(query=True, linear=True) != 'cm':
            raise ValueError('Set Maya working units to centimeters for this demo.')
        import maya.api.OpenMaya as om
        matrix = cmds.xform(mesh_transform, query=True, worldSpace=True, matrix=True)
        if om.MMatrix(matrix).det4x4() <= 0:
            raise ValueError('Resolve mirrored/zero scale before publishing this teaching asset.')
        return mesh_transform

    def inspect_selection(self):
        import maya.cmds as cmds
        mesh_transform = self._source()
        bounds = cmds.exactWorldBoundingBox(mesh_transform)
        dimensions = [bounds[i + 3] - bounds[i] for i in range(3)]
        if cmds.upAxis(query=True, axis=True) == 'y':
            dimensions = [dimensions[0], dimensions[2], dimensions[1]]
        return {
            'host': 'maya',
            'source_file': cmds.file(query=True, sceneName=True),
            'object_name': mesh_transform,
            'mesh_count': 1,
            'face_count': cmds.polyEvaluate(mesh_transform, face=True),
            'dimensions_cm': dimensions,
        }

    def export_fbx(self, path):
        import maya.cmds as cmds
        import maya.mel as mel
        source = self._source()
        selection = cmds.ls(selection=True, long=True)
        temporary = None
        modified = cmds.file(query=True, modified=True)
        undo_enabled = cmds.undoInfo(query=True, state=True)
        if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
            cmds.loadPlugin('fbxmaya', quiet=True)
        mel.eval('FBXPushSettings;')
        try:
            # Export a copy so the source mesh and its history stay intact.
            cmds.undoInfo(stateWithoutFlush=False)
            temporary = cmds.duplicate(source, returnRootsOnly=True, name='__BridgeExport')[0]
            if cmds.listRelatives(temporary, parent=True):
                temporary = cmds.parent(temporary, world=True)[0]
            cmds.delete(temporary, constructionHistory=True)
            # Place the source pivot at the exported mesh origin.
            pivot = cmds.xform(temporary, query=True, worldSpace=True, rotatePivot=True)
            cmds.move(-pivot[0], -pivot[1], -pivot[2], temporary, relative=True, worldSpace=True)
            cmds.makeIdentity(temporary, apply=True, translate=True, rotate=True, scale=True)
            cmds.xform(temporary, worldSpace=True, pivots=(0, 0, 0))
            cmds.select(temporary, replace=True)
            mel.eval('FBXResetExport;')
            mel.eval('FBXExportSmoothingGroups -v true;')
            mel.eval('FBXExportTriangulate -v true;')
            mel.eval('FBXExportInputConnections -v false;')
            mel.eval('FBXExportBakeComplexAnimation -v false;')
            mel.eval('FBXExportUpAxis z;')
            filename = str(path).replace('\\', '/').replace('"', '\\"')
            mel.eval('FBXExport -f "' + filename + '" -s;')
        finally:
            # Remove the copy and restore the artist's session settings.
            if temporary and cmds.objExists(temporary):
                cmds.delete(temporary)
            cmds.select(selection, replace=True)
            mel.eval('FBXPopSettings;')
            cmds.undoInfo(stateWithoutFlush=undo_enabled)
            cmds.file(modified=modified)

