---
layout: default
parent: Field Opcodes
title: 158_LASTOUT
nav_order: 345
permalink: /technical-reference/field/field-opcodes/158-lastout/
---

-   Opcode: **0x158**
-   Short name: **LASTOUT**
-   Long name: Last dungeon out

#### Argument

none

#### Stack

none

#### Description

Ends the effects of [LASTIN](../157-lastin/). Takes no arguments: clears bit `0x0800` of the field `miscFlag`, zeroes the map seal (`MAP_SEAL = 0`, `SG_SETTING.mapSeal = 0`) so all features are unlocked again, and calls `engine_restore_game_status`.

PC handler: `SCRIPT_LASTOUT`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_LASTOUT` | 0x51E990 | Field script opcode handler (verified IDA function) |
