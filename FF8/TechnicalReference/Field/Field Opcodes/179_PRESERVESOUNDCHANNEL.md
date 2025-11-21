---
layout: default
parent: Field Opcodes
title: 179_UNKNOWN14
permalink: /technical-reference/field/field-opcodes/179-unknown14/
---

-   Opcode: **0x179**
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
