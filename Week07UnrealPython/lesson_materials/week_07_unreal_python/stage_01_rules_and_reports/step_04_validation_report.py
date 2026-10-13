"""04: return findings; validation does not need to modify anything."""
from sample_data import load_records


def expected_label(actor):
    return f"W07_{actor['kind']}_{actor['id'] + 1:02d}"


def validate(actors):
    findings = []
    for actor in actors:
        if actor["label"] != expected_label(actor):
            findings.append({"path": actor["path"], "issue": "LABEL"})
        if not actor["has_mesh"]:
            findings.append({"path": actor["path"], "issue": "MISSING_MESH"})
    return findings


def main():
    actors = [a for a in load_records() if "W07_DemoProp" in a["tags"]]
    return {"checked": len(actors), "findings": validate(actors)}
