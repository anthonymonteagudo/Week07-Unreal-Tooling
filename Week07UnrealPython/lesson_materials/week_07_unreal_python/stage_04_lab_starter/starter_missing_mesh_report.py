"""Optional student starter. Intentional TODO; it does not run through lessons.py."""


def missing_mesh_paths(records):
    # TODO: collect paths only when tagged W07_DemoProp AND has_mesh is false.
    raise NotImplementedError("Implement the reporting rule; do not modify the records.")


if __name__ == "__main__":
    sample = [
        {"path": "sample://crate-0", "tags": ["W07_DemoProp"], "has_mesh": True},
        {"path": "sample://barrel-1", "tags": ["W07_DemoProp"], "has_mesh": False},
        {"path": "sample://light", "tags": [], "has_mesh": False},
    ]
    print(missing_mesh_paths(sample))
