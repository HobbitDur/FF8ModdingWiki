---
layout: default
parent: Field Opcodes
title: 0CC_BATTLEMODE
nav_order: 205
permalink: /technical-reference/field/field-opcodes/0cc-battlemode/
---

-   Opcode: **0x0CC**
-   Short name: **BATTLEMODE**
-   Long name: Edit random battle flags

#### Argument

none

#### Stack

  
*Battle Flags*

**BATTLEMODE**

#### Description

Set which flags are present during random battles.

#### Battle Flags

  
+0: Regular battle.

+1: ?

+2: Disable victory fanfare (battle music keeps playing after win/loss)

+4: Inherit countdown timer from field.

+8: ? (prevents items/xp from being earned when used in otherwise regular battles)

+16: Use current music as battle music.

+32: ?

+64: ?

+128: ?

+256: ?

The handler pops one 16-bit value and stores it both into a savemap field and into the global `ENCOUTER_BATTLE_FLAG`, which the encounter/battle setup reads when the next battle starts.

PC handler: `SCRIPT_BATTLEMODE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_BATTLEMODE` | 0x523230 | Field script opcode handler (verified IDA function) |
