# Technical Art course wiki

Open [index.html](index.html). The generated pages work directly from disk, including search; no local server or account is needed. This is a local working edition in Perforce, not a published website or a browser-editable collaborative wiki service.

## Edit and build

Content lives in `content/*.md`. Each file has a small front-matter block: `title`, `group`, `order`, `status`, `summary`, and `updated` (YYYY-MM-DD). Keep page filenames stable. The build derives navigation, the table of contents, and search from these files.

With Node installed:

```powershell
npm install
npm run build
```

The project pins `marked` 17.0.5, matching the bundled runtime used for this edition. If using Codex's existing Node dependency bundle, set `COURSE_NODE_MODULES` to the bundle's `node_modules` directory and run `node tools/build.mjs`; the build can resolve `marked` there without another installation. The generated pages have no external JavaScript or CSS dependency.

Use [templates/week.md](templates/week.md) and [templates/topic.md](templates/topic.md) to extend the course. A new content page enters navigation automatically through its group and order. `Planned` produces the explicit outline label. `Preview` distinguishes Week 3's proposed exercise from a finalized lesson.

## Current scope

- Developed study pages for Weeks 1–2, a Week 3 Python preview, and syllabus-based outlines for Weeks 4–12.
- Topic explanations, a museum investigation companion, an exhibit design guide, documentation example and template, glossary, and curated readings/visuals.
- Real Epic and Khronos images copied from existing reviewed course resources, with provenance in [assets/images/README.md](assets/images/README.md).
- Instructor revision proposals remain in `../Slides`. The student's topic pages provide explanation and diagnostic questions rather than copying the full museum repair manifest.

This is the first iteration of a full-course structure. Later weeks have useful guiding questions but are not represented as completed lecture material. Add specific examples and approved assignments as those weeks are developed.

## Source grounding and inspiration

Course sequencing comes from the local Fall 2026 syllabus and the existing Week 1 and Week 2 deck reviews. The current instructor direction changes Week 2's assignment to creating a museum exhibit; this wiki does not inherit the older syllabus assignment name or invent replacement policies.

The instructor requested inspiration from [CCS Entertainment Arts: Modeling/Texturing 2.0](http://ccsentertainmentarts.wikidot.com/modeling-texturing-2-0). The page could not be retrieved by the available browser/search tools on 8 September 2026. Its content, layout, and claims were not copied or represented as inspected. This first structure uses the instructor's requested weekly expansion, fundamentals, practical inspection, and curated-resource goals. Refine the navigation when the instructor identifies the aspects of that reference to preserve.

## Verification

Run `node --check tools/build.mjs` and `node --check assets/wiki.js`, then rebuild. `../Tools/verify_course.py` checks generated local links, required pages, unique anchors, image availability, and the illustrative Python exercise. The browser tools' local-file restriction prevented a rendered-preview check in this session; structural checks do not claim classroom playback or browser-layout verification.

## Perforce contents

Version Markdown, templates, build code, styles/scripts, generated HTML/search data, and required image assets. Ignore `node_modules`, Python caches, and PowerPoint lock files. Add future changes in a focused changelist. The first edition is intended to be shelved for review; see the root course README for the actual changelist status.
