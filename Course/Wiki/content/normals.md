---
updated: 2026-09-08
title: Normals and normal maps
group: Topics
order: 31
status: Foundation
summary: Distinguish face orientation, mesh shading directions, and sampled normal-map information before choosing a repair.
---

## A normal is a direction

A vector can describe a direction and magnitude. A face normal is perpendicular to the face. The directions used for shading may be authored or interpolated across the surface to control its appearance.

Face orientation also depends on the ordered vertices around a face. The front/back relationship and the shading directions are related concepts, but they are different things to inspect. [Autodesk's polygon-normal guide](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Modeling/files/GUID-9C257D44-924D-4B3F-ADEF-C71FAA98EAB1.htm) grounds the Maya workflow.

## Hard and soft shading

Look at two adjacent faces. A hard boundary can preserve a sharp shading transition; a soft boundary can allow a smoother transition. That shading change does not itself add a bevel or round the outline.

In Maya, compare hard/soft-edge behavior while keeping the mesh visible in wireframe. Predict whether the vertex positions changed, then check the silhouette.

## What a normal map adds

A normal map supplies direction information across the surface. It can create apparent fine detail in the lighting response while the mesh outline remains the same. In the ordinary normal-input example, it does not create physical grooves or change collision.

[LearnOpenGL's direction illustration](https://learnopengl.com/img/advanced-lighting/normal_mapping_surfaces.png) and [brick comparison](https://learnopengl.com/img/advanced-lighting/normal_mapping_compare.png) are useful visual explanations. They are renderer-independent illustrations, not UE captures. The [full chapter](https://learnopengl.com/Advanced-Lighting/Normal-Mapping) explains tangent-space detail for further study.

## A useful Unreal inspection

1. Confirm which texture and material are actually used.
2. Identify the intended normal-data convention and interpretation.
3. Inspect the texture's compression/sampling configuration and the receiving material connection.
4. Compare the result from more than one lighting direction.
5. Check that geometry and unrelated surface inputs stayed as intended.

Use the [Texture Asset Editor reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-asset-editor-in-unreal-engine?application_version=5.7) to locate the relevant settings. The visual color of a texture alone is not a pass/fail test for its interpretation.

## A question for the museum

If a channel flip, compression change, and sampler change happen together, which one explained the result? Separate the presence of normal-map detail from whether the data is interpreted correctly. A suspected convention mismatch needs evidence from the actual pipeline.

For a deeper historical connection, Blinn's [Simulation of Wrinkled Surfaces](https://www.microsoft.com/en-us/research/publication/simulation-of-wrinkled-surfaces/) explains bump mapping. Treat it as research context, not a current Unreal import recipe.
