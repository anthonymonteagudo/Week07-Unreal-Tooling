"""Only Maya-specific scene access and export. Same Publisher as Blender."""
class MayaAdapter:
    def _source(self):
        import maya.cmds as cmds
        selected = cmds.ls(selection=True, long=True) or []
        if len(selected) != 1 or cmds.nodeType(selected[0]) != 'transform':
            raise ValueError('Select exactly one polygon mesh transform (no components).')
        obj = selected[0]
        shapes = cmds.listRelatives(obj, shapes=True, noIntermediate=True, fullPath=True) or []
        if len(shapes) != 1 or cmds.nodeType(shapes[0]) != 'mesh':
            raise ValueError('Select a transform containing exactly one polygon mesh.')
        if cmds.listRelatives(obj, children=True, type='transform'):
            raise ValueError('Select a single mesh without child transforms.')
        history = cmds.listHistory(obj) or []
        if any(cmds.nodeType(n) in ('skinCluster', 'blendShape') for n in history):
            raise ValueError('This static-mesh lesson excludes skin and blend shapes.')
        if cmds.currentUnit(query=True, linear=True) != 'cm':
            raise ValueError('Set Maya working units to centimeters for this demo.')
        import maya.api.OpenMaya as om
        if om.MMatrix(cmds.xform(obj, query=True, worldSpace=True, matrix=True)).det4x4() <= 0:
            raise ValueError('Resolve mirrored/zero scale before publishing this teaching asset.')
        return obj

    def inspect_selection(self):
        import maya.cmds as cmds
        obj = self._source()
        box = cmds.exactWorldBoundingBox(obj)
        dims = [box[i + 3] - box[i] for i in range(3)]
        if cmds.upAxis(query=True, axis=True) == 'y':
            dims = [dims[0], dims[2], dims[1]]
        return dict(host='maya', source_file=cmds.file(query=True, sceneName=True),
                    object_name=obj, mesh_count=1, face_count=cmds.polyEvaluate(obj, face=True),
                    dimensions_cm=dims)

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
            cmds.undoInfo(stateWithoutFlush=False)
            temporary = cmds.duplicate(source, returnRootsOnly=True, name='__BridgeExport')[0]
            if cmds.listRelatives(temporary, parent=True):
                temporary = cmds.parent(temporary, world=True)[0]
            cmds.delete(temporary, constructionHistory=True)
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
            if temporary and cmds.objExists(temporary):
                cmds.delete(temporary)
            cmds.select(selection, replace=True)
            mel.eval('FBXPopSettings;')
            cmds.undoInfo(stateWithoutFlush=undo_enabled)
            cmds.file(modified=modified)
