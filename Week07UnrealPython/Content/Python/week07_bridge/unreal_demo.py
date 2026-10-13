"""Presentation setup for the explicitly prepared comparison map only."""
def style():
    import unreal
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    if world.get_path_name().split('.')[0] != '/Game/Week07/Bridge/W07_BridgeComparison':
        raise RuntimeError('Open the bridge comparison map first.')
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    by_name = {a.get_actor_label(): a for a in actors.get_all_level_actors()}
    library = unreal.EditorAssetLibrary
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    for host, color in [('Blender', (.04, .32, .65)), ('Maya', (.75, .21, .045))]:
        name = 'M_Bridge' + host
        path = '/Game/Week07/Bridge/' + name
        material = unreal.load_asset(path) if library.does_asset_exist(path) else None
        if material is None:
            material = tools.create_asset(name, '/Game/Week07/Bridge', unreal.Material, unreal.MaterialFactoryNew())
            node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionConstant3Vector, -250, 0)
            node.set_editor_property('constant', unreal.LinearColor(*color, 1))
            unreal.MaterialEditingLibrary.connect_material_property(node, '', unreal.MaterialProperty.MP_BASE_COLOR)
            unreal.MaterialEditingLibrary.recompile_material(material)
            library.save_loaded_asset(material)
        mesh = unreal.load_asset('/Game/Week07/Bridge/SM_Compare_' + host)
        mesh.set_material(0, material)
        library.save_loaded_asset(mesh)
        label = by_name[host + ' label']
        label.set_actor_location(unreal.Vector(0, -160 if host == 'Blender' else 160, 265), False, False)
        label.text_render.set_text(host + '   (2 instances)')
        label.text_render.set_world_size(25)
        label.text_render.set_text_render_color(unreal.Color(240, 240, 240, 255))
        label.set_actor_hidden_in_game(True)
    light = by_name['Bridge key light']
    light.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    light.set_actor_rotation(unreal.Rotator(-40, 135, 0), False)
    light.light_component.set_intensity(6)
    light.light_component.set_editor_property('forward_shading_priority', 1)
    if 'Bridge fill light' not in by_name:
        fill = actors.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 500), unreal.Rotator(-50, -45, 0))
        fill.set_actor_label('Bridge fill light')
        fill.light_component.set_intensity(2)
    else:
        fill = by_name['Bridge fill light']
    fill.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    fill.set_actor_rotation(unreal.Rotator(-50, -45, 0), False)
    if 'Bridge sky' not in by_name:
        sky = actors.spawn_actor_from_class(unreal.SkyAtmosphere, unreal.Vector(0, 0, 0))
        sky.set_actor_label('Bridge sky')
    light.light_component.set_editor_property('atmosphere_sun_light', True)
    if 'Bridge ambient light' not in by_name:
        ambient = actors.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0, 0, 400))
        ambient.set_actor_label('Bridge ambient light')
    else:
        ambient = by_name['Bridge ambient light']
    ambient.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    ambient.light_component.set_real_time_capture(True)
    if 'Bridge camera fill' not in by_name:
        camera_fill = actors.spawn_actor_from_class(unreal.PointLight, unreal.Vector(400, -500, 350))
        camera_fill.set_actor_label('Bridge camera fill')
    else:
        camera_fill = by_name['Bridge camera fill']
    camera_fill.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    camera_fill.light_component.set_intensity(100)
    camera_fill.light_component.set_attenuation_radius(3000)
    camera = by_name['Bridge comparison camera']
    camera.set_actor_location(unreal.Vector(850, -900, 650), False, False)
    rotation = unreal.MathLibrary.find_look_at_rotation(camera.get_actor_location(), unreal.Vector(0, 0, 120))
    camera.set_actor_rotation(rotation, False)
    camera.camera_component.set_field_of_view(45)
    for host in ('Blender', 'Maya'):
        label = by_name[host + ' label']
        face = unreal.MathLibrary.find_look_at_rotation(label.get_actor_location(), camera.get_actor_location())
        label.set_actor_rotation(face, False)
    unreal.EditorLevelLibrary.set_level_viewport_camera_info(camera.get_actor_location(), rotation)
