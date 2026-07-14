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
>`ComputeMagicAndGFDamage`@0x491ad0 reads TargetSpr from the same `BATTLE_SLOT_DATA[]` slot array for players and monsters: the SPR term is one shared code path. The only monster-related asymmetry found is on the attacker side: if the caster is a monster, magic damage dealt is halved after this formula.

## Demi, Percent

$$
\text{Damage} = \frac{\text{AttackPower} \times \text{TargetCurrentHP}}{16}
$$

{: .note }
>Demi power = 4  
>Percent = 15

# GF

## Classic damage:

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

## Classic

Base physical damage, straight from the engine (`ComputeWithDamageSTRFormula`@0x492c40 and the
hit+crit-rolling `computeAttackPhysical`@0x492e10 — identical arithmetic):

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

Then `HpModifierComputationForPhysical`@0x48f600 applies, in order: **Protect** ÷2, **Back Attack**
×2, **Critical** ×2, **Zombie target** ÷2, and the elemental term
`dmg += dmg × elemAttack% × (800 − elemDef)/10000`. (VIT is read from the same `BATTLE_SLOT_DATA[]`
slot array for players and monsters — one shared code path.)

## Compute crit

Rolled in `Damage_RollCrit`@0x492b60: **crit if a random byte `0..255` ≤ `CritBonus + LUCK`** (the
`255×x/255` in the code is a no-op), so

$$
P(\text{crit}) = \frac{\text{CritBonus} + \text{LUCK}}{256}
$$

`CritBonus` is the weapon's crit bonus (or the enemy attack's / Shot's crit increase), staged in
`RELATED_TO_CRIT_BONUS`. A crit doubles the physical damage above.

## Hit %

Physical accuracy, from `computeAttackPhysical`@0x492e10:

$$
\text{hit\%} = \text{HitRate} + \left\lfloor\frac{\text{LUCK}}{2}\right\rfloor - \text{EVA}_{tgt} - \text{LUCK}_{tgt}
\qquad(\text{clamped} \ge 0)
$$

The attack lands if `255 × hit% / 100 ≥ rand(0..255)`. **`HitRate = 255` always hits** (the roll is
skipped); **Darkness** quarters `HitRate` first; **Sleep/Stop** targets are always hit.


# Stat

## Character stat
Each character stat is defined by 4 coefficients (noted `stat_0`..`stat_3`, i.e. the four
bytes stored per stat in the [Characters kernel section]({{site.baseurl}}/technical-reference/main/kernel/characters/#stat-curves)).
There are three distinct curve shapes — HP, the STR family, and the SPD/LCK pair — all read
below from the engine (`Stat_ComputeCharaMaxHP`@0x496310 for HP, `Stat_ComputeCharaStat`@0x496440
for the rest; the final sum is clamped by `CapTo255`@0x495930).

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
(`ff8_battle_monster_info`): 4 bytes per stat. HP: `computeMonsterHP`@0x48c500; the other
stats: `Stat_ComputeMonsterStatCurve`@0x48c3f0 (with SPR/SPD computed inline in
`updateStatChange`@0x48c1c0). Curve→stat mapping: STR and MAG use the quadratic curve; VIT,
SPR, SPD, EVA use the linear curve. All divisions truncate.

{: .note }
>`updateStatChange`@0x48c1c0 applies a final per-monster multiplier to every battle stat:
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
>`Stat_ComputeLevelFromExp`@0x4961d0 accumulates this threshold per level and returns the first
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

`getGFhpForLvl`@0x496120. The quadratic term is genuinely **added** (unlike character HP, which
subtracts it). `HPMod_1/2/3` = the `gfHPModifier1/2/3` bytes at kernel offsets 0x14/0x15/0x16.

$$
\text{GFHP} = \text{HPMod}_3 + \text{GFLvl} \times \text{HPMod}_1 + \frac{10 \times \text{GFLvl}^2}{\text{HPMod}_2}
$$

{: .note }
>No clamp in this function; the caller `computeGFBattleStats`@0x495e6b does
>`gf_hp = percentHPBonus% × GFHP` (default ×1.0, raised by HP-Up abilities), capped at 9999.

## GF exp for next level needed

`getGFExpNeededForNextLevel`@0x496080 (÷256 confirmed). `NextLvlMod_1/2` = the
`nextLevelModifier1/2` bytes at kernel offsets 0x18/0x19.

$$
\text{GFNextLevelExp} = \frac{\text{GFLvl}^2 \times \text{NextLvlMod}_2}{256} + 10 \times \text{GFLvl} \times \text{NextLvlMod}_1
$$




