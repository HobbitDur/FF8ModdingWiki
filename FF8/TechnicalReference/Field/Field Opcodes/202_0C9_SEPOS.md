---
layout: default
parent: Field Opcodes
title: 0C9_SEPOS
nav_order: 202
permalink: /technical-reference/field/field-opcodes/0c9-sepos/
---

-   Opcode: **0x0C9**
-   Short name: **SEPOS**
-   Long name: Set Sound Effect Pan

#### Argument

none

#### Stack

  
*Sound channel*

*Pan (0-255)*

**SEPOS**

#### Description

Sets the pan of the sound playing in *sound channel*. 0=left, 255=right. Pops two values (channel mask, then pan) and calls the SFX pan routine (`Sfx_SetPan_Mask`); *sound channel* is the channel bit-mask used when the effect was started.

PC handler: `SCRIPT_SEPOS` at 0x520110.
