# Week 7 UI/UX integration plan

Prepared 15 October 2026 against **Week_7_Python_in_Unreal_v15.pptx**: 134 slides, with UI/UX on slides 39–60 and task preparation on 61–62. This is a content and implementation preparation package. It does not claim that v15 has been edited. The earlier review based on the first ten notes is retained as history.

## Follow-up direction: fuller slides and the supplied GOLF+ example

The instructor is considering placing more readily available explanation directly in the slides because the teaching tools have not been extensively manually tested and colleagues have room to elaborate on their demos. This revision adopts that as the working direction for the proposal; it does not silently change demo allocations or the class schedule.

Make the slide sequence understandable without a successful live tool run. Put definitions, worked user stories, acceptance checks, state tables, annotated observations and a small readable implementation excerpt on the slides themselves. Keep read-aloud notes for explanation and discussion, rather than making them the only location of essential information. Preserve clean mantra transitions and one main teaching point per slide. More information should come from a useful comparison or worked example; split an overloaded composition instead of shrinking the type.

Prepared examples become the baseline: static state comparisons for Preview/Apply, a visible user-story worksheet, the supplied GOLF+ interface and an actual source-code excerpt. A live run is optional reinforcement after the exact operation is manually rehearsed. Keep the colleague demonstrations and existing peer-test time available for deeper implementation and behavior.

The new main GOLF+ visual is the instructor-provided **Course Generator — Paynes Valley** screenshot received 15 October. Its six visible stages are Input, Parameters, Generate, optional Edit, Finalize and Integrate. The earlier overlay and Spline Suite captures are separate tools/process history. Use the supplied screenshot now for sequence, dominant emphasis, optional detail, typography and shared visual roles; no new Unity capture is necessary for those claims.

The warning beside Input is a particularly useful critique prompt: what does it mean, and should the artist proceed? The screenshot alone cannot establish the cause or the code's response. Muted controls and filled stage markers also do not establish enabled/completed state. A future behavior example can add warning, in-progress, completed and recoverable-failure captures from one prepared task. Keep those as proposed evidence, not a prerequisite for the visual lesson.

The October playbook's Detect → Generate → Finalize → Adopt terminology differs from the six-stage screenshot. Reconcile the intended names and scope before describing the document as a perfect match for the implementation. This is a concrete reason to maintain a style sheet over time.

## Assessment

The new notes give the section a much stronger visual-design vocabulary: rhythm, harmony, dominance, alignment, proximity, color roles, contrast, data presentation and distinct interaction cues. These explain *why* a tool feels organized and how an artist can improve it deliberately. Their most useful teaching contribution is a repeatable method for critiquing the same interface, rather than a succession of unrelated website critiques.

The current deck already handles matters the visual-design course covers less deeply: scope, preview, stale state, guarded application, recovery, observed testing and telemetry limits. Preserve those strengths. Attractive presentation does not establish correct behavior, and a robust backend does not establish usability. The revised section should connect the two.

The selected notes contain 34 lesson files, including a duplicate of 04 in 06. Lessons 19, 22, 26–29 and 34–42 were not supplied as distinct notes. The recap mentions some omitted topics; that is not evidence that their detailed lessons were completed. The refined notes preserve each original and its available screenshots, repair transcription into paraphrases, separate the lecturer’s principle from the game-tool adaptation, and identify claims that should not be repeated literally.

## Five teaching mantras

These are the proposed course structure, adapted from the notes and the existing Week 7 objectives. They are not presented as verbatim Joe Natoli quotations or as a replacement for his full recap.

1. **Know the task.** Establish the user, situation, desired outcome, benefit and evidence of success.
2. **Guide the eye.** Use art principles to communicate priority and relationships.
3. **Make actions clear.** Distinguish information from controls, expose state and scope, and support recovery.
4. **Keep a shared visual language.** Record and maintain the visual and interaction rules across tools and contributors.
5. **Test the whole workflow.** Match prototype fidelity to the question, observe attempts, verify results, and retest changes.

Reuse existing section transitions as mantra dividers. Within a subsection, use short descriptive slide titles and one visual argument per slide. Avoid printing every principle on every slide. A small mantra label supplies continuity while the example changes.

