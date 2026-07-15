---
layout: default
parent: Field Opcodes
title: 03F_MOVEA
nav_order: 64
permalink: /technical-reference/field/field-opcodes/03f-movea/
---

-   Opcode: **0x03F**
-   Short name: **MOVEA**
-   Long name: Move to Actor

#### Argument

none

#### Stack

  
*Actor ID* (always use PSHAC)

*Movement angle*

**MOVEA**

#### Description

Makes this entity move towards another actor. The top stack value is popped into the entity's movement-angle field (`move_angle_current`, entity+538); the actor ID beneath it stays on the stack and is re-read every frame, so the destination (`move_pos_x/y/z`, entity+436/+440/+444) is refreshed from that actor's live position (`pos_x/y/z`, entity+400/+404/+408) as it moves. Uses the same walk/run animation selection as [MOVE](../03e-move/) and sets `motion_state` (entity+572) to 1. On arrival (`motion_substate` == 2) it pops the actor ID, restores the idle animation and returns 2.

PC handler: `SCRIPT_MOVEA`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MOVEA` | 0x523640 | Field script opcode handler (verified IDA function) |
