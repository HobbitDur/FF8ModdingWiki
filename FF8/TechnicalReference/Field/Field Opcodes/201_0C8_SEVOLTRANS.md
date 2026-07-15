---
layout: default
parent: Field Opcodes
title: 0C8_SEVOLTRANS
nav_order: 201
permalink: /technical-reference/field/field-opcodes/0c8-sevoltrans/
---

-   Opcode: **0x0C8**
-   Short name: **SEVOLTRANS**
-   Long name: Sound Effect Volume Transition

#### Argument

none

#### Stack

  
*Sound channel*

*Frame count*

*Final volume*

**SEVOLTRANS**

#### Description

Fades the volume of one sound-effect channel to a target level over a duration. The handler pops the final volume first (top of stack), the frame count second, and the channel third, then calls `Sfx_SetVolumeTrans_Mask` with the frame count doubled as the transition step count. Returns 2.

PC handler: `SCRIPT_SEVOLTRANS`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SEVOLTRANS` | 0x5200C0 | Field script opcode handler (verified IDA function) |
