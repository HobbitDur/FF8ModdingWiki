---
layout: default
parent: Battle
title: Preemptive Attack
author: HobbitDur
permalink: /technical-reference/battle/preemptive-attack/
---

When starting a fight, there is some computation done to decide if you are lucky (or unlucky) for a strike first or a back attack.

A RNG value is computed

$$
\text{preemptive-rng} = [0..255] + 20 \times \text{MonsterFlagIncrease} - 20 \times \text{MonsterFlagDecrease} + 20 \times \text{AbilityAlert}
$$

With [MonsterFlagIncrease]({{site.baseurl}}/FF8/TechnicalReference/Battle/FileFormat_DAT#section-7-informations--stats), MonsterFlagDecrease being bool (so 1 or 0). If one monster has the flag on his dat file, then the flag is applied (only once so)
With AbilityAlert being a bool (0 or 1) set to 1 if the ability *Alert* is equiped.

