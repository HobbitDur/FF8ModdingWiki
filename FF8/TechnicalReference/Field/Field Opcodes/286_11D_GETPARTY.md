---
layout: default
parent: Field Opcodes
title: 11D_GETPARTY
nav_order: 286
permalink: /technical-reference/field/field-opcodes/11d-getparty/
---

-   Opcode: **0x11D**
-   Short name: **GETPARTY**
-   Long name: Get characetr in party slot

#### Argument

none

#### Stack

  
*Party Slot*

**GETPARTY**

#### Description

Writes the character ID in the given party slot into temporary variable 0 (the entity's I[0] result register at +320). The handler pops the slot index and reads `SG_PARTY_FIELD1[slot]` from the savemap; only slots 0-2 are valid, so passing 3 or greater reads out of bounds and gives garbage (so don't do it!).

PC handler: `SCRIPT_GETPARTY`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_GETPARTY` | 0x51E640 | Field script opcode handler (verified IDA function) |
