---
updated: 2026-09-08
title: Mips, mesh LOD, and streaming
group: Topics
order: 37
status: Foundation
summary: Several systems change what data is used at a distance. Identify which representation changed before explaining the result.
---

## Three different questions

| Concept | Main question |
|---|---|
| Texture mip | Which lower-resolution representation of the texture is sampled? |
| Mesh LOD | Which geometry representation is active? |
| Streaming | Which required data is currently available in memory? |

Instancing is another idea: it reuses a mesh representation for multiple instances. It should not be taught as another name for selecting a lower-detail mesh.

## Why a smaller texture representation can help

A detailed pattern can cover less than a screen pixel. Sampling needs to account for that footprint; simply using the highest-resolution source everywhere does not guarantee a stable or faithful distant image.

Use a fixed camera path to observe shimmer, then pause on a comparable frame. The [Texture Asset Editor reference](https://dev.epicgames.com/documentation/en-us/unreal-engine/texture-asset-editor-in-unreal-engine?application_version=5.7) grounds the settings. Williams's [Pyramidal Parametrics, page 4](https://users.cs.northwestern.edu/~ago820/cs395/Papers/Williams_1983.pdf#page=4) gives historical visual context for minification.

## Why geometry may change

A conventional static-mesh LOD setup can select a representation based on projected screen size. Inspect the active LOD and statistics while moving the camera, then check the silhouette and material behavior. [Epic's automatic LOD guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/static-mesh-automatic-lod-generation-in-unreal-engine?application_version=5.7) explains that workflow.

The lower-detail result should preserve what matters under the intended viewing conditions. A numerical reduction alone does not establish an acceptable asset.

## A lab comparison

If an object suddenly looks different at a distance, record the camera condition, active mesh representation, texture representation, and relevant residency information. Change one system at a time in a prepared example.

The same symptom can have several causes. Do not collapse a texture-mip demonstration, geometry-LOD demonstration, and streaming delay into one unexplained “quality” setting.

For more depth, PBRT's [Image Texture chapter](https://www.pbr-book.org/4ed/Textures_and_Materials/Image_Texture) discusses filtering footprints. Its implementation context is a further reading, not a set of UE editor instructions.
