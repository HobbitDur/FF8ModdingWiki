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

PC handler: `SCRIPT_HAS_ITEM` at 0x522350.
