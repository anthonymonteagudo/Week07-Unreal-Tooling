---
updated: 2026-09-08
title: Mesh anatomy
group: Topics
order: 30
status: Foundation
summary: Geometry, topology, normals, UVs, and assignments describe different parts of the same asset.
---

## Shape and structure

A vertex has a position. Edges connect vertices. Faces use ordered boundaries to describe a surface. **Geometry** describes the shape; **topology** describes its connections. Moving a point changes the shape. Adding a face or splitting a connection changes the structure as well.

That structure can support different jobs: a static silhouette, a subdivision surface, a bake target, or a mesh that needs to bend. A useful modeling rule must account for the operation and intended result.

## A mesh carries more than positions

| Data | What it helps determine |
|---|---|
| Positions and connectivity | Shape and structure |
| Shading normals | How directions vary across the shaded surface |
| UV coordinates | Where textures are sampled |
| Material membership / slots | Which surface definition applies to a region |
| Transform and pivot | How the object relates to its scene |

Two faces can meet at one editable point but need distinct UV or normal values at the boundary. Different applications may count different representations of a vertex. Ask what is being counted before treating a numerical difference as a failure. Autodesk's [polygon data-model explanation](https://help.autodesk.com/cloudhelp/2023/CHS/Maya-SDK/files/Polygon-API/Maya_SDK_Polygon_API_How_polygons_are_handled_html.html) is a useful deeper reference.

## Inspect in Maya, verify in Unreal

Select the actual components around the problem. Compare the outline, wireframe, face orientation, and shading. An unusual surface appearance alone does not establish a topology problem.

After a source edit and import, check the original symptom and the relationships that should survive: dimensions, UVs, material assignment, and required motion or interaction. See [Epic's static-mesh pipeline](https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine?application_version=5.7) for the transfer context.

## Avoid automatic conclusions

An open boundary can be intentional. Overlapping UVs may deliberately reuse a pattern. Generated normals can be a pipeline choice. Each becomes a problem when it conflicts with the asset's requirements or invalidates another dependency.

**Try this:** compare a beveled edge with a shading-only change. Which effect remains visible in silhouette? Continue with [normals](normals.html), then [UV lookup](uvs.html).
