---
layout: default
parent: Field Opcodes
title: 0C1_MUSICVOLTRANS
nav_order: 194
permalink: /technical-reference/field/field-opcodes/0c1-musicvoltrans/
---

-   Opcode: **0x0C1**
-   Short name: **MUSICVOLTRANS**
-   Long name: Music Volume Transition

#### Argument

none

#### Stack

  
*Channel slot (0 or 1)*

*Transition time (in frames)*

*Final volume (0-127)*

**MUSICVOLTRANS**

#### Description

Fades a field music channel's volume to a target level over a duration. The handler pops the final volume first, the transition time second, and the channel slot third (masked to 0 or 1). It calls `Music_SetVolumeTrans` with the transition time doubled internally (the step count passed is 2 × the frame value) and stores the target volume in the savemap. The 0/1 parameter selects which of the two music channels to act on. Returns 2.

PC handler: `SCRIPT_MUSICVOLTRANS`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MUSICVOLTRANS` | 0x51FCD0 | Field script opcode handler (verified IDA function) |
