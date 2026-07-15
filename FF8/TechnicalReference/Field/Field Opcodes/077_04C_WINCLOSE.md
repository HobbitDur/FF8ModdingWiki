---
layout: default
parent: Field Opcodes
title: 04C_WINCLOSE
nav_order: 77
permalink: /technical-reference/field/field-opcodes/04c-winclose/
---

-   Opcode: **0x04C**
-   Short name: **WINCLOSE**
-   Long name: Close Message Window

#### Argument

none

  
*Message Channel*

**WINCLOSE**

#### Description

Pops one value (message channel) and closes the window on that channel: it clears the channel's "open"/"persistent" bits in `VAR_MAP unk[1]` and `unk[2]` and, if the window is still animating open, plays its close animation (retrying, return 1, until finished). Used to close a persistent window opened by [AMES](../065-ames/).

PC handler: `SCRIPT_WINCLOSE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_WINCLOSE` | 0x529B60 | Field script opcode handler (verified IDA function) |
