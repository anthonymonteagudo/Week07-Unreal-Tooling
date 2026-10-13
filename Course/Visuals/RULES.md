# A reusable visual system for Technical Art

This system carries the Week 1 identity into Week 2 and future lectures. It supports the instructor's existing deck, rather than replacing its entire theme. The library has three roles: original Week 1 lens badges, simple companion icons, and explanatory diagrams. [Open the gallery](index.html) for direct previews and usable files.

## What remains consistent

The source is **Week 1 - Intro to Tech Art - STUDENT.pptx**, especially slides 78 and 82. The source hash, original fonts, exact lens colors, and extracted assets are recorded in [tokens.json](tokens.json). The four 1024×1024 lens PNGs are unmodified byte extractions with genuine alpha transparency. Their original external provenance is not established by the presentation; preserve them as existing course assets without inventing attribution.

| Element | Course convention | Week 2 use |
|---|---|---|
| Constraints | Original badge; coral `#FC4037` | Intended camera, acceptable silhouette, platform or asset requirements |
| Systems | Original badge; teal `#029990` | Mesh, assignments, textures, importer and dependencies |
| Leverage | Original badge; gold `#ED9C03` | A reusable rule or shared source of truth |
| Throughput | Original badge; blue `#0163D5` | Reimport reliability, reduced repeated repair |
| Core drawing | Dark navy `#0A4054`, white, restrained teal | Shared outline, labels, connectors, focal relationship |
| Week 2 context | Existing deep-purple deck/review headings may surround the shared assets | Contextual compatibility; do not reassign the four lens colors |
| Typography | Native slides retain Posterama/Avenir where already available; Consolas for code | New portable SVG/PNG starters explicitly use Arial fallback. No font files distributed and no exact-font claim. |

Artistic intent is not a fifth analytical lens. It states what should be preserved, and the four lenses help frame the work needed to preserve it. Likewise, a red icon must not silently mean both Constraints and FAIL. The status icons use distinct shapes and explicit PASS, FAIL, or REVIEW labels in a neutral ink.

## Icons: reuse, find, draw, or generate

