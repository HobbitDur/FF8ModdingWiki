---
layout: default
parent: Field Opcodes
title: 058_TALKOFF
nav_order: 89
permalink: /technical-reference/field/field-opcodes/058-talkoff/
---

-   Opcode: **0x058**
-   Short name: **TALKOFF**
-   Long name: Talk script off

#### Argument

none

#### Stack

none

#### Description

Disables talking to this entity by setting its talk-disabled flag (+587 = 1). No stack use.

PC handler: `SCRIPT_TALKOFF` at 0x51EBD0.
