---
updated: 2026-09-08
title: Museum investigation lab
group: Practice
order: 50
status: Lab companion
summary: Observe first, choose a test with a reason, and leave evidence that another person can understand.
---

## Pass 1: observe

Use the available reference and the instructor's station list. Record the exhibit you are viewing and the exact visible difference. Include the camera, lighting, distance, pose, or interaction when it matters.

Then propose a possible explanation and a useful inspection. You do not need to claim a cause that the available evidence cannot establish.

| Instead of stopping at… | Add a testable observation |
|---|---|
| “The material is broken.” | Which region differs, and how does the difference respond to light or view? |
| “The UVs are wrong.” | Which part of the pattern is reversed, stretched, or displaced? |
| “The model disappears.” | At what distance or viewing condition, and which representation is active? |

## Look up the mechanism

| Museum topic | Read this | Inspection prompt |
|---|---|---|
| Normal response / EX24 | [Normals](normals.html) | Which directions reach the shading calculation, and how are they interpreted? |
| RGB/sRGB / EX23 | [Texture data](textures.html) | What do the channels represent, and which interpretation matches that role? |
| Coordinates / EX29 | [UV lookup](uvs.html) | Is the image correct, and which coordinates read it? |
| Material assignment and alpha / EXMAT | [Materials](materials.html), [handoff](handoff.html) | Are the intended faces using the correct surface definition and coverage behavior? |
| Mesh detail / EXLOD | [Representations](representations.html) | Which mesh representation is selected when the difference appears? |
| Geometry extension / EX20 | [Mesh anatomy](meshes.html) | What structural evidence supports the diagnosis beyond the final shading? |
| Skeletal displays / EXA, EX21 | [Skeletal assets](skeletal.html) | Is the pose wrong, the surface following wrong, or the wrong motion playing? |

The instructor's prepared station list determines what you can edit. Some documented candidates are source-ready or display-only; their presence in the museum does not promise a supported repair exercise.

## Pass 2: investigate and verify

Work with the prepared group-owned editable assets. A map copy can still reference shared meshes, textures, and materials, so identify the actual asset before editing it.

1. Reproduce the original symptom and keep the reference available.
2. Inspect the relevant data and state a hypothesis.
3. Choose a change that tests the hypothesis.
4. Refresh or reimport if the workflow requires it.
5. Repeat the original check under comparable conditions.
6. Record the result and what remains uncertain.

A source-owned fault may need a Maya edit. An engine interpretation fault may belong in Unreal. Follow the responsibility revealed by the test.

## If the repair is blocked

Record the last fact you established, the missing evidence or access, and the next useful test. A precise blocked investigation remains useful. Avoid making several untracked changes simply to produce a visually improved screenshot.

## Carry the work forward

Use the [exhibit record](exhibit-record.html) to structure the evidence in the course's existing group-document workflow. Identify one condition that could become a [Python check](week03.html) and one observation that still needs human judgment.

For your own [museum exhibit](exhibit.html), reuse the same observation/test/verification relationship as the basis of a visitor experience.
