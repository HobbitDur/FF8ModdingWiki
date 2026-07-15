---
layout: default
parent: Battle
title: Surprise Attack
author: HobbitDur
permalink: /technical-reference/battle/surprise-attack/
---

When starting a fight, there is some computation done to decide if you are lucky (or unlucky) for a strike first or a back attack.

PC runtime function: `computeBattleSurpriseAttack` (renamed from `Battle_InitPreemptiveBackAttackStatus`). Scripted battles can force or suppress the result with `ENCOUTER_BATTLE_FLAG`; see [Battle Runtime](../battle-runtime/) and [Encounter Trigger Runtime](../encounter-trigger-runtime/).

A RNG value is computed

$$
\text{SurpriseRng} = [0..255] + 20 \times \text{MonsterFlagIncrease} - 20 \times \text{MonsterFlagDecrease} + 20 \times \text{AbilityAlert}
$$

With [MonsterFlagIncrease]({{site.baseurl}}/technical-reference/battle/model-sections/information-stats/#increase-surprise-rng), [MonsterFlagDecrease]({{site.baseurl}}/technical-reference/battle/model-sections/information-stats/#increase-surprise-rng) being bool (so 1 or 0). If one
monster has the flag on his dat file, then the flag is applied (only once so)
With AbilityAlert being a bool (0 or 1) set to 1 if the ability [Alert]({{site.baseurl}}/technical-reference/list/ability-list/#passif-abilities) is equipped.

For this RNG, 3 possible values are computed:

- SurprisePositiveForPlayer: if SurpriseRng < 20
- SurpriseNegativeForPlayer: if SurpriseRng >= 236
- NoSurprise: if 236 > SurpriseRng > 19

Those value defines for whom the surprise attack is.

From this, some special cases change the result:

if SurpriseNegativeForPlayer and AbilityAlert, then it's converted to NoSurprise
if [MonsterFlagImmuneSurpriseAttack]({{site.baseurl}}/technical-reference/battle/model-sections/information-stats/#surprise-attack-immunity) and SurprisePositiveForPlayer, then it's
converted to NoSurprise

Now we know if a side has an advantage starting the fight. From this it is decided with $$\frac{1}{2}$$ chance if it's simply an ATB fill (strike first) or also a back attack.

All 4 values are resume here:

| Formation                | Ally ATB | Enemy ATB | Additional Effects                                                                                                                        |
|--------------------------|----------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------|
| Back attacked!           | Empty    | Full      | Allies face the opposite direction and take double damage from the first physical attack against them. Fleeing with R2+L2 becomes harder. |
| Struck first!            | Empty    | Full      | Fleeing with R2+L2 becomes harder.                                                                                                        |
| Chance for first strike! | Full     | Empty     |                                                                                                                                           |
| Back attack!             | Full     | Empty     | Enemies face the opposite direction and take double damage from the first physical attack against them.                                   |

## Function addresses

| Function | Address | Description |
|---|---|---|
| `computeBattleSurpriseAttack` (formerly documented as `Battle_InitPreemptiveBackAttackStatus`) | 0x48AFD0 | Computes the surprise/back-attack RNG result (verified IDA function) |