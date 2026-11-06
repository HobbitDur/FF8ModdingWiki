---
layout: default
parent: Field Opcodes
title: 0DE_MENUENABLE
nav_order: 223
permalink: /technical-reference/field/field-opcodes/0de-menuenable/
---

-   Opcode: **0x0DE**
-   Short name: **MENUENABLE**
-   Long name: Enable the menu

#### Argument

none

#### Stack

none

**MENUENABLE**

#### Description

Lets the player open the menu again: clears `MENU_DISABLED`. Undoes [MENUDISABLE](../0df-menudisable/).

PC handler: `SCRIPT_MENUENABLE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MENUENABLE` | 0x521D00 | Field script opcode handler (verified IDA function) |
