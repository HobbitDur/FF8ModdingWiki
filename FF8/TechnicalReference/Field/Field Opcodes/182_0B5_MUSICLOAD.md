---
layout: default
parent: Field Opcodes
title: 0B5_MUSICLOAD
nav_order: 182
permalink: /technical-reference/field/field-opcodes/0b5-musicload/
---

-   Opcode: **0x0B5**
-   Short name: **MUSICLOAD**
-   Long name: Load Music

#### Argument

none

#### Stack

  
*Music Track*

**MUSICLOAD**

#### Description

Preloads a new field music track. The handler pops one byte (the track number) into the savemap and kicks off an asynchronous load of that AKAO sequence. It blocks the script until the load finishes, returning 1 (wait) while loading and 2 once the track is ready. Start the loaded track with [MUSICCHANGE](../0b4-musicchange/).

PC handler: `SCRIPT_MUSICLOAD`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MUSICLOAD` | 0x51F730 | Field script opcode handler (verified IDA function) |
