---
layout: default
parent: Field Opcodes
title: 0C5_ALLSEPOS
nav_order: 198
permalink: /technical-reference/field/field-opcodes/0c5-allsepos/
---

-   Opcode: **0x0C5**
-   Short name: **ALLSEPOS**
-   Long name: Set Pan for all Sound Effects

#### Argument

none

#### Stack

  
*Pan*

**ALLSEPOS**

#### Description

Sets the stereo pan of all sound-effect channels at once. The handler pops one value (the pan position) and applies it to every SE channel immediately (no transition). Returns 2. Never used in the retail game.

PC handler: `SCRIPT_ALLSEPOS`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_ALLSEPOS` | 0x520010 | Field script opcode handler (verified IDA function) |
