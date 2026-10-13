
	def getAssetClass():
	
	    EAL = unreal.EditorAssetLibrary
	
	    assetPaths = EAL.list_assets('/Game')
	
	
	    assets = []
	
	
	    for assetPath in assetPaths:
	
	        assetData = EAL.find_asset_data(assetPath)
	
	        assetClass = assetData.asset_class
	
	        if assetClass == classType:
	
	            assets.append(assetData.get_asset())
	
	  
	    for asset in assets: print(asset)
	
	    return assets