---
layout: default
parent: Field Opcodes
title: 132_MOVIECUT
nav_order: 307
permalink: /technical-reference/field/field-opcodes/132-moviecut/
---

-   Opcode: **0x132**
-   Short name: **MOVIECUT**
-   Long name: ?

#### Argument

none

#### Stack

  
**MOVIECUT**

#### Description

Sets bit `0x0100` of the field variable-map `miscFlag` (`VAR_MAP_ADDRESS->miscFlag`) and returns. This is a persistent flag on the field savemap; it takes no stack or inline arguments. Mostly seen in debug rooms, so its visible in-game effect is minimal, but it is not a pure no-op — it does flip that flag bit.

PC handler: `SCRIPT_MOVIECUT`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MOVIECUT` | 0x51F600 | Field script opcode handler (verified IDA function) |
