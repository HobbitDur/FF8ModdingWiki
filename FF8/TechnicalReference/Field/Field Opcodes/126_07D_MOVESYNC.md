---
layout: default
parent: Field Opcodes
title: 07D_MOVESYNC
nav_order: 126
permalink: /technical-reference/field/field-opcodes/07d-movesync/
---

-   Opcode: **0x07D**
-   Short name: **MOVESYNC**
-   Long name: Move Sync

#### Argument

none

#### Stack

  
**MOVESYNC**

#### Description

Pauses script execution until this entity has finished its current move. The handler tests this entity's move-state word (`entity+542`): it returns 2 (done, advance) when the state equals 2, otherwise returns 1 (wait, retry next frame). Takes no arguments and pops nothing.

PC handler: `SCRIPT_MOVESYNC` at 0x524600.
