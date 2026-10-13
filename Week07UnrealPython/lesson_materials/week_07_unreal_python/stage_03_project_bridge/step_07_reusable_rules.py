"""07: call the SAME pure rules used by the editor adapter; still no Unreal."""
from copy import deepcopy
from sample_data import load_records
from week07_tooling import rules


def main():
    actors = [a for a in load_records() if "W07_DemoProp" in a["tags"]]
    states = [{key: a[key] for key in ("path", "id", "label", "location")} for a in actors]
    # The production rules add placement and derive kind from a known fixture ID.
    # This string is an illustrative context, not a loaded Unreal world.
    plan = rules.make_plan("sample://week07-world", states)
    updated = deepcopy(states)
    targets = {item["before"]["path"]: item["after"] for item in plan["items"]}
    for state in updated:
        state.update(targets[state["path"]])
    meshes = {a["path"]: a["has_mesh"] for a in actors}
    return {
        "plan": plan,
        "findings_before": {s["path"]: rules.issues_for(s, meshes[s["path"]]) for s in states},
        "findings_after_copy_update": {s["path"]: rules.issues_for(s, meshes[s["path"]]) for s in updated},
    }
