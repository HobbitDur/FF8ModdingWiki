---
layout: default
parent: Field Opcodes
title: 11B_MENUPHS
nav_order: 284
permalink: /technical-reference/field/field-opcodes/11b-menuphs/
---

-   Opcode: **0x11B**
-   Short name: **MENUPHS**
-   Long name: Open PHS menu

#### Argument

none

#### Stack

none

#### Description

Opens the PHS (switch) menu. Requests the menu module (`globalFieldNextModuleID = 5`) with menu id 1 (PHS) and marks the menu state as save-enabled (value 2). Takes no stack arguments. Returns 3 (yield).

PC handler: `SCRIPT_MENUPHS` at 0x521D40.
