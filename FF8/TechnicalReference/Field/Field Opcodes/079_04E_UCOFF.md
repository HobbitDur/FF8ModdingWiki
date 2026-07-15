---
layout: default
parent: Field Opcodes
title: 04E_UCOFF
nav_order: 79
permalink: /technical-reference/field/field-opcodes/04e-ucoff/
---

-   Opcode: **0x04E**
-   Short name: **UCOFF**
-   Long name: User Control Off

#### Argument

none

#### Stack

none

#### Description

Disable user control. Sets `MENU_DISABLED` and the user-control-off flag, then freezes each of the up-to-three party field entities: their animation is reset to the base (idle) animation and their execution flags are set so the player can no longer move them. Player can still advance dialogue. No stack use. Ends when [UCON](../04d-ucon/) is called.

PC handler: `SCRIPT_UCOFF`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_UCOFF` | 0x51DE90 | Field script opcode handler (verified IDA function) |
