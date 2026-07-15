---
layout: default
parent: Field Opcodes
title: 12E_MENUSAVE
nav_order: 303
permalink: /technical-reference/field/field-opcodes/12e-menusave/
---

-   Opcode: **0x12E**
-   Short name: **MENUSAVE**
-   Long name: Open save menu

#### Argument

none

#### Stack

none

#### Description

Opens the save menu. Requests the menu module (`globalFieldNextModuleID = 5`) with menu id 24 (save) and marks the menu state as save-enabled (value 1). Takes no stack arguments. Returns 3 (yield).

PC handler: `SCRIPT_MENUSAVE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MENUSAVE` | 0x522190 | Field script opcode handler (verified IDA function) |
