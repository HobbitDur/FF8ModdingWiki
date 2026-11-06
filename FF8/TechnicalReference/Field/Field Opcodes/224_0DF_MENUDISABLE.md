---
layout: default
parent: Field Opcodes
title: 0DF_MENUDISABLE
nav_order: 224
permalink: /technical-reference/field/field-opcodes/0df-menudisable/
---

-   Opcode: **0x0DF**
-   Short name: **MENUDISABLE**
-   Long name: Disable the menu

#### Argument

none

#### Stack

none

**MENUDISABLE**

#### Description

Stops the player opening the menu: sets `MENU_DISABLED`. Undone by [MENUENABLE](../0de-menuenable/), and field entry clears it. The Raijin dog chase in occupied Balamb uses it.

PC handler: `SCRIPT_MENUDISABLE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MENUDISABLE` | 0x521CF0 | Field script opcode handler (verified IDA function) |
