# Week 7 preparation · start here

**Latest review · runnable API revision v8:** [Slide review and latest PowerPoint](../CheckpointDeck20261013/index.html) · [17 runnable checkpoints with copy buttons](../CheckpointDeck20261013/checkpoints.html) · [Current teaching route](../CheckpointDeck20261013/teach.html). Slide code is extracted from the runnable files. Setup, expected results and recovery are explicit. This supersedes v7 below and retains the 150-minute schedule. New checkpoint host rehearsal remains outstanding after offline validation.

**Current revision · 13 October:** [Sectioned deck, visible Unreal Python API examples, Karol integration and current demo review](../SectionsAndAPI20261013/index.html). This supersedes the v3 deck and slide-by-slide timing below. [Current teaching route](../SectionsAndAPI20261013/teach.html) preserves the 150-minute schedule and student activity blocks. The Material/VFX rehearsal and Maya/Blender bridge verification are now recorded; the bridge still needs a complete interactive publisher click-through. [Evidence and Downloads audit](../SectionsAndAPI20261013/audit.html).

**Finalized class pack · 13 October:** [Current slides, demo script, Lab 1 and structured peer reviews](../FinalClass20261013/index.html). Includes the full 150-minute deck, a timed facilitator guide, printable preparation/review/reflection sheets, and a projected round timer. The current Material & VFX Tools practice route replaces the older prop-cleanup demo in the live sequence. Live Unreal integration and the separate Maya/Unreal handoff still require rehearsal. This pack supersedes the activity drafts below.

**Expanded visual lecture · current:** [Review the 65-slide deck](../ExpandedDeck20261013/index.html): 43 live slides and 22 optional slides, with actual old/new comparisons, read-aloud notes, six new editable diagrams, AAA GDC production examples, and a playable 16-second Guerrilla clip. [Complete source and visual register](../ExpandedDeck20261013/sources.html) preserves all earlier collected sources; [motion companion](../ExpandedDeck20261013/media.html) contains the clip and course comparison GIF. Rehearse the classroom route and Maya → Unreal bridge before teaching.

**Refined deck and complete compilation · 13 October:** [Review the 38-slide deck, speaker notes, citations, and proposed timing](../RefinedDeck20261013/index.html). [Complete source audit](../ProductionHandoff20261013/source_audit.html) covers Python, Unreal, all collected Oster tutorials, Qt, UI/UX, limited Blueprint tie-ins, and later study. This is the preceding deck-production pass; the expanded visual lecture above is current. The Maya → Unreal demonstration still needs rehearsal.

**Consolidated production handoff · 13 October:** [Start here for slide generation](../ProductionHandoff20261013/index.html). One eight-slide UI/UX route, read-aloud notes, citations, Qt implementation insets, activity links, visual readiness, and the complete source register. This supersedes the separate UI/UX draft routes for the next production pass.

**UI/UX slide draft:** [Expanded UI/UX sequence: assessment → overview → peer testing](../UXDraft20261012/index.html). Proposes 20 minutes for discussion and task preparation, with six core slides, four optional topics, professional visual sources, and explicit revisiting of students’ initial judgments. Ten extra minutes still need allocation within the confirmed session; the earlier activity timetable is retained as a baseline.

**New activity draft:** [Group tool assessment and three peer reviews](../ActivitiesDraft20261012/index.html), including timing, rotations, printable sheets, and participation routes for unfinished tools.

**Consolidated working plan · 10 October 2026.** The source collection is sufficient. Focus on a reliable demo, Unreal's data model, and a useful tool-testing activity. This is a preparation recommendation, not a changed class agenda.

[Demo and UX guide](Bridge_and_UX.html) · [Student worksheet](Tool_UX_Lab_Sheet.html) · [Tutorial library](Unreal_Tutorial_Index.html) · [Research background](Research_Background.html)

## Prepare in this order

