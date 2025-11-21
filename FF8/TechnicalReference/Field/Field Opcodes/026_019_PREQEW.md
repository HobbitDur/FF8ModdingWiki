---
layout: default
parent: Field Opcodes
title: 019_PREQEW
nav_order: 26
permalink: /technical-reference/field/field-opcodes/019-preqew/
---

-   Opcode: **0x019**
-   Short name: **PREQEW**
-   Long name: Request party entity execution (synchronous, guaranteed)

#### Argument

The ID of the current party member Entity (0, 1 or 2).

#### Stack

..., *Priority*, *Label* =&gt; ...

#### Description

Go to the method *Label* in the entity associated with the character **Argument** in the current party with a specified *Priority*.
