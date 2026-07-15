---
layout: default
parent: Field Opcodes
title: 01F_IDLOCK
nav_order: 32
permalink: /technical-reference/field/field-opcodes/01f-idlock/
---

-   Opcode: **0x01F**
-   Short name: **IDLOCK**
-   Long name: Lock walkmesh ID

#### Argument

Walkmesh triangle ID

#### Stack

none

#### Description

Locks a walkmesh triangle so nothing can walk over it. The handler sets the corresponding bit in the walkmesh blocked-triangle bitmap (`FIELD_WALKMESH_BLOCKED_BITS[id/8] |= 1 << (id%8)`). Takes no stack values. Returns 2.

PC handler: `SCRIPT_IDLOCK`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_IDLOCK` | 0x51D7F0 | Field script opcode handler (verified IDA function) |
