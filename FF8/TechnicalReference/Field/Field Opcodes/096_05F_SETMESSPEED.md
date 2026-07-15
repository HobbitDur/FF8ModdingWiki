---
layout: default
parent: Field Opcodes
title: 05F_SETMESSPEED
nav_order: 96
permalink: /technical-reference/field/field-opcodes/05f-setmesspeed/
---

-   Opcode: **0x05F**
-   Short name: **SETMESSPEED**
-   Long name: Set Message Speed

#### Argument

none

#### Stack

  
*Message Channel*

*Speed (always 6144)*

**SETMESSPEED**

#### Description

Reads two stack values (message channel and speed) and calls the text engine's set-message-speed routine with them. Higher speed values print the message faster.

This is only used twice and both in the same place: During the Ragnarok scene right before the dialogue goes to "auto-play" mode and that dreadful song starts. Because it's never called anywhere else, it's safe to assume that it's field-specific. In other words, changing areas "resets" the message speed.

PC handler: `SCRIPT_SETMESSPEED`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SETMESSPEED` | 0x528E10 | Field script opcode handler (verified IDA function) |
