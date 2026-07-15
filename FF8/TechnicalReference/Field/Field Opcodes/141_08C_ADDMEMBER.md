---
layout: default
parent: Field Opcodes
title: 08C_ADDMEMBER
nav_order: 141
permalink: /technical-reference/field/field-opcodes/08c-addmember/
---

-   Opcode: **0x08C**
-   Short name: **ADDMEMBER**
-   Long name: Add party member to game

#### Argument

none

#### Stack

  
*Player-Character ID*

**ADDMEMBER**

#### Description

Adds a PC to the available roster (not to the active party). The handler pops one word (the character id) and sets that character's availability flags: main-cast ids set bits in `SG_ARRAY_CHARA_DATA[id].Exists` (Squall/id 0 and the guest ids 4/6/7 use a reduced flag set, the others get the full "selectable" flags), while Laguna-party ids 8-10 set the matching bit in the savemap `miscFlag`. It does not place the character in the active party. Returns 2.

See [SETPARTY](../08a-setparty/) for the character id list.

PC handler: `SCRIPT_ADDMEMBER`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ADDMEMBER` | 0x51E670 | Field script opcode handler (verified IDA function) |
