---
updated: 2026-09-08
title: Week 1 · Technical Art foundations
group: Weeks
order: 11
status: Study guide
summary: Turn a production problem into an investigation that another person can understand and continue.
---

## What carries forward

Technical Art connects artistic intention with the tools, data, and production conditions needed to achieve it. Sometimes the useful intervention is code. It can also be a clearer standard, a better handoff, a reproducible test, or an explanation that prevents repeated confusion.

Before choosing a solution, identify the intended experience. An attractive screenshot is only one condition: the asset may also need to survive animation, reimport, another camera, or another person's changes.

## The four lenses

| Lens | Question to ask | Asset-pipeline example |
|---|---|---|
| Constraints | What limits the acceptable solution? | The asset needs to remain readable from the intended camera. |
| Systems | Which people, tools, assets, and dependencies connect? | Maya assignments, exported identities, UE slots, and materials all participate. |
| Leverage | Could the intervention help repeated work? | A known import check could become a reusable validator. |
| Throughput | Does the whole workflow produce reliable work more efficiently? | A quicker export is unhelpful if every import needs manual repair. |

Use the lenses to develop the question. Naming all four without applying them does not explain the production problem.

## Observation before explanation

“The label reads backward on this panel” is an observation. “The texture is broken” is a proposed explanation. A mirrored image, UV layout, or material-coordinate operation could produce similar visible results.

1. State the intended result.
2. Record the actual symptom and conditions.
3. Propose an explanation and a plausible alternative.
4. Choose evidence that would separate them.
5. Describe what remains uncertain.

This is useful work even when you cannot yet perform the repair.

## A small retrieval exercise

Choose one visible feature in a game or a provided production case. Describe it without guessing its implementation. Apply two lenses to explain why it matters, then identify the first source, measurement, or inspection you would seek.

For a shading difference, would you inspect geometry first, the texture role, the material connection, or the point where the result first diverges between tools? Explain what your choice could establish.

## Connection to Week 2

[Week 2](week02.html) supplies specific data to inspect: geometry, normals, UVs, textures, assignments, and import settings. The investigation habit remains the same. [Week 3](week03.html) will turn a well-understood repeated check into a small program.

## Course grounding

This guide summarizes the existing Week 1 student deck: shared vocabulary at slides 78–79, the four lenses at 81–89, the normal-map pipeline case at 130, and observation guidance at 134. The original Canvas journal prompt remains the authority for that activity's formal requirements.
