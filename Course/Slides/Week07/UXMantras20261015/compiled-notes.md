# UI/UX principles for game tools

34 supplied lesson files, with one duplicate (04/06). This is the selected-course compilation, not a claim that all 49 lessons were studied. The earlier ten-note compilation is superseded.

## 01 · Design is Design is Design

Visual design communicates purpose, relationships and available actions. Appearance participates in solving a problem.

**Tool application:** Name the artist, task, intended result and protected scope before styling a tool.

**Qualification:** The lecturer’s career anecdotes illustrate his perspective; they are not comparative usability studies.

**Review prompt:** Which decision does each visible element help the artist make?

## Study detail and teaching translation

- Begin with the problem being solved, not a collection of attractive components. Labels, grouping, hierarchy and available actions all communicate an interpretation of that problem.

- Distinguish visual polish from usefulness. A visually coherent interface can still make the wrong decision prominent or omit information needed to finish the task.

- Teaching adaptation: identify the intended artist, inputs, result and consequences before critiquing the material tool. Keep aesthetic decisions connected to those answers.

[Refined note and captures](notes/01.html)

## 02 · Stop Solving Other People's Problems

Evaluate references against the audience and situation they serve. A polished layout is not evidence that it fits a different workflow.

**Tool application:** Compare a marketing landing page with a repeated-use asset tool. Borrow a useful pattern, then test it in the artist’s context.

**Qualification:** Adapt the warning against copying inspiration into critical reference use; do not teach a ban on references or claims about innate design ability.

**Review prompt:** What assumptions would change if a beginner used the same tool?

## Study detail and teaching translation

- A reference carries assumptions about its audience, business purpose, frequency of use and environment. Copying its appearance also imports some of those assumptions.

- Extract the principle behind a reference—clear grouping, recognizable navigation or a distinct next action—then test that principle in the new context.

- Teaching adaptation: a store page, game HUD and asset-processing panel can share visual principles while requiring different density, interaction speed and levels of explanation.

[Refined note and captures](notes/02.html)

## 03 · Form Doesn't and Shouldn't Follow Function

Appearance and behavior shape each other. A technical requirements list does not uniquely determine an understandable interface.

**Tool application:** One operation can be exposed as raw parameters, a task-oriented form, or a preview-and-apply workflow.

**Qualification:** The architecture and Bauhaus history is background framing, not needed to establish the Week 7 principle.

**Review prompt:** What can your interface explain that a function signature cannot?

## Study detail and teaching translation

- Functional requirements leave many presentation choices open. The same operation can be difficult or straightforward depending on terminology, grouping and the order of decisions.

- Consider appearance and behavior together. A control’s shape and placement imply what it does; implementation must honor that implication.

- Teaching adaptation: expose the material operation as a reviewable artist workflow rather than a direct list of API arguments. Preserve technical detail where it supports inspection.

[Refined note and captures](notes/03.html)

## 04 · Balancing Form and Function - Prescription vs Description

Treat design principles as questions to investigate rather than recipes that decide a layout automatically.

**Tool application:** Compare two arrangements using the same artist task and acceptance checks.

**Qualification:** Nature analogies and generalizations about engineers are rhetoric, not universal laws.

**Review prompt:** What observation would make you revise the first layout?

## Study detail and teaching translation

- The source warns against treating a slogan or principle as an automatic recipe. Context, constraints and the relationships between parts affect the result.

- Use a principle to generate a testable design question. For example, does aligning these fields make their relationship clearer, or imply a relationship that is not real?

- Teaching adaptation: compare alternatives with the same task, prepared inputs and success checks. An explanation of intent is not a substitute for observing an attempt.

[Refined note and captures](notes/04.html)

## 05 · Why Form Follows Function is NOT a UI Design Prescription

Distinguish the implementation model, the user’s mental model, and the representation offered by the interface.

**Tool application:** An artist may reason about VFX duration while the implementation manages separate spawn and kill events.

