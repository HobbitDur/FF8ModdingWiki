---
layout: default
parent: Field Opcodes
title: 087_SUBPARTY
nav_order: 136
permalink: /technical-reference/field/field-opcodes/087-subparty/
---

-   Opcode: **0x087**
-   Short name: **SUBPARTY**
-   Long name: Remove party member from active party

#### Argument

none

#### Stack

  
*Player-Character ID*

**SUBPARTY**

#### Description

Removes a PC from the active party. The handler pops one word (the character id). If the character occupies an active-party slot it clears that field slot (sets it to -1) and clears the battle-party entry. It then refreshes game status and, as a safety pass, revives any remaining active-party member left at 0 HP (sets HP to 1 and clears the KO status bit). The character stays available (this only removes them from the active trio). Returns 2.

See [SETPARTY](../08a-setparty/) for the character id list.

PC handler: `SCRIPT_SUBPARTY` at 0x51E270.
