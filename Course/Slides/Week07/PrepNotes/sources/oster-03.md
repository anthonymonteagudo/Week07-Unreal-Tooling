
	import unreal
	
	
	def listAssetPaths():
	
	    EAL = unreal.EditorAssetLibrary
	  
	    assetPaths = EAL.list_assets('/Game', recursive=True, include_folder=False)
	  
	    unreal.log(f"Found {len(assetPaths)} assets")
	  
	    for assetPath in assetPaths:
	
	        unreal.log(assetPath)
	
	
	def getSelectionContentBrowser():
	
	    EUL = unreal.EditorUtilityLibrary
	
	    selectedAssets = EUL.get_selected_assets()
	
	    for selectedAsset in selectedAssets: print(selectedAssets)
	  
	
	def getAllActors():
	
	    EAS = unreal.EditorActorSubsystem()
	
	
	    actors = EAS.get_all_level_actors()
	
	  
	    for actor in actors: print(actor)
	  
	
	def getSelectedActors():
	
	    EAS = unreal.EditorActorSubsystem()
	  
	    selectedActors = EAS.get_selected_level_actors()
	
	    for selectedActor in selectedActors: print(selectedActor)
	    