**Qualification:** The notes attribute this model to Alan Cooper. Expert users can still need implementation detail; reveal it when it serves a decision.

**Review prompt:** Does the label describe an artist intention or an internal object?

## Study detail and teaching translation

- Implementation model: how the system actually works. Mental model: how the user believes the task or system works. Represented model: what the interface presents.

- Choose representations that help the user reason about the operation. A technically precise internal term can still be a poor everyday label.

- Teaching adaptation: duration is often a useful artist-facing concept even if the underlying effect has separate creation and termination events. Keep detailed controls available when the artist actually needs them.

[Refined note and captures](notes/05.html)

## 06 · Every Force Evolves Form (So Don't Follow the Prescription)

The supplied source duplicates lesson 04. It does not provide a distinct explanation of this lesson.

**Tool application:** Use lesson 04’s qualified principle and the recap only as a recap.

**Qualification:** Do not reconstruct a missing transcript from its title. The duplicate is recorded by content hash.

**Review prompt:** No separate learning claim is assigned to this source.

## Study detail and teaching translation

- This file repeats lesson 04 rather than providing new lesson content. Preserve it as source history and cross-reference 04.

- The recap describes the influence of multiple forces and constraints on the final design, but that summary cannot reconstruct the missing distinct lesson.

[Refined note and captures](notes/06.html)

## 07 · Less is More - Small Screens, Big Challenges

Reduce unnecessary information while preserving the cues that make an action discoverable.

**Tool application:** A compact tool still needs a visible target, action, status and route to useful detail.

**Qualification:** Historical mobile commentary and an uncited first-impression timing claim are not current evidence of a universal effect.

**Review prompt:** What disappears when you make the panel smaller, and is it essential?

## Study detail and teaching translation

- A smaller surface is not a large interface shrunk proportionally. Reassess what must remain visible and what can be deferred.

- Reduction should preserve the clues needed to recognize purpose, current state and the next action. Removing those clues creates uncertainty instead of simplicity.

- Teaching adaptation: test a narrow editor panel. Keep the target and consequence visible while moving optional detail into a disclosed area; avoid making essential scope discoverable only on hover.

[Refined note and captures](notes/07.html)

## 08 · Five Rules for Effective UI Design on Small Screens

Design for the input device, context, available space and cost of repeated entry.

**Tool application:** Desktop tools need keyboard focus, precise selection and resizing; a VR interface additionally needs distance, angular size and controller testing.

**Qualification:** Do not convert mobile millimeter examples into universal pixel sizes or apply thumb-reach rules to desktop editors.

**Review prompt:** Could selection or a preset replace repeated manual path entry?

## Study detail and teaching translation

- Screen dimensions, input method and circumstances of use change interaction requirements. Touch, mouse, keyboard and controller input are not interchangeable.

- Repeated text entry can be a source of friction. Selection, presets and sensible defaults may help when the artist can still inspect and correct them.

- Teaching adaptation: verify keyboard traversal and resizing in the desktop tool. Treat in-game or VR UI as a different test environment rather than converting desktop pixel dimensions into a universal rule.

[Refined note and captures](notes/08.html)

## 09 · Balance Creates Visual Order

Balance distributes visual weight. Negative space and alignment can make relationships clear without symmetrical composition.

**Tool application:** Separate task inputs, review information and actions while retaining a clear reading route.

**Qualification:** A balanced appearance alone does not prove efficient operation.

**Review prompt:** Which group looks important, and is that the intended group?

## Study detail and teaching translation

- Visual weight comes from more than physical size: density, contrast, isolation and surrounding space affect the composition.

- Balance can be symmetrical or asymmetrical. The objective is a readable relationship between regions, not equal quantities on both sides.

- Teaching adaptation: compare the weight of inputs, review information and actions. A large empty table may be acceptable as a stable work area, but it should not obscure the next available action.

[Refined note and captures](notes/09.html)

