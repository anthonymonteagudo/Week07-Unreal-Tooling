# Asset Setup 03 — connect the parent, textures and mesh

The final lesson connects the objects created in the earlier stages. It sets the material instance’s parent, supplies texture parameter values, assigns the instance to the mesh and saves the affected assets. The useful lesson is that a working automation must preserve **relationships and meaning**, not merely create assets with plausible names.

## Four relationships to keep distinct

| Relationship | Question |
| --- | --- |
| Instance → parent material | Which prepared shader and parameters does this instance use? |
| Instance parameter → texture | Which texture supplies a particular input such as base color? |
| Static mesh slot → instance | Which persistent mesh assignment changes? |
| Mesh component → optional override | Does a particular scene placement override the mesh default? |

The tutorial changes the **StaticMesh asset’s slot assignment**. That can affect placements using the mesh’s default materials. It is not equivalent to setting an override on one selected `StaticMeshComponent`.

That distinction matters for Week 7: the prepared Material Setup Assistant is designed around reviewed component assignments. Keep the shared material-instance concepts, but do not describe the tutorial’s asset-level change as affecting only one selected actor.

## Set a valid parent

The source loads a hard-coded parent asset and assigns it through `set_editor_property('parent', material_parent)`. This illustrates an Unreal binding distinction: a Python property’s direct setter and its editable editor property are not always the same interface.

The current `MaterialEditingLibrary` also provides `set_material_instance_parent(instance, parent)`. It expresses the operation directly. Confirm that the loaded object is a suitable material interface and that it exposes the parameters the tool expects; a path string alone is not validation.

The persistent instance is a `MaterialInstanceConstant`. Its overrides are meaningful relative to a parent with named parameters. An arbitrary image file cannot be assigned to an arbitrary material input merely by guessing a suffix.

## Assign the correct mesh slot

`StaticMesh.set_material(index, instance)` uses the numeric slot index. Preserve the index from `enumerate(mesh.static_materials)` rather than searching for each record again. Check the intended slot before mutation, especially when several material regions exist.

A useful verification statement is: “Slot 0, named Body, now references the intended instance.” “A material instance exists” does not establish that assignment, and a viewport appearance alone does not identify which underlying asset or component changed.

## Set texture overrides through MaterialEditingLibrary

A new instance need not have a populated override entry for every parameter inherited from its parent. The lesson therefore uses `set_material_instance_texture_parameter_value` rather than assuming existing entries in the raw override array.

The call takes the instance, parameter name and texture object. The current API also accepts a parameter association and returns a Boolean. Check that result, and use the appropriate association when the parent’s parameter structure requires it. After a set of edits, `update_material_instance` provides the documented update operation. [Epic MaterialEditingLibrary reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MaterialEditingLibrary?application_version=5.7)

The parent in the demonstration uses these names:

| Texture suffix | Parent parameter | Intended meaning |
| --- | --- | --- |
| `_BC` | `BC` | Base color |
| `_N` | `N` | Normal |
| `_ORM` | `ORM` | Packed occlusion, roughness and metallic data |

These are the example’s naming conventions, not reserved Unreal parameter names. Other parents may use `BaseColor`, `Normal` or entirely different names. Record the mapping explicitly. The suffix does not prove the texture’s packing, color-space setting or compression is correct; inspect those against the parent’s actual expectations.

## Avoid the last-texture-wins problem

The first version loops over all imported textures for every material instance. If several texture sets use the same parameter suffixes, later textures can overwrite earlier assignments. The tutorial adds a name test to restrict matching.

Its final code uses `static_mesh.get_name().split('_')[1]` and checks whether that substring appears in a texture name. This is a useful demonstration of the problem, but a weak general matching rule:

- A full identifier such as `AirConditioning_01` is shortened to `AirConditioning`.
- Names with additional underscores lose information.
- Similar identifiers can match each other accidentally.
- Several matching textures for one parameter still create an ordering-dependent result.
- Mesh-name matching does not explain which texture set belongs to each of several material slots.

**Supplemental improvement:** parse an exact family identifier and role, then reject missing or ambiguous matches before editing the instance. For a one-material mesh, the complete mesh stem can be the family identifier. For a multi-material mesh, define the mapping per slot or use an explicit manifest.

This ordinary-Python example demonstrates only the naming rule. It does not load, create or modify Unreal assets.

```python
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
```

Before binding, require one intended texture per required role. Treat “missing,” “duplicate” and “unrecognized suffix” as different results. A fallback texture is a policy to explain, not a silent substitute for a failed match.

## Configure, then assign

