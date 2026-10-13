
	def getStaticMeshData():
	
	    staticMeshes = getAssetClass('StaticMesh')
	
	    for staticMesh in staticMeshes:
	
	  
	        # assetImportData = staticMesh.get_editor_property('asset_import_data')
	
	        # fbxFilePath = assetImportData.extract_filenames()
	
	        # print(fbxFilePath)
	
	  
	        lodGroupInfo = staticMesh.get_editor_property('lod_group')
	
	        print(lodGroupInfo)
	
	  
	        if lodGroupInfo == None:
	
	            if staticMesh.get_num_lods() == 1:
	
	                staticMesh.set_editor_property('lod_group', 'LargeProp')
	
	  
	            # print (staticMesh.get_name())
	
	            # print (staticMesh.get_num_lods())
