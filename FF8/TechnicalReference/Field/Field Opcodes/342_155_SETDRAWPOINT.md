---
layout: default
parent: Field Opcodes
title: 155_SETDRAWPOINT
nav_order: 342
permalink: /technical-reference/field/field-opcodes/155-setdrawpoint/
---

-   Opcode: **0x155**
-   Short name: **SETDRAWPOINT**
-   Long name: Set Draw Point hidden

#### Argument

isHidden

#### Stack

  
Bool (PSHN\_L)

**SETDRAWPOINT**

#### Description

If isHidden is bigger or equal to 1, then hides the draw point. If not, the draw point is visible.

The handler pops one value into the field var-map (`hidden` flag), registers this entity's position (from entity+400/404/408) as a draw-point location via `sub_474750`, and calls `Script_SetDrawPoint` to spawn/refresh the draw-point marker with that hidden state.

-- By MaKiPL

PC handler: `SCRIPT_SETDRAWPOINT` at 0x523030.
