---
updated: 2026-09-08
title: Working glossary
group: Resources
order: 71
status: Growing reference
summary: Short definitions tied to the inspection questions used in the course.
---

| Term | Working meaning |
|---|---|
| Asset | Content and associated information used by a project. Its useful identity includes relevant dependencies. |
| DCC | A digital content creation application, such as Maya. |
| Engine | The application/runtime in which content is assembled and evaluated for its intended use. |
| Handoff | A transfer of data, work, or responsibility between stages or people. |
| Geometry | The positions and shape of a surface. |
| Topology | The relationships connecting components of a mesh. |
| Normal | A direction used in reasoning about a surface; distinguish face orientation and shading directions. |
| Normal map | Texture-provided direction information used for shading. |
| UV | A coordinate pair commonly used to locate a sample in texture space. |
| Texel | A discrete element of a texture image. |
| Texel density | The relationship between texture detail and surface area/size under a stated convention. |
| Texture | Sampled data, often stored as channel values in an image. |
| Shader | A program used in rendering calculations. |
| Material | Surface logic and settings; in UE, commonly authored as a graph and asset configuration. |
| Material Instance | A child asset that inherits a parent material and overrides exposed choices. |
| Parameter | An exposed value or choice used by material logic or another configurable system. |
| Assignment | The association of a surface definition with an object region or material slot. |
| Alpha | A channel whose meaning depends on how the receiving system uses it. |
| Masked | A material coverage behavior that keeps or discards samples using a cutoff. |
| Two Sided | A material choice concerning backface rendering. |
| sRGB | A color encoding/transfer convention; determine whether its decoding is appropriate for the data role. |
| Mip | One resolution level in a texture's multiresolution representation. |
| Mesh LOD | A geometry representation used at a particular level of detail. |
| Streaming | Managing which needed data is currently available in memory. |
| Skeleton | A hierarchy of joint transforms used in a skeletal workflow. |
| Skin weight | A contribution describing how a vertex follows deformation influences. |
| Bind/reference relationship | The connection between a mesh's reference state and the joint transformations used to deform it. |
| Morph target | Shape-change data relying on correspondence with the base mesh. |
| Metadata | Descriptive information about data, such as a declared role, source, or tag. |
| Dependency | Another asset, setting, tool, or resource needed to reproduce the result. |
| Validation | Comparing observed data with an explicit rule and reporting what the evidence establishes. |
| Verification | Checking that a change satisfies the intended result under relevant conditions. |
| Regression | A previously working behavior that fails after a change. |

Definitions here are starting points. Use the topic pages for distinctions and the software references for exact implementation behavior. Add new terms when they support a concrete example in the course, rather than turning the glossary into an unexplained vocabulary inventory.