## 10 · Case Studies - Improving Balance in the User Interface

Targeted changes to column widths, gutters and padding can clarify an existing interface.

**Tool application:** Improve one crowded tool group before proposing a complete visual redesign.

**Qualification:** The captured before/after is a design demonstration, not a measured user-study result.

**Review prompt:** Can a new user correctly group the same controls after the change?

## Study detail and teaching translation

- Inspect the existing structure before redesigning it: unequal gutters, cramped margins and weak separation can make otherwise sensible groups difficult to read.

- Change a small set of relationships, then compare the result using the same content. This makes the reason for the improvement easier to explain.

- Teaching adaptation: use matched material-preview captures. Distinguish a design demonstration from a measured claim about faster task completion.

[Refined note and captures](notes/10.html)

## 11 · Rhythm - Establishing and Reinforcing Comprehension

Rhythm is the predictable recurrence of related elements and the intervals between them.

**Tool application:** Repeat asset-row order, label spacing and state treatment so a user can scan successive items.

**Qualification:** A repeated pattern can also repeat a poor choice; consistency must serve the task.

**Review prompt:** Which detail should remain stable from one row to the next?

## Study detail and teaching translation

- Repetition creates an expectation: users learn where a label, value, status or action will appear in the next instance.

- Intervals participate in the pattern. Consistent spacing within a group and between repeated groups can make the sequence easier to scan.

- Teaching adaptation: keep asset identity, before, after and status in a predictable order. Reserve a deliberate pattern break for an exception that deserves attention.

[Refined note and captures](notes/11.html)

## 12 · Harmony - Shaping the Parts into a Whole

Harmony comes from related visual treatments that make separate elements read as a coherent whole.

**Tool application:** Use shared spacing, type roles, icon treatment and semantic state colors across related tools.

**Qualification:** A visual echo communicates similarity only when the underlying meaning is also consistent.

**Review prompt:** Do two similar-looking controls behave similarly?

## Study detail and teaching translation

- Harmony means the parts support a coherent whole. Related shapes, typography, spacing and color roles can make separate regions feel connected.

- Similarity should correspond to meaning. Reusing one treatment for unrelated states creates visual consistency but semantic confusion.

- Teaching adaptation: use shared form patterns and state labels across Material Setup and VFX Placement. Preserve host-specific differences that serve a real interaction need.

[Refined note and captures](notes/12.html)

## 13 · Using Harmony to Create Directional Flow

Alignment, spacing and emphasis can suggest a reading and action sequence.

**Tool application:** Arrange source, destination, preview and commit in a route that matches the workflow.

**Qualification:** Left-to-right examples reflect a reading context; localization and task structure can require a different route.

**Review prompt:** Where does the eye go after the most prominent element?

## Study detail and teaching translation

- Directional flow emerges from alignment, grouping, repetition and changes in emphasis; it is not limited to adding arrows.

- A strong starting point should lead toward the next relevant information. Multiple unrelated focal points can interrupt the intended sequence.

- Teaching adaptation: organize source inputs, scope, reviewed consequence and Apply in the order the artist needs them. Test the reading route rather than assuming a universal scanning pattern.

[Refined note and captures](notes/13.html)

## 14 · Case Study - Using Harmony for Better Form Design

Repeated field dimensions and spacing establish a pattern; a deliberate difference can distinguish the action.

**Tool application:** Use form layouts and recognizable buttons rather than hand-positioned labels and decorative action text.

**Qualification:** A shorter button is not inherently more usable. Full-width buttons can be appropriate in narrow tools and are explicitly used in the GOLF+ playbook.

**Review prompt:** Is the action distinct while remaining consistent with the host application?

## Study detail and teaching translation

- Repeated field treatment helps the user recognize a form as a sequence of related decisions. Consistent labels, widths and gaps reduce unnecessary variation.

- The action should be recognizable as a control and distinct from descriptive headings. A purposeful change in treatment can mark the transition from entering information to acting.

