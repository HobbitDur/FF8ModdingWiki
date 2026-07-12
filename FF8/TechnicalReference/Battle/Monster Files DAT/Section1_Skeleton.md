---
title: Section 1 - Skeleton
layout: default
parent: Monster files (c0mxxx.dat)
permalink: /technical-reference/battle/monster-files-c0mxxxdat/section-1-skeleton/
nav_order: 1
---

## Section 1: Skeleton

More info on [OpenVIII](https://github.com/MaKiPL/OpenVIII/blob/4ac151daad7cd1475eb0694dd0715bc35d7a4b39/FF8/debug_battleDat.cs)

| Offset | Length                      | Description     |
|--------|-----------------------------|-----------------|
| 0      | 1 byte                      | Number of bones |
| 1      | 1 byte                      | Extra data      |
| 2      | 6 bytes                     | Unknown         |
| 8      | s16f (divide by 4096f)      | scaleX          |
| 10     | s16f (divide by 4096f)      | scale -Z        |
| 12     | s16f (divide by 4096f)      | scale Y         |
| 14     | 2 bytes                     | Unknown         |
| 16     | Number of bones \* 48 bytes | Bones           |

When "Extra data" is 1, it adds 3 axes transformations to be read from the bone struct. In vanilla, this extra data flag is always at 0.

### Bone struct

| Offset | Length                 | Description              |
|--------|------------------------|---------------------------|
| 0      | 2 bytes                | Parent id                |
| 2      | s16f (divide by 4096f) | Bone size (?)            |
| 4      | s16f (divide by 4096f) | RotX, multiplied by 360f |
| 6      | s16f (divide by 4096f) | RotY, multiplied by 360f |
| 8      | s16f (divide by 4096f) | RotZ, multiplied by 360f |
| 10     | s16f (divide by 4096f) | someX                    |
| 12     | s16f (divide by 4096f) | someY                    |
| 14     | s16f (divide by 4096f) | someZ                    |
| 16     | 32 bytes               | Unknown (often empty)    |

SomeX, someY and someZ are read only if the "Extra data" flag is set.
If the entity is slowed, the RotX, RotY and RotZ are divided by 2.
The 3 rotation are added to the animation, so it's a fix bone change applied to all animation.
