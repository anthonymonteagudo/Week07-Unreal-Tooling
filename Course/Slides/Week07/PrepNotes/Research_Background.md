# Week 7 Unreal Python preparation notes

**Latest additions:** [Maya → Unreal bridge, alternative demos, and UI/UX lesson](Bridge_and_UX.html) · [Printable two-page tool-testing lab sheet](Tool_UX_Lab_Sheet.html). The tutorial index now includes further free supplements, the completed playlist, the Spanish UE5.7 resource (language reported by the instructor), and TutorialSearch as an unverified discovery lead.

**Start with the [categorized Unreal tutorial index](Unreal_Tutorial_Index.html):** individual Week 7 Oster videos, optional UI/validation, future PCG and other Unreal topics, and free Unreal-specific supplements. The Oster introduction and the instructor-confirmed YouTube automation playlist are marked already completed; future-topic entries are saved references. Updated 10 October 2026: Unreal is required for new tooling recommendations; Maya-only courses are excluded. The older provider survey below remains research history, not a recommendation to study Maya.

<h2 id="weekend-course-shortlist">Weekend course shortlist and texture/material direction</h2>

**Instructor-confirmed preferences · 10 October 2026:** Seek short, self-paced, approximately **4–10 hour crash courses** in Unreal Python tooling and automation. Udemy-style structure is welcome, but the platform need not be Udemy. Quality and efficient learning matter more than the lowest price. Prof. Monteagudo enjoys the SimonDev shader course and wants a similarly satisfying learning experience for Unreal Python; this is a preference reference, not a claim of equivalence between courses.

The Epic Python documentation, Isaac Oster's introductory course, and the YouTube automation playlist linked below have already been studied and documented here. Do not recommend them again as new weekend material. The Japanese-language Unreal Fest Tokyo talk is not a practical viewing choice for this preparation.

### Saved shortlist

Only the first item's priority is instructor-ranked; the remaining order is organizational. These are candidates, not records of purchase or completion. Durations and update dates below come from the public listings reviewed in this conversation; prices were not verified.

