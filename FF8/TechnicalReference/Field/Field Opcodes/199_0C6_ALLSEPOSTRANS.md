---
layout: default
parent: Field Opcodes
title: 0C6_ALLSEPOSTRANS
nav_order: 199
permalink: /technical-reference/field/field-opcodes/0c6-allsepostrans/
---

-   Opcode: **0x0C6**
-   Short name: **ALLSEPOSTRANS**
-   Long name: Transition Pan for all Sound Effects

#### Argument

none

#### Stack

  
*Final pan*

*Frame count*

**ALLSEPOSTRANS**

#### Description

Fades the stereo pan of all sound-effect channels to a target position over a duration. The handler pops two values (not three): the frame count first (top of stack) and the final pan second, then calls the all-channel pan-transition routine with the frame count doubled as the step count. Returns 2. Never used in the retail game (only in a test area).

PC handler: `SCRIPT_ALLSEPOSTRANS`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ALLSEPOSTRANS` | 0x520040 | Field script opcode handler (verified IDA function) |
