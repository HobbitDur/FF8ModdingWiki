---
layout: default
parent: Field Opcodes
title: 125_ADDITEM
nav_order: 294
permalink: /technical-reference/field/field-opcodes/125-additem/
---

-   Opcode: **0x125**
-   Short name: **ADDITEM**
-   Long name: Add item to party

#### Argument

none

#### Stack

  
*Quantity*

*Item ID*

**ADDITEM**

#### Description

Does exactly what you think. See [Item Codes](../../Lists/Item_list) for a list of item codes. The handler pops the item ID and quantity and calls the inventory add routine (`AddItemToInventory`).

PC handler: `SCRIPT_ADDITEM` at 0x522380.
