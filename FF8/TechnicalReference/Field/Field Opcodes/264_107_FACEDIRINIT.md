---
layout: default
parent: Field Opcodes
title: 107_FACEDIRINIT
nav_order: 264
permalink: /technical-reference/field/field-opcodes/107-facedirinit/
---

-   Opcode: **0x107**
-   Short name: **FACEDIRINIT**
-   Long name: Initiate Head Facing

#### Argument

none

#### Stack

  
**FACEDIRINIT**

#### Description

Call this before using any other FACEDIR functions. It "unlocks" the character's head from its model. The handler reads the model's current head orientation and initializes the entity's head-tracking fields (+552/+556/+560) from it. Takes no stack arguments.

PC handler: `SCRIPT_FACEDIRINIT`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_FACEDIRINIT` | 0x528350 | Field script opcode handler (verified IDA function) |
