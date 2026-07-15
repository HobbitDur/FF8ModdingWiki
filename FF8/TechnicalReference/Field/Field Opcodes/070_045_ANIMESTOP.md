---
layout: default
parent: Field Opcodes
title: 045_ANIMESTOP
nav_order: 70
permalink: /technical-reference/field/field-opcodes/045-animestop/
---

-   Opcode: **0x045**
-   Short name: **ANIMESTOP**
-   Long name: Stop animation, return to base

#### Argument

none

#### Stack

  
**ANIMESTOP**

#### Description

Returns this entity to its [base animation](../02c-baseanime/). The handler reloads the idle animation `baseanim1` (entity+591) as the current animation, resets the animation frame counters, and switches the animation mode to looping (`execution_flags` bits set to 0x20, entity+352). Takes no arguments; returns 3 (done + yield).

PC handler: `SCRIPT_ANIMESTOP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ANIMESTOP` | 0x5264F0 | Field script opcode handler (verified IDA function) |
