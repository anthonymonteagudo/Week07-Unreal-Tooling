"""06: a small in-memory exercise, NOT Unreal Apply or an Undo simulation."""
from copy import deepcopy
from sample_data import load_records


def expected_label(actor):
    return f"W07_{actor['kind']}_{actor['id'] + 1:02d}"


def make_plan(actors):
    return [
        {"path": a["path"], "before": a["label"], "after": expected_label(a)}
        for a in actors if a["label"] != expected_label(a)
    ]


def apply_to_copy(actors, reviewed_plan):
    # Validate the whole plan before changing even the copied records.
    paths = [a["path"] for a in actors]
    if len(paths) != len(set(paths)):
        raise ValueError("Each record needs a unique path.")
    if reviewed_plan != make_plan(actors):
        raise ValueError("Data or rule changed. Make and review a fresh preview.")
    updated = deepcopy(actors)
    by_path = {a["path"]: a for a in updated}
    for change in reviewed_plan:
        by_path[change["path"]]["label"] = change["after"]
    return updated


def main():
    actors = [a for a in load_records() if "W07_DemoProp" in a["tags"]]
    plan = make_plan(actors)
    updated = apply_to_copy(actors, plan)
    return {
        "original_labels": [a["label"] for a in actors],
        "updated_labels": [a["label"] for a in updated],
        "remaining_label_changes": make_plan(updated),
        "missing_meshes_still_need_attention": [a["path"] for a in updated if not a["has_mesh"]],
    }
