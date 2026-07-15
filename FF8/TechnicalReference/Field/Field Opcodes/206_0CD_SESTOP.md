---
layout: default
parent: Field Opcodes
title: 0CD_SESTOP
nav_order: 206
permalink: /technical-reference/field/field-opcodes/0cd-sestop/
---

-   Opcode: **0x0CD**
-   Short name: **SESTOP**
-   Long name: Stop sound effect

#### Argument

none

#### Stack

  
*Channel (must be a power of 2)*

**SESTOP**

#### Description

Stop the sound effect currently playing on the given channel. Channel is defined in the call to [EFFECTPLAY2](../021-effectplay2/) and must be a power of 2. The handler reads the channel value from the stack and, while the entity's ready bit is set, stops the sound; it can yield (return 1) until the stop completes before advancing.

PC handler: `SCRIPT_SESTOP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SESTOP` | 0x5201A0 | Field script opcode handler (verified IDA function) |
