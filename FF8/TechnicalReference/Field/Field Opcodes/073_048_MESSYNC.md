---
layout: default
parent: Field Opcodes
title: 048_MESSYNC
nav_order: 73
permalink: /technical-reference/field/field-opcodes/048-messync/
---

-   Opcode: **0x048**
-   Short name: **MESSYNC**
-   Long name: Message Window Sync

#### Argument

none

#### Stack

  
*Message Channel*

**MESSYNC**

#### Description

Waits for a non-blocking message window to finish. A window opened by [MES](../047-mes/) or [AMES](../065-ames/) stays up while the script continues; MESSYNC pauses the script until that window's channel is closed/dismissed. It pops one value, the message channel number, and each frame checks the channel's window state: it returns 1 (wait) while the message is still active and 2 (done + continue) once the channel has been cleared.

PC handler: `SCRIPT_MESSYNC` at 0x529900.
