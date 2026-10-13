https://www.youtube.com/watch?v=KLExEMFRk00&list=PLKgYiIAqG99cwlb4Y2Pu-cSb_Vw14-t0c&index=6

List Menus Tool:

	import unreal
	
	def list_menu(num=1000):
	
	    menu_list = set()
	
	    for i in range(num):
	
	        obj = unreal.find_object(None, f'/Engine/Transient.ToolMenus_0:RegisteredMenu_%s' % i)
	
	        if not obj:
	
	            obj = unreal.find_object(None, f'/Engine/Transient.ToolMenus_0:ToolMenu_{i}') # for backward compatibility
	
	            continue
	
	        menu_name = str(obj.menu_name)
	
	        if menu_name == "None":
	
	            continue
	
	        menu_list.add(menu_name)
	
	    return list(menu_list)
	
	print(list_menu())

Output: LogPython: ['ContentBrowser.ToolBar', 'ContentBrowser.AssetContextMenu.SkeletalMesh', 'ControlRigEditor.RigHierarchy.DragDropMenu.Align', 'HomeScreen.MainMenu', 'MainFrame.MainMenu', 'ContentBrowser.AssetContextMenu.MaterialFunctionMaterialLayerBlend', 'ContentBrowser.AssetContextMenu.MaterialFunction', 'ContentBrowser.AssetContextMenu.AssetActionsSubMenu', 'ContentBrowser.AssetContextMenu.NiagaraParameterCollection', 'StatusBar.ToolBar.SourceControl', 'HomeScreen.MainMenu.File', 'LevelEditor.MainMenu', 'ContentBrowser.AssetContextMenu.AnimMontage', 'LevelEditor.MainMenu.Build', 'ContentBrowse
r.AssetContextMenu.WidgetBlueprintGeneratedClass', 'LevelEditor.SecondaryToolbar', 'AssetEditor.WidgetBlueprintEditor.ToolBar.DesignerName', 'LevelEditor.LevelEditorToolBar.OpenBlueprint', 'LevelEditor.MainMenu.Select.GeometryCollections', 'MainFrame.MainMenu.Tools', 'LevelEditor.MainMenu.Build.LightingQuality', 'LevelEditor.ActorContextMenu', 'MediaPlayer.AssetPickerAssetContextMenu', 'ContentBrowser.AssetContextMenu.Skeleton', 'LevelEditor.LevelEditorToolBar.Cinematics', 'ControlRigEditor.RigHierarchy.ContextMenu', 'ContentBrowser.AssetContextMenu.MaterialFunctionMaterialLayer', 'ContentBrow
ser.AssetContextMenu.InterchangeSceneImportAsset', 'ContentBrowser.AssetContextMenu.BlueprintGeneratedClass', 'AssetEditor.SkeletalMeshEditor.ToolBar', 'LevelEditor.InViewportPanel', 'ContentBrowser.AssetContextMenu.TextureRenderTarget', 'Sequencer.MainToolBar.ViewOptions', 'LevelEditor.LevelEditorToolBar.SettingsToolbar', 'ContentBrowser.AssetContextMenu', 'ContentBrowser.AssetContextMenu.StaticMesh', 'LevelEditor.MainMenu.Build.LightingInfo.LightingDensity', 'ContentBrowser.AssetContextMenu.MaterialFunctionMaterialLayerBlendInstance', 'LevelEditor.PIEViewportToolbar', 'LevelEditor.MainMenu.E
dit', 'Sequencer.TimelineMenu', 'RewindDebugger.TrackContextMenu', 'LevelEditor.MainMenu.Help', 'ContentBrowser.AssetContextMenu.LevelVariantSets', 'ContentBrowser.AssetContextMenu.NiagaraEmitter', 'ContentBrowser.AssetContextMenu.DataTable', 'LevelEditor.ViewportToolbar.Camera.CameraMovement.CameraSpeed', 'ContentBrowser.AssetContextMenu.MirrorDataTable', 'ContentBrowser.AssetContextMenu.SoundCue', 'ContentBrowser.AssetContextMenu.CurveBase', 'MainFrame.MainMenu.Edit', 'ContentBrowser.AssetContextMenu.WidgetBlueprint.AssetActionsSubMenu', 'RewindDebugger.ToolBar', 'ContentBrowser.AssetContext
Menu.DataAsset', 'ContentBrowser.AssetContextMenu.GroomAsset', 'VrEditor.ToggleVrOptions', 'AssetEditor.WidgetBlueprintEditor.ToolBar.GraphName', 'ContentBrowser.AssetContextMenu.CurveTable', 'LevelEditor.MainMenu.Build.LightingInfo', 'MainFrame.MainMenu.Asset', 'Kismet.SubobjectEditorContextMenu', 'ContentBrowser.AssetContextMenu.MaterialFunctionMaterialLayerInstance', 'LevelEditor.ActorContextMenu.AssetToolsSubMenu', 'ContentBrowser.AssetContextMenu.SoundWave', 'ContentBrowser.AssetContextMenu.MetaSoundSource', 'LevelEditor.ViewportToolbar.ViewModes', 'ContentBrowser.AssetContextMenu.BlendSp
ace', 'LevelEditor.MainMenu.Window', 'HomeScreenComboButtonMenu', 'ContentBrowser.AssetViewOptions.PathViewFilters', 'ContentBrowser.SourceBar', 'ContentBrowser.AssetContextMenu.NiagaraDataChannelAsset', 'ContentBrowser.AssetContextMenu.MaterialInterface', 'UnrealEd.ViewportToolbar.View', 'ContentBrowser.AssetContextMenu.NiagaraAssetTagDefinitions', 'LevelEditor.LevelViewportToolbar.View', 'MainFrame.MainMenu.File', 'ControlRigEditor.RigHierarchy.DragDropMenu.Align.Translation', 'LevelEditor.MainMenu.Tools', 'OutputLog.SettingsMenu', 'ContentBrowser.AssetContextMenu.MaterialFunctionInstance', 
'PropertyEditor.RowContextMenu', 'LevelEditor.StatusBar.ToolBar.CompileComboButton', 'AssetEditor.AnimationBlueprintEditor.MainMenu.Tools', 'ContentBrowser.AssetContextMenu.GeometryCollection', 'LevelEditor.LevelEditorToolBar.AssetsToolBar', 'MainFrame.NomadMainMenu', 'MainFrame.MainMenu.Window', 'ContentBrowser.AssetContextMenu.World', 'ContentBrowser.AssetContextMenu.DatasmithScene', 'HomeScreen.MainMenu.Edit', 'LevelEditor.MainMenu.File', 'ContentBrowser.AssetContextMenu.ControlRigPoseAsset', 'LevelEditor.ViewportToolbar', 'AssetEditor.SkeletonEditor.ToolBar', 'EditorSettingsViewer.LevelEdi
torPlaySettings', 'LevelEditor.LevelEditorSceneOutliner.ContextMenu.EditSubMenu', 'ContentBrowser.AssetContextMenu.NiagaraSimCache', 'EditorViewportDepthBarMenu', 'ContentBrowser.AssetContextMenu.FontFace', 'ContentBrowser.AddNewContextMenu', 'ContentBrowser.FolderContextMenu', 'ContentBrowser.AssetContextMenu.GroomBindingAsset', 'AssetEditor.AnimationEditor.ToolBar', 'ContentBrowser.AssetContextMenu.WorldBookmark', 'ContentBrowser.AssetContextMenu.Skeleton.CreateSkeletalMeshSubmenu', 'LevelEditor.LevelEditorToolBar.AddQuickMenu', 'ContentBrowser.AssetContextMenu.MetaSoundPatch', 'GestureDirec
tionSubmenu_Perspective', 'ContentBrowser.AssetContextMenu.Font', 'ContentBrowser.AssetContextMenu.SparseVolumeTexture', 'ControlRigEditor.ModularRigModel.ContextMenu', 'ControlRigEditor.RigHierarchy.ContextMenu.Naming', 'LevelEditor.ActorContextMenu.EditSubMenu', 'ContentBrowser.AssetContextMenu.SkeletalMesh.CreateSkeletalMeshSubmenu', 'ContentBrowser.AssetContextMenu.IKRigDefinition', 'LevelEditor.LevelEditorSceneOutliner.ContextMenu.LevelSubMenu', 'LevelEditor.LevelEditorSceneOutliner.ContextMenu', 'ContentBrowser.NavigationBar', 'LevelEditor.LevelEditorToolBar.PlayToolBar', 'LevelEditor.Le
velEditorToolBar.User', 'LevelEditor.ViewportToolbar.Snapping', 'LevelEditor.ActorContextMenu.LevelSubMenu', 'ContentBrowser.AssetContextMenu.AnimSequence', 'LevelEditor.ViewportToolbar.Transform', 'ContentBrowser.AssetContextMenu.ForceFeedbackEffect', 'LevelEditor.StatusBar.ToolBar', 'LevelEditor.ViewportToolbar.Camera', 'ContentBrowser.DragDropContextMenu', 'LevelEditor.MainMenu.Build.LightingInfo.LightingResolution', 'ContentBrowser.AssetViewOptions', 'ContentBrowser.AssetContextMenu.WidgetBlueprint', 'ControlRigEditor.RigHierarchy.ContextMenu.NewElement', 'SourceControl.ChangelistContextMe
nu', 'LevelEditor.LevelViewportToolbar.Show', 'GestureDirectionSubmenu_Orthographic', 'MainFrame.MainTabMenu.File', 'OutputLog.ConsoleInputBox.CmdExecMenu', 'ContentBrowser.AssetContextMenu.EditorUtilityBlueprint', 'ContentBrowser.AssetContextMenu.Blueprint', 'ContentBrowser.AssetContextMenu.Texture', 'ContentBrowser.AssetContextMenu.ImgMediaSource', 'ContentBrowser.AssetContextMenu.LevelSequence', 'MainFrame.MainMenu.Help', 'LevelEditor.LevelEditorToolBar.LevelToolbarQuickSettings', 'ContentBrowser.AssetContextMenu.Class', 'ContentBrowser.AssetContextMenu.NiagaraScript', 'ContentBrowser.Asset
ContextMenu.AnimationAsset', 'ContentBrowser.AssetContextMenu.TextureCube', 'ContentBrowser.AssetContextMenu.Texture2D', 'ContentBrowser.AssetContextMenu.MediaSource', 'LevelEditor.LevelViewportToolBar.Camera', 'LevelEditor.LevelEditorToolBar.ModesToolBar', 'ContentBrowser.AssetContextMenu.AnimBlueprint', 'LevelEditor.ViewportToolbar.Show', 'ContentBrowser.AssetContextMenu.ObjectRedirector', 'ContentBrowser.AssetContextMenu.PoseAsset', 'ContentBrowser.AssetContextMenu.MaterialInstanceConstant', 'ContentBrowser.AssetContextMenu.EditorUtilityWidgetBlueprint', 'LevelEditor.MainMenu.Select', 'Cont
rolRigEditor.RigHierarchy.DragDropMenu', 'RewindDebugger.MainMenu', 'HomeScreen.MainMenu.Help']

Extend UE5 Editor Menus:

	import unreal
	

	menus = unreal.ToolMenus.get()
	
	main_menu = menus.find_menu("LevelEditor.MainMenu")
	
	custom_menu = main_menu.add_sub_menu("Custom Menu", "Python Automation", "Menu Name", "Menu Label")
	
	menus.refresh_all_widgets()
	
	  
	
	@unreal.uclass()
	
	class MyScriptObject(unreal.ToolMenuEntryScript):
	
	    @unreal.ufunction(override=True)
	
	    def execute(self, context):
	
	        print("SCRIPT EXECUTED")
	
	  
	
	edit_menu = menus.find_menu("LevelEditor.MainMenu.Edit")
	
	script_object = MyScriptObject()
	
	script_object.init_entry(
	
	    owner_name=edit_menu.menu_name,
	
	    menu=edit_menu.menu_name,
	
	    section="EditMain",
	
	    name="Unreal Engine 5 Python Automation Course",
	
	    label="Unreal Engine 5 Python Automation Course",
	
	    tool_tip="Custom Script Entry"
	
	)
	
	script_object.register_menu_entry()
	
	  
	
	asset_context_menu = menus.find_menu("ContentBrowser.AssetContextMenu.StaticMesh")
	
	script_object2 = MyScriptObject()
	
	script_object2.init_entry(
	
	    owner_name=asset_context_menu.menu_name,
	
	    menu=asset_context_menu.menu_name,
	
	    section="EditMain",
	
	    name="Unreal Engine 5 Python Automation Course 2",
	
	    label="Unreal Engine 5 Python Automation Course 2",
	
	    tool_tip="Custom Script Entry 2"
	
	)
	
	script_object2.register_menu_entry()
	
	# Initialize these custom menus in startup script



