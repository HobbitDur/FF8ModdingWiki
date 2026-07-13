---
title: Skeleton
layout: default
parent: Model file sections
permalink: /technical-reference/battle/model-sections/skeleton/
nav_order: 1
author: HobbitDur
---

## Skeleton

More info on [OpenVIII](https://github.com/MaKiPL/OpenVIII/blob/4ac151daad7cd1475eb0694dd0715bc35d7a4b39/FF8/debug_battleDat.cs)

| Offset | Length                      | Description                                       |
|--------|-----------------------------|---------------------------------------------------|
| 0      | 1 byte                      | Number of bones                                   |
| 1      | 1 byte                      | Per-bone-scale flag (historically "Extra data")   |
| 2      | s16                         | Model scale                                       |
| 4      | 2 bytes                     | Unknown (not read by the PC engine)               |
| 6      | 2 bytes                     | Unknown (not read by the PC engine)               |
| 8      | s16                         | Root translation X (animated)                     |
| 10     | s16                         | Root translation Y (animated)                     |
| 12     | s16                         | Root translation Z (animated)                     |
| 14     | 2 bytes                     | Unknown (not read by the PC engine)               |
| 16     | Number of bones \* 48 bytes | Bones                                             |

**Per-bone-scale flag** (offset 1): when 1, each bone's `scaleX/scaleY/scaleZ` (below) is applied to the bone transforms. It is 0 in **all** vanilla files at rest — but it is not static: every [model animation](../model-animation/) animation frame carries a *mode bit* that overwrites this flag, so it effectively toggles per frame during playback (this is how the squash-and-stretch monsters animate their scale).

**Model scale** (offset 2): the model's global size factor, applied to the root bone matrix and the root translation. It tracks the monster's on-screen size — ≈120–210 for human-sized entities (soldiers ≈ 189, Wedge 73), up to 1822 for Bahamut and 8754 for the final Ultimecia. At battle start the engine also stores this value ×4 on the entity, where it feeds the [animation sequences](../animation-sequences/) distance/speed formulas (C3 `0x10`/`0x11`) — bigger monsters are approached from farther away.

**Root translation X/Y/Z** (offsets 8/10/12, previously documented as "scale x / -z / y"): the model's world-space root offset. Each animation frame *adds* its location-vector deltas to these three fields, and the transform code consumes them as the root position (multiplied by the model scale). The file values are the starting offsets.

### Bone struct

| Offset | Length                 | Description                                              |
|--------|------------------------|----------------------------------------------------------|
| 0      | 2 bytes                | Parent id                                                |
| 2      | s16f (divide by 4096f) | Bone size                                                |
| 4      | s16f (divide by 4096f) | RotX, multiplied by 360f                                 |
| 6      | s16f (divide by 4096f) | RotY, multiplied by 360f                                 |
| 8      | s16f (divide by 4096f) | RotZ, multiplied by 360f                                 |
| 10     | s16 (1024 = 1.0)       | Bone scale X (written per frame by the animation)        |
| 12     | s16 (1024 = 1.0)       | Bone scale Y (idem)                                      |
| 14     | s16 (1024 = 1.0)       | Bone scale Z (idem)                                      |
| 16     | 20 bytes               | Runtime bone matrix (see below)                          |
| 36     | 12 bytes               | Runtime scratch                                          |

The bone **scale** fields (offsets 10/12/14, previously `someX/someY/someZ`) are the per-bone squash-and-stretch factors, base 1024 = 1.0, hierarchical (a child's effective scale is multiplied by its parent's). They are only consumed on frames whose mode bit sets the per-bone-scale flag, and their values come from the animation stream's [scale channels](../model-animation/#scale-channel-formerly-unk1unk2unk3) — the rest-pose values in the file are never read (a few big models even carry garbage there).

If the entity is slowed, the RotX, RotY and RotZ are divided by 2.
The 3 rotation are added to the animation, so it's a fix bone change applied to all animation.

The last 32 bytes of each bone are **not file data** — they are the bone's runtime workspace, which is why they are empty (zero) in the files on disk. The first 20 bytes hold the bone's computed **3×3 rotation matrix** (nine `s16` cells plus padding, in PSX column order) that the animation code rebuilds every frame; the remaining 12 bytes are additional per-frame scratch.
