---
updated: 2026-09-08
title: Texture data and interpretation
group: Topics
order: 33
status: Foundation
summary: A texture stores channel values. Its intended role determines how those values should be interpreted and used.
---

## An image is not always color information

A texture might supply surface color, roughness, normal directions, or a mask. The channels can hold different kinds of information even when the asset looks like an ordinary image in a viewer.

Start by identifying the declared role and the material connection. A grayscale appearance or filename can be a clue, but neither establishes the rule by itself.

## Color and numerical control data

Color encodings such as sRGB serve a different purpose from storing a numerical control signal for direct use. Applying a color-decoding transform to numerical RGB roughness data changes the numbers entering the material. A setting must agree with the intended role.

This does not mean every grayscale texture has the same configuration, or that every channel in a packed texture shares every interpretation rule. Inspect the actual channels and usage. Alpha, in particular, should not be casually assumed to receive the same treatment as RGB.

[Epic's Texture Asset Editor documentation](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-asset-editor-in-unreal-engine?application_version=5.7) explains the available settings. Use the project configuration and its documented data roles to interpret them.

## Separate the decisions

| Decision | Question |
|---|---|
| Role | What should these channels represent? |
| Color interpretation | Is a decoding transform appropriate for those values? |
| Compression | How is the data represented for the target use? |
| Sampling | How does the graph read the data? |
| Connection | Which material input receives the result? |
| Display | What viewing transform helps us see the preview? |

Maya's display/color-management configuration and an Unreal texture's sRGB setting occupy different parts of this process. Do not treat similar-looking previews as proof that their settings are equivalent.

## A controlled comparison

Keep geometry, camera, lighting, and Base Color fixed. Identify a known numerical roughness input. Compare one intended interpretation change and observe the surface response. If other settings also change, record them; you no longer have a one-variable test.

For your record, capture the role, expected setting, observed setting, result, and remaining limits. This is the bridge to [Week 3's Python check](week03.html).

## Explore further

[Adobe's PBR Guide, Part 2](https://www.adobe.com/learn/substance-3d-designer/web/the-pbr-guide-part-2) connects authoring choices with surface models. [Scratchapixel's texturing lessons](https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-texturing/introduction-to-texturing.html) provide the deeper sampling and color-space context. For size and distance behavior, continue with [mips and LOD](representations.html).
