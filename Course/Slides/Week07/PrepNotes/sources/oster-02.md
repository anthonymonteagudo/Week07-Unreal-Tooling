Script:
	
	import unreal
	
	def listAssetPaths():
	
	    EAL = unreal.EditorAssetLibrary
	
	    assetPaths = EAL.list_assets('/Game', recursive=True, include_folder=False)

	    unreal.log(f"Found {len(assetPaths)} assets")

	    for assetPath in assetPaths:
	
	        unreal.log(assetPath)
	
	listAssetPaths()


Result in Output Log:

	LogPython: import importlib
	import import_assets as TS
	TS = importlib.reload(TS)
	LogPython: Found 1038 assets
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_Albedo_Specular_01a.MF_Albedo_Specular_01a
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_Angle_Blend_01a.MF_Angle_Blend_01a
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_BarkUVMap.MF_BarkUVMap
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_Camera_Depth_Landscape_01a.MF_Camera_Depth_Landscape_01a
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_CustomGrassWind.MF_CustomGrassWind
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_Damaged_Wood.MF_Damaged_Wood
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_Debris_01a.MF_Debris_01a
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_Detail_Normal_01a.MF_Detail_Normal_01a
	LogPython: /Game/Northwood/DekogonContent/Materials/Functions/MF_Displacment_01a.MF_Displacment_01a