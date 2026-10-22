---
layout: default
title: Formula
parent: List
permalink: /technical-reference/list/formula/
---

Here you'll find all formula as found in the game

# Magic

## Classic

$$
\text{Damage} =\left (\text{AttackerMag} + \text{Power} \right) 
\times \frac{265 - \text{TargetSpr}}{4} \times \frac{\text{Power}}{256} 
\times \frac{[0..32] + 240}{256}
$$

{: .note }
>`ComputeMagicAndGFDamage` reads TargetSpr from the same `BATTLE_SLOT_DATA[]` slot array for players and monsters: the SPR term is one shared code path. The only monster-related asymmetry found is on the attacker side: if the caster is a monster, magic damage dealt is halved after this formula.

## Demi, Percent

$$
\text{Damage} = \frac{\text{AttackPower} \times \text{TargetCurrentHP}}{16}
$$

{: .note }
>Demi power = 4  
>Percent = 15

# GF

## Classic damage:

`ComputeMagicAndGFDamage` (GF-damage case). `Power` = the `gfPower` byte (offset 0x07);
`LevelMod`/`PowerMod` = the `levelMod`/`powerMod` tail bytes (offsets 0x83/0x82).

$$
\text{Damage} = 
\left
(\text{LevelMod} \times 
\frac{\text{Level}}{10} + \text{Power} + \text{PowerMod} \right) \times \frac{265 - 
\text{TargetSpr}}{8} \times \frac{\text{Power}}{256} \times \frac{\text{Boost}}{100} 
\times \frac{100 + \text{SummonMagBonus}}{100} \times \frac{[0..32] + 240}{256}
$$

### Modifiers
#### Monsters

If monster: 
Damage = Damage / 2

#### Elem
If elem:
Damage = Damage * (900 - ElemDef) / 100

#### Protective magic:
If Shell:
Damage = Damage / 2

## Diablos

$$
\text{Damage} = \frac{\text{TargetMaxHP} \times \text{Level}}{\text{PowerMod} - \text{LevelMod} + 100}
$$

{: .note }
>Diablos PowerMod = 0  
>Diablos LevelMod = 0


## Cactuar

$$
\text{Damage} = 1000 \times \left(\frac{\text{AttackPower} \times \text{GFLevel}}{1000} + 1\right)
$$

{: .note }
>Cactuar AttackPower = 90

## Moomba

$$
\text{Damage} = \text{TargetCurrentHP} - 1
$$

## Angelo recover

$$
\text{DamageHeal} = \frac{\text{Power} \times \text{TargetMaxHP}}{16}
$$

# Item

## Curative item

$$
\text{DamageHeal} = 50 \times \text{Powers}
$$

# Magic
## Curative magic

$$
\text{DamageHeal} = \text{Power} \times  \frac{\text{Power} + \text{AttackerMagic} }{2} \times \frac{[0..32] + 240}{256} 
$$

### Protective magic:
If Shell:
DamageHeal = Damage / 2

## Blue magic
### White wind


$$
\text{DamageHeal} = \text{QuistisMaxHP} - \text{QuistisCurrentHP}
$$ 

# Physical

## Classic {#physical-classic}

Base physical damage, straight from the engine (`ComputeWithDamageSTRFormula` and the
hit+crit-rolling `computeAttackPhysical` — identical arithmetic):

$$
\text{Damage} = \left\lfloor
\frac{\text{AttackPower} \times (265 - \text{VIT}) \times \left(\text{STR} + \left\lfloor \frac{\text{STR}^2}{16} \right\rfloor\right)}{256 \times 16}
\right\rfloor \times \frac{[0..32] + 240}{256}
$$

