---
layout: default
parent: Field Opcodes
title: 077_SCROLLSYNC
nav_order: 120
permalink: /technical-reference/field/field-opcodes/077-scrollsync/
---

-   Opcode: **0x077**
-   Short name: **SCROLLSYNC**
-   Long name: Scroll Sync

#### Argument

none

#### Stack

  
**SCROLLSYNC**

#### Description

Pauses script execution until the last timed scroll command finishes. The handler reads the shared scroll phase byte (`FIELD_SCROLL_STATE`): it returns 2 (done, advance) once the phase reaches 2, otherwise returns 1 (wait, retry next frame). Takes no arguments and pops nothing.

PC handler: `SCRIPT_SCROLLSYNC` at 0x520F50.
