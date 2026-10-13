"""03: turn a naming convention into a function with a return value."""
from sample_data import load_records


def expected_label(actor):
    # IDs begin at zero; the readable suffix begins at one.
    return f"W07_{actor['kind']}_{actor['id'] + 1:02d}"


def main():
    actors = [a for a in load_records() if "W07_DemoProp" in a["tags"]]
    return [{"current": a["label"], "expected": expected_label(a)} for a in actors]
