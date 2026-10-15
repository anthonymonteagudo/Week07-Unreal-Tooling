from pathlib import Path
root=Path('Week07UnrealPython')
p=root/'Content/Python/week07_tooling/ui/assistants.py'
s=p.read_text(encoding='utf-8')
changes={
"'PRACTICE MODE · sample data only · no connection to Unreal'":"'PRACTICE MODE · sample data'",
"'1  Choose inputs    →    2  Preview    →    3  Apply    →    4  Check result'":"'Choose inputs    →    Preview    →    Apply    →    Check'",
"self.material_help = self.label(text + '\\nTexture suffixes: _BaseColor, _Normal, _ORM. ORM = occlusion, roughness, metallic.')":"self.material_help = self.label(text)\n        self.material_help.setToolTip('Texture suffixes: _BaseColor, _Normal, _ORM. ORM = occlusion, roughness, metallic.')",
"self.vfx_help = self.label(text + '\\nOne effect per marker, using its position and rotation.')":"self.vfx_help = self.label(text)\n        self.vfx_help.setToolTip('One effect per marker, using its position and rotation.')",
"'I reviewed the density warning and the number of effects to place.'":"'I reviewed the density warning'",
"'&Preview changes'":"'&Preview'",
"'&Apply reviewed changes'":"'&Apply'",
"'Apply reviewed changes'":"'Apply'",
"'No pending preview. Changing inputs does not undo earlier applied changes.'":"'Input editing does not undo applied changes.'",
"'1  CHOOSE INPUTS    →    2  Preview    →    3  Apply    →    4  Check result'":"'CHOOSE INPUTS    →    Preview    →    Apply    →    Check'",
"'Assigns component overrides; shared mesh assets stay unchanged. Changes are not saved automatically.'":"'Selected components only. Save changes yourself.'",
"'Placement checks limit counts and spacing. They do not measure runtime performance.'":"'Placement limits are not a performance test.'",
"'Ready to preview — choose inputs, then select Preview changes.'":"'Choose inputs, then Preview.'",
"'Instructor setup needed — no prepared choice is available. Ask your instructor to configure this tool.'":"'No preset available. Ask your instructor.'",
"'1  Choose inputs    →    2  REVIEW PREVIEW    →    3  Apply    →    4  Check result'":"'Choose inputs    →    REVIEW PREVIEW    →    Apply    →    Check'",
"'Ready to apply — ' + presentation['next']":"'Review the changes, then Apply.'",
"'1  CHECK INPUTS    →    2  Preview    →    3  Apply    →    4  Check result'":"'CHECK INPUTS    →    Preview    →    Apply    →    Check'",
"'This preview made no changes. Resolve the issue, then preview again.'":"'No changes made. Fix the input, then Preview.'",
"'1  Choose inputs    →    2  Preview    →    3  Applied    →    4  CHECK RESULT'":"'Choose inputs    →    Preview    →    Applied    →    CHECK RESULT'",
"self.message('Completed — ' + result, 'success')":"self.message('Completed. Check the result in Unreal.' if self.session.backend.is_live else 'Completed in sample data.', 'success')\n            self.status.setToolTip(result)",
"'Inspect the target and protected object. Assignment Undo leaves the new instance asset.'":"'Undo restores the assignment; the new asset remains.'",
"'Inspect the placed effects. Undo removes this batch; the map is not saved automatically.'":"'Undo removes this batch. Save changes yourself.'",
"'Practice result recorded. Preview again to test duplicate protection, or reset practice data.'":"'Preview again to test duplicates, or reset sample data.'",
"'1  Choose inputs    →    2  Preview    →    3  APPLY STOPPED    →    4  Check result'":"'Choose inputs    →    Preview    →    APPLY STOPPED    →    Check'",
"'Review the message before retrying. Create a new preview; do not repeat Apply blindly.'":"'Resolve the issue, then create a new preview.'",
"'Practice reset — sample assignments and placements restored. You can repeat either task.'":"'Sample data reset. Choose either task.'",
}
for old,new in changes.items():
    assert old in s,old
    s=s.replace(old,new)
s=s.replace('self.status.setText(text)','self.status.setText(text)\n        self.status.setToolTip(text)')
p.write_text(s.replace(' — ', ': '),encoding='utf-8')
p=root/'Content/Python/week07_tooling/workflow_presentation.py'
s=p.read_text(encoding='utf-8').replace("'—'","'N/A'").replace('ORM texture (occlusion / roughness / metallic)','ORM texture').replace('Apply: create 1 instance','Apply: create instance').replace('loaded components after placement','total components')
s += '\n\ndef display_cell(value):\n    """Compact asset labels; full paths remain available in tooltips."""\n    text = str(value)\n    if text.startswith(("/Game/", "/Engine/", "sample://")) and "\\n" not in text:\n        return text.rsplit("/", 1)[-1].split(".")[0]\n    return text\n'
p.write_text(s,encoding='utf-8')
p=root/'Content/Python/week07_tooling/ui/assistant_views.py'
s=p.read_text(encoding='utf-8').replace('from week07_tooling.ui.views import table, fill','from week07_tooling.ui.views import table, fill\nfrom week07_tooling.workflow_presentation import display_cell')
s=s.replace('Item or target','Item').replace('Applied change','Result')
s=s.replace("fill(self.widget, presentation['rows'])","fill(self.widget, presentation['rows'])\n        for row in range(self.widget.rowCount()):\n            for col in range(3):\n                cell = self.widget.item(row, col)\n                cell.setText(display_cell(cell.text()))\n        self.widget.resizeRowsToContents()")
p.write_text(s,encoding='utf-8')
p=root/'Content/Python/week07_tooling/editor/native_panel.py'
s=p.read_text(encoding='utf-8').replace('Connected to Unreal. Choose inputs, then preview.','Choose inputs, then Preview.').replace('Ready to apply. Review the targets and proposed result.','Review the changes, then Apply.')
p.write_text(s,encoding='utf-8')
# All authored project Python UI copy uses punctuation instead of em dashes.
for p in (root/'Content/Python/week07_tooling').rglob('*.py'):
    s=p.read_text(encoding='utf-8')
    if '—' in s:p.write_text(s.replace(' — ', ': ').replace('—','N/A'),encoding='utf-8')
