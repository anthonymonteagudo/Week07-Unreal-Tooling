	
	def getStaticMeshInstanceCounts():
	
	  
	
	    levelActors = unreal.EditorActorSubsystem().get_all_level_actors()
	
	  
	
	    staticMeshActors = []
	
	    staticMeshActorCounts = []
	
	  
	
	    for levelActor in levelActors:
	
	        if (levelActor.get_class().get_name()) == 'StaticMeshActor':
	
	            staticMeshComponent = levelActor.static_mesh_component
	
	            staticMesh = staticMeshComponent.static_mesh
	
	            staticMeshActors.appen(staticMesh.get_name())
	
	  
	
	    processedActors = []
	
	    for staticMeshActor in staticMeshActors:
	
	        if staticMeshActor not in processedActors:
	
	            actorCounts = (staticMeshActor, staticMeshActors.count(staticMeshActor))
	
	            staticMeshActorCounts.append(actorCounts)
	
	            processedActors.append(staticMeshActor)
	
	  
	
	    staticMeshActorCounts.sort(key = lambda a: a[1], reverse = True)
	
	  
	
	    # for item in staticMeshActorCounts: print(item)
	
	  
	
	    LODData = getStaticMeshLODData()
	
	  
	
	    # for item in LODData: print (item)
	
	  
	
	    aggregateTriCounts - []
	
	  
	
	    for i in range(len(staticMeshActorCounts)):
	
	        for j in range(len(LODData)):
	
	            if staticMeshActorCounts[i][0] == LODData[j][0]:
	
	                aggregateTriCount = (staticMeshActorCounts[i][0], staticMeshActorCounts[i][1] * LODData[j][1])
	
	                aggregateTriCounts.append(aggregateTriCount)
	
	  
	
	    aggregateTriCounts.sort(key = lambda a: a[1], reverse = True)
	
	  
	
	    for item in aggregateTriCounts: print (item)