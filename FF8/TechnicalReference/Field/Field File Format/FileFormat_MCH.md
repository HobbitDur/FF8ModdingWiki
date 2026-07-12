---
layout: default
parent: Field File Format
title: Field Character Models
author: Koral, JWP, Vehek, HobbitDur
permalink: /technical-reference/field/field-file-format/field-character-models/
---

1. TOC
{:toc}

## Overview

Each MCH file contains a skinned, animated model of a main character on the field. The `field/model/main_chr.fs` archive holds one MCH per main character variant (d000–d075: Squall, Rinoa, Laguna, SeeD uniforms, spacesuits, kid versions...). Extract it with [Deling](https://github.com/myst6re/deling).

An MCH contains TIM textures, mesh geometry, a skeleton, skinning information and a single rest-pose animation. **Field animations for main characters are not stored in the MCH**: each field's [chara.one](FileFormat_ONE) stores the animations used on that field, and the game combines them with the MCH geometry at runtime.

NPC models embedded inside chara.one use the exact same **Model Data** structure described below (sections 1–7), just without the 256-byte MCH header — everything on this page except the header applies to them too.

The skeleton/animation details below were verified against the field model runtime of FF8_EN.exe (2000 PC version); see [Runtime](#runtime-ff8_enexe) for the function addresses.

## Coordinate systems and units

- Model data uses PSX-style axes: **x right, y down (vertical), z forward**. Vertices are stored in bone-local space.
- The field world above the model is **z-vertical** (entity facing is a rotation around Z); the engine stands the y-authored model up with a constant RotY(+90°) "pre-root" (see [Decoding the skeleton](#decoding-the-skeleton)).
- Vertices, bone lengths and animation root offsets share the same unit: 1/256 of a world unit. The character scale stored in [chara.one](FileFormat_ONE) (main characters only, scale = raw/16, typically 256) rescales vertices: `effective_vertex = raw * 256 / scale`.
- All angles: **4096 = full circle** (360°).

## Header

`0x100 bytes [256 bytes]`

| Offset | Length  | Description                                             |
|--------|---------|---------------------------------------------------------|
| 0x00   | 4 bytes | Offset to texture 0 (TIM)                               |
| ...    | 4 bytes | Offset to texture n, until the value 0xFFFFFFFF is read |
| next   | 4 bytes | 0xFFFFFFFF terminator                                   |
| next   | 4 bytes | Offset to Model Data                                    |
| ...    | ...     | Padding up to 0x100                                     |

All offsets are absolute (from the start of the file).

## Textures

Standard [TIM format](../PSX/TIM_format) textures, 128x128, 4-bit (16 colors) or 8-bit (256 colors) paletted. The face's `texture index` (section 4) selects the TIM in header order.

## Model Data

The model data starts with a 64-byte header. All offsets in it are relative to the start of the model data.

| Offset | Length  | Description                            |
|--------|---------|----------------------------------------|
| 0x00   | 4 bytes | Number of skeleton bones               |
| 0x04   | 4 bytes | Number of vertices                     |
| 0x08   | 4 bytes | Size of the texture animation section  |
| 0x0C   | 4 bytes | Number of faces                        |
| 0x10   | 4 bytes | Number of unknown data entries (section 5) |
| 0x14   | 4 bytes | Number of skin objects                 |
| 0x18   | 4 bytes | Unknown                                |
| 0x1C   | 2 bytes | Triangle count                         |
| 0x1E   | 2 bytes | Quad count                             |
| 0x20   | 4 bytes | Offset of bones (section 1)            |
| 0x24   | 4 bytes | Offset of vertices (section 2)         |
| 0x28   | 4 bytes | Offset of texture animations (section 3) |
| 0x2C   | 4 bytes | Offset of faces (section 4)            |
| 0x30   | 4 bytes | Offset of unknown data (section 5)     |
| 0x34   | 4 bytes | Offset of skin objects (section 6)     |
| 0x38   | 4 bytes | Offset of animation data (section 7)   |
| 0x3C   | 4 bytes | Unknown (often 0x01040118 / 0x01180104-like values) |

## Section 1: Skeleton

64 bytes per bone, in hierarchy order (parents always come before their children). These records are copied **verbatim** into the engine's runtime bone array at model creation, which is why most of the record is zero: the engine uses it as scratch space for the per-frame matrices.

| Offset | Length   | Description                                                                     |
|--------|----------|---------------------------------------------------------------------------------|
| 0x00   | 2 bytes  | Parent bone (1-based; 0 = root)                                                  |
| 0x02   | 2 bytes  | Parent **runtime record index** (byte offset / 64). The runtime array has an extra record 0 (the engine "pre-root"), so this equals (parent bone 0-based index + 1); 0 for the root bone |
| 0x04   | 2 bytes  | Bone vector X (always 0)                                                         |
| 0x06   | 2 bytes  | Bone vector Y (always 0)                                                         |
| 0x08   | 2 bytes  | Bone vector Z = **bone length** (signed, always negative)                        |
| 0x0A   | 54 bytes | Zero padding. Runtime scratch: +6..+11 current angles, +20 computed 3x3 matrix, +38 computed world position |

A bone's children are positioned at `parent_world_matrix * (0, 0, parent_length) + parent_position`: bones extend along their parent's local Z axis.

## Section 2: Vertices

8 bytes per vertex, in bone-local space (see section 6 for which bone owns which vertices).

```
struct vertex {
    int16    x, y, z;
    int16    unknown;
};
```

(sizeof = 8)

## Section 3: Texture animation

Used for eye blinking (that is why the minimum size is 0x14). The engine picks a random delay, then cycles the replacement frames by copying rectangles in VRAM over the original area.

```
struct tex_anim {
    uint8    unknown;
    uint8    total_textures;
    uint8    unknown;
    uint8    uSize;
    uint8    vSize;
    uint8    replacement_coords_count;
    uv_pair  original_area_coords;   // 2 bytes: u, v
    uint8    unknown[2];
    uv_pair  replacement_coords[replacement_coords_count];
};
```

## Section 4: Faces

64 bytes per face. Triangles and quads share the same record size; the opcode tells them apart.

```
struct face {
    uint32   opcode;             // 0x25010607 = triangle, 0x2d010709 = quad (values read little-endian)
    uint8    unknown[4];
    int16    flags;              // bit 0x04 = semi-transparency
    uint8    unknown[2];
    uint16   vertex_indexes[4];  // GPU strip order; triangles use the first 3
    uint16   edge_data[4];       // unknown, edge related?
    uint32   vertex_colors[4];   // RGBA per corner
    uint16   tex_coords[4];      // low byte = u, high byte = v (0..128); pairs with vertex_indexes slot by slot
    uint16   padding;
    uint16   texture_index;      // index into the header TIM list
    uint32   padding2[2];
};
```

(sizeof = 64)

Notes for decoding:

- Vertex indices are in triangle-strip order: a quad's perimeter is `(0, 1, 3, 2)`; drawn as triangles it is `(0,1,3)` + `(0,2,3)`.
- Each `tex_coords[i]` belongs to `vertex_indexes[i]`.
- UVs are in pixels of the 128x128 TIM selected by `texture_index` (divide by 128 to normalize). The V axis is top-down like the TIM data (only flip it for tools with bottom-left UV origins, like Blender).

## Section 5: Unknown data

Seems to split up the skin objects, triangles and quads into draw groups:

```
struct unknown_group {
    uint16   start_skinobject_index;
    uint16   skinobject_count;
    uint8    unknown[12];
    uint16   start_triangle_index;
    uint16   triangle_count;
    uint16   start_quad_index;
    uint16   quad_count;
    uint8    unknown2[8];
};
```

(sizeof = 32)

## Section 6: Skin objects

8 bytes per skin object. Skinning is rigid: each vertex belongs to exactly one bone, by contiguous ranges.

```
struct skin_object {
    uint16   first_vertex;   // 0-based
    uint16   vertex_count;
    uint16   bone_id;        // 1-based
    uint16   unknown;
};
```

(sizeof = 8)

To pose a vertex: `world_vertex = bone_world_matrix * vertex + bone_world_position` using the matrices from [Decoding the skeleton](#decoding-the-skeleton).

## Section 7: Animation data

Two different layouts exist. Both start with the same header:

| Offset | Length  | Description          |
|--------|---------|----------------------|
| 0x00   | 2 bytes | Number of animations |

Then for each animation:

| Offset | Length  | Description  |
|--------|---------|--------------|
| 0x00   | 2 bytes | Frame count  |
| 0x02   | 2 bytes | Bone count   |
| 0x04   | ...     | Frames       |

### Uncompressed frames (main_chr MCH rest pose)

The single animation embedded in a main_chr MCH uses plain 16-bit values. Frame layout:

| Offset | Length          | Description                                        |
|--------|-----------------|----------------------------------------------------|
| 0x00   | 3 \* 2 bytes    | Root offset x, y, z (signed, 1/256 world units)    |
| 0x06   | bone_count \* 6 | Per bone: int16 rotX, rotY, rotZ (4096 = full circle) |

### Packed frames (chara.one animations, and NPC models' section 7)

The format used by every field animation. Frame layout:

| Offset | Length          | Description                                     |
|--------|-----------------|-------------------------------------------------|
| 0x00   | 3 \* 2 bytes    | Root offset x, y, z (signed, 1/256 world units) |
| 0x06   | bone_count \* 4 | Packed poses, 4 bytes per bone                  |

Each 4-byte pose packs three **10-bit** angles; byte 4 holds the two extra high bits of each. The engine shifts them left twice before using its 4096-entry sine/cosine tables (indexed `& 0xFFF`), so the effective resolution is 1024 steps per full circle:

```
rotX = ((b1 | ((b4 & 0x03) << 8)) << 2) & 0xFFF
rotY = ((b2 | ((b4 & 0x0C) << 6)) << 2) & 0xFFF
rotZ = ((b3 | ((b4 & 0x30) << 4)) << 2) & 0xFFF
```

Values are 12-bit two's complement after the shift (4096 = 360°). Bits 0x40/0x80 of byte 4 are unused. Note: older community documentation assigned these three values to Z/X/Y — the engine's own decode maps byte 1→X, byte 2→Y, byte 3→Z.

## Decoding the skeleton

The complete, engine-exact recipe to pose a model (verified against in-game poses, including compound-rotation bones like Irvine's coat and Rinoa's duster):

```
// Angles from section 7 (either format), 4096 = full circle, classic
// right-handed rotation matrices, positive angles, column vectors.

// The engine parents every model under an extra "pre-root":
world[PRE_ROOT]    = RotY(+90 deg)                       // stands the y-down model up into the z-vertical field world
position[PRE_ROOT] = frame_root_offset (x, y, z)         // plus the SETGETA height on z

for each bone i (parents first):
    local     = RotX(a_i) * RotY(b_i) * RotZ(c_i)
    p         = parent of i (PRE_ROOT for the root bone)
    world[i]  = world[p] * local
    position[i] = world[p] * (0, 0, length[p]) + position[p]   // length[PRE_ROOT] = 0

for each skin object, for each of its vertices v:
    world_v = world[bone] * v + position[bone]
```

On the field, two more matrices sit above the pre-root: the entity rotation (facing, built from angles (0, 0, yaw) — a Z rotation, since the field world is z-vertical) and the camera.

Beware of representation pitfalls when re-implementing: the engine stores its 3x3 matrices column-major and its vector transform consumes the words row-wise. The formulas above are expressed in the standard "matrix times column vector" form, which is what you want in a modern renderer; if your result looks plausible on single-axis rotations but twists torsos or coat panels, your composition order/signs are conjugated — test against a compound-rotation bone.

## Runtime (FF8_EN.exe)

Function addresses for the 2000 PC version:

| Address  | Name                                | Role |
|----------|-------------------------------------|------|
| 0x531980 | Field_CharaCreateModelInstance      | Copies the bone records into the runtime array of (bone_count + 1) 64-byte records, creates the pre-root record 0 with angles (0, 1024, 0), builds the GPU primitive buffers from the faces |
| 0x533CD0 | Field_CharaAnimateAndBuildSkeletons | Per frame: decodes packed poses into the bone records, writes the root offset (+ GETA height, field script opcode SETGETA) into the pre-root, walks the hierarchy building matrices/positions |
| 0x533F90 | Field_CharaBuildBoneRotationMatrix  | Builds a rotation matrix from 3 angles using SIN_TABLE_4096 (0xB924BC) / COS_TABLE_4096 (0xB944C0), index & 0xFFF |
| 0x531DA0 | Field_CharaModelCommand             | Command-style API for field scripts (command 32 = read a bone's decoded pose, used by the FACEDIR opcodes) |
| 0x532930 | Field_CharaUpdateTextureAnim        | Eye-blink texture animation (random timer, VRAM rectangle copies) |
| 0x532AE1 | Field_CharaOne                      | chara.one loader |

Useful model instance fields (instances in `CHARA_MODEL_INSTANCE_TABLE`, 0x1DCB340): +4 runtime bone array, +8 animation data pointer, +82 frame counter (frame << 4, low bits = interpolation subframe), +98 GETA height offset, +112/113 blink texture ids, +114 flags (bit 2 = uncompressed 8-byte poses).

A working reference implementation of this whole page (parser + skeleton math) is available in [FF8UltimateEditor](https://github.com/HobbitDur/FF8UltimateEditor) (`FF8GameData/mch/mchanalyser.py`, used by the Seed field model viewer).

## MCH Model File List

<small>todo</small>
