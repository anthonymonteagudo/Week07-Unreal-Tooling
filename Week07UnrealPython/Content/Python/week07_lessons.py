"""Optional launcher. Actual teaching code lives in the readable checkpoint files.

Inside Unreal: import week07_lessons; week07_lessons.run('UE02')
This module has no startup action and never launches or connects to an editor.
"""
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
LESSONS = ROOT / "lesson_materials/week_07_api_checkpoints"


def catalog():
    return json.loads((LESSONS / "sequence.json").read_text(encoding="utf-8"))["steps"]


def resolve(step_id):
    step = next((s for s in catalog() if s["id"] == step_id), None)
    if step is None:
        raise ValueError("Unknown checkpoint. Use week07_lessons.catalog().")
    file = (LESSONS / step["file"]).resolve()
    if not file.is_relative_to(LESSONS.resolve()) or not file.is_file():
        raise ValueError("Checkpoint must be a file within the lesson folder.")
    return step, file


def blocks(step_id):
    """Return the exact ordered source blocks used by the guide and slides."""
    _, file = resolve(step_id)
    result, current, lines = {}, None, []
    for line in file.read_text(encoding="utf-8").splitlines():
        if line.startswith("# %% "):
            if current is not None:
                result[current] = "\n".join(lines).strip()
            current, lines = line[5:].strip(), []
            if current in result:
                raise ValueError("Duplicate block: " + current)
        elif current is not None:
            lines.append(line)
    if current is not None:
        result[current] = "\n".join(lines).strip()
    return result


def source(step_id):
    """Return the complete independent checkpoint, including its host imports."""
    return resolve(step_id)[1].read_text(encoding="utf-8")


def run(step_id):
    step, file = resolve(step_id)
    if step["host"] == "unreal":
        try:
            import unreal
            version = unreal.SystemLibrary.get_engine_version()
            if not isinstance(version, str) or not version:
                raise RuntimeError("A running Unreal editor is required, not an API stub.")
        except ImportError as error:
            raise RuntimeError("Run this checkpoint inside Unreal's Python editor.") from error
    elif step["host"] == "blender":
        try:
            import bpy
            if not bpy.app.version_string:
                raise RuntimeError("A running Blender host is required.")
        except ImportError as error:
            raise RuntimeError("Run this checkpoint inside Blender's Text Editor.") from error
    # Each full checkpoint gets a new namespace, avoiding accidental prior-step variables.
    return runpy.run_path(str(file), run_name="__main__")
