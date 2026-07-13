---
layout: default
parent: Field Opcodes
title: 173_PRESERVESOUNDCHANNEL
nav_order: 372
permalink: /technical-reference/field/field-opcodes/173-preservesoundchannel/
---

-   Opcode: **0x173**
-   Short name: **PRESERVESOUNDCHANNEL**
-   Long name: Preserve Sound Channel

#### Argument

none

#### Stack

  
*Sound channel*

**PRESERVESOUNDCHANNEL**

#### Description

Prevents the given sound channel from being silenced when a new field is loaded. The currently playing sound effect will continue to play during the fade.

Does not work on channel 0.

PC handler: `SCRIPT_PRESERVESOUNDCHANNEL` at 0x520230.
