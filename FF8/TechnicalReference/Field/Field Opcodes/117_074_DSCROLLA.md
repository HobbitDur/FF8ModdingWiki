---
layout: default
parent: Field Opcodes
title: 074_DSCROLLA
nav_order: 117
permalink: /technical-reference/field/field-opcodes/074-dscrolla/
---

-   Opcode: **0x074**
-   Short name: **DSCROLLA**
-   Long name: Scroll To Actor

#### Argument

none

#### Stack

  
*Actor Code (use PSHAC)*

**DSCROLLA**

#### Description

Scrolls the screen onto the given actor. The handler pops one word (the script actor id, normally pushed with [PSHAC](../013-pshac/)), looks up that entity, and stores its character/model index (`entity+598`) as the scroll target (`FIELD_SCROLL_TARGET_ENTITY`). It selects scroll **mode 0** (`FIELD_SCROLL_MODE = 0`, the "track this entity" mode) and resets the scroll phase to 0. Returns 3 (done + yield).

PC handler: `SCRIPT_DSCROLLA`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_DSCROLLA` | 0x520D50 | Field script opcode handler (verified IDA function) |
