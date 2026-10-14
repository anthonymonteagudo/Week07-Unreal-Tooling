"""Blender native sidebar. Buttons call the same client used by the Maya UI."""
import bpy
from .client import Publisher
from .blender_adapter import BlenderAdapter
from .core import default_exchange

_client = None


def client(context):
    global _client
    exchange = bpy.path.abspath(context.scene.w7_bridge_exchange)
    if _client is None:
        _client = Publisher(BlenderAdapter(), exchange)
    _client.set_exchange(exchange)
    return _client


class W7_OT_publish(bpy.types.Operator):
    bl_idname = 'w7bridge.publish'
    bl_label = 'Publish FBX + JSON'
    send_to_unreal: bpy.props.BoolProperty(default=False)

    def execute(self, context):
        publisher = client(context)
        try:
            publisher.publish(context.scene.w7_bridge_name, send=self.send_to_unreal)
            self.report({'INFO'}, publisher.message)
        except Exception as error:
            publisher.message = str(error)
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        return {'FINISHED'}


class W7_OT_send(bpy.types.Operator):
    bl_idname = 'w7bridge.send'
    bl_label = 'Send Published Revision'

    def execute(self, context):
        publisher = client(context)
        try:
            publisher.send()
        except Exception as error:
            publisher.message = str(error)
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        return {'FINISHED'}


class W7_OT_fixture(bpy.types.Operator):
    bl_idname = 'w7bridge.fixture'
    bl_label = 'Create Comparison Prop'
    revised: bpy.props.BoolProperty(default=False)

    def execute(self, context):
        from .fixture import create_blender
        try:
            create_blender(self.revised)
        except Exception as error:
            self.report({'ERROR'}, str(error))
            return {'CANCELLED'}
        return {'FINISHED'}


class W7_PT_bridge(bpy.types.Panel):
    bl_label = 'Maya / Blender to Unreal'
    bl_idname = 'W7_PT_bridge'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Week 7'

    def draw(self, context):
        layout = self.layout
        publisher = client(context)
        layout.label(text='One static mesh | source origin | cm')
        layout.prop(context.scene, 'w7_bridge_exchange', text='Exchange')
        layout.prop(context.scene, 'w7_bridge_name', text='Asset name')
        layout.label(text='/Game/Week07/Bridge')
        layout.label(text='Unreal: ' + ('Connected' if publisher.connected else 'Offline'))
        layout.operator('w7bridge.publish')
        layout.operator('w7bridge.publish', text='Publish & Send to Unreal').send_to_unreal = True
        layout.operator('w7bridge.send')
        box = layout.box()
        import textwrap
        for line in textwrap.wrap(publisher.message, width=40):
            box.label(text=line)
        layout.separator()
        layout.operator('w7bridge.fixture')
        layout.operator('w7bridge.fixture', text='Create Revised Prop (+40 cm)').revised = True


CLASSES = (W7_OT_publish, W7_OT_send, W7_OT_fixture, W7_PT_bridge)


def _poll():
    if _client:
        _client.poll()
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
    return 1.0


def register():
    if hasattr(bpy.types, 'W7_PT_bridge'):
        return
    for cls in CLASSES:
        bpy.utils.register_class(cls)
    bpy.types.Scene.w7_bridge_exchange = bpy.props.StringProperty(
        name='Exchange', subtype='DIR_PATH', default=str(default_exchange()))
    bpy.types.Scene.w7_bridge_name = bpy.props.StringProperty(default='SM_Compare_Blender')
    bpy.app.timers.register(_poll, persistent=True)


def unregister():
    global _client
    if bpy.app.timers.is_registered(_poll):
        bpy.app.timers.unregister(_poll)
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)
    for name in ('w7_bridge_exchange', 'w7_bridge_name'):
        if hasattr(bpy.types.Scene, name):
            delattr(bpy.types.Scene, name)
    _client = None
