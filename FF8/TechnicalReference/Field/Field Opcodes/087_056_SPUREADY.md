---
layout: default
parent: Field Opcodes
title: 056_SPUREADY
nav_order: 87
permalink: /technical-reference/field/field-opcodes/056-spuready/
---

-   Opcode: **0x056**
-   Short name: **SPUREADY**
-   Long name: SPU Start

#### Argument

none

#### Stack

  
*0*

**SPUREADY**

#### Description

Pops one value (a sound-effect index) and kicks off an asynchronous load/prepare of that sound resource, resetting the async progress trackers to 0. Execution yields (returns 3) so the load runs in the background; [SPUSYNC](../164-spusync/) later waits for it to finish. On the original PSX this streamed the sound from disc (hence the drive noise).

PC handler: `SCRIPT_SPUREADY` at 0x51F520.
