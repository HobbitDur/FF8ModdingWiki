---
layout: default
parent: Field Opcodes
title: 025_LADDERUP
nav_order: 38
permalink: /technical-reference/field/field-opcodes/025-ladderup/
---

-   Opcode: **0x025**
-   Short name: **LADDERUP**
-   Long name: Climb ladder (up)

#### Argument

Destination walkmesh triangle ID (16-bit).

#### Stack

  
*XCoord*

*YCoord*

*ZCoord*

*Climb animation ID*

**LADDERUP**

#### Description

Moves this entity onto a ladder and climbs "up". The top stack value is an animation ID that is started immediately (looping) via the model animation call; the next three values are the destination X, Y, Z, stored as fixed-point world coordinates (`move_pos_x/y/z`, entity+436/+440/+444, shifted left by 12). The inline 16-bit argument is the destination walkmesh triangle ID (entity+508). The handler sets `motion_state` (entity+572) to 3 (ladder mode) and seeds the climb direction field `move_angle_current` (entity+538) with 1 (up). It returns 1 (wait) while climbing and 2/3 when the motion completes, pausing the script until the climb finishes.

Identical to [LADDERDOWN](../026-ladderdown/) except for the direction seed (1 for up, 0 for down).

PC handler: `SCRIPT_LADDERUP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_LADDERUP` | 0x525900 | Field script opcode handler (verified IDA function) |