where `AttackPower` = weapon attack power, `STR` = attacker STR (with the weapon's STR bonus added),
`VIT` = target VIT (0 under Vit0/Meltdown or the ignore-VIT sub-formula). All divisions truncate.

{: .warning }
>The STR term is **`STR + STR²/16`**, not the widely-circulated `STR²/(16+STR)` — the two differ
>by an order of magnitude (for STR 128: 1152 vs 114). This page previously used the wrong term and
>a spurious `(CritDamage+40)/20` factor; neither is in the exe.

Then `HpModifierComputationForPhysical` applies, in order: **Protect** ÷2, **Back Attack**
×2, **Critical** ×2, **Zombie target** ÷2, and the elemental term
`dmg += dmg × elemAttack% × (800 − elemDef)/10000`. (VIT is read from the same `BATTLE_SLOT_DATA[]`
slot array for players and monsters — one shared code path.)

## Compute crit {#compute-crit}

Rolled in `Damage_RollCrit`: **crit if a random byte `0..255` ≤ `CritBonus + LUCK`** (the
`255×x/255` in the code is a no-op), so

$$
P(\text{crit}) = \frac{\text{CritBonus} + \text{LUCK}}{256}
$$

`CritBonus` is the weapon's crit bonus (or the enemy attack's / Shot's crit increase), staged in
`RELATED_TO_CRIT_BONUS`. A crit doubles the physical damage above.

`LUCK` is read from the attacker's battle slot (`charaStat[5]`). **When the attacker is a monster it
is always 0** — `setMonsterInfoFromDatInfoSection` zeroes that byte at load and nothing writes it
again (monster stat data has no LUCK curve), so an
[enemy attack]({{site.baseurl}}/technical-reference/main/kernel/enemy-attacks/)'s crit chance is
exactly `CritBonus/256`. The same applies to the `LUCK/2` term of the hit% below.

## Hit % {#hit-rate}

Physical accuracy, from `computeAttackPhysical`:

$$
\text{hit\%} = \text{HitRate} + \left\lfloor\frac{\text{LUCK}}{2}\right\rfloor - \text{EVA}_{tgt} - \text{LUCK}_{tgt}
\qquad(\text{clamped} \ge 0)
$$

The attack lands if `255 × hit% / 100 ≥ rand(0..255)`. **`HitRate = 255` always hits** (the roll is
skipped); **Darkness** quarters `HitRate` first; **Sleep/Stop** targets are always hit.

## Status inflict chance {#status-accuracy}

Every "Status attack accuracy" byte across the kernel (Magic, GF, Enemy attacks, Renzokuken,
Battle items, Non-J GF, Command abilities, Blue Magic, Shot, Duel, Rinoa, ...) is the SAME kernel
field — but which formula actually reads it (if any) depends entirely on the ability's own
[Attack Type]({{site.baseurl}}/technical-reference/list/kernel#attack-type) byte, which selects a
damage-compute function in `Battle_DamageGettingRelated`. Each function below was
individually decompiled — nothing here is inferred from the byte's *name* alone:

| Attack Types | Function | Behaviour |
|---|---|---|
| Physical Attack, % Physical Damage, Renzokuken Finisher, Squall Gunblade Attack, Kamikaze, Everyone's Grudge, Physical Attack (Ignore Target VIT) | `Battle_ApplyStatusWithResistRoll` via the STR/VIT physical core | `chance = accuracy + STR/4 − VIT/4 − resistance`, rolled |
| Magic Attack, % Magic Damage, GF, GF (Ignore Target SPR), % GF Damage, Magic Attack (Ignore Target SPR), LV? Attack, Magic damage from step count (`0x21`) | same roll, via `Damage_ComputeMagicAndGF`'s MAG/SPR path | `chance = accuracy + MAG/4 − SPR/4 − resistance`, rolled |
| Curative Item, White Wind, Give Percentage HP (Angelo Recover) | `Damage_ComputeCurativeItemSpecial` | `cures if accuracy > rand(1..100)` — flat %, no stat terms. **Cures** the listed statuses, doesn't inflict them |
| Curative Magic, Curative Magic % of target's Max HP (`0x15`) | `Damage_ComputeCurativeMagic` | `checkDoubleStatusApply` runs **unconditionally** — `HIT_ATTACK_ACCURACY` is never read. **Byte is dead** |
| Revive, Revive At Full HP | `GetReviveHP` | Clears Death unconditionally if present and not sealed — accuracy never read. **Byte is dead**, except reviving a Zombie-status target instead deals unmissable magic damage via the Magic-dispatch path |
| LV Down, LV Up | `computeLvlUpDown` | `succeeds if accuracy > rand(0..255)` — gates the WHOLE level-change action (not a status roll at all); also fails outright if the target is level-change-immune |
| Fixed Damage, Target Current HP - 1, Fixed Magic Damage Based on GF Level, 1 HP Damage | `Damage_ComputeFixedSpecial` | No reference to `HIT_ATTACK_ACCURACY` anywhere in the function. **Byte is dead** |
| Card | `Battle_RollCardCommand` | Capture depends on the **target's HP ratio**, not this byte: `chance = (256 − 255×curHP/maxHP)/256` (~0.4% at full HP → 100% near 0 HP); a second `rand < 16` (6.25%) gives the rare card. **Byte is dead** |
| Devour | Devour dispatcher case | Uses the [Devour HP-ratio roll](#devour-success), including integer rounding and a nonzero-threshold check. The effect comes from the Devour kernel section. **Byte is dead** |
| Scan, Angelo Search, Moogle Dance | Scan / Angelo Search / Moogle Dance dispatcher cases | Utility actions (reveal info / find item / GF HP recovery) — no roll, accuracy never read. **Byte is dead** |
| None, `0x1E`, `0x1F` | dispatcher `LABEL_46` / no-op default | No damage or status roll at all. **Byte is dead** |
| Summon item (`0x0E`) | rerouted before damage by `computeCommandAction` | The item's own bytes are never consulted — the action becomes the Non-junctionable GF attack named by its Special action ID, and that entry's accuracy applies instead. **Byte is dead** |

```
Battle_ApplyStatusWithResistRoll roll (the two confirmed-rolled rows above):
chance = accuracy + atkStat/4 − tgtStat/4 − targetResistance
accuracy = 255      -> guaranteed (stat/resistance check skipped entirely)
chance ≤ 0          -> fails (0%)
accuracy 250..254   -> guaranteed, as long as chance > 0
otherwise           -> roll floor(chance × 255 / 100) against rand(0..255)
(fails outright if the target already has the status, or per-status resistance ≥100)
```

{: .note }
>All 37 defined Attack Types (0–36) are accounted for above — every one was read out of the
>dispatcher `Battle_DamageGettingRelated`. Only two groups actually consume the
>status-accuracy byte (the STR/VIT and MAG/SPR rows); for the rest it is genuinely dead, or the
>Attack Type has its own success mechanic (Card HP-ratio, Devour HP-ratio, LV Up/Down action gate).

# Devour {#devour}

Read from the English PC `FF8_EN.exe` (2013 release; image base `0x400000`,
MD5 `be8b278becf6757bb811acd45d717d9c`). Devour has two separate calculations:
the chance to consume the monster, then the selected kernel effect on the devourer.

## Effect selection and immunity

`computeDevour` (`0x48fc60`) selects an effect ID from the monster's
[information section]({{site.baseurl}}/technical-reference/battle/model-sections/information-stats/):
byte **251** for its low level tier, **252** for medium, or **253** for high. The tier
boundaries are the monster's own medium/high level-start bytes **244/245**; they are
not a universal level requirement. Effect ID **255** means immune and rejects Devour
before the HP roll. Other IDs select a record in the
[Devour kernel section]({{site.baseurl}}/technical-reference/main/kernel/devour/).

## Success chance {#devour-success}

Let `A` be the devourer's **current HP**, `T` the monster's **current HP**, and
`R = GetRandomInt()` a random byte in `0..255`. For a living devourer (`A > 0`),
the Devour dispatcher case (`0x4926bc`, HP reads at `0x4926cf`) does:

```text
if A < T: fail
q = floor(255 * (A - T) / A)
succeed if q != 0 and R <= q
```

The helper `isRandomNumeratorDenominator` (`0x48f0c0`) computes
`floor(255 * q / 255)`, which leaves `q` unchanged, and explicitly rejects zero.
Thus, counting the successful byte values out of 256:

$$
q = \left\lfloor \frac{255 \times (A-T)}{A} \right\rfloor
\qquad (A \ge T)
$$

$$
P(\text{Devour}) =
\begin{cases}
0 & \text{if immune, } A<T \text{, or } q=0 \\
\frac{q+1}{256} & \text{otherwise}
\end{cases}
$$

The familiar `100 * (A - T) / A` percentage is an approximation. Both HP values
are **current**, so healing the devourer also improves the chance; the monster's
maximum HP is not used in this roll. Equal current HP always fails, and a positive
HP difference can still fail automatically when rounding gives `q = 0`.

| Devourer current HP (`A`) | Monster current HP (`T`) | `q` | Exact success chance |
|---|---|---|---|
| 8000 | 9000 | Not rolled | 0% |
| 8000 | 8000 | 0 | 0% |
| 8000 | 7999 | 0 | 0% |
| 8000 | 4000 | 127 | 128/256 = 50% |
| 8000 | 2000 | 191 | 192/256 = 75% |
| 8000 | 1 | 254 | 255/256 = 99.609375% |

On success the monster receives **Eject**, the result suppresses the damage
number, and the selected Devour message is shown. The dispatcher returns the
monster's **category byte 255** as its internal hit amount; this is separate from
the effect ID and from the HP effect below. On a failed HP roll it instead returns
**8**, sets the **Miss** flag, and clears `DEVOUR_SUCEED`; no Devour benefit is applied.
See [Devour category]({{site.baseurl}}/technical-reference/battle/model-sections/information-stats/#byte-255-devour-category).

## HP and status effect on the devourer {#devour-hp-effect}

The follow-up effect in `Battle_applyDamage` (HP calculation at `0x490479`)
reads the selected kernel record. Let `H` be its **HP heal/damage quantity** byte
at offset `0x03`, and `M` the devourer's **battle maximum HP**:

$$
\text{HPAmount} = \left\lfloor \frac{H \times M}{16} \right\rfloor
$$

`H` is a linear quantity in sixteenths of maximum HP: **4 = 25%**, **8 = 50%**,
**12 = 75%**, and **16 = 100%**. There is no damage-variance roll or MAG/SPR term
in this HP calculation. It uses the devourer's maximum HP, not either participant's
current HP or the monster's maximum HP.

| Kernel offset `0x02` | HP effect | Status effect |
|---|---|---|
| `0x1E` (Cure) | Restore `HPAmount` | Cure the record's status masks via `Battle_CureStatusesAndSetFeedback`; then apply its permanent stat bonuses |
| `0x1F` (Damage) | Deal `HPAmount` | Pass the record's status masks through the normal MAG/SPR status-infliction routine (`sub_4914E0`); this follow-up stages status accuracy **200** |

These are the calculated HP amounts before the common HP application and caps.
The record's status masks are at offsets **0x04** (Status 2) and **0x08** (Status 1).
The command ability's status-accuracy byte does not control the consumption roll.

## Permanent stat bonuses {#devour-stat-bonuses}

For a Cure (`0x1E`) record, `relatedToDevour` (`0x492220`) tests each bit in the
**Raised Stat Flag** byte at kernel offset **0x0A** independently:

| Bit | Saved stat increased |
|---|---|
| `0x01` | STR |
| `0x02` | VIT |
| `0x04` | MAG |
| `0x08` | SPR |
| `0x10` | SPD |
| `0x20` | LUCK |

For each selected stat, `increaseCharaStatBy1` (`0x495f90`) writes:

$$
\text{SavedStat}' = \min(255,\ \text{SavedStat}+1)
$$

Multiple bits can raise multiple stats in one effect. The separate **Raised Stat HP
Quantity** byte at offset **0x0B**, `B`, is added directly to the character's saved
base maximum HP by `sub_495F50` (`0x495f50`):

$$
\text{SavedBaseMaxHP}' = \min(9999,\ \text{SavedBaseMaxHP}+B)
$$

Thus a Max HP +10 effect stores **10** in `B`; it is not multiplied by 10 or
divided by 16. This permanent HP bonus is separate from `H`, the immediate HP
heal/damage quantity. The selected effect record determines the bonus; the
monster's category byte does not. See the [Devour effect IDs]({{site.baseurl}}/technical-reference/list/devour-list/#devour-effects).

# Stat

## Character stat
Each character stat is defined by 4 coefficients (noted `stat_0`..`stat_3`, i.e. the four
bytes stored per stat in the [Characters kernel section]({{site.baseurl}}/technical-reference/main/kernel/characters/#stat-curves)).
There are three distinct curve shapes — HP, the STR family, and the SPD/LCK pair — all read
below from the engine (`Stat_ComputeCharaMaxHP` for HP, `Stat_ComputeCharaStat`
for the rest; the final sum is clamped by `CapTo255`).

{: .warning }
>The [doomtrain](https://github.com/DarkShinryu/doomtrain) editor charts SPD and LCK with the
>STR-family formula, which is **incorrect** — those two use the simpler linear shape below
>(no quadratic term, no `/4`). Its HP and STR/VIT/MAG/SPR charts are correct.

### LCK & SPD

magicJunctionnedValue is the junction value defined in kernel.bin for the stat.

$$
\text{charaStat} = \text{CapTo255}\left( 
\text{charaBasedStat} 
+ \text{charaLvl} \times \text{stat}_0 
+ \frac{\text{charaLvl}}{\text{stat}_1}
+ \text{stat}_2 
- \frac{\text{charaLvl}}{\text{stat}_3}
+ \frac{\text{magicJunctionnedValue} \times \text{magicAmount}}{100} 
\right)
$$


### STR & VIT & MAG & SPR

strBonus is 0 if we don't compute STR

$$
\text{statResult} = \frac{\text{charaLvl}^2}{\text{stat}_3}
$$

$$
\text{statResult} = \text{CapTo255}\left( 
\text{charaBasedStat} 
+ \text{strBonus} 
+ \frac{\text{stat}_2 
+ \frac{\text{charaLvl} \times \text{stat}_0}{10} 
+ \frac{\text{charaLvl}}{\text{stat}_1} - \left( \frac{\text{getLow32bit}(\text{statResult})
- \text{getHigh32bit}(\text{statResult})}{2} \right)}{4}
+ \frac{\text{magicJunctionnedValue} \times \text{magicAmount}}{100} 
\right)
$$

### HP

$$
\text{charaHP} = \text{charaBaseMaxHP} 
+ \text{charaLvl} \times \text{hp}_0 
- \frac{10 \times \text{charaLvl}^2}{\text{hp}_1}
+ \text{hp}_2
+ \text{magicAmount} \times \text{magicJunctionnedValue}
$$

{: .note }
>Only 3 of HP's 4 coefficients are used: `hp_3` (the 4th byte) is never read. There is no cap
>in this function; the final battle max-HP is `junctionMultiplier% × charaHP`, capped at 9999.


## Monster stat

Read from the exe. Coefficient blocks live in the monster's battle-`.dat` info section
(`ff8_battle_monster_info`): 4 bytes per stat. HP: `computeMonsterHP`; the other
stats: `Stat_ComputeMonsterStatCurve` (with SPR/SPD computed inline in
`updateStatChange`). Curve→stat mapping: STR and MAG use the quadratic curve; VIT,
SPR, SPD, EVA use the linear curve. All divisions truncate.

{: .note }
>`updateStatChange` applies a final per-monster multiplier to every battle stat:
>`finalStat = CapTo255(curveResult × statMult / 10)`. `statMult` defaults to **10 (×1.0)**, so
>the curve formulas below give the base value; AI scripts can scale a stat via this byte.

### HP

$$
\text{MonsterHP} =
\left\lfloor \frac{\text{HP}_0 \times \text{Lvl}^2}{20} \right\rfloor
+ \text{Lvl} \times \left(\text{HP}_0 + 100 \times \text{HP}_2\right)
+ 10 \times \left(\text{HP}_1 + 100 \times \text{HP}_3\right)
$$

{: .note }
>No outer `/100` (an earlier version of this page divided by 100, which is wrong — it made
>HP 100× too small). Written directly to max-HP; no clamp in this function.

### STR & MAG

Same shape as the character STR family (a single outer `/4`, quadratic term **subtracted**),
capped at 255:

$$
\text{Stat} = \text{CapTo255}\left(
\left\lfloor \frac{
    \text{S}_2
    + \left\lfloor \frac{\text{Lvl} \times \text{S}_0}{10} \right\rfloor
    + \left\lfloor \frac{\text{Lvl}}{\text{S}_1} \right\rfloor
    - \left\lfloor \frac{1}{2}\left\lfloor \frac{\text{Lvl}^2}{\text{S}_3} \right\rfloor \right\rfloor
}{4} \right\rfloor \right)
$$

### VIT & SPR & SPD & EVA

Plain linear curve, capped at 255:

$$
\text{Stat} = \text{CapTo255}\left(
\text{Lvl} \times \text{V}_0
+ \left\lfloor\frac{\text{Lvl}}{\text{V}_1}\right\rfloor
+ \text{V}_2
- \left\lfloor\frac{\text{Lvl}}{\text{V}_3}\right\rfloor
\right)
$$

# Experience

## Character level-up curve

The cumulative EXP a character needs to **reach level L** is driven by two bytes in the kernel
[Characters section]({{site.baseurl}}/technical-reference/main/kernel/characters/): `expLow` at
offset **0x06** scales a linear term, `expHigh` at offset **0x07** a quadratic term. (These were
historically read together as one little-endian "EXP modifier" WORD, but they are independent
parameters.)

$$
\text{TotalExp}(L) = 10 \times (L-1) \times \text{expLow} + \left\lfloor \frac{(L-1)^2 \times \text{expHigh}}{256} \right\rfloor
$$

{: .note }
>`Stat_ComputeLevelFromExp` accumulates this threshold per level and returns the first
>level whose threshold exceeds the character's EXP. Retail value **100** (`expLow=100, expHigh=0`)
>gives a flat **1000 EXP per level** (99 000 to reach level 100). A non-zero high byte makes the
>curve accelerate.

## Monster-given experience

{: .warning }
>Work in progress
>

### Regular experience

$$
\text{Exp} = \left\lfloor X \times \left(5 \times \frac{\text{M} - \text{P}}{\text{P}} + 4\right) \right\rfloor
$$

{: .note }
>Minimum of 1, provided X > 0 and it's not a boss.

### Kill bonus

$$
\text{KillBonusExp} = \left\lfloor Y \times \left(5 \times \frac{\text{M} - \text{C}}{\text{C}} + 4\right) \right\rfloor
$$

{: .note }
>Minimum of 1, provided Y > 0 and it's not a boss.

M = monster level  
P = average party level (active members only, rounded down)  
C = level of character/GF who gets kill shot and thus kill bonus  
X and Y depend on the monster

# Draw formula

MagicDrawResist is defined in the kernel associated to the magic  
MagicQuantity is the number of magic in the draw magic defined in the c0m file (always 0 in vanilla)


$$
\text{NumberMagDraw} = \frac{\left( \frac{\text{CharaLvl} - \text{MonsterLvl} + 10}{2} - \text{MagicDrawResist} + [1..32] + \text{MagChara} \right)}{5} - \text{MagicQuantity}
$$

# Crisis level

$$
\text{CrisisValue} = \frac{15300 \times \text{CrisisLevel}}{255}
$$

# Stat formula per level
## GF HP

`getGFhpForLvl`. The quadratic term is genuinely **added** (unlike character HP, which
subtracts it). `HPMod_1/2/3` = the `gfHPModifier1/2/3` bytes at kernel offsets 0x14/0x15/0x16.

$$
\text{GFHP} = \text{HPMod}_3 + \text{GFLvl} \times \text{HPMod}_1 + \frac{10 \times \text{GFLvl}^2}{\text{HPMod}_2}
$$

{: .note }
>No clamp in this function; the caller `computeGFBattleStats` does
>`gf_hp = percentHPBonus% × GFHP` (default ×1.0, raised by HP-Up abilities), capped at 9999.

## GF exp for next level needed

`getGFExpNeededForNextLevel` (÷256 confirmed). `NextLvlMod_1/2` = the
`nextLevelModifier1/2` bytes at kernel offsets 0x18/0x19.

$$
\text{GFNextLevelExp} = \frac{\text{GFLvl}^2 \times \text{NextLvlMod}_2}{256} + 10 \times \text{GFLvl} \times \text{NextLvlMod}_1
$$

# Function addresses

Reverse-engineering addresses for the functions referenced above, for readers who want to look them up in the exe.

| Function | Address |
|---|---|
| `ComputeMagicAndGFDamage` | 0x491ad0 |
| `ComputeWithDamageSTRFormula` | 0x492c40 |
| `computeAttackPhysical` | 0x492e10 |
| `HpModifierComputationForPhysical` | 0x48f600 |
| `Damage_RollCrit` | 0x492b30 |
| `Battle_DamageGettingRelated` | 0x4922b0 |
| `Battle_ApplyStatusWithResistRoll` | 0x48f9f0 |
| `Damage_ComputeCurativeItemSpecial` | 0x493450 |
| `Damage_ComputeCurativeMagic` | 0x493280 |
| `GetReviveHP` | 0x491940 |
| `computeLvlUpDown` | 0x493650 |
| `Damage_ComputeFixedSpecial` | 0x4931c0 |
| `Battle_RollCardCommand` | 0x48fba0 |
| Devour dispatcher case (HP reads at `0x4926cf`) | 0x4926bc |
| `computeDevour` | 0x48fc60 |
| `isRandomNumeratorDenominator` | 0x48f0c0 |
| `GetRandomInt` | 0x48f020 |
| Devour HP/status follow-up in `Battle_applyDamage` | 0x490479 |
| `Battle_CureStatusesAndSetFeedback` | 0x491820 |
| `sub_4914E0` (status-infliction core) | 0x4914e0 |
| `relatedToDevour` | 0x492220 |
| `increaseCharaStatBy1` | 0x495f90 |
| `sub_495F50` (permanent HP bonus) | 0x495f50 |
| Scan dispatcher case | 0x4925a6 |
| Angelo Search dispatcher case | 0x49284b |
| Moogle Dance dispatcher case | 0x4928d3 |
| `Stat_ComputeCharaMaxHP` | 0x496310 |
| `Stat_ComputeCharaStat` | 0x496440 |
| `CapTo255` | 0x495930 |
| `computeMonsterHP` | 0x48c500 |
| `Stat_ComputeMonsterStatCurve` | 0x48c3f0 |
| `updateStatChange` | 0x48c1c0 |
| `Stat_ComputeLevelFromExp` | 0x4961d0 |
| `getGFhpForLvl` | 0x496120 |
| `computeGFBattleStats` | 0x495e6b |
| `getGFExpNeededForNextLevel` | 0x496080 |


