---
title: Model geometry
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/model-geometry/
nav_order: 2
author: HobbitDur
---

## Model geometry

### Header (data sub table)

| Offset             | Length               | Description             |
|--------------------|----------------------|--------------------------|
| 0                  | 4 bytes              | Number of objects       |
| 4                  | nbObjects \* 4 bytes | Object Positions        |
| 4 + nbObjects \* 4 | Varies               | Object Data (see below) |
| Varies             | 4 bytes              | Total count of vertices |

### Object Data

| Offset | Length                          | Description                                        |
|--------|---------------------------------|----------------------------------------------------|
| 0      | 2 bytes                         | Number of Vertices Data                            |
| 2      | Varies \* NbVerticesData        | Vertices Data (see below)                          |
| Varies | 4 - (absolutePosition % 4)      | Padding (0x00)                                     |
| Varies | 2 bytes                         | Num textured triangles                             |
| Varies | 2 bytes                         | Num textured quads                                 |
| Varies | 2 bytes                         | Num colored triangles (0 in every vanilla monster) |
| Varies | 2 bytes                         | Num colored quads (0 in every vanilla monster)     |
| Varies | 4 bytes                         | Unused (skipped by the renderer)                   |
| Varies | numTriangles \* 16 bytes        | Textured triangles                                 |
| Varies | numQuads \* 20 bytes            | Textured quads                                     |
| Varies | numColoredTriangles \* 20 bytes | Colored triangles                                  |
| Varies | numColoredQuads \* 24 bytes     | Colored quads                                      |

The renderer processes **four** primitive lists per object, not two. What was previously documented as "8 bytes always empty" is really two more list counts plus an unused u32: every vanilla monster has 0 colored primitives, which is why those bytes are always zero in monster files. The colored lists are fully supported by the engine (the same object format is used by the [battle stages](../../battle-stages/) and the magic-effect 3D models, which do use them).

#### Vertice Data

| Offset | Length                | Description                       |
|--------|-----------------------|-----------------------------------|
| 0      | 2 bytes               | Bone id                           |
| 2      | 2 bytes               | Number of vertices                |
| 4      | nbVertices \* 6 bytes | Vertices (nbVertices \* 3 shorts) |

Each vertex is three `s16` (x, y, z), relative to the bone: at render time the whole batch is transformed by the world matrix of `Bone id`.

### Primitive records

All four record types share the same building blocks:

- **Vertex index** (`u16`): the low 12 bits index the object's vertex pool. On the **first** index of each record, the top 4 bits are a **depth bias** (see below); on the other indexes they must be 0 (the renderer uses them unmasked).
- **UV** (2 × `u8`): texture coordinate of one corner, in texture-page pixels.
- **CLUT** (`u16`): PSX colour look-up table selector — which palette from the [textures](../textures/) TIMs the face is drawn with.
- **TPage** (`u16`): PSX texture-page selector — which VRAM page the texture is sampled from. If any of bits `0xFE00` are set, the face is **skipped** by the renderer (disabled face).
- **Color command** (`u32`, colored records only): the raw GPU command dword `{red, green, blue, code}` used for that face. When the object's lighting flag is on, the RGB is re-modulated by the current light before drawing.

Textured triangle (16 bytes):

| Offset | Length | Description                     |
|--------|--------|---------------------------------|
| 0      | 2      | Vertex index A (+ depth bias)   |
| 2      | 2      | Vertex index B                  |
| 4      | 2      | Vertex index C                  |
| 6      | 2      | UV of C                         |
| 8      | 2      | UV of A                         |
| 10     | 2      | CLUT                            |
| 12     | 2      | UV of B                         |
| 14     | 2      | TPage                           |

Note the UV order quirk: **C, A, B** — not A, B, C.

Textured quad (20 bytes):

