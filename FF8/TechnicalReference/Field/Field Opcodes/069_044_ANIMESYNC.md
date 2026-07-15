---
layout: default
parent: Field Opcodes
title: 044_ANIMESYNC
nav_order: 69
permalink: /technical-reference/field/field-opcodes/044-animesync/
---

-   Opcode: **0x044**
-   Short name: **ANIMESYNC**
-   Long name: Animation Synchronize

#### Argument

none

#### Stack

none

#### Description

Pauses this script until the entity's current animation is finished playing. Each frame it tests the "animation active" bit (0x800) of `execution_flags` (entity+352): while the bit is set it returns 1 (wait), and once it clears it returns 2 (done + continue). Takes no arguments and pops nothing.

PC handler: `SCRIPT_ANIMESYNC`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ANIMESYNC` | 0x5264D0 | Field script opcode handler (verified IDA function) |