# Tests continue to assert complete identity in tooltips after label compaction.
p=root/'Tests/test_assistant_stages.py';s=p.read_text(encoding='utf-8').replace(".item(r, c).text()", ".item(r, c).toolTip()").replace('Applied change','Result').replace('create 1 instance','create instance').replace('Apply reviewed changes','Apply');p.write_text(s,encoding='utf-8')
p=root/'Tests/test_ui_widgets.py';s=p.read_text(encoding='utf-8').replace('Applied change','Result');p.write_text(s,encoding='utf-8')
# Native UI: same state labels, shorter prompts, full asset paths in hover help.
p=root/'Plugins/Week07Tools/Source/Week07Tools/Private/Week07Tools.cpp'
s=p.read_text(encoding='utf-8').replace('#include "Editor.h"','#include "Editor.h"\n#include "Framework/Application/SlateApplication.h"\n#include "ImageUtils.h"\n#include "Misc/FileHelper.h"\n#include "Misc/Paths.h"')
s=s.replace('return SNew(STextBlock).Text(FText::FromString(Value))','FString Display=Value;if(Value.StartsWith("/Game/")||Value.StartsWith("/Engine/"))Display=FPaths::GetBaseFilename(Value);\n  return SNew(STextBlock).Text(FText::FromString(Display))')
s=s.replace('ApplyLabel="Apply reviewed changes"','ApplyLabel="Apply"').replace('bool CanApply=false,NeedsAck=false,Ack=false','bool CanApply=false,NeedsAck=false,Ack=false,Applied=false')
s=s.replace('void Clear(){CanApply=false;', 'void Clear(){Applied=false;CanApply=false;')
s=s.replace('Summary="Inputs changed. Preview again."','Summary="Input editing does not undo applied changes.";Status="Choose inputs, then Preview."')
s=s.replace('auto Result=Send(Action);if(!Result)return FReply::Handled();','auto Result=Send(Action);if(!Result)return FReply::Handled();\n  Applied=false;')
s=s.replace('if(Action=="apply"&&!CanApply)ApplyLabel="Preview before next Apply";', '''if(Action=="apply"){
   ApplyLabel="Apply";bool Ok=false;Result->TryGetBoolField("ok",Ok);Applied=Ok;
   if(Ok){Status="Completed. Check the result in Unreal.";Summary=Kind=="material"?"Undo restores the assignment; the new asset remains.":"Undo removes this batch. Save changes yourself.";}
   else{Rows.Empty();Summary="Resolve the issue, then create a new preview.";}
  }''')
s=s.replace('UNREAL EDITOR  |  Real assets and Actors  |  Changes are not saved automatically','UNREAL EDITOR  |  Current selection')
s=s.replace('Material Setup - prepared classroom surface','Material Setup').replace('VFX Placement - reviewed classroom fountain','VFX Placement')
s=s.replace('Item or target','Item').replace('.DefaultLabel(FText::FromString("Proposed / applied result"))','.DefaultLabel_Lambda([this](){return FText::FromString(Applied?"Result":"After Apply");})')
s=s.replace('Preview changes','Preview').replace('Choose inputs | Preview | Apply | Check in the editor. Assignment Undo and new-asset cleanup are separate.','Choose inputs  >  Preview  >  Apply  >  Check')
s += '''\nbool UWeek07EditorLibrary::CaptureTools(const FString& Filename){
 auto Tab=FGlobalTabmanager::Get()->FindExistingLiveTab(ToolTab);
 if(!Tab.IsValid())return false;
 TArray<FColor> Pixels;FIntVector Size;
 if(!FSlateApplication::Get().TakeScreenshot(Tab->GetContent(),Pixels,Size))return false;
 TArray<uint8> Png;FImageUtils::CompressImageArray(Size.X,Size.Y,Pixels,Png);
 return FFileHelper::SaveArrayToFile(Png,*Filename);
}\n'''
p.write_text(s,encoding='utf-8')
p=root/'Plugins/Week07Tools/Source/Week07Tools/Public/Week07EditorLibrary.h';s=p.read_text(encoding='utf-8').replace('static void OpenTools();','static void OpenTools();\n UFUNCTION(BlueprintCallable,Category="Week07") static bool CaptureTools(const FString& Filename);');p.write_text(s,encoding='utf-8')
print('UI copy, labels, compact asset paths, and cursor-free native capture updated.')
