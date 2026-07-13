---
layout: default
parent: Field Opcodes
title: 086_ADDPARTY
nav_order: 135
permalink: /technical-reference/field/field-opcodes/086-addparty/
---

-   Opcode: **0x086**
-   Short name: **ADDPARTY**
-   Long name: Add party member to active party

#### Argument

none

#### Stack

  
*Player-Character ID*

**ADDPARTY**

#### Description

Adds a PC to the active party. The handler pops one word (the character id). If the character is not already in the active party it fills the first free active-party slot with them, points the corresponding battle-party entry at that character's data, and sets their availability flags: for main-cast ids (< 8) it flags `SG_ARRAY_CHARA_DATA[id].Exists` (with extra bits for Squall = id 0) and refreshes game status; for Laguna-party ids (8-10) it sets the matching bit in the savemap `miscFlag`. Returns 2.

See [SETPARTY](../08a-setparty/) for the character id list.

PC handler: `SCRIPT_ADDPARTY` at 0x51E160.