The tutorial assigns the instance to the mesh before filling its texture parameters. For a reusable tool, validate the full plan first, create/configure the instance, verify the parameter bindings, and then assign the reviewed target slots. This reduces the opportunity to leave a mesh pointing at an incompletely configured instance, but does not create automatic rollback.

This editor-context excerpt illustrates configuration of an existing instance. `bindings` maps known parameter names to loaded texture objects. It does not create an instance, assign a mesh, save packages or automatically undo a partial failure.

```python
import unreal

def configure_instance(instance, parent, bindings):
    if not isinstance(instance, unreal.MaterialInstanceConstant):
        raise TypeError("Expected a MaterialInstanceConstant")
    if not isinstance(parent, unreal.MaterialInterface):
        raise TypeError("Expected a material parent")

    library = unreal.MaterialEditingLibrary
    available = {str(name) for name in library.get_texture_parameter_names(parent)}
    for parameter, texture in bindings.items():
        if parameter not in available or not isinstance(texture, unreal.Texture):
            raise ValueError(f"Invalid texture binding: {parameter}")

    library.set_material_instance_parent(instance, parent)
    for parameter, texture in bindings.items():
        setter_result = library.set_material_instance_texture_parameter_value(
            instance, parameter, texture
        )
        actual = library.get_material_instance_texture_parameter_value(
            instance, parameter
        )
        if actual != texture:
            raise RuntimeError(
                f"Texture readback mismatch: {parameter}; setter={setter_result}"
            )
    library.update_material_instance(instance)
```

This short example uses the default global parameter association. More complex layered parent materials need a more explicit parameter plan. If a setter fails after an earlier edit succeeds, report the partial state rather than claiming that nothing changed.

**Classroom rehearsal qualification:** the recorded UE 5.7.4 fixture exposed a texture setter returning `False` even though the requested binding was present. The current backend therefore checks the actual parameter readback. This is local runtime evidence, not a claim that every engine version has the same behavior. Epic documents a Boolean setter result and a texture-valued getter; keep the return value for diagnostics, verify the relationship, and inspect the scene separately. The excerpt above now follows that distinction. See the [recorded fixture report](../../FinalClass20261013/live-captures/rehearsal.json) and [Epic’s MaterialEditingLibrary API](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MaterialEditingLibrary?application_version=5.7).

## Save the actual changes

The source collects meshes, textures and newly created instances into lists, then saves each by path. It uses `list` as a loop variable, which shadows Python’s built-in name; use a descriptive name such as `asset_group`.

A refined workflow tracks created and modified assets, removes duplicate save requests, and checks each save result. Saving an asset is distinct from assigning it correctly or verifying its appearance. Source-control checkout can also affect saving.

Inspect the instance parent and overrides, the mesh slot, and the intended rendered result. Confirm what remains unchanged. If the intended scope is one component override, verify another placement of the same mesh as well.

## Read the supplied complete script as a worked example

The complete `buildSelectedAssets` source is preserved separately, unchanged. Its sequence is useful for learning, while its assumptions should remain visible:

1. Destination-folder scan plus first-source-filename matching.
2. Hard-coded parent and asset/texture naming conventions.
3. Immediate deletion of the currently assigned material.
4. Instance names derived from slots without a collision policy.
5. Asset-level mesh assignment and substring texture matching.
6. Setter, creation, deletion and save results that are not all checked.

The refinement clarifies these choices; it does not present the script as a fully validated production tool. The new snippets are teaching adaptations, with syntax checks and selected naming cases checked offline. No Unreal import, export, mutation or save was executed during this work.

**Course application:** use a visible worked mapping—mesh, slot, parent, three texture roles and assignment scope—then show one relevant API call. This supports the fuller slide explanations you prefer while leaving colleagues room to elaborate on the implementation.

**Review question:** if two imported texture sets both have a `_BC` texture, what evidence should determine the binding before any material is changed?

## References

- [Oster: Asset Setup with the Unreal Python API](https://dev.epicgames.com/community/learning/tutorials/xrnE/unreal-engine-asset-setup-with-the-unreal-python-api)
- [Epic MaterialEditingLibrary reference, UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MaterialEditingLibrary?application_version=5.7)
- [Epic StaticMesh reference, UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/StaticMesh?application_version=5.7)
- [Epic EditorAssetLibrary reference, UE 5.7](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/EditorAssetLibrary?application_version=5.7)


## Additional original captures

No additional captures were embedded in this source note.

## Source note

[Original Asset Setup 03.md](file:///C:/Users/antho/OneDrive/Desktop/Notes/anthony/personal/Duke%20Tech%20Art%20Course%20Notes/18%20Oster%20Asset%20Setup%20UE%20Python%20API/Asset%20Setup%2003.md)

[Preserved complete source script](../original-script.html)
