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

$$
\text{Damage} =  \frac{\text{CritDamage} + 40}{20} \times \frac{\text{StrAttacker}^2}{16 + \text{StrAttacker}} \times \frac{265 - \text{VitReceiver}}{256} \times \frac{\text{AttackDamage}}{16} \times \frac{[0..32] + 240}{256}
$$

With CritDamage being 0 if no crit, 20 for Squall/Seifer if crit, 40 if crit from other characters.

## Compute crit

  v1 = 255 * (RELATED_TO_CRIT_BONUS + (unsigned __int8)BCI_LUCK[208 * p_attacker_slot_id]) / 255;


# Stat

## Character stat
Each character stat as 4 part (noted with a low number between 0 and 3)
Those stat can be seen with [doomtrain](https://github.com/DarkShinryu/doomtrain) for example.

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


## Monster stat

{: .warning }
>Monster stat formula have note been read from the code so they might not be exact
>

### HP

$$
\frac{
    \left\lfloor 
        \text{HP}_0 \times \left(\frac{\text{Lvl}^2}{20} + \text{Lvl}\right) 
    \right\rfloor 
    + 10 \times \text{HP}_1
    + \text{HP}_2 \times 100 \times \text{Lvl} 
    + 1000 \times \text{HP}_3
}{100}
$$

### STR MAG

$$
\left\lfloor \frac{\text{Lvl} \times \text{STR\_MAG}_0}{40} \right\rfloor
+ \left\lfloor \frac{\text{Lvl}}{4 \times \text{STR\_MAG}_1} \right\rfloor
+ \left\lfloor \frac{\text{STR\_MAG}_2}{4} \right\rfloor
+ \left\lfloor \frac{\text{Lvl}^2}{8 \times \text{STR\_MAG}_3} \right\rfloor
$$

### VIT & SPD & EVA

$$
\text{Lvl} \times \text{VIT\_SPD\_EVA}_0 + \left\lfloor\frac{\text{Lvl}}{\text{VIT\_SPD\_EVA}_1}\right\rfloor + \text{VIT\_SPD\_EVA}_2 - \left\lfloor\frac{\text{Lvl}}{\text{VIT\_SPD\_EVA}_3}\right\rfloor
$$

# Experience


{: .warning }
>Work in progress
>

Regular experience: X * (5 * (M - P) / P + 4), rounded down at the end, minimum of 1 provided X > 0 and it's not a boss.

Kill bonus: Y * (5 * (M - C) / C + 4), rounded down at the end, minimum of 1 provided Y > 0 and it's not a boss.

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

crisis_value = 15300 * BATTLE_SLOT_DATA[p_attacker_slot_id].crisis_level / 255;

# Stat formula per level
## GF HP
 K_GF_JUNCTIONABLE[gf_id].gfHPModifier3
       + gf_lvl * K_GF_JUNCTIONABLE[gf_id].gfHPModifier1
       + 10 * gf_lvl * gf_lvl / K_GF_JUNCTIONABLE[gf_id].gfHPModifier2;




