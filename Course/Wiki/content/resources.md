---
updated: 2026-09-08
title: Reading and visual library
group: Resources
order: 70
status: Curated starting points
summary: Choose a source by the question it answers, with practical references first and deeper theory available when it becomes useful.
---

## Start here for Week 2

| Resource | Read for this question | Suggested scope |
|---|---|---|
| [Epic: Essential Material Concepts](https://dev.epicgames.com/documentation/en-us/unreal-engine/essential-unreal-engine-material-concepts?application_version=5.7) | What are the UE graph, inputs, and surface preview? | Follow one graph/preview example. |
| [Scratchapixel: Basic Implementation](https://www.scratchapixel.com/lessons/3d-basic-rendering/introduction-to-texturing/introduction-to-texturing-basic-implementation.html) | How does a surface location lead to a texture lookup? | Begin with the mapping explanation and Maya UV figure; return to code later. |
| [Adobe: PBR Guide, Part 1](https://www.adobe.com/learn/substance-3d-designer/web/the-pbr-guide-part-1) | What physical surface ideas motivate material controls? | Read to explain a visible surface response; defer complete model detail. |
| [Maya: shading networks](https://help.autodesk.com/cloudhelp/2027/ENU/Maya-LightingShading/files/GUID-599CACDB-76C1-4FAC-AA94-0E77F0042C8D.htm) | How do texture, material, and assignment roles connect in the DCC? | Follow the node relationships. |
| [Epic: FBX Material Pipeline](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-material-pipeline-in-unreal-engine?application_version=5.7) | Which surface relationships can transfer? | Study the Maya multiple-material example and supported-conversion limits. |

## Short visual examples

- [Epic Material Instance chair clip](https://dev.epicgames.com/community/api/cms/videos/1_hr0fnlml/embed.html), approximately 37 seconds: predict which object changes when an exposed value changes.
- [Epic Mapping Roughness clip](https://dev.epicgames.com/community/api/cms/videos/1_4goroask/embed.html), 34 seconds: watch the control and reflection together. The patterned graph is more complex than a first uniform-roughness example.
- [Autodesk Maya 2027 Skin Tools](https://www.youtube.com/watch?v=gJSkEyXkyHE&t=142s), suggested excerpt 2:22–3:04: compare a weight edit with the resulting bend.
- [Epic blend-mode comparisons](https://dev.epicgames.com/documentation/en-us/unreal-engine/material-blend-modes-in-unreal-engine?application_version=5.7): compare stored alpha with coverage behavior.
- [LearnOpenGL normal mapping](https://learnopengl.com/Advanced-Lighting/Normal-Mapping): use the direction diagram and brick comparison before exploring implementation.

The three video selections were spot-checked during the earlier media review. Source playback is separate from classroom embedding or offline availability. For study, keep a still comparison and its explanation alongside the link.

## Go deeper by mechanism

**Shader programming:** [The Book of Shaders](https://thebookofshaders.com/01/) introduces the idea through approachable examples; its [uniforms chapter](https://thebookofshaders.com/03/) has a live time-driven result. [LearnOpenGL: Shaders](https://learnopengl.com/Getting-started/Shaders) connects the concept to an explicit graphics-programming workflow. Their GLSL examples are conceptual/programming resources, not UE editor instructions.

**Texture sampling:** [PBRT, fourth edition](https://www.pbr-book.org/4ed/Textures_and_Materials/Image_Texture) develops image filtering in depth. Use it after a UV/mip example is familiar. [Heckbert's Survey of Texture Mapping](https://publications.ri.cmu.edu/survey-of-texture-mapping) provides a historical research overview.

**Surface models:** [Burley's Disney 2012 notes](https://media.disneyanimation.com/uploads/production/publication_asset/48/asset/s2012_pbs_disney_brdf_notes_v3.pdf) include parameter comparisons; start with one row rather than the whole model. [Karis's 2013 UE4 shading notes](https://blog.selfshadow.com/publications/s2013-shading-course/karis/s2013_pbs_epic_notes_v2.pdf) are historical engine-model context, not a current UE5 settings reference.

**Deformation:** [Kavan et al., Skinning with Dual Quaternions](https://users.cs.utah.edu/~ladislav/kavan07skinning/kavan07skinning.html) illustrates why the deformation method can contribute to artifacts. Use the comparison first and the derivation later.

## Read a source actively

Write the question before opening the reference. Identify the source's software version or model assumptions, then turn one explanation into a test on your example. A cited technique does not by itself prove that your asset uses it or that your repair worked.

For wider exploration, Bartosz Ciechanowski's [Lights and Shadows](https://ciechanow.ski/lights-and-shadows/) offers interactive explanations in a first-principles style. Its full lighting scope belongs beyond the short Week 2 introduction.
