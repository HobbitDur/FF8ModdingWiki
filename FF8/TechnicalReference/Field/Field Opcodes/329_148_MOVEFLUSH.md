---
layout: default
parent: Field Opcodes
title: 148_MOVEFLUSH
nav_order: 329
permalink: /technical-reference/field/field-opcodes/148-moveflush/
---

-   Opcode: **0x148**
-   Short name: **MOVEFLUSH**
-   Long name: Flush Movement

#### Argument

none

#### Stack

  
**MOVEFLUSH**

#### Description

Halts the current entity's scripted movement: when the entity holds the active priority it clears the "moving" bit `0x10000` of its motion-flags dword (entity+352), which stops an in-progress MOVE/MOVEA. Returns 1 (does not advance the IP that frame).

PC handler: `SCRIPT_MOVEFLUSH`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MOVEFLUSH` | 0x5247E0 | Field script opcode handler (verified IDA function) |
