---
updated: 2026-09-08
title: Week 2 · Assets, pipelines, and validation
group: Weeks
order: 12
status: Study guide
summary: Follow a surface from Maya to Unreal, identify the data behind its appearance, and investigate a museum example with evidence.
---

## The common goal

You should be able to locate relevant asset data, explain a useful test, and document what the result establishes. You are not expected to master every modeling, rendering, or rigging technique in one lecture.

We begin with the parts of an asset, follow a DCC-to-engine handoff, and observe the museum. The focused anatomy examples then give you mechanisms to use in the repair investigation.

## A map of the relationships

| Part | Its role | First useful question |
|---|---|---|
| [Mesh](meshes.html) | Positions and connections define the surface. | Did the actual shape or structure change? |
| [Normals](normals.html) | Directions influence the shading response. | Which direction data is being used? |
| [UVs](uvs.html) | Coordinates guide a texture lookup. | Where are we reading the image? |
| [Texture](textures.html) | Stored values provide sampled inputs. | What do the channels mean? |
| [Material](materials.html) | Logic and settings describe surface behavior. | Which input or operation controls this difference? |
| Assignment | Associates a material with a mesh region or slot. | Is the intended region using the intended material? |
| [Import configuration](handoff.html) | Controls how a representation becomes a destination asset. | What was preserved, converted, or generated? |

The rendering system combines asset information with scene and viewing conditions to produce the displayed image. Keep that system as one box for now. The useful task is to identify which input or relationship could explain the difference.

## Follow one handoff

In Maya, inspect a texture connection and the faces assigned to its receiving material. At export, identify the mesh and attributes that need to travel. In Unreal, inspect the resulting mesh, material slots, and material or instance assignments.

Then revise the source and reimport. Verify both the intended change and the relationships that should remain stable. This second delivery tests whether the bridge is maintainable. The [handoff guide](handoff.html) explains what to inspect without prescribing a universal preset.

## Before the museum repair

Use the first pass to gather observations. For each selected example, record the intended result, the difference, and a possible next test. An uncertain cause is a valid starting point.

Before changing a setting, use these concept prompts:

- **Normal response:** did the outline change, or only the response to lighting? [Normal guide](normals.html).
- **Color/data interpretation:** what does the input represent, and does its interpretation match that role? [Texture guide](textures.html).
- **UV lookup:** is the source image correct, and which coordinates sample it? [UV guide](uvs.html).
- **Assignment/alpha:** which faces use the material, and how does the material use coverage data? [Material guide](materials.html).
- **Distance changes:** which texture or mesh representation is active? [Representation guide](representations.html).

These prompts suggest inspections. They do not identify the cause of every similar-looking failure.

## During the investigation

Use the instructor's prepared station list and group-owned editable assets. Keep the reference visible, change one relevant variable at a time, and repeat the original test. A copied map alone may still reference shared textures and materials.

The [museum lab guide](museum-lab.html) gives the observation and evidence structure. The [documentation guide](documentation.html) shows how to leave a record that someone else can reproduce and reset.

## After the lab

For your [own exhibit](exhibit.html), choose one mechanism that a visitor can observe. Build a controlled variation and a useful prediction question. More elaborate assets are valuable only when they make the explanation clearer.

For [Week 3](week03.html), identify one explicit rule: what information is needed, what state is expected, and what should be reported when the role is unknown?

## Review questions

1. Can a material work without an image texture? Explain an example.
2. Why might a correct source image appear mirrored on a surface?
3. What evidence would distinguish a normal-map effect from a geometry change?
4. Why is a successful reimport a different test from the first import?
5. What would another person need to repeat your verification?

## Explore further

Use the [reading library](resources.html) for specific chapters rather than reading entire rendering references at once. The core software examples are Maya and Unreal; the underlying questions about data, interpretation, and evidence transfer across tools.
