---
layout: default
parent: Field Opcodes
title: 164_SPUSYNC
nav_order: 357
permalink: /technical-reference/field/field-opcodes/164-spusync/
---

-   Opcode: **0x164**
-   Short name: **SPUSYNC**
-   Long name: SPU Sync

#### Argument

none

#### Stack

  
*Frame count*

**SPUSYNC**

#### Description

Pauses this script until *frame count* frames have passed since [SPUREADY](../056-spuready/) was called.

The handler compares the popped *frame count* against the elapsed-frame counter (`unk_1D9CDCC`): while fewer frames have elapsed it returns 1 (retry next frame) without advancing the IP. A frame count of 0 (or negative) instead waits on the SPU-ready poll `sub_5305C0`.

PC handler: `SCRIPT_SPUSYNC` at 0x51F5B0.
