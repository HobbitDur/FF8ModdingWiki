---
layout: default
parent: Field Opcodes
title: 0CA_SEPOSTRANS
nav_order: 203
permalink: /technical-reference/field/field-opcodes/0ca-sepostrans/
---

-   Opcode: **0x0CA**
-   Short name: **SEPOSTRANS**
-   Long name: Sound Effect Pan Transition

#### Argument

none

#### Stack

  
*Sound channel*

*Frame count*

*Final pan (0-255)*

**SEPOSTRANS**

#### Description

Transitions the pan of the sound in *sound channel* over *frame count*. 0=left, 255=right.