- Teaching adaptation: use Qt form layouts and explicit button labels. The course example’s narrower button is one solution; a full-width primary action can also be appropriate in a narrow game-tool panel.

[Refined note and captures](notes/14.html)

## 15 · Dominance - Directing (and Maintaining) User Focus

Dominance gives the viewer an entry point and suggests relative importance through size, contrast, position and surrounding space.

**Tool application:** Emphasize the current decision. Before a valid preview, the next action is Preview rather than an unavailable Apply.

**Qualification:** No single visual feature determines attention in every situation; task and familiarity also matter.

**Review prompt:** Does the strongest emphasis correspond to the current state?

## Study detail and teaching translation

- Dominance establishes a focal point and an order of importance. Consider what wins attention before reading every label.

- Size, contrast, position and empty space work together; the strongest feature should correspond to a meaningful priority.

- Teaching adaptation: the priority changes with state. Preview leads before a plan exists; Apply leads after review and required acknowledgment; the result deserves attention after completion.

[Refined note and captures](notes/15.html)

## 16 · - Using Dominance to Increase Focus - and Decrease Cognitive Effort

Competing emphasis can obscure priorities. Reduce unnecessary competition while preserving readable secondary information.

**Tool application:** Distinguish primary operations, supporting controls and reset/recovery without making any essential label illegible.

**Qualification:** Claims that red/black/white is an unbeatable combination, or that a layout inevitably causes abandonment, are too absolute.

**Review prompt:** What can become quieter without becoming inaccessible?

## Study detail and teaching translation

- When many headings, accents, containers and actions compete at similar strength, the user must work harder to infer priority.

- Reduce unnecessary competition by adjusting the hierarchy as a whole. Do not make secondary but essential information unreadable.

- Teaching adaptation: distinguish the forward workflow from practice Reset. Keep both recognizable, and do not use bright emphasis to encourage an unavailable or unsafe action.

[Refined note and captures](notes/16.html)

## 17 · Creating Dominance with Size, Negative Space and Contrast

Size, negative space and contrast interact to establish emphasis. A small isolated element can be more noticeable than a large busy one.

**Tool application:** Use one intentional accent for an available task action; let decorative headings remain secondary.

**Qualification:** Replace “contrast trumps size every time” with a contextual design hypothesis.

**Review prompt:** Would the action still be apparent without its color?

## Study detail and teaching translation

- Compare an element with its surroundings. Isolation and local contrast can give a small item considerable emphasis; large size alone does not establish priority.

- Negative space is active structure: it separates unrelated items and gives important regions room to be perceived.

- Teaching adaptation: use the same screenshot in original, grayscale and coarse squint views. Inspect whether the intended task action remains prominent without relying entirely on hue.

[Refined note and captures](notes/17.html)

## 18 · Alignment - Leading the Eye Across the Screen

Consistent alignment reduces unnecessary visual paths and helps associate labels with fields.

**Tool application:** Use shared label edges, logical field order and host layout managers; test the smallest supported window.

**Qualification:** Do not repeat unquantified dramatic performance gains. Borders can be necessary to identify controls; removing every boundary is not the goal.

**Review prompt:** Which edge can align without implying an incorrect relationship?

## Study detail and teaching translation

- Alignment creates shared reference lines. Consistent edges help associate labels, fields, rows and groups without adding a rule around every region.

- Simplify a screen into shapes to inspect alignment independently of its detailed content. Restore text afterward to check actual readability and meaning.

- Teaching adaptation: let layout managers express relationships, then test window resizing. Keep borders where they communicate a necessary control boundary or state.

[Refined note and captures](notes/18.html)

## 20 · Proximity - Showing and Communicating Visual Relationships

Closer items tend to be perceived as related. Larger gaps can separate different tasks or information groups.

**Tool application:** Keep a label, its input and its validation message together; separate global actions from per-item controls.

