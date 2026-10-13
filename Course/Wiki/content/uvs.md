---
updated: 2026-09-08
title: UVs and texture lookup
group: Topics
order: 32
status: Foundation
summary: The image stores values; coordinates determine where the surface reads them.
---

## Follow one sample

A surface location needs coordinates for a texture lookup. In a common mesh workflow, UV coordinates provide a two-dimensional location in texture space. A texture sample uses the coordinates and filtering behavior to obtain values.

Think about a label on a panel. The image can remain unchanged while the label appears mirrored because the coordinates changed. The material can also transform coordinates before sampling. These are different possible causes of a similar observation.

Use the Maya figure in [Scratchapixel's Basic Implementation chapter](https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-texturing/introduction-to-texturing-basic-implementation.html) to follow the correspondence between a surface and an image region.

## Inspect the correspondence

In Maya's [UV Editor](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-Modeling/files/GUID-73BF7546-3BF2-44F3-9192-15A024CEC173.htm), select a surface region and locate its UVs. A directional checker with labeled corners is easier to interpret than a symmetric pattern.

In Unreal, identify the selected UV channel and any coordinate operations before the Texture Sample. The same image and mesh can produce different placement through the graph.

## A small mathematical nugget

Within a simple normalized interval, replacing `U` with `1 − U` reverses the horizontal coordinate. At `U = 0.2`, the new value is `0.8`. This describes the sampling coordinate; it does not edit the pixels stored in the source image.

Outside that simple example, wrapping, tiling, and other coordinate transforms affect the result. Begin with the labeled 0–1 case before extending it.

## Layout choices have a purpose

Stretching, seams, orientation, and texel density affect how a pattern reads. An overlap is not automatically a defect: a repeated or symmetric surface may intentionally reuse data. Unique detail or a particular bake can impose a different requirement.

**Try this:** keep the image fixed and mirror one UV region. Record what changed. Then restore it and perform the corresponding material-coordinate change in a prepared example. What evidence identifies which layer owns the difference?

Continue with [textures](textures.html), [representations](representations.html), or the [museum prompts](museum-lab.html).
