def texture_identity(name):
    if not name.startswith("T_"):
        raise ValueError(f"Expected T_ prefix: {name}")
    family, separator, role = name[2:].rpartition("_")
    if not separator or not family or role not in {"BC", "N", "ORM"}:
        raise ValueError(f"Unrecognized texture name: {name}")
    return family, role

mesh_family = "AirConditioning_01"
family, role = texture_identity("T_AirConditioning_01_BC")
matches_mesh = family == mesh_family  # True; keeps the complete identifier.
