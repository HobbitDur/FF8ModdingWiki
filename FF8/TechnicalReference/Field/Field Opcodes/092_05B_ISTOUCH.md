---
layout: default
parent: Field Opcodes
title: 05B_ISTOUCH
nav_order: 92
permalink: /technical-reference/field/field-opcodes/05b-istouch/
---

-   Opcode: **0x05B**
-   Short name: **ISTOUCH**
-   Long name: Is Touching

#### Argument

none

#### Stack

  
*Actor code* (set by [PSHAC](../013-pshac/)

**ISTOUCH**

#### Description

Pops one value (an actor code, set with [PSHAC](../013-pshac/)) and writes into temp variable I[0] (+320) the result of a touch test between this entity and that actor: nonzero if they are in contact/touch range, 0 if the actor has no live field entity. Read the result with `PSHI_L 0`. Non-blocking.

PC handler: `SCRIPT_ISTOUCH`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ISTOUCH` | 0x51ED80 | Field script opcode handler (verified IDA function) |
