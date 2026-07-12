---
title: Section 3 - Model animation
layout: default
parent: Monster files (c0mxxx.dat)
permalink: /technical-reference/battle/monster-files-c0mxxxdat/section-3-model-animation/
nav_order: 3
---

## Section 3: Model animation

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

| Offset | Length                          | Description                                                              |
|--------|----------------------------------|----------------------------------------------------------------------------|
| 0      | LocationVectorData              | LocationVectorData                                                       |
| Varies | 1 BIT                           | Mode bit (1 if there is additional data in RotationVectorData, bUnk1...) |
| Varies | RotationVectorData * bonesCount | Rotation Vector data per bone                                            |

### Location vector data

| Offset | Length       | Description |
|--------|--------------|-------------|
| 0      | PositionType | Location X  |
| Varies | PositionType | Location Y  |
| Varies | PositionType | Location Z  |

### Rotation vector data

| Offset | Length                      | Description |
|--------|-------------------------------|-------------|
| 0      | RotationType                | Rotation X  |
| Varies | RotationType                | Rotation Y  |
| Varies | RotationType                | Rotation Z  |
| Varies | 1 BIT                       | bUnk1       |
| Varies | 0 if bUnk1==0, else 16 BITs | Unk1 data   |
| Varies | 1 BIT                       | bUnk2       |
| Varies | 0 if bUnk2==0, else 16 BITs | Unk2 data   |
| Varies | 1 BIT                       | bUnk3       |
| Varies | 0 if bUnk3==0, else 16 BITs | Unk3 data   |

We don't know what the Unk1, Unk2 and Unk3 do. Enemies works without them, but as it's important to keep up with the current bit position, we need to read it
anyway

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

| PositionTypeBits value | Bits to read for one vector axis |
|--------------------------|-----------------------------------|
| 0b00                   | 3                                 |
| 0b01                   | 6                                 |
| 0b10                   | 8                                 |
| 0b11                   | 12                                |
