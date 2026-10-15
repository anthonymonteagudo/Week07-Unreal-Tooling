#pragma once
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Week07EditorLibrary.generated.h"
class UNiagaraSystem;
UCLASS()
class WEEK07TOOLS_API UWeek07EditorLibrary : public UBlueprintFunctionLibrary {
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintCallable,Category="Week07") static bool UndoDemo();
 UFUNCTION(BlueprintCallable,Category="Week07") static bool RedoDemo();
 UFUNCTION(BlueprintCallable,Category="Week07") static void OpenTools();
 UFUNCTION(BlueprintCallable,Category="Week07") static bool CaptureTools(const FString& Filename);
 UFUNCTION(BlueprintCallable,Category="Week07") static bool CaptureEditor(const FString& Filename);
 UFUNCTION(BlueprintCallable,Category="Week07") static FString InspectEffect(UNiagaraSystem* System);
};