**Qualification:** Proximity is a strong cue, not a universal winner over every other cue.

**Review prompt:** Does the nearest action affect that group or something elsewhere?

## Study detail and teaching translation

- Distance suggests association: nearby items tend to read as a group, and larger gaps can signal a transition to another group.

- Apply proximity to the relationship being communicated. A validation message should be clearly associated with the affected field; a global action should not appear to affect only its nearest row.

- Teaching adaptation: compare within-group gaps with between-group gaps. Use alignment and labels to reinforce relationships where proximity alone is ambiguous.

[Refined note and captures](notes/20.html)

## 21 · - Using Proximity to Make Cognition Faster

Use spacing at several scales: tight relationships inside a group and larger separation between groups.

**Tool application:** Keep an asset’s name, before/after values and result associated, while separating each asset row predictably.

**Qualification:** The source predicts easier scanning; it does not provide a measured time saving for our tool.

**Review prompt:** What grouping does a new tester perceive before you explain it?

## Study detail and teaching translation

- Use more than one spacing scale. A label and value can be close, fields within a section moderately separated, and sections further apart.

- Predictable grouping supports scanning because the viewer can identify meaningful chunks before reading every item.

- Teaching adaptation: keep each asset’s identity and change together, then separate asset rows consistently. Verify the grouping with an unfamiliar reader rather than claiming a specific speed improvement.

[Refined note and captures](notes/21.html)

## 23 · Color - Getting Attention and Communicating Emotion

Color can direct attention, carry learned meaning and support identity when used consistently.

**Tool application:** Reserve semantic colors for meaningful states and pair them with text or recognizable symbols.

**Qualification:** Omit the unsupported dopamine explanation and universal emotional claims. Color associations depend on context and experience.

**Review prompt:** Could the same hue be mistaken for a different state elsewhere?

## Study detail and teaching translation

- Color can attract attention and suggest learned associations, but those associations depend on context and experience.

- Choose color for a communication role—state, emphasis, identity or grouping—rather than adding an accent to every element.

- Teaching adaptation: label warnings and completion explicitly. Keep focus, selection and availability distinct; a single bright hue should not silently stand for all three.

[Refined note and captures](notes/23.html)

## 24 · How Color Influences Interaction

Consistent color roles support continuity. Meaning must remain understandable without color alone.

**Tool application:** Use labels for warning, blocked, complete and selected states; retain focus and shape cues in both light and dark hosts.

**Qualification:** Do not mandate light backgrounds for all long sessions or repeat the transcript’s physiology explanation. Grayscale is not a simulation of all color-vision differences.

**Review prompt:** Can you understand the status when the hue cue is unavailable?

## Study detail and teaching translation

- Once an interface establishes a color cue, consistent reuse helps users predict its meaning. Breaking the cue can create false expectations.

- Evaluate color on the actual background and within the host application. Saturation and competing accents can change the apparent hierarchy.

- Teaching adaptation: a dark editor tool can be appropriate, but its labels and states still need inspection. Test meaning without hue and use color-vision/accessibility checks separately.

[Refined note and captures](notes/24.html)

## 25 · A Word on Color Theory - and Using Color Correctly

Evaluate color by its function: hierarchy, consistency, context and accessible communication.

**Tool application:** Use palette tools for exploration, then assign roles and validate actual foreground/background pairs.

**Qualification:** The lecturer’s dismissal of color theory is opinion. Art fundamentals are useful here and are explicitly retained in this adaptation.

**Review prompt:** What is the purpose of each accent, and does that purpose stay consistent?

## Study detail and teaching translation

- The source favors practical communication over elaborate color-theory exercises. Retain that practical focus without dismissing the value of art fundamentals.

- A palette does not specify which color belongs to which role. Establish surfaces, text, emphasis and semantic states, then test their actual combinations.

- Teaching adaptation: explore options with Coolors, document the chosen roles in the style sheet, and check real text/background pairs rather than judging isolated swatches.

