---
layout: default
parent: Field Opcodes
title: 03A_LINEON
nav_order: 59
permalink: /technical-reference/field/field-opcodes/03a-lineon/
---

-   Opcode: **0x03A**
-   Short name: **LINEON**
-   Long name: Line Collisions On

#### Argument

none

#### Stack

  
**LINEON**

#### Description

Enables line collisions with this entity by writing 1 to the line's active flag (entity+404). Returns 2 (done + continue).

PC handler: `SCRIPT_LINEON`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_LINEON` | 0x51DCE0 | Field script opcode handler (verified IDA function) |
