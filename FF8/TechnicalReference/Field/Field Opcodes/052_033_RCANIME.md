---
layout: default
parent: Field Opcodes
title: 033_RCANIME
nav_order: 52
permalink: /technical-reference/field/field-opcodes/033-rcanime/
---

-   Opcode: **0x033**
-   Short name: **RCANIME**
-   Long name: Resume script, controlled animation

#### Argument

Model Animation ID

#### Stack

  
*Last frame of animation*

*First frame of animation*

**RCANIME**

#### Description

Play a frame range of an animation, then return the model to its base animation. The "R" (resume) variant of [CANIME](../02f-canime/): pops the first frame (top) and last frame, uses play-once mode (`execution_flags` bit 0x40, entity+352) and returns 3 immediately without waiting.

PC handler: `SCRIPT_RCANIME`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_RCANIME` | 0x526990 | Field script opcode handler (verified IDA function) |
