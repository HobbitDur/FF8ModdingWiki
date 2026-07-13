---
layout: default
parent: Field Opcodes
title: 02B_SETMODEL
nav_order: 44
permalink: /technical-reference/field/field-opcodes/02b-setmodel/
---

-   Opcode: **0x02B**
-   Short name: **SETMODEL**
-   Long name: Set model

#### Argument

Model ID to load.

#### Stack

none

#### Description

Set this entity's display model. The inline 16-bit argument is written to `model_id` (entity+536); the model itself is loaded/bound later by the field setup. Returns 2 (done + continue).

PC handler: `SCRIPT_SETMODEL` at 0x51D8F0.