| Candidate | Format and scope | Reason to retain |
| --- | --- | --- |
| **Top of the list: [Unreal Engine 5 Python Automation — Karol Kowalczyk](https://www.udemy.com/course/unreal-engine-5-python-automation/)** | Paid; 8h 39m; updated January 2026. | Broad Python automation course; especially relevant lessons include texture compression settings, material-instance parameters, batch texture import, validation, and undo. |
| [Python for Unreal Engine Editor Tools Scripting — Muhammad A. Moniem](https://www.udemy.com/course/ue4python/) | Paid; 4h 8m; updated June 2022. | Compact alternative, including material-instance creation and editor tools. Allow for adapting older examples to UE5.7. |
| [Building a Texture Utility with the Unreal Python API — Isaac Oster](https://isaacoster.artstation.com/projects/qeAwqe) | Free; three-part project series, not a 4–10 hour course. | Directly relevant: gather materials and textures, evaluate properties, and modify texture settings. |
| [Becoming an Unreal Automation Expert — Tim Großmann, Andreas Hauber, Jonas Roth](https://www.udemy.com/course/becoming-an-unreal-automation-expert/) | Paid; 4h 42m; updated May 2020. | Compare Python, Blueprint, and C++ approaches to common automation tasks. Older UE4 material requires adaptation. |
| [PyQt for Maya and Unreal — Isaac Oster](https://dev.epicgames.com/community/learning/tutorials/aVyX/unreal-engine-pyqt-for-maya-and-unreal) | Free; nine-part series, published 2023 and tagged UE5.2; total duration not verified. | Artist-facing interfaces, Qt Designer, file dialogs, and reusable UI patterns across Maya and Unreal. Optional interface depth after the core tool works. |

Karol's Blueprint Automation course is interesting but outside the desired direction here. Vertex School's longer program is outside the requested crash-course format. C++ editor extension remains a possible later interest, not the immediate preparation priority.

### Demonstration options

**Instructor clarification:** textures/materials were a suggestion connecting to the following three-week rendering/shader/material block, not a fixed demo requirement. Explore alternatives. The requested opening is a clean Maya → Unreal handoff; UI/UX thinking and a tangible peer-testing sheet are also preparation priorities. See the [bridge and UX guide](Bridge_and_UX.html) and [student lab sheet](Tool_UX_Lab_Sheet.html). These are proposals; no replacement Unreal demo has been implemented.

**Proposed project, not yet an approved lesson specification:** a texture-set-to-material-instance tool. Start with one named texture set and a prepared parameterized master material; inspect the inputs, preview the proposed texture settings and parameter assignments, create or update one material instance, apply it to a demonstration mesh, and verify the visual result. Add import/reimport, missing-map reporting, repeat-run behavior, and a small UI only as scope allows. Establish project-specific texture-role rules rather than assuming every texture requires the same settings. Rehearse recovery separately for property edits and imported/created assets.

### Additional focused series discovered for this direction

These are supplemental recommendations, separate from the five instructor-selected candidates; neither is represented as a full crash course.

- [Asset Setup with the Unreal Python API — Isaac Oster](https://isaacoster.artstation.com/projects/xDB8zR): three parts covering organization of imported textures and geometry, creation of a material instance, parent/texture parameter assignment, and assignment to the static mesh; code linked by the author. Especially close to the proposed demo.
- [Asset Import / Export using Unreal Python API — Isaac Oster](https://isaacoster.artstation.com/projects/Dvdrke): two parts on importing and exporting assets, with linked code. A possible companion to the setup series.

<h2 id="expanded-source-library">Expanded UE Python source library</h2>

**Research update · 10 October 2026.** Requested by the instructor: gather Oster's relevant UE/Python work, additional Karol material, related SimonDev/Ben Cloward resources, and alternatives to Udemy. This is a curated inventory of publicly discoverable resources, not a claim that every upload has been located or every video watched. Course descriptions establish scope; they do not establish hands-on verification in UE5.7. Short projects, reference articles, full courses, and adjacent shader material are labeled separately. Existing source snapshots remain historical records.

### Isaac Oster: collected UE/Python series

The [author's portfolio](https://isaacoster.artstation.com/) identifies the following six directly relevant collections. Keep the completed introduction as a reference, then prioritize texture inspection, import/export, and asset setup. None of the short-series counts below establishes a 4–10 hour runtime.

| Collection | Type | Use for this preparation |
| --- | --- | --- |
| [An Introduction to the Unreal Python API / Utilizing Python for Editor Scripting](https://isaacoster.artstation.com/projects/G8ZDYa) | Full introductory course; already studied. | Foundation and existing Northwood provenance; do not count the ArtStation and Epic links as different courses. |
| [Building a Texture Utility](https://isaacoster.artstation.com/projects/qeAwqe) | Three-part project series. [Epic code/tutorial](https://dev.epicgames.com/community/learning/tutorials/wZEz/unreal-engine-building-a-texture-utility-with-the-unreal-python-api). | Gather materials, find textures, inspect/change properties. Highest immediate relevance alongside Asset Setup. |
| [Asset Import / Export](https://isaacoster.artstation.com/projects/Dvdrke) | Two-part project series. [Epic code/tutorial](https://dev.epicgames.com/community/learning/tutorials/LnE7/unreal-engine-asset-import-export-using-unreal-python-api). | Import/export workflow supporting a material-preparation pipeline. |
| [Asset Setup](https://isaacoster.artstation.com/projects/xDB8zR) | Three-part project series. [Epic code/tutorial](https://dev.epicgames.com/community/learning/tutorials/xrnE/unreal-engine-asset-setup-with-the-unreal-python-api). | Organize imported assets, create a material instance, assign its parent/textures, apply it to a mesh. Closest direct project match. |
| [Enable Nanite with Python](https://isaacoster.artstation.com/projects/el0XE3) | Two-part project series. [Epic code/tutorial](https://dev.epicgames.com/community/learning/tutorials/4x7v/unreal-engine-enable-nanite-with-python). | Example of checking material eligibility before editing mesh assets. The author's description explicitly discusses UE5.1 restrictions: recheck those rules against the teaching engine instead of repeating them as current universal rules. |
| [PyQt for Maya and Unreal](https://dev.epicgames.com/community/learning/tutorials/aVyX/unreal-engine-pyqt-for-maya-and-unreal) | Nine-part UI series. | Interface construction, host integration, dialogs, subwidgets, and styling. Optional later depth; Qt setup is not necessary for the core Week 7 demo. |

### Karol Kowalczyk / Tech Art Corner

The [Python Automation course](https://www.udemy.com/course/unreal-engine-5-python-automation/) remains the instructor's first choice. For the texture/material direction, select these listed lessons: **Texture Compression Settings Validator**, **PropertyAccessChangeNotifyMode**, **Editing Material Instance Parameters**, **Batch Import Textures**, **Undo and Redo**, and **Python Scripts in Asset Scripted Action Blueprints**. ImportSubsystem/post-import callbacks and packaging can follow. These are course sections, not separate new courses.

Additional author material, mostly short articles with some accompanying videos:

| Resource | Why retain it | Priority |
| --- | --- | --- |
| [Getting Started With Python in Unreal Engine 5](https://medium.com/@TechArtCorner/getting-started-with-python-in-unreal-engine-5-15a2ae765d86) | Author's setup overview and pointers to IDE configuration. | Reference; overlaps completed preparation. |
| [Filtering asset and actor lists with EditorFilterLibrary](https://medium.com/@TechArtCorner/filtering-asset-and-actor-lists-with-unreal-editorfilterlibrary-python-59ac8234b395) | Scope by class/name/tag/selection; useful for selecting eligible textures. | High. |
| [Adding Python Scripts to Unreal Engine Interface](https://medium.com/@TechArtCorner/executing-python-scripts-from-unreal-engine-5-menus-90b917981020) | Menu entry as a simple way for artists to invoke a tool. | High after the underlying script works. |
| [Python Remote Debugging with PyCharm](https://medium.com/@TechArtCorner/python-remote-debugging-debug-external-applications-with-pycharm-1da72a88fde0) | Debug code hosted in external applications, including Unreal. | Instructor troubleshooting; published January 2026. |
| [I don't do pip install in Unreal Engine](https://medium.com/@TechArtCorner/i-dont-do-pip-install-in-unreal-engine-f78ce635415d) | Dependency-management reading. | Later, especially if pursuing external UI packages; not a prerequisite. |
| [All the ways you can set Metadata Tags in Unreal Engine](https://medium.com/@TechArtCorner/all-the-ways-you-can-set-metadata-tags-in-unreal-engine-38793d08dcc0) | Metadata as an explicit tool input or classification aid. | Optional pipeline depth. |
| [Using Details View in Editor Utility Widgets](https://medium.com/@TechArtCorner/using-details-view-widget-in-editor-utility-widgets-in-unreal-engine-37af4a6b48a3) | Expose properties through an editor tool. | Adjacent Blueprint UI reference. |
| [Single Property View: selectors and pickers](https://medium.com/@TechArtCorner/selectors-and-pickers-with-dragn-drop-support-in-ue-a-single-property-view-in-unreal-engine-5511ab679b2a) | Artist-facing inputs without designing every property control. | Adjacent Blueprint UI reference. |
| [Remote Control tutorial](https://youtu.be/UzMgV_964lA) | Web-based control of scene properties; linked by Karol in his public post. | Later; already represented in A3 notes. |

Medium availability may vary by article/account. The existing [A1](sources/intro-a1.html), [A2](sources/intro-a2.html), [A3](sources/intro-a3.html), and [A4](sources/intro-a4.html) notes retain menu, debugging, remote-control, and batch-import video bookmarks; avoid counting these study references as newly completed material. The public playlist and paid course may overlap; no complete lesson-by-lesson equivalence was verified. His [Blueprint Automation course](https://www.udemy.com/course/unreal-engine-blueprint-automation/) remains adjacent material, outside the present Python-first study direction.

### SimonDev, Ben Cloward, and other providers

| Source | What was found | Recommendation for this goal |
| --- | --- | --- |
| [SimonDev](https://simondev.io/) | Public catalog lists GameDev, Shader, and Math courses. No dedicated UE Python automation course was located. | Retain as the instructor's preferred learning-experience reference and shader background. Do not represent the shader course as Unreal Python training. |
| [Ben Cloward's resources](https://www.bencloward.com/resources.shtml) | Author links his Unreal/Unity material tutorials and HLSL training. No dedicated UE Python course was located. | Useful for understanding the materials and parameters the automation edits. Select a specific material topic when the demo's master material is decided. |
| [Tuatara: Getting started with Python in Unreal Engine](https://dev.epicgames.com/community/learning/tutorials/K8Pe/getting-started-with-python-in-unreal-engine) · [project repository](https://github.com/Tuatara-VFX/getting-started-python-ue) | Free tutorial resource with code; already bookmarked in the existing notes. | An alternative explanation and code reference; not a new discovery or established advanced crash course. |
| [Alex Quevillon: UnrealPythonLibrary](https://github.com/AlexQuevillon/UnrealPythonLibrary) · [Python in UE4 series](https://www.youtube.com/playlist?list=PLBLmKCAjA25Br8cOVzUroqi_Nwipg-IdP) | Older pipeline-oriented examples and videos. | Useful supplementary recipes, with UE4-to-UE5 adaptation expected. Not first choice for minimum-friction preparation. |
| [Inside Unreal: Simplifying Tool Creation with Blueprints & Python](https://forums.unrealengine.com/t/inside-unreal-simplifying-tool-creation-with-blueprints-python/629768) | Epic's English-language 2022 session with Krzysztof Pachulski; linked examples and code. Already in the note library. | Especially relevant to a brief Python-to-editor-UI bridge; a session, not a 4–10 hour course. |
| [CGMA catalog](https://www.cgmasteracademy.com/showcase/compositing-lighting) · [CGMA's Python course preview](https://www.youtube.com/watch?v=5_PM63_oFH0) | Located Python for VFX and Animation in Maya and multiweek Unreal introductions. The catalog has inconsistent legacy durations, and the old direct Python course URL returned 404. | No verified short UE Python course or current enrollment offering matching this request. Do not recommend a purchase from stale listing details. |
| [Gnomon Workshop: Master Rigging & Python Scripting in Maya](https://www.thegnomonworkshop.com/workshops/master-rigging-python-scripting-in-maya) | 5h 20m, ten lessons: the desired workshop format, but Maya rigging subject matter. | Format match, topic mismatch. No direct UE texture/material Python course located in this search. |
| [fxphd catalog](https://www.fxphd.com/courses/) | Indexed catalog includes Unreal courses and Python courses for other DCCs. A subsequent live page fetch was blocked (403). | No dedicated matching UE Python crash course verified; not a reason to subscribe for this task. |
| ArtStation / Gumroad search | Oster's project series were directly relevant; other discovered courses were largely environment/asset creation or supplied Python utilities. | Using a supplied Python script is not equivalent to teaching Unreal Python tool development. No stronger matching paid course verified. |

This search supports **Karol for structured course progression plus Oster for concrete texture/material projects**. It does not establish that no other course exists. Recommendations remain based on public curricula and the instructor's stated fit, not a full independent viewing of paid content.

<h2 id="blueprints-week7-scope">Should Week 7 include Blueprints?</h2>

**Advisory recommendation, not an instructor-approved agenda change:** keep Python texture/material automation as the lesson's core. Do not start a second substantial Blueprint authoring lesson. A tightly bounded **3–5 minute editor-UI connection** can still be useful if already rehearsed and time permits.

The linked [Unreal 5 Blueprint Tools for Artists, by Thomas Harle](https://www.udemy.com/course/unreal-5-blueprint-tools-for-artists/) is a **7h 2m** course, listed as updated October 2024. Its curriculum includes material/Blueprint inheritance, exposed parameters, a configurable light prefab, procedural book piles, splines, and runtime events. It is a worthwhile adjacent artist-tool direction, but largely a different lesson objective from batch importing textures and producing persistent material-instance assets with Python. Reserve substantial work from it for another session. Its material-inheritance and exposed-parameter lessons can inform instructor preparation without becoming new Week 7 exercises.

| Meaning of "Blueprints" | Week 7 treatment |
| --- | --- |
| Actor Blueprints, construction scripts, procedural generators, and runtime interactions like Harle's projects | Defer substantial instruction. These introduce a second execution model and workflow alongside the first Unreal Python session. |
| Editor Utility Widget or Scripted Action calling the existing Python function | Optional prepared demonstration only: show an input, a button, the same Python operation, and the resulting material. Explain UI versus processing. |
| Material graph and material-instance parameters | Necessary visual context for this demo. The Material Editor's graph is not a Blueprint Event Graph. Show the existing parent and named texture parameters; avoid turning the class into master-material construction. |

For the existing short UI/UX block, compare running the same tool from a console and from an editor button, then ask which input/feedback/recovery the artist needs. Skip this bridge if Python setup or the core material workflow consumes the time; it is not a prerequisite for the student activity. Do not add Qt, Slate/C++, or a UI-building lab on top.

Technical boundary: [Epic's Python documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python?application_version=5.7) places Python execution nodes in editor-only Blueprint classes such as Editor Utility Widgets and Editor Utility Blueprints. Do not imply that an ordinary gameplay Actor Blueprint can call editor Python at runtime. This recommendation follows the current proposed agenda's limited demo/lab time and substantial peer-review commitment; reconsider it if those priorities change.

<h2 id="northwood-project-provenance">Northwood project provenance</h2>

**Instructor-confirmed context · 10 October 2026:** Prof. Monteagudo confirmed after this source compilation that the original **Northwood** project was the result of working through Isaac Oster’s publicly available online UE Python course, **Utilizing Python for Editor Scripting in Unreal Engine**. The compiled notes document sources he had already reviewed. Northwood therefore provides continuity between that course study and the upcoming Week 7 demonstration.

**Week07UnrealPython** is the subsequent classroom-preparation spinoff. Its six-prop lab, controlled-edit tooling, and new captures were added during Week 7 preparation; they should be attributed separately from the original course-study work. See the [Week 7 Python demo guide](../UnrealPythonDemo/index.html) and [Oster course notes](sources/oster-01.html).

Use Isaac Oster’s lessons as the conceptual sequence for Week 7: find editor data, establish selection scope, inspect types and properties, then explain the effects of a change. Pair that sequence with the **Unreal Engine 5 Python Automation Course** notes in `00 Unreal Python Intro` for import workflows, validation, debugging, and eventual menu integration. The strongest classroom connection is your own Northwood example: Oster L2 records 1,038 asset paths, including `/Game/Northwood/DekogonContent/...`. That count is historical output from your study session, not the current project inventory.

This is instructor preparation for the existing 4:00–6:30 agenda. The teaching sequence below is proposed; it adds no assignment or grading requirements. [Existing agenda and slide review](../AgendaRevision20261010/Preparation_and_Source_Compilation.html) · [Week 7 Python demo and commands](../UnrealPythonDemo/index.html) · [Full source index](source_index.html).

## What to use first

| Preparation need | Read | Use in Week 7 |
| --- | --- | --- |
| Get a script running | [Setup](sources/intro-00.html), [Oster L1](sources/oster-01.html) | Plugins, Output Log, Content/Python, import and reload. |
| Explain what Python can inspect | [Oster L2](sources/oster-02.html), [L3](sources/oster-03.html), [L7](sources/oster-07.html) | Assets, selected Actors, Components, and shared mesh references. |
| Explain a controlled change | [Oster L4](sources/oster-04.html), [L5](sources/oster-05.html), [L8](sources/oster-08.html) | Filter eligible objects, inspect before editing, distinguish asset edits from instance overrides. |
| Show production applications | [Batch import A4](sources/intro-a4.html), [Validation A5](sources/intro-a5.html) | Consistent import settings and explicit rules that yield actionable reports. |
| Connect to peer review | [Artist-facing UX checklist](sources/ux-checklist.html), [FIEA UI UX](sources/fiea-ux.html) | Give the tester a task; observe scope, feedback, errors, and recovery. |

## Isaac Oster lesson guide

The notes identify the course as **Utilizing Python for Editor Scripting in Unreal Engine**. [L1](sources/oster-01.html) and [B1](sources/intro-b1.html) point to the same Epic course; B1 is a duplicate reference, not another course.

| Lesson | What your notes contain | Teaching use and preparation |
| --- | --- | --- |
| L1 API documentation | A script under Content/Python, Hello World, and reload screenshots. | Establish the edit/run/read-output loop. Explain that the editor supplies `unreal`. |
| L2 Using the API | `EditorAssetLibrary.list_assets`, asset paths, logging, and your Northwood output. | Show the scale of a real content library, then narrow to a small fixture. `/Game` is a content path, not a Windows folder. |
| L3 User input | Content Browser selection, all level Actors, and selected level Actors. | Selection is already user input. Selecting a mesh asset and selecting one of its placed Actors answer different questions. |
| L4 Asset class | Asset metadata, class filtering, and loading matching assets. | Explain why eligibility is checked before doing work. Repair the missing function parameter before reuse. |
| L5 Editor properties | Source import filenames, LOD group, number of LODs, and a conditional property edit. | Read a property before discussing a write. A shared StaticMesh asset change may affect many placements; a LOD-group assignment is not universally appropriate. |
| L6 Mesh details | Nested loops over LODs and sections, triangle counts, and relative LOD sizes. | Optional report-building depth. Name the LOD and metric; handle missing LODs and a zero baseline. Mesh complexity alone does not establish frame cost. |
| L7 Actors and Components | Actor → StaticMeshComponent → StaticMesh; repeated-use counts; joining counts to mesh data. | Core data-model lesson. Two Actors can reference one mesh asset. Treat the aggregate as a scoped inventory estimate, not rendered triangles or GPU timing. |
| L8 Discovery and materials | Material inspection, texture parameters, and assigning a test material to component slots. | Inspect first; use `dir`/`help` as discovery aids. The replacement example affects component material assignments, and its loop currently covers the whole level. |
| L9 API and Blueprints | Screenshot-led material/instance setup and a Level Blueprint example. | Optional bridge to editor tools. Do not infer from the title that ordinary runtime Blueprints can execute editor Python. |
| Full Script | Combined fragments from the lessons. | Historical study reference. It contains the same defects and broad edits as the individual notes; it is not a ready demo script. |

**Classroom narration:** “This crate in the level is an Actor. Its mesh Component points to a mesh asset in the Content Browser. Another crate can point to that same asset. Before we change anything, we need to know which of those objects our script is holding.”

## The companion course and related resources

The instructor confirms having worked through and liked the [Unreal Engine 5 Python Automation playlist](https://www.youtube.com/playlist?list=PLKgYiIAqG99cwlb4Y2Pu-cSb_Vw14-t0c), also recorded in [A1 Unreal Engine 5 Python Automation Course](sources/intro-a1.html). A1–A4 share YouTube playlist identifier `PLKgYiIAqG99cwlb4Y2Pu-cSb_Vw14-t0c`; [UE Python Tutorials](sources/tutorials.html) labels that playlist “Series 3.” This identifies the notes by their saved title and links; it does not establish an instructor attribution or current playlist contents.

- **A1 menus:** registers editor menu and StaticMesh context-menu entries with `ToolMenus` and a `ToolMenuEntryScript`. Useful after students understand the underlying action: a menu improves access to a tool; it does not define the tool’s behavior. Leave transient menu enumeration and startup registration as optional depth.
- **A2 debugging:** records an embedded UE 5.7 interpreter path and a working local `debugpy` attachment, including `localhost:5678`. Preserve it as an instructor reference. Its `D:\Personal Projects\...` and engine paths must be adapted; installing a package into a different Python interpreter will not make it available inside Unreal.
- **A3 Remote Control:** screenshot walkthrough of exposing properties, material parameters, and web controls. This is an additional interface/integration topic, not a prerequisite for editor Python.
- **A4 batch import:** enumerates FBXs, constructs import tasks and settings, runs the importer, and reports imported paths. The saved snippet uses `replace_existing=True` and `save=True`; review those choices before demonstration. Rehearse one known FBX and its resulting mesh/materials before scaling up. `glob` covers one directory; `rglob` includes nested directories.
- **A5 validation:** naming, texture dimensions, compression, and polycount checks. Translate each into a stated project rule and a useful failure message. “Square texture” is an example constraint, not a universal requirement. This note is a concept list and screenshots, not a full custom validator implementation.

[UE Python Tutorials](sources/tutorials.html) also records Tuatara’s **Getting started with Python in Unreal Engine** as “Series 1.” That is another plausible related resource, but the local note is a link collection rather than detailed lesson notes. [Courses for Prep](sources/prep-courses.html) separately lists two Udemy automation offerings; do not assume either is the same as the YouTube series.

## Setup for the fifteen minute block

The existing [Week 7 Python demo](../UnrealPythonDemo/index.html) targets UE 5.7. Its project descriptor explicitly enables `PythonScriptPlugin` and `EditorScriptingUtilities`. The demo page records prior testing in 5.7.4; the saved validation report has nine true checks, including empty selection, stale selection rejection, six changes, repeat-apply behavior, and reset. These are existing preparation records, not a new rehearsal performed for this compilation.

1. **First 4 minutes:** Open the intended project. In Edit → Plugins, confirm Python Editor Script Plugin and Editor Scripting Utilities; restart if changed. Use the project’s engine version.
2. **Next 3 minutes:** Open Output Log and switch its input to Python. Run the three lines below. Expected result: a Week 7 message and the actual embedded interpreter path in the log.
3. **Next 5 minutes:** Save a small script in the project’s `Content/Python` folder. Import it, edit its message, reload it, and observe the new output. Explain that a second `import` alone normally reuses the loaded module.
4. **Last 3 minutes:** Demonstrate the difference between Content Browser and level selection. Confirm everyone can identify where the output appears. Use a prepared report if a machine is still restarting.

```python
import unreal
unreal.log("Week 7 Python is running")
print(unreal.get_interpreter_executable_path())
```

For a teaching file named `week7_hello.py` containing `import unreal` and a log statement:

```python
import week7_hello
import importlib
importlib.reload(week7_hello)
```

Epic’s [UE 5.7 setup documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python?application_version=5.7) confirms the per-project plugins, embedded Python, Output Log execution, and automatic Content/Python search path. Python scripting is for editor work; it is not a gameplay scripting environment. Python execution nodes belong to editor-only Blueprint classes such as Editor Utility Widgets. Autocomplete and debugger configuration can follow after the first successful script.

| Symptom | First useful check |
| --- | --- |
| Python mode is unavailable | Correct project, plugin enabled, editor restarted. |
| `import unreal` fails in a terminal | Run the command in Unreal’s Python console; an ordinary terminal Python session is a different host. |
| New module cannot be found | Confirm the real filename ends in `.py`, its directory is the open project’s Content/Python, and inspect `sys.path` if needed. |
| Edits do not appear | Save the file and reload the module; confirm which file is imported with `print(week7_hello.__file__)`. |
| Selection report is empty | Identify which selection API is being used, then select in the corresponding browser or level. |
| A copied API example fails | Match the documentation to the installed engine. The saved API bookmark note links 5.1, 5.0, and 4.27. |

## Fit the notes into the current agenda

During **4:20–4:40**, use Oster L2/L3/L7 to establish the asset–Actor–Component relationship, then L4/L5 for eligibility and properties. Keep the object in the viewport visible while its information appears in the log. Use one shared mesh example instead of a full-project inventory dump.

During **4:40–5:10**, anchor the demonstration in the existing Northwood Inspect → Check → Preview → Apply → Verify → Undo sequence. It turns the broad editing ideas in the study notes into an explicit scope and recovery story. Use A4 and A5 to explain additional production applications; a batch-import demonstration still needs its own rehearsal. The earlier compilation’s “no sample project” wording predates the Northwood preparation.

For the proposed **5:10–5:25 lab**, ask students to predict which objects a selection report will include, run it, and explain one result to a partner. A useful question is: “If these two Actors share a mesh, which changes should affect both, and which should affect only one?” Keep creation of a complete menu or debugger outside this short activity.

For **5:40–5:50 UI/UX**, bring forward the [UX checklist](sources/ux-checklist.html): user, task, pain point, smallest useful prototype, real-user testing, and maintenance. In **5:50–6:30 peer review**, ask testers to attempt a task and report expected versus actual behavior, help needed, and one retestable improvement. These are proposed observation prompts, not a replacement rubric.

**Classroom narration:** “The report tells us what the tool thinks is selected. The preview tells us what it intends to change. After Apply, we check again. A useful tool helps the artist understand each of those steps, including what to do when the input is wrong.”

## Corrections before reusing copied code

Keep the original notes intact. The following are defects or limitations in the saved text, not claims about the original instructors’ code.

| Source | Repair or clarification |
| --- | --- |
| L3 | Print `selectedAsset`, not the full `selectedAssets` list on every iteration. Use the editor’s subsystem accessor pattern, as the current Northwood teaching module does. |
| L4 and Full Script | `getAssetClass()` references an undefined `classType` but callers pass a class argument. Add the parameter and verify the asset-class API against the target engine. |
| L5 | Check the actual representation of an unset LOD group before comparing it with Python `None`; choose a LOD policy for the asset’s intended use. |
| L6 | Remove the extra parenthesis. Calculate the ratio before integer rounding: `100 * lod_triangles / base_triangles`. This is percent remaining; percent reduction is `100 - percent_remaining`. Guard a zero denominator. |
| L6 | LOD index 1 may not exist. The broad exception can leave `LODData` undefined or reuse a previous value. Return an explicit missing-data result. |
| L7 | Correct `appen` to `append` and `aggregateTriCounts - []` to assignment. Guard absent meshes and join by full asset path rather than short name. Exact `StaticMeshActor` filtering does not cover every Blueprint or instancing arrangement. |
| L8 | Guard empty material slots and validate the replacement asset. Do not apply the all-Actors replacement loop to an unprepared level. |
| A1 | The menu fallback branch immediately continues, so a fallback result is skipped. Transient object names are not a stable basis for a beginner tool. |
| A3 | The material override note describes that demonstrated setup; do not generalize it to every Remote Control property. |
| A4 | Replace machine-specific paths; declare replacement/save behavior; check the active importer and outputs in the actual engine build. |
| Udemy A3 Scripting | The refresher has a missing colon after `def multiply(a, b)` and uses `//` in Python examples. Correct those before distributing executable examples. |

## Useful context from the wider prep library

[Udemy A3 Scripting](sources/udemy-scripting.html) gives a compact prerequisite list: data types, conditions/loops, functions, imports, and filesystem work. Use it to diagnose a specific gap, not to restart a general Python course during Week 7.

[Udemy A7 Pipelines](sources/udemy-pipelines.html) connects naming, folder structure, source versus export files, version history, and validation. Its asset-management examples support a concrete motivation: rules should be explicit enough for both an artist and a script to follow. Use the named sections on Python filesystem tasks, naming validation, and automated export paths as optional reading.

The [FIEA UI UX lecture](sources/fiea-ux.html) supplies discovery, requirements, dependencies, and prototypes. The shorter checklist is the better classroom handout basis; the full lecture supports instructor preparation. Its historical examples should not become universal interface rules.

The source index preserves snapshots, original paths, hashes, and available embedded screenshots from the relevant notes. Screenshots are historical study captures and are not evidence of today’s editor state. Video links are retained for navigation; this compilation does not claim a fresh review of the videos or all subjects in the larger notes library.
