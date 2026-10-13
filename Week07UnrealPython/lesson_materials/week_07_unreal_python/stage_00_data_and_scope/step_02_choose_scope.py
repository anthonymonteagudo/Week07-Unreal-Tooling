"""02: a selection can contain objects the tool should not process."""
from sample_data import load_records


def choose_scope(actors):
    included = []
    excluded = []
    for actor in actors:
        if "W07_DemoProp" in actor["tags"]:
            included.append(actor)
        else:
            excluded.append(actor)
    return included, excluded


def main():
    included, excluded = choose_scope(load_records())
    return {
        "included": [actor["label"] for actor in included],
        "excluded": [actor["label"] for actor in excluded],
    }
