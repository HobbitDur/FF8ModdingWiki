---
layout: default
parent: Field Opcodes
title: 0AD_GAMEOVER
nav_order: 174
permalink: /technical-reference/field/field-opcodes/0ad-gameover/
---

-   Opcode: **0x0AD**
-   Short name: **GAMEOVER**
-   Long name: Game Over

#### Argument

none

#### Stack

  
*1* (seems optional)

**GAMEOVER**

#### Description

Ends the game in failure. The handler sets the engine's next module to the game-over screen (`globalFieldNextModuleID = GLOBAL_STATE_SCREEN_SQUARESOFT`) and returns 1. It does **not** read or pop the stack, so any value pushed before it (the historical "1") is ignored and simply left on the stack.

PC handler: `SCRIPT_GAMEOVER` at 0x523370.
