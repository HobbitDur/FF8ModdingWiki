---
layout: default
parent: Field Opcodes
title: 0BD_EFFECTLOAD
nav_order: 190
permalink: /technical-reference/field/field-opcodes/0bd-effectload/
---

-   Opcode: **0x0BD**
-   Short name: **EFFECTLOAD**
-   Long name: Play Ambient Sound Loop

#### Argument

none

#### Stack

  
*Effect ID*

**EFFECTLOAD**

#### Description

Start playing a background looping ("ambient") sound effect. The handler pops one byte (the effect id), stores it in the savemap (`unk777[18]`), and triggers the ambient-effect change (`SmEffectChange`) which selects the effect file by id from the filename table (`off_B8ED00`). It blocks until the effect is ready (returning 1 while loading, 2 when done). The stored id is also re-applied by the field's sound reset path, so the ambient loop persists. Sound effect IDs follow no pattern I can see from the FMT file.

  
Test data

-   5 = Train
-   10 = Lava cavern

PC handler: `SCRIPT_EFFECTLOAD`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_EFFECTLOAD` | 0x51FDE0 | Field script opcode handler (verified IDA function) |
