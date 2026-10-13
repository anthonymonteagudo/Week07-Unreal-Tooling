"""The same asymmetric wedge in both hosts, expressed in centimetres, Z-up.

120 wide x 60 deep x 180 high; front (+X) roof is lower than back (-X).
Geometry, topology and revision are shared. Only scene construction differs.
"""
POINTS_CM = [(-60, -30, 0), (60, -30, 0), (60, 30, 0), (-60, 30, 0),
             (-60, -30, 180), (60, -30, 100), (60, 30, 100), (-60, 30, 180)]
FACES = [(0, 3, 2, 1), (0, 1, 5, 4), (1, 2, 6, 5),
         (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7)]


def points(revised=False):
    return [(x, y, z + (40 if revised and z > 0 else 0)) for x, y, z in POINTS_CM]


def create_blender(revised=False):
    import bpy
    if bpy.context.mode != 'OBJECT':
        raise ValueError('Switch to Object Mode to create the example.')
    name = 'BridgeCompare_Revised' if revised else 'BridgeCompare'
    mesh = bpy.data.meshes.new(name)
    scale = bpy.context.scene.unit_settings.scale_length * 100
    mesh.from_pydata([(x / scale, y / scale, z / scale) for x, y, z in points(revised)], [], FACES)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    for item in list(bpy.context.selected_objects):
        item.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    return obj


def create_maya(revised=False):
    import maya.cmds as cmds
    import maya.api.OpenMaya as om
    if cmds.currentUnit(query=True, linear=True) != 'cm':
        raise ValueError('Set Maya working units to centimeters first.')
    y_up = cmds.upAxis(query=True, axis=True) == 'y'
    coords = [(x, z, -y) if y_up else (x, y, z) for x, y, z in points(revised)]
    mesh = om.MFnMesh()
    node = mesh.create([om.MPoint(*v) for v in coords], [len(f) for f in FACES],
                       [v for f in FACES for v in f])
    created = om.MFnDagNode(node).fullPathName()
    if cmds.nodeType(created) == 'mesh':
        created = cmds.listRelatives(created, parent=True, fullPath=True)[0]
    obj = cmds.rename(created,
                      'BridgeCompare_Revised' if revised else 'BridgeCompare')
    cmds.sets(obj, edit=True, forceElement='initialShadingGroup')
    cmds.select(obj, replace=True)
    return obj
