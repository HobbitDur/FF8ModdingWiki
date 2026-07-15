---
layout: default
parent: Field Opcodes
title: 02D_ANIME
nav_order: 46
permalink: /technical-reference/field/field-opcodes/02d-anime/
---

-   Opcode: **0x02D**
-   Short name: **ANIME**
-   Long name: Play animation

#### Argument

Model Animation ID

#### Stack

none

#### Description

Play an animation, then return the model to its base animation. The inline argument is the animation ID; the handler starts it in play-once mode (sets animation-mode bits in `execution_flags` entity+352 to 0x40) and pauses the script — returning 1 (wait) each frame — until the "animation active" flag (bit 0x800) clears, then returns 3 (done + yield).

PC handler: `SCRIPT_ANIME`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ANIME` | 0x526570 | Field script opcode handler (verified IDA function) |
