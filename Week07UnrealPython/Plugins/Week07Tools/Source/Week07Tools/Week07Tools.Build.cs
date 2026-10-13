using UnrealBuildTool;
public class Week07Tools : ModuleRules {
 public Week07Tools(ReadOnlyTargetRules Target) : base(Target) {
  PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;
  PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine"});
  PrivateDependencyModuleNames.AddRange(new string[]{"Slate","SlateCore","UnrealEd","ToolMenus","PythonScriptPlugin","Json","Niagara","InputCore"});
 }
}
