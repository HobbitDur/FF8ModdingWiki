---
layout: default
parent: Field Opcodes
title: 027_LADDERUP2
nav_order: 40
permalink: /technical-reference/field/field-opcodes/027-ladderup2/
---

-   Opcode: **0x027**
-   Short name: **LADDERUP2**
-   Long name: Climb ladder along 3-point path (up)

#### Stack

  
*X1?*

*Y1?*

*Z1?*

*X2?*

*Y2?*

*Z2?*

*X3?*

*Y3?*

*Z3?*

**LADDERUP2**

#### Description

Extended ladder-climb ("up" direction) that follows a three-waypoint path. Nine coordinates are popped and stored as fixed-point world coordinates (shifted left by 12): the first point into `move_pos_x/y/z` (entity+436/+440/+444), the second into `move_target_x/y/z` (entity+448/+452/+456), and the third into a further coordinate triple (entity+424/+428/+432). The inline 16-bit argument is the destination walkmesh triangle ID (entity+508). The handler sets `motion_state` (entity+572) to 4 (three-point ladder mode) and seeds the direction field `move_angle_current` (entity+538) with 1 (up). Unlike [LADDERUP](../025-ladderup/) it does not start an animation itself. It pauses the script until the motion completes.

Identical to [LADDERDOWN2](../028-ladderdown2/) except for the direction seed (1 for up, 0 for down).

PC handler: `SCRIPT_LADDERUP2`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_LADDERUP2` | 0x525B60 | Field script opcode handler (verified IDA function) |
