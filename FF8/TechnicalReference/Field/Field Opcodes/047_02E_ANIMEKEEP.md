---
layout: default
parent: Field Opcodes
title: 02E_ANIMEKEEP
nav_order: 47
permalink: /technical-reference/field/field-opcodes/02e-animekeep/
---

-   Opcode: **0x02E**
-   Short name: **ANIMEKEEP**
-   Long name: Animate, keep last frame

#### Argument

Model Animation ID

#### Stack

none

#### Description

Play an animation, then freeze the model on the last frame of the animation. Same as [ANIME](../02d-anime/) but the handler uses the "keep last frame" animation mode (sets the `execution_flags` animation bits, entity+352, to 0x80 instead of 0x40). Pauses the script until the animation finishes, then returns 3.

PC handler: `SCRIPT_ANIMEKEEP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ANIMEKEEP` | 0x526620 | Field script opcode handler (verified IDA function) |
