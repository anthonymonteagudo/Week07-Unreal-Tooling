# Two interfaces, one Python tool

> Current classroom route, 13 October 2026: Material/VFX workflows were rehearsed in Unreal 5.7.4 with both live PySide and the native C++ Slate tab in `Plugins/Week07Tools`. Prepared assets and `W07_MaterialVFXLab` now exist. Use the [live run sheet and actual capture fallback](../../../Course/Slides/Week07/FinalClass20261013/live-demo.html). Pending statements below describe the earlier plan, not current Material/VFX readiness. The separate Maya bridge is outside this rehearsal.


The existing interface is **PySide6 Qt Widgets** (`QWidget`, `QTableWidget`, etc.).
The dark appearance comes from a Qt stylesheet. It is not HTML, a browser, WebView,
or Electron. Preserve it as the Python/PySide teaching tool.

The instructor also requires an **Unreal-native editor interface**. An external
Qt window parented to Unreal is still a Qt window; it does not satisfy the native
dockable-tab requirement. The two interfaces should share operations and behavior,
not try to embed the Qt widgets into Slate.

## Recommendation for this class

Build **an Editor Utility Widget (EUW)** for the Unreal-facing version, using
UMG/Blueprint for presentation and the existing Python controller/backend for tool
operations. This keeps Python central while adding a real Level Editor tab. Epic's
5.7 documentation describes EUWs as editor tabs dockable with Level Editor tabs;
EUW remains a Beta feature. This is the recommended first native implementation,
not a claim that it has every capability of a C++ Slate plugin.

| Option | Strength | Cost / boundary | Role here |
| --- | --- | --- | --- |
| PySide6 Qt Widgets | Python-authored UI, portable patterns across DCC tools, easy offline tests | External window; parenting is not native docking | Keep the implemented staged PySide tool. |
| Editor Utility Widget | Native editor tab, visual layout authoring, Blueprint events call Python | Editor asset must be created and wired; UMG controls need deliberate editor styling | Recommended Week 7 Unreal-facing tool. |
| C++ Slate editor plugin | Direct editor framework, `SDockTab`, detailed styling and integration | C++ module/build/reload lifecycle expands teaching scope | Advanced extension if the class needs deeper editor-framework work. |
| ToolMenus | Discoverability from editor menus/toolbars | Launch surface, not a panel UI framework | Add a launcher after the native widget is working. |

Epic's Slate quickstart uses the **Editor Standalone Window** plugin template and
a C++ `SDockTab`. That is the direct editor-window system the instructor referred
to. For the current Python-focused lecture, EUW is a smaller first integration.
Use normal editor spacing, restrained emphasis, meaningful labels, keyboard focus,
and visible scope; native docking alone does not guarantee good UX.

## Shared architecture

```text
PySide widgets ──────────────────┐
                               ├─ ToolController ─ UnrealBackend ─ demo/rules
EUW Blueprint ─ native_bridge ──┘

Offline PySide/tests ─ ToolController ─ OfflineBackend ─ same pure rules
```

`Content/Python/week07_tooling/editor/native_bridge.py` is now prepared and tested
offline. It imports no Qt. Each widget owns its own opaque session ID; the reviewed
plan stays in Python. Dispatch is restricted to known actions. Stale/expired
sessions cannot apply changes. Reload clears sessions and requires reconnection.
The controller currently lives under `ui/` but has no Qt dependency.

**Status:** PySide implemented; native Python bridge prepared; EUW `.uasset`,
Blueprint wiring, native menu entry and native captures **not created yet**.
No editor was launched or manipulated to do this investigation. Creating/wiring
and validating the EUW is the next in-engine work, outside the current code-only
session. No project plugin/build settings were changed.

## Native assembly specification for a later editor session

Proposed asset: `/Game/Week07/Tools/EUW_PropInspector` (not present yet).
Create via Editor Utilities → Editor Utility Widget. Keep domain logic in Python;
use Blueprint only for widget state, UI events and presentation.

