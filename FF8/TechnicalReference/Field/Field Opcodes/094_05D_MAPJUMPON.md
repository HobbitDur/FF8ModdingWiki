---
layout: default
parent: Field Opcodes
title: 05D_MAPJUMPON
nav_order: 94
permalink: /technical-reference/field/field-opcodes/05d-mapjumpon/
---

-   Opcode: **0x05D**
-   Short name: **MAPJUMPON**
-   Long name: Enable Field Exits

#### Argument

none

#### Stack

  
**MAPJUMPON**

#### Description

Lets the player leave a field via a field exit (ie walk off the screen to go to another area) by clearing the field-exit-disable flag (= 0). This is the default behavior of fields; this opcode only undoes [MAPJUMPOFF](../05e-mapjumpoff/). No stack use.

PC handler: `SCRIPT_MAPJUMPON`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MAPJUMPON` | 0x521CB0 | Field script opcode handler (verified IDA function) |
| field-exit-disable flag byte | 0x1CE4902 | Global byte, not a function |