1. **Reuse** the manifest entry when its meaning matches. Select the variant needed for the actual background. Keep a familiar symbol's meaning stable across weeks.
2. **Find** an icon when a recognizable symbol is missing. [Lucide](https://github.com/lucide-icons/lucide) is a candidate vector family; check its [ISC and inherited Feather notices](https://github.com/lucide-icons/lucide/blob/main/LICENSE) for the selected artwork. [Openverse](https://docs.openverse.org/) helps locate media, but verify the original item's creator, license, and attribution. Do not equate a search engine's code license with the returned artwork's rights.
3. **Draw** a simple new symbol as SVG when deterministic geometry is suitable. The starter companion set is original code-authored artwork, not copied Lucide icons. Use its 64-unit grid, 2.5-unit round stroke, clear silhouette, and generous edge clearance. Avoid decorative gradients, glossy 3D, tiny internal detail, and baked-in text.
4. **Generate** a bespoke raster illustration only when that medium helps explain the topic. Use ImageGen with the selected course references. Request an isolated object with actual alpha transparency, matched perspective, flat shapes, restrained colors, and no lettering. Record the prompt, tool, reference assets, date, and edits. Reject generated UI or generated scientific evidence presented as real captures.

Suggested raster-generation brief: “Create one isolated [subject] for a Technical Art teaching slide, matching the attached approved course reference. Dark navy outlines, restrained teal accent, simple readable silhouette, consistent perspective, no text, no glow, no drop shadow, genuine transparent background. This illustrates [role], not a software screenshot.” Adjust the brief for the actual subject instead of making every object look like a generic technology badge.

The new companion icons export as **256² and 512² PNGs**, each in ink and white. Keep their SVG masters. Test alpha values, transparent margins, and readable silhouettes at approximately 32–64 displayed pixels. Preview on white, the Week 2 paper color, and dark navy. A checkerboard baked into RGB is a failed transparent export. Do not remove a background from an existing bitmap with an unreviewed heuristic that erases parts of the object.

The four elaborate Week 1 badges remain a separate, stable family for the four lenses. The simpler companion symbols label content and actions within slides. They do not replace those badges or compete with screenshots.

## Diagrams: a consistent language with an explicit job

Use `diagram-design` with [the course profile](diagram-profile.md). The profile is project-scoped and does not overwrite the installed package. The course skill and profile installation instructions are in [the build instructions](BUILD.md).

- Keep one teaching question per diagram. Choose a relationship overview, ordered process, comparison, or numerical illustration deliberately. Split overview from detail when the labels or relationships become unreadable.
- Use 1280×720 logical coordinates and a 2560×1440 PNG export for the slide starters. Prefer 24–28 px node labels, 32–44 px headings, and at least 20 px secondary text at the logical size. These are working conventions to inspect in the actual slide, not universal legibility thresholds.
- Use ordinary labels for people and concepts. Keep code-like labels for actual data, indices, values, and identifiers. Leave long citations in an adjacent source note or clean reader page.
- Align the primary flow left to right or top to bottom. Use clear arrowheads and rounded orthogonal turns. Avoid crossing paths, hidden endpoints, and a label sitting across its connector. Explain what a dashed path means in that diagram.
- Use teal for one or two focal relationships. The four lens colors appear when those lenses are the subject. Never use color as the only information channel.
- Keep node and arrow meanings technically accurate. A material graph, an optional instance, assignment, shader compilation, and runtime rendering are related but distinct. A dependency arrow is not automatically a chronological processing step.
- Pair schematics with real evidence when the learner must operate a control. Use actual Maya/Unreal captures with version and relevant setting visible. A generic icon does not teach which asset is assigned to a component.
- Keep source SVG, exported PNG, a clean HTML preview, semantic description, intended slides, and conceptual sources together. Mark illustrative content and prepared captures honestly.

### Instructor preference: transparent, concise, concrete

These defaults apply to every new or revised diagram. They supersede the earlier white-canvas starter style; unchanged older starters are not examples of the revised standard.

| Requirement | Apply it this way |
|---|---|
| Transparent | No full-canvas fill or white matte. Export RGBA with zero-alpha margins and gaps. Screenshot rectangles keep their original backgrounds; do not erase genuine UI. |
| Minimal text | Usually 1–4 words per label: Texture, UVs, Material graph, Assign. Preserve necessary distinctions such as optional and parent. Move sentences, teaching prompts, qualifications, and long credits to HTML and notes. Avoid oversized title bands and deck-like footers baked into the asset. |
| Strong route | Use bold 5–6 px primary strokes at 1280×720, substantial arrowheads, generous spacing, and one obvious main route. Secondary optional paths can use 4 px dashed strokes with an explicit meaning. Label ambiguous relationships. Number only an actual sequence, or identify numbers as a teaching walkthrough in the HTML. |
| Real context first | Use actual cropped texture samples, UV layouts, mesh views, controls, assignments, and results. Prefer matching views of one asset. Generic icons may orient the viewer but do not replace obtainable evidence. Keep the GPU internals closed for the introductory Week 2 overview. |
| Honest crops | Preserve source pixels and aspect ratios. Retain the relevant control name, value, and asset context where needed. Record the original file/URL, credit, version if known, crop rectangle, and any scaling. Identify node-preview thumbnails as thumbnails rather than full-resolution texture exports. |
| Mixed examples | Mark separate examples in the diagram and explain the distinction next to it in HTML. An unrelated UV layout must not be presented as the mapping of the displayed mesh; a different instance must not be presented as the parent of the result. |
| Useful detail | At lecture size the image should identify the real thing; the review must link to its original or an enlarged crop for inspection. Do not reconstruct unreadable UI or use generated detail to impersonate a better screenshot. |

Use a diagram as an overview plus a guided reveal: main route first, optional branches second. Put the full explanation and read-aloud wording in the clean diagram page and the relevant review entry. Keep alt text/semantic descriptions outside visible diagram labels. Test on white and the Week 2 slide paper color; transparent navy artwork needs a deliberate alternate ink treatment for dark slides.

## Specific starter uses

| Asset | Proposed placement | Intended teaching use |
|---|---|---|
| Original four lens badges | 30, 62, 136 | Recall Week 1 questions while applying them to an asset handoff or repeated check |
| intent + inspect icons | 28, 52, 117 | Separate intended appearance from the evidence that supports a technical conclusion |
| mesh / texture / material / skeleton | Anatomy sections | Mark which asset representation is being discussed; show its actual contents alongside |
| question icon | Existing 15 discussion pauses | Make the invitation visible beside its specific prompt |
| appendix icon | Named Explore further pointers | Identify an optional route with a title and a return link |
| record / reset / status icons | Museum and documentation | Label evidence, starting state, and the scope of a check |
| visual-intent-to-check diagram | 28, then revisit at 52 or 117 | A short live art-lens bridge linked to a concrete inspection |
| maya-unreal-handoff diagram | 62 / 83 | Orient the recorded or live assignment/reimport demonstration |
| material-relationships diagram | 100 / 102 | Trace parent, instance, assignment, and renderer relationships while keeping GPU details closed |

Do not add every icon to every slide. Use one when it helps recognition or navigation. The library is reusable because its meanings are stable, not because every slide contains the whole set.

## Review and provenance

The asset manifest records the ID, role, editable source, PNG exports, method, provenance, and intended use. For a fetched or generated addition, also record exact source URL, author/license or generation details, and modifications. Preserve existing versions when their meaning changes; do not silently overwrite an icon that now stands for a different concept.

The HTML review should show the actual asset preview, a direct download, the intended slide, and the instructional reason for using it. Link prepared documents to clean reader views; keep original Markdown/CSV and primary external sources as clearly labeled secondary links. Do not strip attribution or misrepresent a locally prepared explanation as a reproduced primary source.
