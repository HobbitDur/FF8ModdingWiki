---
layout: default
parent: Field Opcodes
title: 072_LSCROLL
nav_order: 115
permalink: /technical-reference/field/field-opcodes/072-lscroll/
---

-   Opcode: **0x072**
-   Short name: **LSCROLL**
-   Long name: L? Scroll

#### Argument

none

#### Stack

  
*X*

*Y*

*Frame count*

**LSCROLL**

#### Description

Starts a background/camera scroll toward target offset (*X*, *Y*), taking *frame count* frames to get there. The handler pops the three words (frame count first, then *Y*, then *X*), stores them in the shared scroll state (`FIELD_SCROLL_TARGET_X`, `FIELD_SCROLL_TARGET_Y`, `FIELD_SCROLL_DURATION`) and selects scroll **mode 4** (`FIELD_SCROLL_MODE = 4`), resetting the scroll phase to 0. The opcode only arms the scroll and returns immediately; use [SCROLLSYNC](../077-scrollsync/) to wait for completion.

`LSCROLL` differs from [DSCROLL](../071-dscroll/) (mode 3) only in the mode index it writes: `DSCROLL` takes no duration (snaps directly), `LSCROLL` interpolates over *frame count*, and [CSCROLL](../073-cscroll/) (mode 5) uses the same three parameters with a different interpolation curve.

PC handler: `SCRIPT_LSCROLL`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_LSCROLL` | 0x520C90 | Field script opcode handler (verified IDA function) |
