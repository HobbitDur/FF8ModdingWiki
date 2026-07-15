---
layout: default
parent: Field Opcodes
title: 020_IDUNLOCK
nav_order: 33
permalink: /technical-reference/field/field-opcodes/020-idunlock/
---

-   Opcode: **0x020**
-   Short name: **IDUNLOCK**
-   Long name: Unlock walkmesh ID

#### Argument

Walkmesh triangle ID

#### Stack

none

#### Description

Unlocks a walkmesh triangle so things can walk over it. The handler clears the corresponding bit in the walkmesh blocked-triangle bitmap (`FIELD_WALKMESH_BLOCKED_BITS[id/8] &= ~(1 << (id%8))`). Takes no stack values. Returns 2.

PC handler: `SCRIPT_IDUNLOCK`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_IDUNLOCK` | 0x51D830 | Field script opcode handler (verified IDA function) |
