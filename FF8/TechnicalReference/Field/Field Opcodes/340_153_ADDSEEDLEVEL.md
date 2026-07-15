---
layout: default
parent: Field Opcodes
title: 153_ADDSEEDLEVEL
nav_order: 340
permalink: /technical-reference/field/field-opcodes/153-addseedlevel/
---

-   Opcode: **0x153**
-   Short name: **ADDSEEDLEVEL**
-   Long name: Add SeeD Level

#### Argument

none

#### Stack

  
Amount

**ADDSEEDLEVEL**

#### Description

Add the given amount of points to the player's SeeD level. Pops one value (the amount) and adds it to `VAR_MAP_ADDRESS->SeeDRankPoints`, then clamps the result: if below 100 it is forced to 100, and it is capped at 3100.

100 points per rank - minimum 100 (rank 1), maximum 3100 (rank A)

PC handler: `SCRIPT_ADDSEEDLEVEL`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ADDSEEDLEVEL` | 0x522480 | Field script opcode handler (verified IDA function) |