| Offset | Length | Description                     |
|--------|--------|---------------------------------|
| 0      | 2      | Vertex index A (+ depth bias)   |
| 2      | 2      | Vertex index B                  |
| 4      | 2      | Vertex index C                  |
| 6      | 2      | Vertex index D                  |
| 8      | 2      | UV of A                         |
| 10     | 2      | CLUT                            |
| 12     | 2      | UV of B                         |
| 14     | 2      | TPage                           |
| 16     | 2      | UV of C                         |
| 18     | 2      | UV of D                         |

Colored triangle (20 bytes) = textured triangle + color command `u32` at offset 16.
Colored quad (24 bytes) = textured quad + color command `u32` at offset 20.

### Depth bias (the "unknown" top bits)

The top 4 bits of the **first vertex index** of every record are a per-face **depth-sort bias**: the renderer computes `bias = (index >> 12) − 8` and adds it to the face's depth before inserting it into the ordering table. So:

| Top nibble | Effect                                    |
|------------|-------------------------------------------|
| 8          | No bias (the normal value — hence `0x8000` looks "always set") |
| < 8        | Face sorts closer to the camera            |
| > 8        | Face sorts further from the camera         |

This is used to fix depth-sorting artifacts on a per-face basis (e.g. forcing decals/eyes in front of the surface they sit on). Masking indices with `& 0xFFF` is still the correct way to extract the vertex index.

### Semi-transparency

Monster models have **no per-face semi-transparency flag**. The renderer builds each GPU primitive with its command byte taken from a **per-object render state**: the entity's model palette word supplies the command RGB, and its bit 25 is the GPU ABE (semi-transparency enable) bit — so a whole object is drawn either opaque (codes `0x24`/`0x2C`) or semi-transparent (`0x26`/`0x2E`). That bit is set at runtime by transparency effects (e.g. the *Vanish*/hidden state, ghost enemies), **not** stored in the geometry or textures.

Consequently the [textures](../textures/) CLUTs set the PSX STP bit (`0x8000`) on essentially every colour as a convention: when an object's ABE is enabled every pixel blends, and by default (ABE off) everything is opaque. A static model viewer should therefore render monsters **opaque** and ignore the ubiquitous texel STP bit.

### How an entity is rendered (pipeline summary)

Every frame, the per-entity renderer:

1. Draws the shadow quad (unless hidden).
2. Composes the camera × entity-scale matrix, then multiplies it through every bone of the [skeleton](../skeleton/) skeleton (the per-bone results live in the bones' runtime matrix area).
3. For each geometry object whose bit is set in the entity's **visibility bitmask** (`some_flag_data`; bits are cleared by [animation sequences](../animation-sequences/) `E5 0x20` hide-part and the `A6` detach opcode):
   - transforms each Vertice Data batch with its bone matrix into a screen-space pool (x, y, depth + clip flags per vertex);
   - walks the four primitive lists; each face is dropped if any vertex is off-screen/clipped, if all its vertices are outside the same frustum plane, if it is back-facing (screen-space cross product), or if its TPage has the disabled-face bits;
   - emits the GPU packet into the ordering table at `min(vertex depths) + depth bias`.
4. Repeats with the weapon model (`dXwYYY.dat`), if any.

The same `RenderGeometry` routine draws monsters, characters, weapons, battle-stage groups and magic-effect models — the object format is identical everywhere.

### Reference (names & addresses)

FF8_EN.exe:

| Name                           | Address    | Role                                                                     |
|--------------------------------|------------|--------------------------------------------------------------------------|
| `BS_RenderBattleEntity`        | `0x502D40` | Per-entity draw: shadow, bone matrices, model then weapon                 |
| `BS_ComputeBonesWorldMatrices` | `0x5095B0` | Multiplies the camera matrix through every bone of a skeleton             |
| `RenderGeometry`               | `0x5099D0` | Walks the object table, applies the visibility bitmask            |
| `ParseVertices`                | `0x50F900` | Transforms one bone's vertex batch to screen space (x, y, depth, clip)    |
| `ParsePolygons`                | `0x50FDF0` | Builds GPU packets from the four primitive lists (bias, cull, hide, ABE)  |
| `IsPolygonFrontFacing_Cross2D` | `0x510680` | Screen-space cross product for backface culling                           |