## User stories with enough substance to guide design

A user story expresses an outcome and its value from the user’s perspective. The familiar “As a …, I want …, so that …” structure helps expose assumptions, but writing that sentence is only the beginning. Discuss it with the person who does the work. [Atlassian](https://www.atlassian.com/agile/project-management/user-stories) and [NN/g’s story-mapping guidance](https://www.nngroup.com/articles/user-story-mapping/) support this distinction.

Build the classroom example in four passes:

| Pass | Material-tool example | What it establishes |
| --- | --- | --- |
| Situation | An environment artist is trying a supplied texture set on a selected crate in the teaching level. | Actual context, frequency, starting data and host |
| Story | As an environment artist, I want to preview a material assignment on selected props so I can compare a look without changing other placements. | User, outcome and benefit |
| Acceptance checks | The intended texture mapping and target slot are visible; applying changes only the named components; the protected crate stays unchanged; a stale preview cannot apply. | Observable behavior and scope |
| Test scenario | “Try this texture set on the target crate and show me the result. Leave the protected crate unchanged.” | A goal a peer can attempt without a click script |

This is an illustrative teaching story, not a newly discovered production requirement. The import/reimport story on v15 slide 41 remains a second example: distinguish the stable Unreal asset identity from the revised source file, and check material assignments after reimport.

Avoid stories such as “As a user I want a blue Apply button.” That prematurely chooses a solution and leaves the benefit unspecified. Split a large story into an end-to-end slice: choose inputs → inspect scope → review proposed change → apply → inspect result/recover. A slice should deliver a meaningful outcome, not just finish one layer of implementation.

Acceptance criteria are not implementation instructions. For example: **Given** a prepared texture set and target selection, **when** a preview is created, **then** the target, slot and mapping are visible and no scene change has occurred. Add a second criterion for an input changing after preview: Apply becomes unavailable until a fresh review. A testing task then asks the participant to reach the outcome without prescribing those interface actions.

Keep the four-minute peer preparation block. The richer story guidance belongs in the lecture and preparation reference; do not add a new graded deliverable or imply that a full Agile process is required for this lab.

## Art fundamentals and visual diagnostics

Use the instructor’s art vocabulary as a bridge. Balance describes the distribution of visual weight; rhythm and repetition establish expectations; emphasis suggests a focal point; unity/harmony makes related elements feel coherent; negative space and proximity communicate relationships. A composition can be asymmetrical and still balanced. [Getty’s principles](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) provide a concise reference.

In a game environment, a focal area may help a player orient themselves. In an editor tool, emphasis helps an artist locate the relevant target, warning or next action. That analogy explains the design intention; it does not establish that the same palette, density or input method works for both. Distinguish a desktop tool, a player HUD and a VR panel when discussing viewing distance, controller focus, motion and changing backgrounds.

**Value** in art refers to lightness and darkness. **Contrast** is a relationship: how different neighboring elements appear, including differences in value, hue, size, shape and texture. HSV “Value” is a software color-coordinate term, not the same thing as perceived lightness or WCAG relative luminance. Revise v15 slide 55 so this distinction is explicit. Hue difference alone can disappear when the interface is viewed in grayscale. [Getty’s elements of art](https://www.getty.edu/education/teachers/building_lessons/formal_analysis.html) supports the art vocabulary.

Apply three quick checks to the **same screenshot**:

| Check | Procedure | Useful question | What it cannot prove |
| --- | --- | --- | --- |
| Shape blockout | Reduce regions to simple masses, preserving their location, size and gaps. Use the existing lesson 18 capture as the first example. | Are groups and a reading route apparent without detailed labels? | That labels, focus or behavior are clear |
| Grayscale | Temporarily remove hue from a copy/view. | Does hierarchy and status meaning survive? | All color-vision experiences or a contrast ratio |
| Squint test | Briefly squint or step back; a blurred preview is an approximation for demonstration. | Which large shapes and light/dark masses dominate? | Text readability, accessibility, correctness or measured attention |

Restore the original image, read the text, inspect the actual color pairs and test the controls. Keep all essential text readable; quieter does not mean faint. As a practical benchmark, WCAG text contrast is 4.5:1 for ordinary text and 3:1 for large text, with definitions and exceptions in the standard. Desktop use of that benchmark is not a claim of complete conformance. [W3C](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

The Week 1 source found in this workspace verifies the four course lenses and the broader artistic/technical connection. It did not yield a specific text slide covering every art principle above. Link explicitly to those verified lenses and present the art vocabulary as a recap/extension; do not invent Week 1 slide-number attribution.

## Color tools and consistency

Mention [Coolors](https://coolors.co/generate) as a palette exploration tool and its [contrast checker](https://coolors.co/contrast-checker) as a practical pointer. The links returned 403 to automated retrieval in this session, so the review does not claim a current interface walkthrough or feature verification. A palette is a starting point. Give the colors roles, test pairs on actual surfaces, and inspect the real application. A pleasing palette alone does not establish readable text or meaningful states.

Use the existing color-with-labels example. Separate selected, focused, available, warning, blocked and complete; they are different states. Pair meaning with text or shape rather than hue alone. [W3C use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

## Style sheets, design systems and AI

A **style sheet** is a maintained specification of the visual and interaction decisions a team agrees to reuse: typography roles, spacing, alignment, color meanings, icons, control states, wording, density and examples. It records the reason and the scope of each rule, not just a color swatch. A **design system** adds reusable components, patterns and a process for maintaining them. A **QSS/CSS file** implements part of the appearance; it is not the entire design specification.

Large organizations commonly use shared style guides and design systems to coordinate contributors, reduce contradictory patterns, support onboarding and make updates consistent. Avoid “every large organization always does this”: names, maturity and adoption vary. [Figma’s design-system overview](https://www.figma.com/design-systems/) gives a concrete example of shared styles, tokens and libraries.

Use GOLF+ as the instructor’s case: the UI Quality Playbook records repeated workflow steps, a shared wrapper, semantic colors, icon conventions and screenshot review. It also records unresolved palette consolidation. Present that as evidence of a maintained design process, not proof that every tool already follows every rule. Keep its green/gold brand separate from the Week 7 tool’s blue/dark-neutral palette.

Show an example style-sheet entry:

> **Forward action:** Emphasize the available next action. Before preview, emphasize Preview. After a valid reviewed plan, emphasize Apply. If a warning needs acknowledgment, keep attention on the review. Backend checks still govern execution.

Then show how the instructor uses AI: give the agent the style sheet, token source, representative examples and change scope; ask it to use existing components; compare the output against the same reference states; update the rules deliberately when an exception is accepted. A skill makes the reference reusable and discoverable. It does not guarantee that an agent loaded it, interpreted it correctly or produced conforming work. Check the result.

The included local `style-skill/SKILL.md` is a small teaching example, not a global installation or a new agent configuration. It does not automatically spawn agents. A shared review role can be assigned when parallel agent work is already authorized.

## Practical grounding and prototyping

The general principles are necessary but insufficient on their own. Retain **one short implementation bridge** using the actual Material/VFX tool, rather than introduce a full Qt or Blueprint course. Explain the same operation through a sketch, prepared PySide states and a small source excerpt. Use the native Unreal panel as a comparison when a matching capture is available; the lesson does not depend on opening it live. These are different front ends with different integration constraints.

In PySide, show one layout decision and one state decision: a form layout associates labels and fields; signals invalidate an old preview after input changes; the session computes readiness; `setEnabled` reflects it. The revised demo also changes visual emphasis with state. Explain the backend recheck using the existing source and prepared state sequence; show a live stale-selection attempt only after manually rehearsing that exact operation. The executable source is the teaching evidence; update slide code from that source. [Qt layouts](https://doc.qt.io/qtforpython-6.8/overviews/qtwidgets-layout.html)

Explain the Unreal choices accurately: Editor Utility Widgets use UMG/Blueprint for editor tools, while this project’s existing native panel is C++ Slate. A PySide window parented to Unreal is still a separate Qt interface and is not native docking. Do not imply the older attached talk’s `unreal_engine` plugin is the current official `unreal` module. [Epic EUW documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/editor-utility-widgets-in-unreal-engine)

Use **Figma or paper** to test interpretation and flow before building the operation. Prepare a start state, a valid preview, a blocked state and a completion state. Ask the artist to attempt a goal. Figma can connect frames and interactions; it cannot establish asset integrity, real file I/O, undo or engine latency. Use a running tool when those are the questions. [Figma prototyping](https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma)

## GOLF+ and attached talk placement

The local GOLF+ notes supply real examples with useful process context:

- **Course Overlay TODO:** compact toolbar capture and a shortcut-conflict note. Use for discoverability and host interaction, clearly labeled as an August capture with existing annotations.
- **GUI Feedback:** the instructor explicitly identifies competing colors/contrast and asks for categories, sizing and design rules. Use as a problem statement. Do not invent a matched “after” capture or a measured improvement.
- **UI Quality Playbook:** connects repeated workflow steps, shared visual rules and review practice. Use as the instructor’s style-sheet case.

The Notion documentation was not accessed; these historical notes were found locally. The newly supplied Course Generator screenshot is now the primary teaching visual on 52A and 53C. A fresh overlay walkthrough is optional additional process evidence, not required to insert or explain the supplied image.

Marcus White’s attached **Using Python to Streamline Asset Workflows for a Small Team** supplies a complementary production case. Pages 13–18 establish the small-team ingestion need; page 26 shows a compact batch importer; page 33 compares the workflow; pages 35–37 show asset overview/reporting. Use the workflow and UI evidence to ask what the tool removes from the artist’s effort and what information remains visible. “No room for error” is the presenter’s aspiration, not a guarantee to repeat. The UE4-era Python details on pages 8–10 are historical; do not copy them into the current UE5 setup. Preserve the source footer and attribution in borrowed captures.

## Timing and insertion

The v15 agenda allocates **16 minutes to UX concepts/discussion plus four protected minutes for task preparation**. The expanded content is a substantial teaching sequence, not a credible extra minute or two. The earlier full-sequence estimate was **28–35 minutes**. The fuller visible content now needs rehearsal; this is not a measured runtime or authorization to take time from colleagues.

Keep the schedule unchanged in this preparation pass. Do not silently hide useful slides or squeeze the peer-test rounds. The integration manifest preserves every current anchor and separates proposed order from current numbers. All requested additions are marked for coverage; source-history detail and additional implementation study are explicitly references.

For a fast 16-minute overview, the five mantras can guide five prepared explanations: story and criteria (3 minutes); one interface through the art checks (4); state/recovery with the short implementation connection (3); shared style sheet and AI workflow (3); prototype/test/retest handoff (3). That is an overview with references, not comprehensive delivery of every prepared slide. The full preparation stays available so the instructor can choose depth during rehearsal. Resolve pacing before finalizing a new full-deck export.

## Integration sequence and acceptance

1. Refine and archive sources; keep source lesson numbers and provenance. **Prepared.**
2. Review the mantra sequence and field-level changes against v15. **Prepared in the illustrated review and JSON manifest.**
3. Align showcase tools with the lecture contract. **Focused PySide change implemented and checked offline; remaining host-specific checks are identified in the demo audit.**
4. Use the supplied GOLF+ image and prepared PySide states as the baseline. **The visual lesson is ready to author; live captures and an instructor walkthrough are optional extensions requiring their own checks.**
5. Import a copy of v15, preserve its masters, visuals, agenda and unrelated slides, then apply the manifest. Use stable insertion IDs until the new deck is exported. **Ready for authoring around the prepared explanations; preserve the schedule and resolve pacing in rehearsal. Any live claim remains subject to its own checks.**
6. Regenerate slide code from the changed source; replace affected tool crops; render every changed slide and its neighbors; verify notes, source links, font sizes, images, live/reference order and unchanged schedule. **Required at direct integration.**

Do not certify every showcased interface from one offscreen PySide test. Native Slate, Blender and Maya need their own resize, focus, state and recovery checks in the relevant host. Existing historical captures remain labeled as such until replaced.
