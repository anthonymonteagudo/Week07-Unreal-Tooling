---
updated: 2026-09-08
title: Maya-to-Unreal handoffs
group: Topics
order: 35
status: Foundation
summary: Follow identity, data, and dependencies through export, import, assignment, revision, and reimport.
---

## Begin in the source application

In Maya, a texture node can feed a material input. Material assignment associates that surface definition with an object or selected faces. UVs supply a separate relationship used for texture placement. Inspect each relationship before exporting.

The [Maya shading-network overview](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-LightingShading/files/GUID-599CACDB-76C1-4FAC-AA94-0E77F0042C8D.htm) and [assignment documentation](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-LightingShading/files/GUID-6BA1E3DF-F033-443C-989F-9A3295FFC152.htm) explain these roles.

## What should survive?

For one asset with two material regions, write down the intended dimensions, regions, UVs, shading data, and texture dependencies. A handoff has succeeded only in relation to those requirements.

Arbitrary Maya or Arnold shading networks should not be assumed to translate intact through FBX. Supported material conversion and texture handling have limits, and the selected importer matters. A deliberate Unreal material setup may be needed even when mesh regions and slot identities arrive correctly. See [Epic's FBX Material Pipeline](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-material-pipeline-in-unreal-engine?application_version=5.7).

## Read settings by consequence

| Area | What to establish before choosing an option |
|---|---|
| Selection and hierarchy | Which objects and required relationships should travel? |
| Scale, axes, transforms | What dimensions and orientation should appear in the destination? |
| Normals and tangents | Is the pipeline preserving authored data or generating destination data? |
| Materials and textures | Which assignments or supported inputs can transfer, and which are rebuilt? |
| Animation/deformation | Which skeleton, skin, morph, and animation information does this asset require? |

Use [Maya's FBX Export options](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Interoperability/files/GUID-FE8DBEAA-C2DD-43B3-9933-4BA4CDDEAA89.htm) and the reference for the importer you actually use: [FBX options](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-import-options-reference-in-unreal-engine?application_version=5.7) or [Interchange](https://dev.epicgames.com/documentation/unreal-engine/interchange-import-reference-in-unreal-engine?application_version=5.7). Record the chosen path and software versions with your example.

## Test the second delivery

1. Inspect the source and record the intended state.
2. Export and inspect the destination asset.
3. Assign the appropriate Unreal Material or Instance to the intended regions.
4. Revise one source relationship.
5. Reimport and verify the revision.
6. Check that unrelated assignments, scale, UVs, and behavior stayed correct.

Import can generate data deliberately. Call that a failure when it violates the handoff requirement, not simply because a value was recomputed.

## Maintenance is part of the asset

Record source ownership, dependencies, version assumptions, and verification. If the same problem returns after a source revision, a downstream patch may not have repaired the responsible layer.

In the lab, a material-interpretation fault may belong in Unreal; a source-geometry error may belong in Maya. Follow the evidence instead of forcing every repair through the same application. Continue with the [documentation example](documentation.html).
