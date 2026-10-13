# Build and maintain course visuals

Canonical rules and tokens live in this directory. The discoverable skill is installed from `../Skills/course-visuals/SKILL.md`. Future edits should update that tracked source, then refresh the installed copy.

Run with Node.js and the `sharp` package available:

```powershell
node Course/Visuals/Source/build_visuals.mjs
python -B Course/Visuals/Source/verify_visuals.py
```

Set `COURSE_NODE_MODULES` if the bundled dependency path in the script is unavailable. The generator uses only local vector geometry and assets. It never downloads artwork or edits PowerPoint. The four legacy PNGs and Week 1 reference slide exports are stored snapshots; do not recreate or substitute them from a different deck without updating provenance.

The revised material diagram is authored in `Source/material_relationships.mjs`. It uses genuine rectangular crops from existing Epic screenshots and the current deck's UV illustration. The generator records original hashes, native dimensions, crop rectangles, source pages, and credit in the manifest. `Diagrams/MaterialImages` contains the reusable crop PNGs; the SVG embeds their bytes for portability. `Reference/week2-uv-source.png` is the unmodified `ppt/media/image113.png` from the refined deck, current slide 54. The original material diagram is retained in `Reference/material-relationships-before.*` for old → new comparison. The two unchanged earlier diagrams remain legacy white-canvas starters; new and revised work follows the transparent standard.

`verify_visuals.py` verifies alpha for diagrams marked transparent and compares every crop's decoded pixels with the declared rectangle in its original. Inspect composition and legibility separately. Paper/white preview composites are QA aids, not replacement slide PNGs. Browser visual QA remains unavailable where a browser policy restriction has been returned; do not bypass that restriction to inspect local HTML.

Run the profile/skill installer from the workspace root:

```powershell
python -B Course/Visuals/Source/install_course_visuals.py
```

It copies the tracked course skill to the user's `.codex/skills/course-visuals` directory and the tracked diagram profile to `.diagram-design/profiles/tech-art-course.md`. An unrelated existing file at either destination is preserved and reported for review. The project marker is `Course/.diagram-design`; the generic diagram-design installation is left unchanged.

Run the course reader builder after generating any HTML with new Markdown/CSV links:

```powershell
node Course/Tools/build_readers.mjs
```

This creates clean local reading views and updates local document links in course HTML. Original Markdown/CSV documents remain the editable sources. The reader pages show their source path, modification time, and a source-file link. External websites remain primary references and are not silently copied.
