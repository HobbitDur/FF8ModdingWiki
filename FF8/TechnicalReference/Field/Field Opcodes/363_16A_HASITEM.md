---
layout: default
parent: Field Opcodes
title: 16A_HASITEM
nav_order: 363
permalink: /technical-reference/field/field-opcodes/16a-hasitem/
---

-   Opcode: **0x16A**
-   Short name: **HASITEM**
-   Long name: Has item

#### Argument

#### Stack

  
*Item ID*

**HASITEM**

#### Description

If the party has the item with the given ID, pushes 1 to temporary variable 0. Otherwise, pushes 0.

PC handler: `SCRIPT_HAS_ITEM`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_HAS_ITEM` | 0x522350 | Field script opcode handler (verified IDA function) |
