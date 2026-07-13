---
layout: default
parent: Field Opcodes
title: 16F_UNKNOWN10
nav_order: 368
permalink: /technical-reference/field/field-opcodes/16f-unknown10/
---

-   Opcode: **0x16F**
-   Short name: **UNKNOWN10**
-   Long name: Music status (PC stub)

#### Argument

none

#### Stack

none

#### Description

On PSX this pushed the playing music track's current position into temporary variable 0 — it is always called just before a map transition, and the stored result is the parameter of MUSICSKIP after the transition.

On PC the underlying music-position function is a stub that returns 0, so the opcode writes 0 into temporary variable 0 (`SCRIPT_UNKNOWN10` at 0x51FC40 calling a return-0 stub). This is why MUSICSKIP-based music continuation does not work on PC.
