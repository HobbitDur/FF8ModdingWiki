---
layout: default
parent: Field Opcodes
title: 0B4_MUSICCHANGE
nav_order: 181
permalink: /technical-reference/field/field-opcodes/0b4-musicchange/
---

-   Opcode: **0x0B4**
-   Short name: **MUSICCHANGE**
-   Long name: Start music

#### Argument

none

#### Stack

none

#### Description

Starts playing the music track preloaded by [MUSICLOAD](../0b5-musicload/), replacing the current field music. Takes no arguments and pops nothing. If nothing has been loaded (the load flag `unk_1D9CDE0` is 0) it does nothing and returns 2. Otherwise it clears the load flag, plays the loaded track, applies the saved music volume and returns 3 (yield).

PC handler: `SCRIPT_MUSICCHANGE` at 0x51F7F0.
