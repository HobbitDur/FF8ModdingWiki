---
layout: default
parent: Field Opcodes
title: 175_SETDRAWPOINTID
nav_order: 374
permalink: /technical-reference/field/field-opcodes/175-setdrawpointid/
---

-   Opcode: **0x175**
-   Short name: **SETDRAWPOINTID**
-   Long name: Set Draw Point ID

#### Argument

none

#### Stack

  
*Draw point ID*

**SETDRAWPOINTID**

#### Description

Assigns this draw point an ID. Draw points with identical IDs share Full/Drained status.

The handler pops one value and stores `id - 1` into the field var-map (`unk3`), so the pushed ID is 1-based while the stored index is 0-based.

PC handler: `SCRIPT_SETDRAWPOINTID` at 0x5230A0.
