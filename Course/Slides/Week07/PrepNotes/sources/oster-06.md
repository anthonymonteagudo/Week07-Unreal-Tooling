	def getStaticMeshLODData():
	
	    PML = unreal.ProceduralMeshLibrary
	
	  
	
	    staticMeshes = getAssetClass('StaticMesh')
	
	  
	
	    staticMeshLODData = []
	
	  
	
	    for staticMesh in staticMeshes:
	
	        staticMeshTriCount = []
	
	        numLODs = staticMesh.get_num_lods()
	
	  
	
	        for i in range(numLODs):
	
	            numSections = staticMesh.get_num_sections(i)
	
	            LODTriCount = 0
	
	  
	
	            for j in range(numSections):
	
	                sectionData = PML.get_section_from_static_mesh(staticMesh, i, j)
	
	  
	
	                sectionTriCount = (len(sectionData[1])/3)
	
	                LODTriCount += sectionTriCount
	
	  
	
	            staticMeshTriCount.append(LODTriCount)
	
	  
	
	        staticMeshReductions = [100]
	
	  
	
	        for i in range(1, len(staticMeshTriCount)):
	
	            staticMeshReductions.append(int(staticMeshTriCount[i]/staticMeshTriCount[0]) * 100))
	
	  
	
	        print(staticMesh.get_name())
	
	        print(staticMeshTriCount)
	
	        print(' ____ ')
	
	  
	
	        try:
	
	            LODData = (staticMesh.get_name(), staticMeshTriCount[1])
	
	        except:
	
	            pass
	
	        staticMeshLODData.append(LODData)
	
	  
	
	    return staticMeshLODData