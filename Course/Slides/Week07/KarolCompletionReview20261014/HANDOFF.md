# Karol course completion handoff for Week 7

14 October 2026. The remaining course notes are refined. Use the current v13 deck and the existing Blender bridge as the integration baseline. This handoff proposes teaching edits; the PowerPoint and project implementation are unchanged.

## Current baseline

- Deck: Course/Slides/Week07/UnrealFirst20261013/output/Week_7_Python_in_Unreal_v13.pptx, 115 physical slides including the cover.
- Main sequence: Python in Unreal, brief Blender API/bridge, colleague material/Maya demonstrations, then the existing assessment, UI/UX and peer-testing blocks.
- Do not use the old v3 slide numbers or restore the earlier material-demo timing. Preserve the current 150-minute session and discussion/activity opportunities.
- The 14 October UI/UX, Golden Path imagery and motion reviews are separate proposals. Reconcile them with this handoff before producing a new deck; they do not establish that v13 was already edited.

## Implement the teaching edits in this order

1. Slide 10 / CALL: keep the table. Explain editor-managed subsystem retrieval and direct iteration of Array[Actor] in narration. Lesson 49 is already correctly implemented.
2. Slide 13 / RUN: keep the saved-file procedure. Link a short import troubleshooting reference based on lesson 48; keep installation work in preparation.
3. Slide 29 / 10D: keep the Blender revision and reset sequence. Explain exported, sent, acknowledged and verified as distinct stages. Reuse the existing Golden Path before/after captures.
4. Slide 61 / 08A: keep the correct PySide/Slate labels. Add the optional dependency-direction explanation from lesson 48.
5. After optional slide 75 / 08: consider K2, a typed Map output example using lesson 50 screenshots 10–11. Make output variable/pin names consistent and show Map<String, Integer> explicitly.
6. Slide 106 / K1: link the five completed lessons. Keep detailed import troubleshooting (proposed K3) and Remote Control object-path discovery (proposed K4) as optional material if dedicated slides are useful. Do not add them automatically to the live route.

## Bridge implementation facts to preserve

- The classroom bridge uses file-based requests and acknowledgements, not Remote Control HTTP. Karol's direct export/import idea transfers; his transport does not describe this implementation.
- Current shared code is Content/Python/week07_bridge/client.py, transport.py, core.py and unreal_receiver.py in Week07UnrealPython. Host adapters supply Blender/Maya scene/export behavior.
- Existing behavior includes heartbeat, session protection, completed-request no-replay, explicit pending state and surfaced importer failure. Do not list these as unimplemented features.
- Receiver checks the destination asset and returned import paths, preserves existing materials, and temporarily selects/restores the demonstrated FBX importer setting. Do not replace those explicit choices with the older course defaults.
- Existing UI rehearsal evidence is Docs/Bridge/UI-Rehearsal/verification.json: the same Blender asset is revised from 180 to 220 cm and both blue placements use it; orange Maya examples remain at 180 cm. This is saved evidence, not a fresh session check.

## Smallest useful new feature

Add a read-only Copy diagnostics report to the existing publisher: host/Python version, module location, exchange root, receiver project/session and request/result identity. Reuse shared state in both host views. It must not export, import, resend, cancel or mutate pending work. Check offline, mismatched environment, pending, failed and completed states with fixtures, then verify actual UI behavior in a separate authorized rehearsal.

The offline-publish/send-later failure path is already implemented and tested. Consider showcasing it after rehearsal; do not implement a duplicate recovery mechanism.

## Completed note work

Created REFINED lessons 46–50 with all 70 new screenshots and key code/setup details. Updated the course index and linked lessons 44–45 to the runtime object-path correction. The user's edited lesson 45 was preserved around that small cross-reference addition.

Corrected two misplaced supplemental paragraphs from the earlier audit: lesson 23 is square-texture validation, while lesson 24 checks membership in an explicit list of power-of-two dimensions. Their original lesson explanations/images were retained. A backup of the pre-edit refined collection is under history/.

## Verification before the next deck revision

Use actual PPTX physical slide numbers; adjacent metadata can use a different index. Preserve Isaac Oster/Northwood project attribution and credit Karol/Tech Art Corner for supplemental examples. Keep instructor instructions outside read-aloud notes. Do not present expected-result slides or historical rehearsal captures as new live evidence. New code snippets are syntax-checked examples; current-engine behavior must be checked separately before classroom execution.
