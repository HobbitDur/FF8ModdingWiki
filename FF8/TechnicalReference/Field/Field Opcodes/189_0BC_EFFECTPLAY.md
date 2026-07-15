---
layout: default
parent: Field Opcodes
title: 0BC_EFFECTPLAY
nav_order: 189
permalink: /technical-reference/field/field-opcodes/0bc-effectplay/
---

-   Opcode: **0x0BC**
-   Short name: **EFFECTPLAY**
-   Long name: Play sound effect

#### Argument

none

#### Stack

  
*FF8Audio Field ID -7850*

*Sound channel (must be power of 2)*

*Pan (0=left, 255=right)*

*Volume (0-127)*

**EFFECTPLAY**

#### Description

Plays a sound effect through the given sound channel. The channel is important because it's the parameter used in [SESTOP](../0cd-sestop/).

Unlike [EFFECTPLAY2](../021-effectplay2/). For example, when you touch a save point, it calls EFFECTPLAY on sound 30, which turns out to be sound 7880 in field IDs.

Sound channel 0 appears to be able to play sounds while it's already playing sounds. Each other channels can only play one sound at a time.

The handler pops all four values (volume first, then pan, then channel, then the sound id) and calls `PlayWorldSound(soundId, channel, pan, volume)`. Returns 2.

PC handler: `SCRIPT_EFFECTPLAY`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_EFFECTPLAY` | 0x51FEA0 | Field script opcode handler (verified IDA function) |