| Priority | Work | Starting references | Ready when… |
| --- | --- | --- | --- |
| **1 · Prove the handoff** | Publish one prop from Maya, import into Unreal, revise, and reimport the same asset. | [Bridge run sheet](Bridge_and_UX.html), [Oster Import/Export](https://isaacoster.artstation.com/projects/Dvdrke), [A4 notes](sources/intro-a4.html). | Scale, orientation, pivot, assignment, and asset identity survive revision. Repeating the operation creates no unintended duplicate. A missing file gets useful feedback. |
| **2 · Choose one follow-up** | Start with a prop intake report. A material variant board is the alternative connection to the next block. | [Demo comparison](Bridge_and_UX.html), [Week 7 Python demo](../UnrealPythonDemo/index.html), [selection](sources/oster-03.html) and [Actors/Components](sources/oster-07.html). | Selection, shared data, intended changes, and verification are clear. One bounded operation is enough. |
| **3 · Trial the UX activity** | Compare two interfaces to the same operation; have a partner try a task using the sheet. | [UX guide](Bridge_and_UX.html), [worksheet](Tool_UX_Lab_Sheet.html), [existing checklist](sources/ux-checklist.html). | The task gives a goal without a click sequence. Observations identify help needed and one retestable improvement. |
| **4 · Rehearse the sequence** | Run setup, explanation, demo, and activity handoff in the teaching engine. | [Agenda review](../AgendaRevision20261010/Preparation_and_Source_Compilation.html), [setup notes](sources/intro-00.html). | The opening works from a clean start, results are visible, recovery is accurate, and the sequence fits the available time. |

**Next action:** prove the import/reimport loop with one known prop before adding a UI or more features. Keep an exported file ready as a fallback. The bridge run sheet is written; implementation and rehearsal remain outstanding.

## Keep the lesson small

Your goals are the Maya → Unreal transition, Python inside Unreal, professional tool UX, and a tangible final-lab test sheet. Materials remain an optional connection to the following three-week rendering/shader/material block.

- **Core:** host-specific APIs; disk versus asset paths; Content Browser versus level selection; Actor → Component → asset; eligibility, preview, results, and recovery.
- **Recommended baseline:** one prop handoff, then a read-only intake report with at most one controlled edit. Show success and one recoverable failure.
- **Alternative extension:** a small material variant board with a prepared master. Choose it instead of adding every texture/import/validation feature.
- **UI:** a menu or prepared Editor Utility Widget can expose the same operation. Full Qt setup and Blueprint authoring can wait.
- **Recovery:** property Undo and import/reimport need different demonstrations. Do not promise that every operation is undoable.

<h2 id="weekend-course-shortlist">Short study queue</h2>

Stop reading when you can apply the relevant idea. These are selections from the existing research, not new course requirements.

| When | Resource | Extract this |
| --- | --- | --- |
| **Now · bridge** | [Oster Import/Export](https://isaacoster.artstation.com/projects/Dvdrke) + [A4 notes](sources/intro-a4.html) | One import with explicit source and destination. Outbound Unreal export is optional. |
| **Now · UX principles** | [Nielsen's heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) + [task scenarios](https://www.nngroup.com/articles/task-scenarios-usability-testing/) | Scope, feedback, recovery, and a realistic goal-based test. Choose three principles to demonstrate. |
| **Now · tool UX example** | [Ryan's Batch Rename series](https://ryandowlingsoka.com/unreal/batch-rename-tool/) | Layout, per-item choice, results/recovery. Browse selectively; implementing the full tool is unnecessary. |
| **If a workflow gap appears** | [Ryan's Python in Unreal Tips](https://ryandowlingsoka.com/unreal/python-in-unreal/) | Only the relevant setup, debugging, progress, or responsiveness section. |
| **If choosing materials** | [Oster Asset Setup](https://isaacoster.artstation.com/projects/xDB8zR) or [Texture Utility](https://isaacoster.artstation.com/projects/qeAwqe) | Setup for instances/assignment, or Texture Utility for inspection/settings. PentaPixels remains an alternate explanation in the library. |

Suggested first pass: **30–45 minutes reviewing bridge references, 60–90 minutes trying the handoff, then 30–45 minutes trying the UX explanation/sheet**. These are adjustable preparation estimates, not video runtimes or a promised completion time. If the bridge needs more work, defer the extension before adding more study.

**Paid courses:** Karol's [UE5 Python Automation](https://www.udemy.com/course/unreal-engine-5-python-automation/) remains your first-choice structured course. Consult relevant sections as needed; finishing it is not a Week 7 prerequisite. Moniem and *Becoming an Unreal Automation Expert* remain alternatives in the background, not extra homework. No purchase is needed to begin the work above.

## Already covered · reuse your notes

- **Epic Python documentation:** reference for a specific question; do not restart as new study.
- **Oster introduction:** reuse [selection](sources/oster-03.html), [properties](sources/oster-05.html), and [Actors/Components](sources/oster-07.html). Its Epic and ArtStation listings are the same course.
- **[YouTube automation playlist](https://www.youtube.com/playlist?list=PLKgYiIAqG99cwlb4Y2Pu-cSb_Vw14-t0c):** completed and liked, as you confirmed. Reuse A1–A4 notes. This does not establish completion of the separate Udemy course.
- **Week07UnrealPython:** existing controlled-edit preparation with prior validation records. Keep as a reference/fallback; it does not prove the new bridge works.

<h2 id="expanded-source-library">One library, four states</h2>

The [tutorial library](Unreal_Tutorial_Index.html) retains individual video links and future topics. Its default view shows the immediate study queue.

| State | Contents |
| --- | --- |
| **Use now** | Import/Export, the batch-rename UX example, and UX principles/task testing. |
| **As needed** | Material examples, progress/debugging, import rules, validation, menu delivery, the Spanish resource, and discovery leads. |
| **Already covered** | Oster introduction and the completed playlist. |
| **Later** | PCG/cities, procedural modeling, landscapes, Niagara/VAT, Sequencer, Nanite depth, full Qt UI, material-parameter tooling, and automated screenshot/test infrastructure. Topic tags are not confirmed week assignments. |

TutorialSearch is a discovery aid, not another course. The Spanish resource remains optional with detailed content/captions unverified. Maya-only training and unsuccessful provider searches are background. The deliberate Maya → Unreal handoff is in scope.

## Deliverables and open work

| Item | State | Next step |
| --- | --- | --- |
| Sources and plan | Organized; provenance retained. | Pause broad searching; consult for a specific need. |
| Maya → Unreal bridge | Written design and rehearsal criteria ready. | Implement/rehearse in the actual Maya/UE versions. |
| Unreal follow-up | Options documented; final choice open. | Try the intake-report baseline; choose one extension only if useful. |
| UI/UX explanation | Draft ready. | Choose one A/B interface example from the selected tool. |
| Student worksheet | Two-page printable draft; prior visual print check completed. | Trial one realistic task and refine before distribution. |
| Classroom integration | Existing agenda and slide review retained. | Fit the rehearsed demo into the agenda; update teaching material afterward. |

<h2 id="blueprints-week7-scope">Blueprint boundary</h2>

A prepared editor UI calling Python is useful if it clarifies inputs and feedback. Defer a substantial Blueprint-building lesson. Material parameters are context only if the chosen demo uses them; a Material graph is not a Blueprint Event Graph. See the [detailed guide](Bridge_and_UX.html).

<h2 id="northwood-project-provenance">Reference and provenance</h2>

The original Northwood project came from your Oster course study. Week07UnrealPython is the teaching-preparation spinoff; attribute its six-prop fixture and controlled-edit tools separately. [Demo guide](../UnrealPythonDemo/index.html).

[Research background](Research_Background.html) preserves the previous compilation: course comparisons, lesson maps, setup run sheet, code corrections, and earlier recommendations. This plan takes precedence where priorities differ. [Source snapshots](source_index.html) remain unchanged. Historical snippets still need the documented corrections before reuse; this consolidation does not newly validate their code.
