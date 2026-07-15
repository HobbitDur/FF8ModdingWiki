---
layout: default
parent: Field Opcodes
title: 133_SETPLACE
nav_order: 308
permalink: /technical-reference/field/field-opcodes/133-setplace/
---

-   Opcode: **0x0133**
-   Short name: **SETPLACE**
-   Long name: Set Area Display Name

#### Argument

none

#### Stack

  
*A number*

**SETPLACE**

#### Description

This controls what shows up at the bottom of the menu and in your saved game slots.

The handler pops one **word** off the stack and stores it into `SG_PREVIEW_LOCATION_ID` — the location-name index shown on the main menu and in save-slot previews.

PC handler: `SCRIPT_SETPLACE`.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_SETPLACE` | 0x523200 | Field script opcode handler (verified IDA function) |
