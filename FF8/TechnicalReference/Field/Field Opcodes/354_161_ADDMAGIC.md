---
layout: default
parent: Field Opcodes
title: 161_ADDMAGIC
nav_order: 354
permalink: /technical-reference/field/field-opcodes/161-addmagic/
---

-   Opcode: **0x161**
-   Short name: **ADDMAGIC**
-   Long name: Add magic stock to character

#### Argument

none

#### Stack

  
*Character ID*

*Magic ID*

*Quantity*

**ADDMAGIC**

#### Description

Does exactly what you think. See [Magic Codes](../../Lists/Magic_list) for a list of magic codes.

The handler pops three values — Character ID (bottom), Magic ID, then Quantity (top). It resolves the character with `getCharIndexInParty`; if that character is in the party it calls `addMagicToPartyMember(partyMember, magicID)` up to *Quantity* times, stopping early if the stock hits its cap (100).

PC handler: `SCRIPT_ADDMAGIC`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ADDMAGIC` | 0x5222D0 | Field script opcode handler (verified IDA function) |
