---
layout: default
parent: Field Opcodes
title: 026_LADDERDOWN
nav_order: 39
permalink: /technical-reference/field/field-opcodes/026-ladderdown/
---

-   Opcode: **0x026**
-   Short name: **LADDERDOWN**
-   Long name: Climb ladder (down)

#### Argument

Destination walkmesh triangle ID (16-bit).

#### Stack

  
*XCoord*

*YCoord*

*ZCoord*

*Climb animation ID*

**LADDERDOWN**

#### Description

Moves this entity onto a ladder and climbs "down". The top stack value is an animation ID that is started immediately (looping); the next three values are the destination X, Y, Z stored as fixed-point world coordinates (`move_pos_x/y/z`, entity+436/+440/+444, shifted left by 12). The inline 16-bit argument is the destination walkmesh triangle ID (entity+508). The handler sets `motion_state` (entity+572) to 3 (ladder mode) and seeds the climb direction field `move_angle_current` (entity+538) with 0 (down). It returns 1 (wait) while climbing and 2/3 on completion, pausing the script until the climb finishes.

Identical to [LADDERUP](../025-ladderup/) except for the direction seed (1 for up, 0 for down).

PC handler: `SCRIPT_LADDERDOWN` at 0x525A30.
