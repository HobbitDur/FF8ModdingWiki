---
layout: default
parent: Field Opcodes
title: 138_PHSPOWER
nav_order: 313
permalink: /technical-reference/field/field-opcodes/138-phspower/
---

-   Opcode: **0x138**
-   Short name: **PHSPOWER**
-   Long name: Enable/Disable PHS

#### Argument

none

#### Stack

  
*0 or 1 (0=disable, 1=enable)*

**PHSPOWER**

#### Description

Enables or disables the ability to switch party members. Pops one value: non-zero **enables** PHS (clears bit `0x0200` of the field `miscFlag`), zero **disables** it (sets bit `0x0200` of `miscFlag` and also clears bit `0x02` of `unk11[5]`).

PC handler: `SCRIPT_PHSPOWER` at 0x522230.
