"""05: represent proposed changes as reviewable data, without applying them."""
from sample_data import load_records


def expected_label(actor):
    return f"W07_{actor['kind']}_{actor['id'] + 1:02d}"


def make_plan(actors):
    changes = []
    for actor in actors:
        target = expected_label(actor)
        if actor["label"] != target:
            changes.append({"path": actor["path"], "before": actor["label"], "after": target})
    return changes


def main():
    actors = [a for a in load_records() if "W07_DemoProp" in a["tags"]]
    plan = make_plan(actors)
    return {"plan": plan, "labels_after_preview": [a["label"] for a in actors]}
