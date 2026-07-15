---
layout: default
parent: Field Opcodes
title: 101_FACEDIROFF
nav_order: 258
permalink: /technical-reference/field/field-opcodes/101-facediroff/
---

-   Opcode: **0x101**
-   Short name: **FACEDIROFF**
-   Long name: Stop head facing

#### Argument

none

#### Stack

  
*Frame count*

**FACEDIROFF**

#### Description

End the current FACEDIR over the course of *frame count*, easing the head back to its neutral/model orientation. The handler pops one frame count, reads the head's current orientation from the model, and interpolates back over that many frames, clearing the head-lock flag. It yields until the interpolation completes.

PC handler: `SCRIPT_FACEDIROFF`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_FACEDIROFF` | 0x527E40 | Field script opcode handler (verified IDA function) |
