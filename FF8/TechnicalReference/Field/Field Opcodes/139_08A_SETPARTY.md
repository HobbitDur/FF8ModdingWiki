---
layout: default
parent: Field Opcodes
title: 08A_SETPARTY
nav_order: 139
permalink: /technical-reference/field/field-opcodes/08a-setparty/
---

-   Opcode: **0x08A**
-   Short name: **SETPARTY**
-   Long name: Set active party members

#### Argument

none

#### Stack

  
*Character ID*

*Character ID*

*Character ID*

**SETPARTY**

#### Description

Sets the active party to be the members with the input IDs. The handler pops the three ids and writes them to field party slots 0, 1 and 2 in push order (the first id pushed becomes the party leader), then rebuilds the battle party from those ids. A value of 255 leaves that slot blank. Afterward it refreshes game status and revives any active member left at 0 HP (HP set to 1, KO status cleared). Returns 2. These IDs also work with the other party related functions.

-   0 Squall
-   1 Zell
-   2 Irvine
-   3 Quistis
-   4 Rinoa
-   5 Selphie
-   6 Seifer
-   7 Edea
-   8 Laguna
-   9 Kiros
-   10 Ward
-   255 Blank

PC handler: `SCRIPT_SETPARTY` at 0x51E400.
