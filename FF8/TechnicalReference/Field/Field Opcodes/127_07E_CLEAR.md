---
layout: default
parent: Field Opcodes
title: 07E_CLEAR
nav_order: 127
permalink: /technical-reference/field/field-opcodes/07e-clear/
---

-   Opcode: **0x07E**
-   Short name: **CLEAR**
-   Long name: New Game

#### Argument

none

#### Stack

  
**CLEAR**

#### Description

Zeroes the entire 0x400-byte (1024-byte) field-script variable block (`memset` of the savemap variable area starting at `MainStoryProgress`). This wipes every script/story variable to 0; it does not touch party, inventory or stats. Takes no arguments and pops nothing. Only used when starting a new game (and in debug rooms).

PC handler: `SCRIPT_CLEAR`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_CLEAR` | 0x51D8B0 | Field script opcode handler (verified IDA function) |
