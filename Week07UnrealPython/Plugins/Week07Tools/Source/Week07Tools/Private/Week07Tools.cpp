#include "Week07EditorLibrary.h"
#include "Editor.h"
#include "Framework/Application/SlateApplication.h"
#include "ImageUtils.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Modules/ModuleManager.h"
#include "Framework/Docking/TabManager.h"
#include "Widgets/Docking/SDockTab.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/Input/SCheckBox.h"
#include "Widgets/Input/SSpinBox.h"
#include "Widgets/Input/SComboBox.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/Views/SListView.h"
#include "Widgets/Views/STableRow.h"
#include "Widgets/Views/SHeaderRow.h"
#include "ToolMenus.h"
#include "IPythonScriptPlugin.h"
#include "Misc/Base64.h"
#include "Serialization/JsonSerializer.h"
#include "NiagaraSystem.h"
#include "NiagaraEmitterHandle.h"
#include "NiagaraEmitterBase.h"
#include "UObject/UnrealType.h"

static const FName ToolTab("Week07MaterialVFX");
struct FReviewRow { FString Item,Before,After; };
class SReviewRow : public SMultiColumnTableRow<TSharedPtr<FReviewRow>> {
public:
 SLATE_BEGIN_ARGS(SReviewRow){} SLATE_ARGUMENT(TSharedPtr<FReviewRow>,Row) SLATE_END_ARGS()
 TSharedPtr<FReviewRow> Row;
 void Construct(const FArguments& Args,const TSharedRef<STableViewBase>& Owner){Row=Args._Row;SMultiColumnTableRow::Construct(FSuperRowType::FArguments().Padding(6),Owner);}
 virtual TSharedRef<SWidget> GenerateWidgetForColumn(const FName& Column) override {
  FString Value=Column=="Item"?Row->Item:Column=="Before"?Row->Before:Row->After;
  FString Display=Value;if(Value.StartsWith("/Game/")||Value.StartsWith("/Engine/"))Display=FPaths::GetBaseFilename(Value);
  return SNew(STextBlock).Text(FText::FromString(Display)).WrapTextAt(Column=="After"?350.f:260.f).ToolTipText(FText::FromString(Value));
 }
};
class SWeek07Tools : public SCompoundWidget {
public:
 SLATE_BEGIN_ARGS(SWeek07Tools){} SLATE_END_ARGS()
 FString Session,Kind="material",Name="MI_Crate_Live";
 FString Status="Choose inputs, then preview.",Summary,ApplyLabel="Apply";
 int32 Slot=0;float Scale=1.f;bool CanApply=false,NeedsAck=false,Ack=false,Applied=false;
 TArray<TSharedPtr<FReviewRow>> Rows;
 TSharedPtr<SListView<TSharedPtr<FReviewRow>>> List;
 virtual ~SWeek07Tools(){if(!Session.IsEmpty())Send("close");}
 TSharedRef<SWidget> Label(const FString& Text){return SNew(STextBlock).Text(FText::FromString(Text)).AutoWrapText(true);}
 TSharedPtr<FJsonObject> Send(const FString& Action){
  auto Req=MakeShared<FJsonObject>();Req->SetStringField("action",Action);Req->SetStringField("session",Session);Req->SetStringField("kind",Kind);Req->SetStringField("name",Name);Req->SetNumberField("slot",Slot);Req->SetNumberField("scale",Scale);Req->SetBoolField("ack",Ack);
  FString Json;FJsonSerializer::Serialize(Req,TJsonWriterFactory<>::Create(&Json));
  FPythonCommandEx Cmd;Cmd.Command=FString::Printf(TEXT("import base64\nfrom week07_tooling.editor import native_panel\nprint('__W07_JSON__'+native_panel.dispatch(base64.b64decode('%s').decode('utf-8')))"),*FBase64::Encode(Json));
  auto Python=IPythonScriptPlugin::Get();
  if(!Python||!Python->ExecPythonCommandEx(Cmd)){CanApply=false;Status="Python unavailable or command failed. See Output Log; reconnect.";return nullptr;}
  for(const auto& Entry:Cmd.LogOutput){FString Output=Entry.Output;int32 At=Output.Find("__W07_JSON__");if(At==INDEX_NONE)continue;Output=Output.Mid(At+12);TSharedPtr<FJsonObject> Result;if(FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Output),Result))return Result;}
  CanApply=false;Status="No response received. Reconnect and preview again.";return nullptr;
 }
 void Clear(){Applied=false;CanApply=false;NeedsAck=false;Ack=false;Rows.Empty();Summary="Input editing does not undo applied changes.";Status="Choose inputs, then Preview.";ApplyLabel="Apply";if(List)List->RequestListRefresh();if(!Session.IsEmpty())Send("clear");}
 FReply Action(const FString& Action){
  if(Action=="connect"){if(!Session.IsEmpty())Send("close");Session.Empty();Clear();}
  auto Result=Send(Action);if(!Result)return FReply::Handled();
  Applied=false;
  Result->TryGetStringField("session",Session);Result->TryGetStringField("message",Status);Result->TryGetBoolField("can_apply",CanApply);Result->TryGetBoolField("warning_ack_required",NeedsAck);Ack=false;
  const TSharedPtr<FJsonObject>* Presentation=nullptr;
  if(Result->TryGetObjectField("presentation",Presentation)){
   Rows.Empty();(*Presentation)->TryGetStringField("summary",Summary);(*Presentation)->TryGetStringField("action",ApplyLabel);
   const TArray<TSharedPtr<FJsonValue>>* Values=nullptr;
   if((*Presentation)->TryGetArrayField("rows",Values))for(auto& Value:*Values){auto Cells=Value->AsArray();if(Cells.Num()!=3)continue;auto Row=MakeShared<FReviewRow>();Row->Item=Cells[0]->AsString();Row->Before=Cells[1]->AsString();Row->After=Cells[2]->AsString();Rows.Add(Row);}
  }else if(Action!="apply"){Rows.Empty();Summary.Empty();}
  if(Action=="apply"){
   ApplyLabel="Apply";bool Ok=false;Result->TryGetBoolField("ok",Ok);Applied=Ok;
   if(Ok){Status="Completed. Check the result in Unreal.";Summary=Kind=="material"?"Undo restores the assignment; the new asset remains.":"Undo removes this batch. Save changes yourself.";}
   else{Rows.Empty();Summary="Resolve the issue, then create a new preview.";}
  }
  List->RequestListRefresh();return FReply::Handled();
 }
 void Construct(const FArguments& Args){
  ChildSlot[SNew(SBorder).Padding(16)[SNew(SVerticalBox)
   +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(STextBlock).Text(FText::FromString("Material & VFX Tools")).Font(FCoreStyle::GetDefaultFontStyle("Bold",18))]
   +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[Label("UNREAL EDITOR  |  Current selection")]
   +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(SHorizontalBox)
    +SHorizontalBox::Slot().AutoWidth().Padding(0,0,8,0)[SNew(SButton).Text(FText::FromString("Material Setup")).OnClicked_Lambda([this](){Kind="material";Clear();Status="Select the texture set in Content Browser and mesh Actors in the level.";return FReply::Handled();})]
    +SHorizontalBox::Slot().AutoWidth().Padding(0,0,8,0)[SNew(SButton).Text(FText::FromString("VFX Placement")).OnClicked_Lambda([this](){Kind="vfx";Clear();Status="Select tagged placement markers in the level.";return FReply::Handled();})]
    +SHorizontalBox::Slot().AutoWidth()[SNew(SButton).Text(FText::FromString("Reconnect")).OnClicked_Lambda([this](){return Action("connect");})]]
   +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(STextBlock).Text_Lambda([this](){return FText::FromString(Kind=="material"?"Material Setup":"VFX Placement");})]
   +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(SHorizontalBox).Visibility_Lambda([this](){return Kind=="material"?EVisibility::Visible:EVisibility::Collapsed;})
    +SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Center).Padding(0,0,10,0)[Label("New instance name")]
    +SHorizontalBox::Slot().FillWidth(1)[SNew(SEditableTextBox).Text(FText::FromString(Name)).OnTextChanged_Lambda([this](const FText& T){Name=T.ToString();Clear();})]
    +SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Center).Padding(12,0,8,0)[Label("Slot")]
    +SHorizontalBox::Slot().AutoWidth()[SNew(SSpinBox<int32>).MinValue(0).MaxValue(15).Value_Lambda([this](){return Slot;}).OnValueChanged_Lambda([this](int32 V){Slot=V;Clear();})]]
   +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(SHorizontalBox).Visibility_Lambda([this](){return Kind=="vfx"?EVisibility::Visible:EVisibility::Collapsed;})
    +SHorizontalBox::Slot().AutoWidth().VAlign(VAlign_Center).Padding(0,0,10,0)[Label("Effect scale")]
    +SHorizontalBox::Slot().AutoWidth()[SNew(SSpinBox<float>).MinValue(.25f).MaxValue(1.f).Value_Lambda([this](){return Scale;}).OnValueChanged_Lambda([this](float V){Scale=V;Clear();})]]
   +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(STextBlock).Text_Lambda([this](){return FText::FromString(Status);}).AutoWrapText(true)]
   +SVerticalBox::Slot().AutoHeight().Padding(0,0,0,10)[SNew(STextBlock).Text_Lambda([this](){return FText::FromString(Summary);}).AutoWrapText(true)]
   +SVerticalBox::Slot().FillHeight(1)[SAssignNew(List,SListView<TSharedPtr<FReviewRow>>).ListItemsSource(&Rows).SelectionMode(ESelectionMode::None).OnGenerateRow_Lambda([](TSharedPtr<FReviewRow> Row,const TSharedRef<STableViewBase>& Owner){return SNew(SReviewRow,Owner).Row(Row);}).HeaderRow(SNew(SHeaderRow)+SHeaderRow::Column("Item").DefaultLabel(FText::FromString("Item")).FillWidth(.3f)+SHeaderRow::Column("Before").DefaultLabel(FText::FromString("Before")).FillWidth(.3f)+SHeaderRow::Column("After").DefaultLabel_Lambda([this](){return FText::FromString(Applied?"Result":"After Apply");}).FillWidth(.4f))]
   +SVerticalBox::Slot().AutoHeight().Padding(0,10)[SNew(SCheckBox).Visibility_Lambda([this](){return NeedsAck?EVisibility::Visible:EVisibility::Collapsed;}).IsChecked_Lambda([this](){return Ack?ECheckBoxState::Checked:ECheckBoxState::Unchecked;}).OnCheckStateChanged_Lambda([this](ECheckBoxState S){Ack=S==ECheckBoxState::Checked;})[Label("I reviewed the density warning")]]
   +SVerticalBox::Slot().AutoHeight()[SNew(SHorizontalBox)
    +SHorizontalBox::Slot().AutoWidth().Padding(0,0,10,0)[SNew(SButton).Text(FText::FromString("Preview")).OnClicked_Lambda([this](){return Action("preview");})]
    +SHorizontalBox::Slot().AutoWidth()[SNew(SButton).Text_Lambda([this](){return FText::FromString(ApplyLabel);}).IsEnabled_Lambda([this](){return CanApply&&(!NeedsAck||Ack);}).OnClicked_Lambda([this](){return Action("apply");})]]
   +SVerticalBox::Slot().AutoHeight().Padding(0,10,0,0)[Label("Choose inputs  >  Preview  >  Apply  >  Check")]
  ]];Action("connect");
 }
};
class FWeek07ToolsModule:public IModuleInterface{
public:
 virtual void StartupModule()override{
  FGlobalTabmanager::Get()->RegisterNomadTabSpawner(ToolTab,FOnSpawnTab::CreateLambda([](const FSpawnTabArgs&){return SNew(SDockTab).TabRole(ETabRole::NomadTab)[SNew(SWeek07Tools)];})).SetDisplayName(FText::FromString("Material & VFX Tools")).SetMenuType(ETabSpawnerMenuType::Hidden);
  UToolMenus::RegisterStartupCallback(FSimpleMulticastDelegate::FDelegate::CreateRaw(this,&FWeek07ToolsModule::Menus));
 }
 void Menus(){FToolMenuOwnerScoped Owner(this);auto* Menu=UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Tools");Menu->AddSection("Week07",FText::FromString("Week 7")).AddMenuEntry("Week07MaterialVFX",FText::FromString("Material & VFX Tools"),FText::FromString("Open the current Python workflows in a native editor tab"),FSlateIcon(),FUIAction(FExecuteAction::CreateStatic(&UWeek07EditorLibrary::OpenTools)));}
 virtual void ShutdownModule()override{UToolMenus::UnRegisterStartupCallback(this);UToolMenus::UnregisterOwner(this);FGlobalTabmanager::Get()->UnregisterNomadTabSpawner(ToolTab);}
};
IMPLEMENT_MODULE(FWeek07ToolsModule,Week07Tools)
bool UWeek07EditorLibrary::UndoDemo(){return GEditor&&GEditor->UndoTransaction();}
bool UWeek07EditorLibrary::RedoDemo(){return GEditor&&GEditor->RedoTransaction();}
void UWeek07EditorLibrary::OpenTools(){FGlobalTabmanager::Get()->TryInvokeTab(ToolTab);}
FString UWeek07EditorLibrary::InspectEffect(UNiagaraSystem* System){
 if(!System)return "No system";
 FString Out=System->GetPathName()+"\n";
 for(const auto& Handle:System->GetEmitterHandles()){
  Out+=FString::Printf(TEXT("Emitter %s Enabled=%d Mode=%d\n"),*Handle.GetName().ToString(),Handle.GetIsEnabled(),int32(Handle.GetEmitterMode()));
  UObject* Emitter=Handle.GetEmitterBase();if(!Emitter)continue;
  for(TFieldIterator<FProperty> It(Emitter->GetClass());It;++It){FString Text;It->ExportTextItem_Direct(Text,It->ContainerPtrToValuePtr<void>(Emitter),nullptr,Emitter,PPF_None);Out+=It->GetName()+"="+Text+"\n";}
 }
 return Out;
}


bool UWeek07EditorLibrary::CaptureTools(const FString& Filename){
 auto Tab=FGlobalTabmanager::Get()->FindExistingLiveTab(ToolTab);
 if(!Tab.IsValid())return false;
 TArray<FColor> Pixels;FIntVector Size;
 if(!FSlateApplication::Get().TakeScreenshot(Tab->GetContent(),Pixels,Size))return false;
 TArray<uint8> Png;FImageUtils::CompressImageArray(Size.X,Size.Y,Pixels,Png);
 return FFileHelper::SaveArrayToFile(Png,*Filename);
}

bool UWeek07EditorLibrary::CaptureEditor(const FString& Filename){
 auto Window=FSlateApplication::Get().GetActiveTopLevelWindow();
 if(!Window.IsValid())return false;
 TArray<FColor> Pixels;FIntVector Size;
 if(!FSlateApplication::Get().TakeScreenshot(Window.ToSharedRef(),Pixels,Size))return false;
 TArray<uint8> Png;FImageUtils::CompressImageArray(Size.X,Size.Y,Pixels,Png);
 return FFileHelper::SaveArrayToFile(Png,*Filename);
}
