Part 1:

	def returnMaterialInformationSMC():
	
	    levelActors = unreal.EditorActorSubsystem().get_all_level_actors()
	
	  
	
	    for levelActor in levelActors:
	
	        if (levelActor.get_class().get_name()) == 'StaticMeshActor':
	
	            staticMeshComponent = levelActor.static_mesh_component
	
	  
	
	            print (levelActor.get_name())
	
	            materials = staticMeshComponent.get_materials()
	
	            for material in materials:
	
	                print (material.get_name())
	
	                try:
	
	                    for item in material.texture_parameter_values: print (item)
	
	                except:
	
	                    pass
	
	                print ('___')


Part 2:

	def returnMaterialInformationSMC():
	
	    levelActors = unreal.EditorActorSubsystem().get_all_level_actors()
	
	  
	
	    testMat = unreal.EditorAssetLibrary.find_asset_data('/Game/python/MI_test').get_asset()
	
	  
	
	    for levelActor in levelActors:
	
	        if (levelActor.get_class().get_name()) == 'StaticMeshActor':
	
	            staticMeshComponent = levelActor.static_mesh_component
	
	  
	
	            for i in range(staticMeshComponent.get_num_materials()):
	
	                staticMeshComponent.set_material(i, testMat)