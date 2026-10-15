import unreal
reg=unreal.AssetRegistryHelpers.get_asset_registry()
for path in ['/Niagara/DefaultAssets/Templates/Systems/FountainLightweight','/Niagara/DefaultAssets/Templates/Systems/SimpleExplosion','/Niagara/DefaultAssets/Templates/Systems/DirectionalBurst']:
 asset=unreal.load_asset(path)
 print(path, asset)
 for prop in ['effect_type','fixed_bounds','fixed_bounds_enabled','warmup_time','warmup_tick_count','override_scalability_settings','scalability_overrides','exposed_parameters','emitters','emitter_handles']:
  try: print(prop,asset.get_editor_property(prop))
  except Exception as e: print(prop,str(e)[:160])
print('Effect type doc',unreal.NiagaraEffectType.__doc__)
print('Scaler',unreal.NiagaraSystemScalabilitySettings.__doc__)
print('StatelessEmitter',unreal.NiagaraStatelessEmitter.__doc__ if hasattr(unreal,'NiagaraStatelessEmitter') else '')
