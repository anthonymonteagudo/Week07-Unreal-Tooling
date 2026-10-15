"""PY01: ordinary Python example. These dictionaries are teaching data."""

# Section: setup
current = {"target": "Cube_A", "material": "MI_Blue"}
reviewed = current.copy()
print("Preview:", reviewed)

# Section: focus
current["target"] = "Cube_B"
if current != reviewed:
    print("BLOCKED: inputs changed. Preview again.")
else:
    print("The inputs still match the preview.")
