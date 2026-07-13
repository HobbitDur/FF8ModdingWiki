---
layout: default
parent: Field Opcodes
title: 129_MENUNAME
nav_order: 298
permalink: /technical-reference/field/field-opcodes/129-menuname/
---

-   Opcode: **0x0129**
-   Short name: **MENUNAME**
-   Long name: Name Character/GF

#### Argument

none

#### Stack

  
*Name ID*

**MENUNAME**

#### Description

Name a character or GF. If it's a GF, this also marks that GF as obtained in the save. The handler pops the *Name ID*, requests the menu module (`globalFieldNextModuleID = 5`), selects the matching naming sub-menu (menu ids 2-28 depending on the ID), and for GF entries calls the "GF obtained" setter so the GF is unlocked. Returns 3 (yield).

| Number | Character  |
|--------|------------|
| 0      | Squall     |
| 1      | Rinoa      |
| 2      | Angelo     |
| 3      | Quetzacotl |
| 4      | Shiva      |
| 5      | Ifrit      |
| 6      | Siren      |
| 7      | Brothers   |
| 8      | Carbuncle  |
| 9      | Diablos    |
| 10     | Leviathan  |
| 11     | Pandemona  |
| 12     | Cerberus   |
| 13     | Alexander  |
| 14     | Bahamut    |
| 15     | Doomtrain  |
| 16     | Cactuar    |
| 17     | Tonberry   |
| 18     | Eden       |
| 19     | Boko       |
| 20+    | Griever    |

PC handler: `SCRIPT_MENUNAME` at 0x521DA0.