[Refined note and captures](notes/25.html)

## 30 · The Power of Contrast

Contrast means perceivable difference and helps distinguish boundaries and information.

**Tool application:** Separate light/dark value, hue, scale, shape and spacing as different sources of visual distinction.

**Qualification:** Omit the boxing anecdote and the source’s inaccurate attribution. Do not translate a metaphor into a guarantee about attention.

**Review prompt:** Which difference is doing the useful work in this interface?

## Study detail and teaching translation

- Contrast is a relationship between elements or between an element and its surroundings. It can distinguish information, controls and boundaries.

- Light/dark difference, hue, size, shape and spacing contribute different cues. Avoid reducing every contrast problem to selecting a brighter color.

- Teaching adaptation: connect the idea to art value and composition. Keep the specific concepts of HSV Value and relative luminance distinct from perceived lightness.

[Refined note and captures](notes/30.html)

## 31 · Using Contrast to Improve Readability, Attention and Focus

Readable foreground/background differences and deliberate hierarchy help information stand out.

**Tool application:** Keep all essential labels readable; use size, spacing and emphasis to distinguish importance rather than simply fading secondary text.

**Qualification:** Dark versus light theme readability depends on user, environment and typography. Complementary hues do not guarantee sufficient luminance contrast.

**Review prompt:** Can the user read the secondary information they need to act safely?

## Study detail and teaching translation

- Readability depends on the foreground/background pair and the treatment of the text. An attractive palette can still produce difficult labels.

- Emphasis should create a useful hierarchy while leaving supporting information readable. Fading all secondary labels is not a sound default.

- Teaching adaptation: inspect labels, data rows, placeholders, disabled states and focus separately. Use measured contrast as one benchmark; do not infer readability from complementary hue choices.

[Refined note and captures](notes/31.html)

## 32 · Three Essential Functions of Contrast in UI Design

Contrast can direct attention, differentiate related elements and communicate hierarchy.

**Tool application:** Use these as three critique questions for the same tool, rather than three disconnected decoration rules.

**Qualification:** “Contrast always wins” is a memorable course mantra, not an empirical universal law.

**Review prompt:** Where should the strongest emphasis move when the tool changes state?

## Study detail and teaching translation

- Use contrast to direct attention toward the next decision, distinguish elements with different roles, and communicate an order of importance.

- These functions can conflict. For example, a strongly tinted status panel may compete with the action it is intended to explain.

- Teaching adaptation: ask what should dominate in the starting, warning, ready and completed states. One fixed prominent button is not necessarily the right hierarchy for every state.

[Refined note and captures](notes/32.html)

## 33 · How to Determine Appropriate Color and Contrast

A grayscale check helps reveal whether hierarchy depends excessively on hue.

**Tool application:** Compare the original and grayscale tool, then inspect actual contrast pairs and test focus and status cues.

**Qualification:** Grayscale does not prove accessibility, simulate every color-vision deficiency, or measure WCAG ratios. Squinting is a separate coarse hierarchy check.

**Review prompt:** Do the target, warning and next action remain distinguishable?

## Study detail and teaching translation

- Temporarily remove hue to inspect light/dark relationships. Look for regions or states that become hard to distinguish.

- Restore color and inspect actual text/background combinations. A successful grayscale view does not establish adequate text contrast or cover all color-vision differences.

- Teaching adaptation: pair this check with the art squint test and a layout blockout. Each answers a different question; none replaces a person attempting the task.

[Refined note and captures](notes/33.html)

## 43 · Dealing with Data

Choose data presentation according to the question the viewer must answer. Tables support exact lookup; charts support appropriate patterns and comparisons.

**Tool application:** Show affected asset, before/after, unit, status and useful next action. Let the artist inspect details behind a summary.

**Qualification:** Informative graphics still encode selection and framing choices. Avoid declaring a chart bias-free or dismissing all dense views as useless.

