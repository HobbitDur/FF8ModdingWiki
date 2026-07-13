---
layout: default
parent: Field Opcodes
title: 067_THROUGHON
nav_order: 104
permalink: /technical-reference/field/field-opcodes/067-throughon/
---

-   Opcode: **0x067**
-   Short name: **THROUGHON**
-   Long name: Through mode on

#### Argument

none

#### Stack

none

#### Description

Disables collision with this entity by setting its through flag (+588 = 1), so the player can walk through it. No stack use.

PC handler: `SCRIPT_THROUGHON` at 0x51ED40.
