---
updated: 2026-09-08
title: Skeletal assets
group: Topics
order: 36
status: Foundation
summary: Separate the joint pose, the surface following that pose, and the animation being played.
---

## The minimum useful model

Joints form a hierarchy of transforms. Skin weights describe how vertices follow those transforms, and a bind/reference relationship connects the original mesh and joints. Animation changes the pose over time.

“Weight” means a contribution to deformation, not the physical mass of a bone. Watch the same joint motion with different weights: the skeleton can move identically while the surface bends differently.

The Autodesk [Skin Tools demonstration, starting at 2:22](https://www.youtube.com/watch?v=gJSkEyXkyHE&t=142s), shows weight editing and deformation testing in Maya 2027. Pair it with the [official quickstart](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-CharacterAnimation/files/GUID-2ABD18C8-8CCF-44B9-99E0-EDEE4A56A3E6.htm).

## Three inspection questions

| Observation | Useful distinction |
|---|---|
| The joints move unexpectedly. | Inspect the pose, hierarchy, and intended motion. |
| The joints move correctly but the surface follows poorly. | Inspect weights, bind relationships, mesh structure, and the deformation method. |
| The wrong motion appears or does not play. | Inspect the animation asset, compatibility, and playback configuration. |

A rest pose does not verify a required bend or complete motion loop. The Unreal [Skeletal Mesh asset guide](https://dev.epicgames.com/documentation/unreal-engine/skeletal-mesh-assets-in-unreal-engine?application_version=5.7) explains the destination asset context.

## A small mathematical picture

For a simplified linear-blend example, let `pA` and `pB` be candidate positions for the **same vertex** after the appropriate joint/bind transformations, expressed in the same coordinate frame. With two weights:

`p′ = 0.75 pA + 0.25 pB`

These candidates are not the positions of the bones. The expression is a teaching model for combining contributions. Different deformation algorithms can produce different artifacts; [Kavan et al.'s skinning paper and comparisons](https://users.cs.utah.edu/~ladislav/kavan07skinning/kavan07skinning.html) provide an advanced continuation.

## Morph targets and the lab

Morph targets provide another form of shape change using corresponding mesh information. Keep that concept distinct from changing the skeleton's pose.

Use skeletal museum examples as directed by the instructor's prepared station list. The current project documentation treats these as display examples; do not assume an available display is also a supported repair task. Full rigging and mathematical derivations return later in the course.
