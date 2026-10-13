"""01: inspect ordinary dictionaries before dealing with engine objects."""
from sample_data import load_records


def main():
    actors = load_records()
    first = actors[0]
    # A label is readable; a path identifies the record even if its label changes.
    return {
        "record_count": len(actors),
        "first_actor": {"path": first["path"], "label": first["label"]},
        "all_labels": [actor["label"] for actor in actors],
    }
