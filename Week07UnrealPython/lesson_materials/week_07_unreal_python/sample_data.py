"""Invented teaching records, NOT an export or a connection to the open editor."""
from copy import deepcopy

_RECORDS = [
    {"path": "sample://crate-0", "id": 0, "kind": "Crate", "label": "crate_old",
     "location": [-130, -470, 0], "tags": ["W07_DemoProp"], "has_mesh": True},
    {"path": "sample://barrel-1", "id": 1, "kind": "Barrel", "label": "barrel_old",
     "location": [100, -300, 18], "tags": ["W07_DemoProp"], "has_mesh": False},
    {"path": "sample://crate-2", "id": 2, "kind": "Crate", "label": "W07_Crate_03",
     "location": [-75, -70, 0], "tags": ["W07_DemoProp"], "has_mesh": True},
    {"path": "sample://light", "id": None, "kind": "Light", "label": "KeyLight",
     "location": [0, 0, 300], "tags": [], "has_mesh": False},
]


def load_records():
    """Each checkpoint starts fresh; edits to one copy cannot affect another."""
    return deepcopy(_RECORDS)