First native stage: a Vertical Box with scope/status Text Blocks, a Select/Refresh/
Validate button row, separately labeled scrollable read-only preview and validation
text, and Preview/Apply actions. Apply starts disabled. Add a reconnect action.
This first stage can use the bridge's text outputs; a later stage should replace
them with real row widgets/structured data for comparison, rather than rely on
space-padded text as a fake table. Reset is separate and needs explicit confirmation.

Use **Execute Python Script**, with typed input/output pins, not string-built Python
commands. Epic recommends this node over Python-generated Blueprint function
libraries, whose transient types have asset save/load problems.

On widget Construct, create an output pin `session_id` of type String:

```python
from week07_tooling.editor import native_bridge
session_id = native_bridge.open_session()
```

Store the returned String on the widget, then invoke Refresh. Reconnect first
closes the old session, opens a new one, clears displays, and disables Apply.

For each action node, input pins are `session_id` (String), `action` (String from
a fixed button mapping), `reset_confirmed` (Boolean, false except confirmed Reset).
Output pins match the variables assigned below:

```python
from week07_tooling.editor import native_bridge
view = native_bridge.dispatch(session_id, action, reset_confirmed)
operation_ok = view['ok']                 # Boolean
session_valid = view['session_valid']     # Boolean
status_text = view['status_text']         # String
tone = view['tone']                       # String
can_apply = view['can_apply']             # Boolean
change_count = view['change_count']       # Integer
selection_count = view['selection_count'] # Integer
world_text = view['world_text']           # String
preview_text = view['preview_text']       # String
validation_text = view['validation_text'] # String
report_json = view['report_json']         # String, for copy/export later
```

Map actions: `select_demo`, `refresh`, `validate`, `preview`, `apply`, `reset`.
After each call, update displays and Apply enabled state. The node's **Success?**
means script execution succeeded; `operation_ok` separately reports whether the
tool action succeeded. Handle either failure inline; clear preview and disable
Apply if the node itself fails. An expired session must offer Reconnect, not retry
Apply automatically. Poll Refresh at a modest interval while active (e.g. 0.75 s),
not on every frame; stop the timer on widget Destruct. Refresh never mutates scene
data. Apply also rechecks immediately, so polling is not the safety boundary.

On Destruct, pass the stored String into:

```python
from week07_tooling.editor import native_bridge
native_bridge.close_session(session_id)
```

Reconstruction may run Construct again: close any existing session before replacing
its ID. Keep a separate session for each tab instance. The native bridge requires
no PySide dependencies. Do not call `show_pyside_ui()` from the EUW button graph.

## Native progression and acceptance gates

1. **Connected tab:** actual EUW, explicit mode/scope/status, buttons call Python,
   empty/stale/error states work. Test closing/reopening and session cleanup.
2. **Reviewable workflow:** native before/after rows, selected scope vs whole fixture
   validation, Apply count, no-op handling, preserved focus and useful empty states.
3. **Integrated editor tool:** menu discoverability, docking/reopening, Undo feedback,
   reset recovery, keyboard/DPI review and consistent editor visual treatment.

Retain the PySide functional/guided/refined examples. Explain why a portable DCC
window and a host-native tab have different presentation code while sharing rules.
Do not substitute the PySide screenshots for native Unreal captures. Native quality
gates remain pending until a real widget runs in the editor.

## Sources checked

- [Epic: Editor Utility Widgets, UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/editor-utility-widgets-in-unreal-engine?application_version=5.7)
  — UMG-based editor tabs and Level Editor docking.
- [Epic: Python scripting, UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python?application_version=5.7)
  — editor-only Blueprint Python nodes, typed custom pins, and the recommended bridge.
- [Epic: Slate editor-window quickstart](https://dev.epicgames.com/documentation/en-us/unreal-engine/slate-editor-window-quickstart-guide-for-unreal-engine)
  — C++ Standalone Window plugin and SDockTab. The current page resolves to 5.8;
  it is an architectural reference, not evidence of a compiled 5.7 implementation.
- Project-generated UE 5.7 stub: `EditorUtilitySubsystem.spawn_and_register_tab`
  and related tab APIs are exposed locally. The stub was inspected, never imported.
