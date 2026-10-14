"""List or run draft teaching checkpoints in ordinary Python. Never starts Unreal."""
import argparse
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "lesson_materials/week_07_unreal_python"


def sequence():
    return json.loads((LESSONS / "sequence.json").read_text(encoding="utf-8"))["steps"]


def step_path(step):
    path = (LESSONS / step["file"]).resolve()
    if not path.is_relative_to(LESSONS.resolve()) or not path.is_file():
        raise ValueError("Lesson must be an existing file inside the lesson folder.")
    return path


def load_step(step_id):
    step = next((s for s in sequence() if s["id"] == step_id), None)
    if step is None:
        raise ValueError(f"Unknown step {step_id!r}. Use 'list' to see available IDs.")
    if step["runtime"] != "python":
        raise ValueError(f"Step {step_id} is reading only. Open {step['file']} manually.")
    path = step_path(step)
    # These two roots contain our code. The autocomplete stub is NEVER a runtime root.
    old_path = sys.path[:]
    try:
        sys.path[:0] = [str(LESSONS), str(ROOT / "Content/Python")]
        return runpy.run_path(str(path), run_name=f"week07_step_{step_id}")
    finally:
        sys.path[:] = old_path


def run_step(step_id):
    return load_step(step_id)["main"]()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    run = commands.add_parser("run")
    run.add_argument("step_id", help="Stable two-digit ID, e.g. 01")
    args = parser.parse_args()
    if args.command == "list":
        print('Optional prop foundations (stable IDs, not slide numbers).')
        print('Direct Unreal/Blender API checkpoints: python Scripts/api_lessons.py list')
        print('Main Material/VFX demo route: Docs/DEMO_SEQUENCE.md\n')
        for step in sequence():
            print(f"{step['id']}  [{step['runtime']}] {step['title']}\n    {step['file']}")
    else:
        try:
            result = run_step(args.step_id)
        except ValueError as error:
            parser.error(str(error))
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
