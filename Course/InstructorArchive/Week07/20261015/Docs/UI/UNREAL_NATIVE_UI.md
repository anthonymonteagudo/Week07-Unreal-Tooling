# Native Slate and PySide interfaces

The current classroom tool has two presentations over the same Python planner and Unreal backend. **Tools → Material & VFX Tools** opens the native C++ Slate editor tab in `Plugins/Week07Tools`. **`w7.show_assistants()`** opens a separate PySide6 Qt Widgets window. A Qt window parented to Unreal is still a Qt window; it is not native Slate docking.

| Surface | Implementation | Classroom use |
| --- | --- | --- |
| Native Unreal | C++ Slate `SDockTab` and native controls call the Python bridge | Prepared editor-integrated showcase |
| Live PySide | Python Qt Widgets call the shared live backend | Compare portable DCC UI patterns |
| Practice PySide | Same staged UI with sample backend | Repeatable, engine-free interaction exercise |
| Editor Utility Widget | UMG/Blueprint editor interface | An alternative architecture, not this tool’s current implementation |

The [recorded UE 5.7.4 rehearsal](../../../Course/Slides/Week07/FinalClass20261013/live-captures/rehearsal.json) checked native Material/VFX Apply and repeat-placement blocking, plus live PySide workflows. The [capture fallback](../../../Course/Slides/Week07/FinalClass20261013/live-demo.html) contains the actual native and PySide captures. The older [EUW assembly proposal](UNREAL_NATIVE_UI_EUW_PROPOSAL_ARCHIVE.md) is archived.

## Shared behavior

Both live interfaces identify scope, preview before mutation, expire stale plans, require acknowledgment for reviewable warnings, reject hard blockers and consume Apply. Backend validation is the boundary; enabling a button is only feedback. `workflow_presentation.describe_plan()` supplies common labels, counts and rows. `editor/native_bridge.py` owns Qt-free sessions for the native tab.

## Lifecycle and recovery

Reopening or reloading invalidates old sessions and plans. Reconnect or reopen the appropriate interface, then preview again. Do not keep a stale plan while stepping through console examples. Native plugin binaries match the recorded Windows UE 5.7.4 build; another engine build requires a rebuild. Use the current [run sheet and mode boundaries](../DEMO_SEQUENCE.md).

## References

- [Epic Slate editor-window quickstart](https://dev.epicgames.com/documentation/en-us/unreal-engine/slate-editor-window-quickstart-guide-for-unreal-engine)
- [Epic Editor Utility Widgets](https://dev.epicgames.com/documentation/en-us/unreal-engine/editor-utility-widgets-in-unreal-engine?application_version=5.7)
- [Epic editor Python scripting](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python?application_version=5.7)

API reference pages explain the architecture. The project code and dated rehearsal establish what this classroom implementation does.
