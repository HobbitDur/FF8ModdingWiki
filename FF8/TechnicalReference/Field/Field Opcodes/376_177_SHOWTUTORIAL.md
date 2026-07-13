---
layout: default
parent: Field Opcodes
title: 177_SHOWTUTORIAL
nav_order: 376
permalink: /technical-reference/field/field-opcodes/177-showtutorial/
---

-   Opcode: **0x177**
-   Short name: **SHOWTUTORIAL**
-   Long name: Show tutorial

#### Argument

none

#### Stack

  
*Tutorial ID*

**SHOWTUTORIAL**

#### Description

Shows a tutorial. The handler pops one value (the tutorial ID) into `LINKED_TO_MENU_CAN_SAVE_HERE`, requests a switch to the menu module (`globalFieldNextModuleID = 5`) with menu id 29 (the tutorial viewer), and returns 3 (done + yield) so the field hands off to the menu.

PC handler: `SCRIPT_SHOWTUTORIAL` at 0x522030. This is the **last opcode of the PC table** (376 entries, 0x000-0x177).
