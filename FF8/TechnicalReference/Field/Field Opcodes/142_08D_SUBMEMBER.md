---
layout: default
parent: Field Opcodes
title: 08D_SUBMEMBER
nav_order: 142
permalink: /technical-reference/field/field-opcodes/08d-submember/
---

-   Opcode: **0x08D**
-   Short name: **SUBMEMBER**
-   Long name: Remove party member from game

#### Argument

none

#### Stack

  
*Player-Character ID*

**SUBMEMBER**

#### Description

Removes a PC from the available roster (and therefore from the active party). The handler pops one word (the character id), releases that character's loaded model, then clears their availability flags: main-cast ids clear the low bits of `SG_ARRAY_CHARA_DATA[id].Exists`, and Laguna-party ids 8-10 clear the matching `miscFlag` bit. Ids 6 and 7 additionally run their own cleanup routine. Returns 2.

See [SETPARTY](../08a-setparty/) for the character id list.

PC handler: `SCRIPT_SUBMEMBER` at 0x51E710.
