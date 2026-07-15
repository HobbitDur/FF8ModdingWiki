---
layout: default
parent: Field Opcodes
title: 0C0_MUSICVOL
nav_order: 193
permalink: /technical-reference/field/field-opcodes/0c0-musicvol/
---

-   Opcode: **0x0C0**
-   Short name: **MUSICVOL**
-   Long name: Set Music Volume

#### Argument

none

#### Stack

  
*Channel slot (0 or 1)*

*Volume (0-127)*

**MUSICVOL**

#### Description

Sets the volume of a field music channel. The handler pops the volume first and the channel slot second (masked to 0 or 1 — the two music handles FF8 keeps). It applies the new volume with a short fixed 16-step transition (`Music_SetVolumeTrans`) and stores it in the savemap so it survives a field reset. The 0/1 parameter shared by the music opcodes selects which of the two music channels to act on. Returns 2.

PC handler: `SCRIPT_MUSICVOL`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MUSICVOL` | 0x51FC70 | Field script opcode handler (verified IDA function) |
