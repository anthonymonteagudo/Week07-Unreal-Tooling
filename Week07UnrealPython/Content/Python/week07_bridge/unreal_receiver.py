"""One Unreal receiver for both publishers. Start explicitly in the editor."""
from pathlib import Path
import time
from .core import default_exchange, load_manifest, validate_target
from .transport import Inbox, receiver_status

_handle = None
_inbox = None
_last_tick = 0.0


def import_manifest(manifest, exchange=None):
    import unreal
    data, fbx = load_manifest(manifest, exchange)
    package = validate_target(data['asset_name'], data['destination_path'])
    existing = unreal.load_asset(package) if unreal.EditorAssetLibrary.does_asset_exist(package) else None
    if existing and not isinstance(existing, unreal.StaticMesh):
        raise ValueError('Destination exists and is not a StaticMesh: ' + package)
    if existing and unreal.EditorAssetLibrary.get_metadata_tag(existing, 'Week07Bridge') != '1':
        raise ValueError('Destination was not created by this bridge. Choose another asset name.')
    # Preserve assignments on the shared mesh as well as per-component overrides.
    materials = list(existing.get_editor_property('static_materials')) if existing else []
    options = unreal.FbxImportUI()
    for key, value in dict(import_mesh=True, import_as_skeletal=False, import_animations=False,
                           import_materials=False, import_textures=False,
                           automated_import_should_detect_type=False,
                           mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH).items():
        options.set_editor_property(key, value)
    mesh_options = options.get_editor_property('static_mesh_import_data')
    for key, value in dict(combine_meshes=True, auto_generate_collision=False,
                           convert_scene=True, convert_scene_unit=True,
                           force_front_x_axis=False, transform_vertex_to_absolute=True,
                           import_uniform_scale=1.0).items():
        mesh_options.set_editor_property(key, value)
    task = unreal.AssetImportTask()
    for key, value in dict(filename=str(fbx), destination_path=data['destination_path'],
                           destination_name=data['asset_name'], automated=True,
                           replace_existing=True, replace_existing_settings=True,
                           save=False, options=options, factory=unreal.FbxFactory()).items():
        task.set_editor_property(key, value)
    # Pin the FBX importer for a predictable lesson on UE versions with Interchange.
    console = 'Interchange.FeatureFlags.Import.FBX'
    old = unreal.SystemLibrary.get_console_variable_int_value(console)
    try:
        unreal.SystemLibrary.execute_console_command(None, console + ' 0')
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    finally:
        unreal.SystemLibrary.execute_console_command(None, console + ' ' + str(old))
    paths = list(task.get_editor_property('imported_object_paths'))
    expected = package + '.' + data['asset_name']
    if expected not in paths:
        raise RuntimeError('Import did not report the expected asset: ' + repr(paths))
    mesh = unreal.load_asset(package)
    if not isinstance(mesh, unreal.StaticMesh):
        raise RuntimeError('Import did not produce a StaticMesh.')
    if materials:
        mesh.set_editor_property('static_materials', materials)
    unreal.EditorAssetLibrary.set_metadata_tag(mesh, 'Week07Bridge', '1')
    unreal.EditorAssetLibrary.set_metadata_tag(mesh, 'BridgeRevision', data['revision'])
    bounds = mesh.get_bounding_box()
    size = bounds.max - bounds.min
    dimensions = [size.x, size.y, size.z]
    if any(abs(actual - wanted) > max(.1, wanted * .005)
           for actual, wanted in zip(dimensions, data['dimensions_cm'])):
        raise RuntimeError('Imported but NOT saved: size/axis verification failed. '
                           + str(dimensions) + ' expected ' + str(data['dimensions_cm']))
    if not unreal.EditorAssetLibrary.save_loaded_asset(mesh):
        raise RuntimeError('Imported but saving failed; check file permissions/Perforce.')
    return {'asset_path': expected, 'revision': data['revision'],
            'dimensions_cm': dimensions, 'updated_existing': existing is not None}


def _tick(delta):
    global _last_tick
    if time.monotonic() - _last_tick < .5 or _inbox is None:
        return
    _last_tick = time.monotonic()
    import unreal
    try:
        _inbox.heartbeat(project=str(Path(unreal.Paths.project_dir()).resolve()))
        result = _inbox.poll()
        if result:
            (unreal.log if result['ok'] else unreal.log_error)('Week 7 bridge: ' + str(result))
    except Exception as error:
        unreal.log_error('Week 7 bridge: ' + str(error))


def start(exchange=None):
    global _handle, _inbox
    import unreal
    if _handle is not None:
        return str(_inbox.root)
    root = Path(exchange or default_exchange()).resolve()
    if receiver_status(root):
        raise RuntimeError('Another receiver is active for this exchange folder.')
    _inbox = Inbox(root, import_manifest)
    _handle = unreal.register_slate_post_tick_callback(_tick)
    _inbox.heartbeat(project=str(Path(unreal.Paths.project_dir()).resolve()))
    unreal.log('Week 7 bridge listening: ' + str(root))
    return str(root)


def stop():
    global _handle, _inbox
    import unreal
    if _handle is not None:
        unreal.unregister_slate_post_tick_callback(_handle)
        _handle = None
    if _inbox:
        _inbox.heartbeat(running=False)
        _inbox = None


def install_menu():
    """Native Unreal Tools menu; no service starts just by importing the module."""
    import unreal
    menus = unreal.ToolMenus.get()
    menu = menus.extend_menu('LevelEditor.MainMenu.Tools')
    menu.add_section('Week07Bridge', 'Maya / Blender Bridge')
    for action in ('start', 'stop'):
        entry = unreal.ToolMenuEntry(name='Week07Bridge.' + action,
                                    type=unreal.MultiBlockType.MENU_ENTRY)
        entry.set_label(action.title() + ' FBX Bridge Receiver')
        entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, '',
                                 'from week07_bridge import unreal_receiver; unreal_receiver.' + action + '()')
        menu.add_menu_entry('Week07Bridge', entry)
    menus.refresh_all_widgets()
