---
layout: default
parent: Field Opcodes
title: 159_SEALEDOFF
nav_order: 346
permalink: /technical-reference/field/field-opcodes/159-sealedoff/
---

-   Opcode: **0x159**
-   Short name: **SEALEDOFF**
-   Long name: Enable Sealed Options (Ultimecia's Castle)

#### Argument

none

#### Stack

  
*Option flags*

**SEALEDOFF**

#### Description

Enables (un-seals) features of the game pertaining to the last dungeon's mechanic (items, saving, etc). Pops one value (the option flags) and **clears** those bits from the current map seal: `map_seal = ~flags & map_seal`. The result is written to `VAR_MAP_ADDRESS->map_seal`, `MAP_SEAL` and `SG_SETTING.mapSeal`, then `engine_restore_game_status` re-applies it. So each bit passed here re-enables (unlocks) the corresponding feature that [LASTIN](../157-lastin/) sealed.

Whether or not these are enabled/disabled is stored in [byte 334](../../Miscellaneous/Variables). 0=Sealed, 1=Unsealed

Flags:

  
1\. Items

2\. Magic

4\. GF

8\. Draw

16\. Command Ability

32\. Limit Break

64\. Resurrection

128\. Save

PC handler: `SCRIPT_SEALEDOFF`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SEALEDOFF` | 0x51E9C0 | Field script opcode handler (verified IDA function) |
