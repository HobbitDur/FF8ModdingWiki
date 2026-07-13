---
layout: default
parent: Battle
title: Escape
author: HobbitDur
permalink: /technical-reference/battle/escape/
---

When trying to run (R2 + L2), around every second (to be confirmed the exact time), there is a random computation if the escape happen.  
The chance to escape is $$\frac{X}{255}$$, with $$X$$ depending on the following factors:  

Scripted battles can also set `ENCOUTER_BATTLE_FLAG` bit 0 (`0x01`) during the field [BATTLE](../../field/field-opcodes/069-battle/) opcode, which sets the cannot-run state during battle init. Scene.out encounter data also has a Disable Escape battle flag; see [Encounters data (scene.out)](../battle-structure-sceneout/).

if StructFirst or BackAttacked, $$X = 16$$  
if ChanceForFirstStrike or BackAttack, $$X = 255$$  
if all monster are disabled (Death or Petrify or Berserk or Sleep or Confusion), $$X = 255$$  
if one monster has flag [DecreaseChanceEscape]({{site.baseurl}}/technical-reference/battle/model-sections/information-stats/#decrease-chance-escape),  $$X = 16$$  
If at least one monster is alive AND has the flag [IncreaseChanceEscape]({{site.baseurl}}/technical-reference/battle/model-sections/information-stats/#increase-chance-escape), $$X = 128$$  

In other cases: $$X = 64$$