**Review prompt:** Does the view answer what changed and what remains uncertain?

## Study detail and teaching translation

- Start with the question the audience needs to answer. Exact lookup, comparison, change over time and distribution are different information needs.

- Tables can preserve precise values; a suitable chart can reveal a pattern. The choice should reflect the task rather than a preference for a visually impressive graphic.

- Teaching adaptation: an asset preview needs identity, proposed change and exceptions. A production overview may benefit from thumbnails and status summaries, with exact records still available.

[Refined note and captures](notes/43.html)

## 44 · Five Rules for Great Data Design

Design data for the user’s context and decisions. Reduce irrelevant decoding work while keeping needed evidence available.

**Tool application:** Summarize affected, skipped and blocked items, with exact records and units available for inspection.

**Qualification:** “Usefulness always decreases with volume” is not universal; experts may need large structured tables. Missing, zero, untested and failed are different states.

**Review prompt:** Which data points let this artist choose the next action?

## Study detail and teaching translation

- The source’s recurring criteria center on useful information, the user’s context, meaningful presentation and avoiding unnecessary decoding. Apply them together rather than optimizing appearance alone.

- Distinguish the essential summary from detail that should remain inspectable. The right amount of information depends on the user and decision.

- Teaching adaptation: show affected, skipped and blocked counts with a route to each record. Keep units and definitions explicit; zero, missing, untested and failed are different meanings.

[Refined note and captures](notes/44.html)

## 45 · Simplifying Visual Information Part 01

Remove redundant decoration and duplicate labels when they do not support interpretation.

**Tool application:** Simplify preview tables and charts while keeping identity, units, scales, exceptions and relevant controls.

**Qualification:** Do not mechanically remove every axis, border or label. Retain them when needed for comparison or correct interpretation.

**Review prompt:** What meaning would be lost by removing this element?

## Study detail and teaching translation

- The chart demonstration removes a decorative background, redundant labeling, unnecessary containers, excessive category colors and misleading three-dimensional effects.

- It then reduces the prominence of guides and labels relative to data, and uses direct values where they make the comparison understandable.

- Teaching adaptation: simplify the preview table by removing visual repetition, not required evidence. Preserve asset names, before/after meaning, units, exceptions and any scale needed for honest comparison.

[Refined note and captures](notes/45.html)

## 46 · Simplifying Visual Information Part 02

Simplify crowded interfaces by clarifying groups, label roles and action hierarchy.

**Tool application:** Use predictable spacing and readable data; distinguish reset, preview and apply by role and current state.

**Qualification:** All-caps labels, low-contrast text, text-only secondary actions and removing every container are examples, not universal prescriptions.

**Review prompt:** Does a quieter control remain visibly actionable and keyboard accessible?

## Study detail and teaching translation

- The interface demonstration first regularizes spacing: outer margins, paragraph separation and padding inside controls and containers.

- It removes redundant rules where spacing or an existing surface already establishes a group. Necessary boundaries remain, and labels are distinguished from values without losing readability.

- It differentiates primary, secondary and less frequent actions, and separates unrelated operations. The particular yellow buttons, all-caps labels and text-link choices are examples rather than universal rules.

- Teaching adaptation: preserve recognizable supporting buttons, keep Reset away from the forward action, and let current readiness determine which action receives emphasis.

[Refined note and captures](notes/46.html)

## 47 · Separating Content from Controls Part 01

Content and controls need distinct, consistent signals so users can predict what is interactive.

**Tool application:** A read-only preview row should not look like an editable field. Buttons need visible labels and state cues.

**Qualification:** Content may legitimately be interactive, such as asset rows that open details. The requirement is clear affordance and consistent behavior, not physical separation of all content.

**Review prompt:** Which elements do users expect to click, and what actually happens?

## Study detail and teaching translation

- Audit the cues that imply interactivity: button shapes, link styling, icons, consistent state changes and learned conventions. A user should be able to make a reasonable prediction before clicking.

