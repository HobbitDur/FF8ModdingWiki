---
layout: default
parent: Field Opcodes
title: 0C4_ALLSEVOLTRANS
nav_order: 197
permalink: /technical-reference/field/field-opcodes/0c4-allsevoltrans/
---

-   Opcode: **0x0C4**
-   Short name: **ALLSEVOLTRANS**
-   Long name: Transition Volume of all Sound Effects

#### Argument

none

#### Stack

  
*Final Volume (0-127)*

*Frame count*

**ALLSEVOLTRANS**

#### Description

Fades the volume of all sound-effect channels to a target level over a duration. The handler pops the frame count first (top of stack) and the final volume second, then calls `Sfx_SetAllChannelsVolumeTrans(volume, 2 × frame count)` — the transition step count is the frame value doubled. Returns 2.

Note the push order: the final volume is pushed **first**, then the frame count (the reverse of most `*TRANS` opcodes).

PC handler: `SCRIPT_ALLSEVOLTRANS` at 0x51FFD0.
