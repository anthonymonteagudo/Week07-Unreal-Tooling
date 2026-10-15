# Week 7 Python preparation

The instructor is working manually on this PC. For Python preparation, edit and
test files without launching Unreal, controlling its session, opening desktop
windows, or running capture automation. `dev.py editor-test` and `dev.py stubs`
both launch Unreal and are outside ordinary code-only validation. Use them only
when the user explicitly requests engine work. Offline checks: `dev.py check`,
`dev.py test`, and `lessons.py run <id>`.

UI is mandatory for the finished teaching tool. Maintain its functional/guided/
refined progression and quality gates. Use `ui_quality.py` and `ui.py --render`
for offscreen validation; never launch `ui.py` without `--render` during code-only
work. A passing offline gate does not establish live Unreal integration readiness.

The user requires BOTH a PySide tool and a separate Unreal-native editor UI.
Do not describe an external Qt window parented to Unreal as native docking.
Native implementation: `Plugins/Week07Tools`; current student route: `README.md`.

Selected functionality: Material Setup Assistant and VFX Placement. No procedural
scattering or material/Niagara graph manipulation yet. Keep VFX validation light:
reviewed presets, bounded placements, duplicate/spacing checks and truthful limits;
do not grow a scene-cost inspector or claim count checks prove production safety.
The prepared map and allowed operations are described in `README.md`. For assistant screenshots, use
`Scripts/assistants.py --render`; do not open its desktop window during code-only work.

The numbered lesson sequence is provisional until the slides are finalized.
Preserve stable step IDs, keep teaching checkpoints readable, and document what
runs in ordinary Python versus Unreal. Do not silently replace teaching examples
with thin wrappers. Keep tested reusable behavior in `Content/Python/week07_tooling`.
Never add the Unreal autocomplete stub to runtime `PYTHONPATH`.

Preserve attribution: original Northwood was the instructor's result of following
Isaac Oster's public UE Python course; this project is the classroom-prep spinoff.