- Do not style a static heading like a button or reuse the same strong cue inconsistently for clickable and non-clickable content.

- Teaching adaptation: a preview can be read-only while an asset row opens details. Make that distinction discoverable. When users call a view “busy,” investigate competing priorities rather than assuming a specific cause.

[Refined note and captures](notes/47.html)

## 48 · Separating Content from Controls Part 02

Differentiate primary, secondary and consequential actions without losing discoverability or familiar conventions.

**Tool application:** Keep Reset away from the forward workflow; emphasize Preview until a reviewed plan allows Apply. Preserve recognizable secondary buttons.

**Qualification:** Do not teach that Cancel must always be a text link, or that full-width buttons are always wrong. The final source mantra number conflicts with recap 49; use topic names.

**Review prompt:** Can an unfamiliar artist predict the consequence of each action?

## Study detail and teaching translation

- Actions differ in priority and consequence. A forward action, draft/save operation and cancellation need a clear hierarchy, but all must remain recognizable and operable.

- The source demonstrates stronger primary emphasis, quieter supporting actions, conventional navigation, clearer field boundaries and removing button-like framing from headings.

- Teaching adaptation: use host conventions and explicit verbs. Keep disabled, secondary and destructive actions conceptually distinct; a neutral appearance does not mean a control is disabled.

- The final mantra number in this lesson conflicts with the recap. Use “separate content from controls” as the topic label rather than repeating the inconsistent number.

[Refined note and captures](notes/48.html)

## 49 · Recap - UI Design Mantras

The recap collects recurring principles about purpose, context, hierarchy, color, data and interaction cues.

**Tool application:** Use the five Week 7 teaching mantras as a smaller, task-oriented structure; retain this recap as the source crosswalk.

**Qualification:** The transcript has substantial speech-recognition errors. Its references to typography/icons do not establish completion or detailed notes for those omitted lessons.

**Review prompt:** Which principle explains a specific observation from the peer test?

## Study detail and teaching translation

- The following 19 items are repaired paraphrases of the supplied recap, not verbatim quotations. Missing detailed lessons remain missing; their recap mentions are not expanded into fabricated transcripts.

- 1. Design solves and communicates a problem; it is more than decoration. → Know the task.

- 2. Solve the problem of this audience and context rather than copying a different product’s solution. → Know the task.

- 3. Function alone does not determine an understandable form. → Know the task / Make actions clear.

- 4. Multiple forces and constraints shape the final design. → Know the task.

- 5. Small surfaces require reconsidering what belongs there. → Guide the eye.

- 6. Balance organizes visual weight and relationships. → Guide the eye.

- 7. Rhythm establishes recognizable repetition. → Guide the eye.

- 8. Harmony makes the parts work together. → Keep a shared visual language.

- 9. Dominance establishes a focal point. → Guide the eye.

- 10. Alignment creates an organized set of relationships. → Guide the eye.

- 11. Proximity groups related content. → Guide the eye.

- 12. Color should communicate and support interaction. → Keep a shared visual language.

- 13. Context, associations and branding inform color selection. → Keep a shared visual language.

- 14. Contrast is powerful for differentiation and emphasis; the source’s absolute “always” is qualified. → Guide the eye.

- 15. Typography should be intentional and readable; the detailed typography lessons were not supplied. → Keep a shared visual language.

- 16. Icons should support recognition; the detailed icon lessons were not supplied. → Make actions clear.

- 17. The user’s data question should determine its visual form. → Know the task / Guide the eye.

- 18. Remove unnecessary complexity while preserving useful information and cues. → Guide the eye / Make actions clear.

- 19. Clearly distinguish what can be read from what can be acted upon. → Make actions clear.

- Test the whole workflow is the integrating Week 7 mantra drawn from the existing lecture and testing method. It is not claimed as a twentieth Joe Natoli mantra.

[Refined note and captures](notes/49.html)
