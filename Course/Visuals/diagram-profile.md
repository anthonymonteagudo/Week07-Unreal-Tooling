<!-- diagram-design-profile
name: Technical Art course
slug: tech-art-course
source-url: none
created: 2026-09-09
updated: 2026-09-09
notes: Derived from the existing Week 1 student deck; course tokens and manifest are canonical.
-->
# Style Guide

Course profile for slide diagrams, based on Week 1 slides 78 and 82. Preserve the established four lens badges and meanings. The Week 2 deck may retain its existing surrounding purple/serif theme while using these shared assets. Use the course's tokens.json and RULES.md for provenance and asset roles. Do not modify the diagram-design installation's global style guide.

## Tokens

### Semantic roles

| Role | Purpose | Light | Dark |
|---|---|---|---|
| `paper` | Preview background only; export canvas is transparent | `#FFFFFF` | `#0A4054` |
| `paper-2` | Secondary surface | `#F2F6F7` | `#163F4D` |
| `ink` | Text and primary strokes | `#0A4054` | `#FFFFFF` |
| `muted` | Connectors and supporting labels | `#4B6070` | `#C8DEE5` |
| `soft` | Secondary labels | `#586B78` | `#B6D0DB` |
| `rule` | Subtle separators | `rgba(10,64,84,0.16)` | `rgba(255,255,255,0.20)` |
| `rule-solid` | Strong separators | `#C9D7DD` | `#607E8A` |
| `accent` | One or two focal items | `#029990` | `#9FD1D0` |
| `accent-tint` | Focal fill | `#E4F2F1` | `#204F57` |
| `link` | Navigation or explicitly named external relationship | `#0163D5` | `#9FD1D0` |

The four-lens colors are semantic reservations: Constraints `#FC4037`, Systems `#029990`, Leverage `#ED9C03`, Throughput `#0163D5`. When color denotes one of those lenses, display its name. Status results use explicit words and distinguishable shapes, rather than repurposing these colors silently.

## Typography

| Role | Family | Size at 1280×720 | Weight | Usage |
|---|---|---|---|---|
| `title` | Arial, sans-serif (declared fallback for Posterama) | 44px | 700 | Diagram title |
| `node-name` | Arial, sans-serif (declared fallback for Avenir Next LT Pro) | 28px | 700 | Entity or concept |
| `sublabel` | Consolas, monospace for code; Arial for prose | 24px | 400 | Data or explanation |
| `eyebrow` | Arial, sans-serif | 20px | 700 | Small topic label |
| `arrow-label` | Arial, sans-serif | 20px | 400 | Relationship |
| `callout` | Arial, sans-serif | 32px | 400 | Teaching question |

The native Week 1 fonts are Posterama and Avenir Next LT Pro Light. They are not redistributed here. The portable diagram starters deliberately use Arial and are labeled as fallback typography. Retain native fonts for editable labels within the instructor's deck when available. Never claim an exact font match from an unverified CSS declaration.

## Geometry and export

Use the selected diagram type's connector grammar with a 4-unit layout grid, 8-unit rounded turns, generous image/label clearance, and bold 5–6-unit primary strokes. Use substantial arrowheads; optional paths may use 4-unit dashed strokes. Use 1280×720 logical coordinates, SVG masters, and 2560×1440 slide PNGs. Keep labels legible at the actual placement size. No shadows or decorative dot patterns. New and revised diagrams have a transparent canvas and genuine alpha PNG exports. Screenshot rectangles retain their native backgrounds; the surrounding canvas has no white matte or checkerboard. Preview background colors are not exported.

Keep one teaching question and a small enough set of relationships to trace. Visible labels are short noun phrases, usually 1–4 words; arrow verbs are brief. Full sentences, context, teaching questions, caveats, and sources belong in HTML and notes. Avoid title furniture and word-filled boxes. In Week 2, GPU implementation remains one box. A dependency map is not a claim about exact chronological execution.

Build concrete diagrams around real cropped textures, UV layouts, Maya/UE controls, mesh assignments, and observed results. Prefer one asset across views; visibly label separate examples and explain mixed sources in HTML. Preserve source pixels, aspect ratio, original files, source credit, crop bounds, and known software version. Provide original/enlarged crops for inspection. A generic icon or generated UI is not a substitute for available evidence. Inspect alpha and legibility on the actual slide background.
