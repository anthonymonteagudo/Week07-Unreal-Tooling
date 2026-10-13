# Week 3 instructor reference library

This folder holds instructor-only source reading and the notes mined from it for
Week 3. It is not student release content.

## Distribution boundary

- `Sources/` contains the eight supplied PDFs in their original form.
- Do not copy `Sources/` into GitHub, `class-resources`, a student ZIP, or slides.
- Cite or paraphrase small relevant ideas in course material rather than
  redistributing book pages.
- `01_RELEVANCE_ASSESSMENT.md` is the first-pass triage.
- `02_DEEP_DIVE_WEEK03.md` contains the useful teaching synthesis and page routes.

## Suggested review order

1. Read `Maya-Tools/course_docs/week_03/instructor/PRIMARY_BOOK_INTEGRATION.md`
   for the new primary 2026 reference.
2. Read the assessment table.
3. Read the deep-dive sections for Chad Vernon, Norman, and Krug.
4. Review the Practical Maya Programming section for instructor architecture only.
5. Use Automate the Boring Stuff as supplemental file-safety support.
6. Leave the VFX and animation-short sources for later course planning.
7. Read `03_SUPPLEMENTAL_NOTES.md` for the small Python-language and launcher
   additions from the locally supplied course notes.

## Additional supplied notes

`03_SUPPLEMENTAL_NOTES.md` assesses the locally supplied Simon batch-file material
and Anthony's HarvardX CS50P notes. The source notes remain in the private OneDrive
course-notes library; they are not duplicated into Git or student materials.

## Important age/version warning

The Fisher source is a modern Maya 2026/Python 3 reference. Several other sources
teach Maya 2013-2016, Python 2, `reload()`, `os.path`, PyMEL, or old Qt conventions.
Their durable concepts are useful, but their code is not the Week 3 implementation
standard. The course remains Maya 2025+ with Maya 2027 as the classroom reference,
Python 3, PySide6, `pathlib`, and the existing `week3_tools` entry points.
