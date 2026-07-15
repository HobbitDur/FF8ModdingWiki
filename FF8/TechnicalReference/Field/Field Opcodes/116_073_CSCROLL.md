---
layout: default
parent: Field Opcodes
title: 073_CSCROLL
nav_order: 116
permalink: /technical-reference/field/field-opcodes/073-cscroll/
---

-   Opcode: **0x073**
-   Short name: **CSCROLL**
-   Long name: C? Scroll

#### Argument

none

#### Stack

  
*X*

*Y*

*Frame count*

**CSCROLL**

#### Description

Starts a background/camera scroll toward target offset (*X*, *Y*) over *frame count* frames, identical to [LSCROLL](../072-lscroll/) except it selects scroll **mode 5** instead of mode 4. The handler pops the three words (frame count first, then *Y*, then *X*), stores them in the shared scroll state (`FIELD_SCROLL_TARGET_X`, `FIELD_SCROLL_TARGET_Y`, `FIELD_SCROLL_DURATION`), sets `FIELD_SCROLL_MODE = 5` and resets the scroll phase to 0. Wait for completion with [SCROLLSYNC](../077-scrollsync/).

The original Square symbol for this opcode is `SCSROLL` (a typo for CSCROLL preserved in the executable).

PC handler: `SCRIPT_SCSROLL`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SCSROLL` | 0x520CF0 | Field script opcode handler (verified IDA function) |
