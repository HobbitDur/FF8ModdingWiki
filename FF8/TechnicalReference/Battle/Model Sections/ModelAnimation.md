---
title: Model animation
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/model-animation/
nav_order: 3
author: HobbitDur
---

## Model animation

More info on [OpenVIII](https://github.com/MaKiPL/OpenVIII/blob/4ac151daad7cd1475eb0694dd0715bc35d7a4b39/FF8/debug_battleDat.cs)

### Header (data sub table)

| Offset      | Length                  | Description          |
|-------------|-------------------------|-----------------------|
| 0           | 4 bytes                 | Number of animations |
| 4           | nbAnimations \* 4 bytes | Animations Pointers  |
| AnimPointer | Varies                  | Animation            |

### Animation

| Offset | Length | Description      |
|--------|--------|-------------------|
| 0      | 1 byte | Number of frames |
| 1      | Varies | Animation frame  |

### Animation frame

Each frame is one vector location and BonesCount*RotationVectorData. Vector location is used to manipulate the model in world space, where all the animation is
rotating each bone.
The frames work accumulatively, so in order to get the final rotation at in example frame 5, you have to add all rotations from frames 0,1,2,3 and 4.
(The location vector deltas accumulate the same way, into the root-translation fields of the [skeleton](../skeleton/) header. Per-bone **scale** values, on the other hand, are absolute — see below.)

| Offset | Length                          | Description                                                                                   |
|--------|---------------------------------|-----------------------------------------------------------------------------------------------|
| 0      | LocationVectorData              | LocationVectorData                                                                            |
| Varies | 1 BIT                           | Mode bit: 1 = every RotationVectorData of this frame carries the per-bone scale channels      |
| Varies | RotationVectorData * bonesCount | Rotation Vector data per bone                                                                 |

The **mode bit** is stored into the skeleton's per-bone-scale flag each frame (the byte at offset 1 of the [skeleton](../skeleton/) header, historically called "Extra data"). It selects, for that frame only, which of the two bone-transform paths the engine uses: rotation-only, or rotation + per-bone scale.

### Location vector data

| Offset | Length       | Description |
|--------|--------------|-------------|
| 0      | PositionType | Location X  |
| Varies | PositionType | Location Y  |
| Varies | PositionType | Location Z  |

### Rotation vector data

| Offset | Length                        | Description                                    |
|--------|-------------------------------|------------------------------------------------|
| 0      | RotationType                  | Rotation X                                     |
| Varies | RotationType                  | Rotation Y                                     |
| Varies | RotationType                  | Rotation Z                                     |
| Varies | ScaleChannel (see below)      | Bone scale X — only present when the frame's mode bit is 1 |
| Varies | ScaleChannel                  | Bone scale Y — idem                            |
| Varies | ScaleChannel                  | Bone scale Z — idem                            |

### Scale channel (formerly Unk1/Unk2/Unk3)

The three optional 16-bit payloads are **per-bone scale factors** — FF8's squash-and-stretch animation system. Each channel is:

| Offset | Length                        | Description                                    |
|--------|-------------------------------|------------------------------------------------|
| 0      | 1 BIT                         | Payload present                                |
| Varies | 0 if not present, else 16 BITs| Scale value − 1024                             |

Semantics (all verified in the PC engine):

- The final scale is `payload + 1024` when the payload bit is set, and exactly **1024 when it is not** — and 1024 means **1.0 (neutral)**. So an absent payload is not "no data", it is "reset this bone's scale to normal".
- Unlike rotations, scale values are **absolute per frame**, not accumulated.
- Scale is **hierarchical**: at transform time a child bone's effective scale is `parent_scale × value / 1024`, so scaling a parent squashes its whole subtree.
- The values land in the bone's `scaleX/scaleY/scaleZ` fields (offsets 10/12/14 of the [skeleton](../skeleton/) bone struct); when the frame's mode bit is 0 the engine takes the rotation-only path and those fields are ignored.

**Vanilla usage** (from an exact re-implementation of the engine's bit reader, run over all 143 monster files — 3103 animations, 0 decode mismatches): 22 monsters use the scale channels in 259 animations, values typically 0.7×–1.2×. The users are exactly what squash-and-stretch suggests — gelatinous monsters (Blobra, Gerogero, Abyss Worm, Funguar, Tonberry King, Creeps, Forbidden, Imp, Torama, Gargantua, Abadon, Elvoret, Elnoyle) and machines with pistons/telescoping parts (X-ATM092, BGH251F2 both forms, Mobile Type 8, Droma), plus Odin and Fujin.

So enemies indeed "work without them" — any monster whose animations never set the mode bit — but for the 22 listed monsters these channels are real animation data that a viewer/exporter must apply to reproduce the original motion.

### Position type

Position is BIT length. First we read the count of bits to read by reading first 2 bits.

| Offset | Length           | Description      |
|--------|------------------|-------------------|
| 0      | 2 BITs           | PositionTypeBits |
| 0+0b11 | PositionTypeBits | Vector axis      |

#### PositionTypeBits

| PositionTypeBits value | Bits to read for one vector axis |
|-------------------------|-----------------------------------|
| 0b00                   | 3                                 |
| 0b01                   | 6                                 |
| 0b10                   | 9                                 |
| 0b11                   | 16                                |

### Rotation type

Rotation is also BIT length. First read first bit to see, if there's rotation data. If no, continue. If yes, then read the rotation data similar to Position
Type

| Offset  | Length           | Description                           |
|---------|-------------------|-----------------------------------------|
| 0       | 1 BIT            | IsRotationTypeAvailable               |
| 0+0b1   | 2 BIT            | RotationTypeBits                      |
| 0+0b100 | RotationTypeBits | Rotation vector axis (pitch/yaw/roll) |

#### RotationTypeBits

| RotationTypeBits value | Bits to read for one vector axis |
|------------------------|----------------------------------|
| 0b00                   | 3                                |
| 0b01                   | 6                                |
| 0b10                   | 8                                |
| 0b11                   | 12                               |

### Bitstream details

- Bits are read **LSB-first** within each byte.
- Multi-bit values (position, rotation, scale payloads) are **sign-extended** from their bit width.
- The stream is continuous across frames — frames are **not** byte-aligned; the engine saves its byte+bit position between rendered frames and resumes there.
- When the entity is *Slow*ed, the engine halves the decoded position and rotation deltas as it applies them (the stream itself is unchanged).

### Reference (names & addresses)

FF8_EN.exe:

| Name                                | Address    | Role                                                                    |
|-------------------------------------|------------|-------------------------------------------------------------------------|
| `Battle_ReadAnimation`              | `0x508F90` | Per-frame decoder: location vector, mode bit, per-bone rotations/scales  |
| `bitReader`                         | `0x5092A0` | Reads n bits LSB-first, sign-extends                                     |
| `Battle__ReadPositionType`          | `0x509320` | 2-bit type + {3,6,9,16}-bit signed value                                 |
| `Battle__ReadRotationType`          | `0x509370` | 1 presence bit, then 2-bit type + {3,6,8,12}-bit signed value            |
| `Battle__ReadBoneScale`             | `0x5093F0` | 1 presence bit; absent → 1024 (neutral), present → 16-bit payload + 1024 |
| `ProcessFieldEntitiesTransformation`| `0x508C90` | Builds bone world matrices; separate rotation-only / rotation+scale paths|
| `positionReadHelper`                | `0xB8B9F0` | {3, 6, 9, 16} bit-count table                                            |
| `rotationReadHelper`                | `0xB8B9F4` | {3, 6, 8, 12} bit-count table                                            |
