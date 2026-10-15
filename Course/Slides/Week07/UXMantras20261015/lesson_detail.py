"""Expanded study detail: paraphrased course ideas, with explicit tool adaptations."""
DETAILS={
1:[
 'Begin with the problem being solved, not a collection of attractive components. Labels, grouping, hierarchy and available actions all communicate an interpretation of that problem.',
 'Distinguish visual polish from usefulness. A visually coherent interface can still make the wrong decision prominent or omit information needed to finish the task.',
 'Teaching adaptation: identify the intended artist, inputs, result and consequences before critiquing the material tool. Keep aesthetic decisions connected to those answers.'
],
2:[
 'A reference carries assumptions about its audience, business purpose, frequency of use and environment. Copying its appearance also imports some of those assumptions.',
 'Extract the principle behind a reference—clear grouping, recognizable navigation or a distinct next action—then test that principle in the new context.',
 'Teaching adaptation: a store page, game HUD and asset-processing panel can share visual principles while requiring different density, interaction speed and levels of explanation.'
],
3:[
 'Functional requirements leave many presentation choices open. The same operation can be difficult or straightforward depending on terminology, grouping and the order of decisions.',
 'Consider appearance and behavior together. A control’s shape and placement imply what it does; implementation must honor that implication.',
 'Teaching adaptation: expose the material operation as a reviewable artist workflow rather than a direct list of API arguments. Preserve technical detail where it supports inspection.'
],
4:[
 'The source warns against treating a slogan or principle as an automatic recipe. Context, constraints and the relationships between parts affect the result.',
 'Use a principle to generate a testable design question. For example, does aligning these fields make their relationship clearer, or imply a relationship that is not real?',
 'Teaching adaptation: compare alternatives with the same task, prepared inputs and success checks. An explanation of intent is not a substitute for observing an attempt.'
],
5:[
 'Implementation model: how the system actually works. Mental model: how the user believes the task or system works. Represented model: what the interface presents.',
 'Choose representations that help the user reason about the operation. A technically precise internal term can still be a poor everyday label.',
 'Teaching adaptation: duration is often a useful artist-facing concept even if the underlying effect has separate creation and termination events. Keep detailed controls available when the artist actually needs them.'
],
6:[
 'This file repeats lesson 04 rather than providing new lesson content. Preserve it as source history and cross-reference 04.',
 'The recap describes the influence of multiple forces and constraints on the final design, but that summary cannot reconstruct the missing distinct lesson.'
],
7:[
 'A smaller surface is not a large interface shrunk proportionally. Reassess what must remain visible and what can be deferred.',
 'Reduction should preserve the clues needed to recognize purpose, current state and the next action. Removing those clues creates uncertainty instead of simplicity.',
 'Teaching adaptation: test a narrow editor panel. Keep the target and consequence visible while moving optional detail into a disclosed area; avoid making essential scope discoverable only on hover.'
],
8:[
 'Screen dimensions, input method and circumstances of use change interaction requirements. Touch, mouse, keyboard and controller input are not interchangeable.',
 'Repeated text entry can be a source of friction. Selection, presets and sensible defaults may help when the artist can still inspect and correct them.',
 'Teaching adaptation: verify keyboard traversal and resizing in the desktop tool. Treat in-game or VR UI as a different test environment rather than converting desktop pixel dimensions into a universal rule.'
],
9:[
 'Visual weight comes from more than physical size: density, contrast, isolation and surrounding space affect the composition.',
 'Balance can be symmetrical or asymmetrical. The objective is a readable relationship between regions, not equal quantities on both sides.',
 'Teaching adaptation: compare the weight of inputs, review information and actions. A large empty table may be acceptable as a stable work area, but it should not obscure the next available action.'
],
10:[
 'Inspect the existing structure before redesigning it: unequal gutters, cramped margins and weak separation can make otherwise sensible groups difficult to read.',
 'Change a small set of relationships, then compare the result using the same content. This makes the reason for the improvement easier to explain.',
 'Teaching adaptation: use matched material-preview captures. Distinguish a design demonstration from a measured claim about faster task completion.'
],
11:[
 'Repetition creates an expectation: users learn where a label, value, status or action will appear in the next instance.',
 'Intervals participate in the pattern. Consistent spacing within a group and between repeated groups can make the sequence easier to scan.',
 'Teaching adaptation: keep asset identity, before, after and status in a predictable order. Reserve a deliberate pattern break for an exception that deserves attention.'
],
12:[
 'Harmony means the parts support a coherent whole. Related shapes, typography, spacing and color roles can make separate regions feel connected.',
 'Similarity should correspond to meaning. Reusing one treatment for unrelated states creates visual consistency but semantic confusion.',
 'Teaching adaptation: use shared form patterns and state labels across Material Setup and VFX Placement. Preserve host-specific differences that serve a real interaction need.'
],
13:[
 'Directional flow emerges from alignment, grouping, repetition and changes in emphasis; it is not limited to adding arrows.',
 'A strong starting point should lead toward the next relevant information. Multiple unrelated focal points can interrupt the intended sequence.',
 'Teaching adaptation: organize source inputs, scope, reviewed consequence and Apply in the order the artist needs them. Test the reading route rather than assuming a universal scanning pattern.'
],
14:[
 'Repeated field treatment helps the user recognize a form as a sequence of related decisions. Consistent labels, widths and gaps reduce unnecessary variation.',
 'The action should be recognizable as a control and distinct from descriptive headings. A purposeful change in treatment can mark the transition from entering information to acting.',
 'Teaching adaptation: use Qt form layouts and explicit button labels. The course example’s narrower button is one solution; a full-width primary action can also be appropriate in a narrow game-tool panel.'
],
15:[
 'Dominance establishes a focal point and an order of importance. Consider what wins attention before reading every label.',
 'Size, contrast, position and empty space work together; the strongest feature should correspond to a meaningful priority.',
 'Teaching adaptation: the priority changes with state. Preview leads before a plan exists; Apply leads after review and required acknowledgment; the result deserves attention after completion.'
],
16:[
 'When many headings, accents, containers and actions compete at similar strength, the user must work harder to infer priority.',
 'Reduce unnecessary competition by adjusting the hierarchy as a whole. Do not make secondary but essential information unreadable.',
 'Teaching adaptation: distinguish the forward workflow from practice Reset. Keep both recognizable, and do not use bright emphasis to encourage an unavailable or unsafe action.'
],
17:[
 'Compare an element with its surroundings. Isolation and local contrast can give a small item considerable emphasis; large size alone does not establish priority.',
 'Negative space is active structure: it separates unrelated items and gives important regions room to be perceived.',
 'Teaching adaptation: use the same screenshot in original, grayscale and coarse squint views. Inspect whether the intended task action remains prominent without relying entirely on hue.'
],
18:[
 'Alignment creates shared reference lines. Consistent edges help associate labels, fields, rows and groups without adding a rule around every region.',
 'Simplify a screen into shapes to inspect alignment independently of its detailed content. Restore text afterward to check actual readability and meaning.',
 'Teaching adaptation: let layout managers express relationships, then test window resizing. Keep borders where they communicate a necessary control boundary or state.'
],
20:[
 'Distance suggests association: nearby items tend to read as a group, and larger gaps can signal a transition to another group.',
 'Apply proximity to the relationship being communicated. A validation message should be clearly associated with the affected field; a global action should not appear to affect only its nearest row.',
 'Teaching adaptation: compare within-group gaps with between-group gaps. Use alignment and labels to reinforce relationships where proximity alone is ambiguous.'
],
21:[
 'Use more than one spacing scale. A label and value can be close, fields within a section moderately separated, and sections further apart.',
 'Predictable grouping supports scanning because the viewer can identify meaningful chunks before reading every item.',
 'Teaching adaptation: keep each asset’s identity and change together, then separate asset rows consistently. Verify the grouping with an unfamiliar reader rather than claiming a specific speed improvement.'
],
23:[
 'Color can attract attention and suggest learned associations, but those associations depend on context and experience.',
 'Choose color for a communication role—state, emphasis, identity or grouping—rather than adding an accent to every element.',
 'Teaching adaptation: label warnings and completion explicitly. Keep focus, selection and availability distinct; a single bright hue should not silently stand for all three.'
],
24:[
 'Once an interface establishes a color cue, consistent reuse helps users predict its meaning. Breaking the cue can create false expectations.',
 'Evaluate color on the actual background and within the host application. Saturation and competing accents can change the apparent hierarchy.',
 'Teaching adaptation: a dark editor tool can be appropriate, but its labels and states still need inspection. Test meaning without hue and use color-vision/accessibility checks separately.'
],
25:[
 'The source favors practical communication over elaborate color-theory exercises. Retain that practical focus without dismissing the value of art fundamentals.',
 'A palette does not specify which color belongs to which role. Establish surfaces, text, emphasis and semantic states, then test their actual combinations.',
 'Teaching adaptation: explore options with Coolors, document the chosen roles in the style sheet, and check real text/background pairs rather than judging isolated swatches.'
],
30:[
 'Contrast is a relationship between elements or between an element and its surroundings. It can distinguish information, controls and boundaries.',
 'Light/dark difference, hue, size, shape and spacing contribute different cues. Avoid reducing every contrast problem to selecting a brighter color.',
 'Teaching adaptation: connect the idea to art value and composition. Keep the specific concepts of HSV Value and relative luminance distinct from perceived lightness.'
],
31:[
 'Readability depends on the foreground/background pair and the treatment of the text. An attractive palette can still produce difficult labels.',
 'Emphasis should create a useful hierarchy while leaving supporting information readable. Fading all secondary labels is not a sound default.',
 'Teaching adaptation: inspect labels, data rows, placeholders, disabled states and focus separately. Use measured contrast as one benchmark; do not infer readability from complementary hue choices.'
],
32:[
 'Use contrast to direct attention toward the next decision, distinguish elements with different roles, and communicate an order of importance.',
 'These functions can conflict. For example, a strongly tinted status panel may compete with the action it is intended to explain.',
 'Teaching adaptation: ask what should dominate in the starting, warning, ready and completed states. One fixed prominent button is not necessarily the right hierarchy for every state.'
],
33:[
 'Temporarily remove hue to inspect light/dark relationships. Look for regions or states that become hard to distinguish.',
 'Restore color and inspect actual text/background combinations. A successful grayscale view does not establish adequate text contrast or cover all color-vision differences.',
 'Teaching adaptation: pair this check with the art squint test and a layout blockout. Each answers a different question; none replaces a person attempting the task.'
],
43:[
 'Start with the question the audience needs to answer. Exact lookup, comparison, change over time and distribution are different information needs.',
 'Tables can preserve precise values; a suitable chart can reveal a pattern. The choice should reflect the task rather than a preference for a visually impressive graphic.',
 'Teaching adaptation: an asset preview needs identity, proposed change and exceptions. A production overview may benefit from thumbnails and status summaries, with exact records still available.'
],
44:[
 'The source’s recurring criteria center on useful information, the user’s context, meaningful presentation and avoiding unnecessary decoding. Apply them together rather than optimizing appearance alone.',
 'Distinguish the essential summary from detail that should remain inspectable. The right amount of information depends on the user and decision.',
 'Teaching adaptation: show affected, skipped and blocked counts with a route to each record. Keep units and definitions explicit; zero, missing, untested and failed are different meanings.'
],
45:[
 'The chart demonstration removes a decorative background, redundant labeling, unnecessary containers, excessive category colors and misleading three-dimensional effects.',
 'It then reduces the prominence of guides and labels relative to data, and uses direct values where they make the comparison understandable.',
 'Teaching adaptation: simplify the preview table by removing visual repetition, not required evidence. Preserve asset names, before/after meaning, units, exceptions and any scale needed for honest comparison.'
],
46:[
 'The interface demonstration first regularizes spacing: outer margins, paragraph separation and padding inside controls and containers.',
 'It removes redundant rules where spacing or an existing surface already establishes a group. Necessary boundaries remain, and labels are distinguished from values without losing readability.',
 'It differentiates primary, secondary and less frequent actions, and separates unrelated operations. The particular yellow buttons, all-caps labels and text-link choices are examples rather than universal rules.',
 'Teaching adaptation: preserve recognizable supporting buttons, keep Reset away from the forward action, and let current readiness determine which action receives emphasis.'
],
47:[
 'Audit the cues that imply interactivity: button shapes, link styling, icons, consistent state changes and learned conventions. A user should be able to make a reasonable prediction before clicking.',
 'Do not style a static heading like a button or reuse the same strong cue inconsistently for clickable and non-clickable content.',
 'Teaching adaptation: a preview can be read-only while an asset row opens details. Make that distinction discoverable. When users call a view “busy,” investigate competing priorities rather than assuming a specific cause.'
],
48:[
 'Actions differ in priority and consequence. A forward action, draft/save operation and cancellation need a clear hierarchy, but all must remain recognizable and operable.',
 'The source demonstrates stronger primary emphasis, quieter supporting actions, conventional navigation, clearer field boundaries and removing button-like framing from headings.',
 'Teaching adaptation: use host conventions and explicit verbs. Keep disabled, secondary and destructive actions conceptually distinct; a neutral appearance does not mean a control is disabled.',
 'The final mantra number in this lesson conflicts with the recap. Use “separate content from controls” as the topic label rather than repeating the inconsistent number.'
],
49:[
 'The following 19 items are repaired paraphrases of the supplied recap, not verbatim quotations. Missing detailed lessons remain missing; their recap mentions are not expanded into fabricated transcripts.',
 '1. Design solves and communicates a problem; it is more than decoration. → Know the task.',
 '2. Solve the problem of this audience and context rather than copying a different product’s solution. → Know the task.',
 '3. Function alone does not determine an understandable form. → Know the task / Make actions clear.',
 '4. Multiple forces and constraints shape the final design. → Know the task.',
 '5. Small surfaces require reconsidering what belongs there. → Guide the eye.',
 '6. Balance organizes visual weight and relationships. → Guide the eye.',
 '7. Rhythm establishes recognizable repetition. → Guide the eye.',
 '8. Harmony makes the parts work together. → Keep a shared visual language.',
 '9. Dominance establishes a focal point. → Guide the eye.',
 '10. Alignment creates an organized set of relationships. → Guide the eye.',
 '11. Proximity groups related content. → Guide the eye.',
 '12. Color should communicate and support interaction. → Keep a shared visual language.',
 '13. Context, associations and branding inform color selection. → Keep a shared visual language.',
 '14. Contrast is powerful for differentiation and emphasis; the source’s absolute “always” is qualified. → Guide the eye.',
 '15. Typography should be intentional and readable; the detailed typography lessons were not supplied. → Keep a shared visual language.',
 '16. Icons should support recognition; the detailed icon lessons were not supplied. → Make actions clear.',
 '17. The user’s data question should determine its visual form. → Know the task / Guide the eye.',
 '18. Remove unnecessary complexity while preserving useful information and cues. → Guide the eye / Make actions clear.',
 '19. Clearly distinguish what can be read from what can be acted upon. → Make actions clear.',
 'Test the whole workflow is the integrating Week 7 mantra drawn from the existing lecture and testing method. It is not claimed as a twentieth Joe Natoli mantra.'
]}
