---
layout: default
parent: Field Opcodes
title: 10D_WORLDMAPJUMP
nav_order: 270
permalink: /technical-reference/field/field-opcodes/10d-worldmapjump/
---

-   Opcode: **0x10D**
-   Short name: **WORLDMAPJUMP**
-   Long name: Jump to world map

#### Argument

none

#### Stack

  
*Location*

*Vehicle flags?*

*?*

**WORLDMAPJUMP**

#### Description

Jumps the player to the world map. The game has a preset list of locations to jump to - there is no way AFAIK to jump to a specific XY point. The handler requests the world-map module by setting `globalFieldNextModuleID = 7`, pops three values (the destination *Location* into `MenuState_opcode_menu_id`, plus two transition parameters written to `wm2field_FieldZ` and `wm2field_FieldTarget`), and adjusts the savemap "can save here" bit. It yields (return 1) until the module switch happens.

PC handler: `SCRIPT_WORLDMAPJUMP` at 0x521820.
