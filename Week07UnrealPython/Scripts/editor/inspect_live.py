import json
import unreal
import week07_tools as w7
print('ENGINE', unreal.SystemLibrary.get_engine_version())
print('WORLD', w7.world().get_path_name())
print('ACTORS', [(a.get_actor_label(),a.get_class().get_name()) for a in w7.actors().get_all_level_actors()])
reg=unreal.AssetRegistryHelpers.get_asset_registry()
systems=reg.get_assets_by_class(unreal.TopLevelAssetPath('/Script/Niagara','NiagaraSystem'), True)
print('SYSTEMS', [str(a.package_name) for a in systems][:50])
print('NIAGARA_FACTORY', unreal.NiagaraSystemFactoryNew.__doc__)
print('SYSTEM_MEMBERS', [n for n in dir(unreal.NiagaraSystem) if 'emitter' in n or 'scal' in n or 'effect' in n])
print('UNDO_MEMBERS', [n for n in dir(unreal) if 'Transaction' in n])
print('EDITOR_LIBRARY', [n for n in dir(unreal.EditorLevelLibrary) if 'undo' in n.lower()])
print('TEXTURES', [str(a.package_name) for a in reg.get_assets_by_path('/Game/Northwood/Textures',True) if any(s in str(a.package_name).lower() for s in ('crate','box','fill_01'))][:25])
