---
layout: default
parent: Field Opcodes
title: 035_RANIMELOOP
nav_order: 54
permalink: /technical-reference/field/field-opcodes/035-ranimeloop/
---

-   Opcode: **0x035**
-   Short name: **RANIMELOOP**
-   Long name: Resume script, Play looping animation

#### Argument

Model Animation ID

#### Stack

none

#### Description

Loops an animation. Starts the animation given by the inline argument in looping mode (`execution_flags` bits set to 0x20, entity+352) and returns 3 (done + yield) immediately, so the animation keeps cycling while the script continues.

PC handler: `SCRIPT_RANIMELOOP`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_RANIMELOOP` | 0x526A30 | Field script opcode handler (verified IDA function) |
