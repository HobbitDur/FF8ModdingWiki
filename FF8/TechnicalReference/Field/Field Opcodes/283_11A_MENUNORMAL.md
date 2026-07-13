---
layout: default
parent: Field Opcodes
title: 11A_MENUNORMAL
nav_order: 283
permalink: /technical-reference/field/field-opcodes/11a-menunormal/
---

-   Opcode: **0x11A**
-   Short name: **MENUNORMAL**
-   Long name: Open menu

#### Argument

none

#### Stack

none

#### Description

Opens the main menu. Requests the menu module (`globalFieldNextModuleID = 5`) with menu id 0 (normal menu) and copies the field's "can save here" flag into the menu state. Takes no stack arguments. Returns 3 (yield).

PC handler: `SCRIPT_MENUNORMAL` at 0x521D10.
