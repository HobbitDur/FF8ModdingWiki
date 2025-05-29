---
layout: default
parent: Battle
title: Battle Scripts
author: nihil, hobbitdur
permalink: /technical-reference/battle/battle-scripts/
---

FF8 monster battle scripts are divided into 5 sections, **init**, **turn**, **counter**, **death** and **pre-counter**.  
Each section contains code that is executed at different times during the battle.
- Init: executes once when the monster is loaded into battle.
- Turn: executes once the monster's ATB bar fills. This happens after the monsters turn counter is incremented.
- Counter: executes when the monster is targeted by a battle command.
- Death: executes when the monster’s HP reaches 0 or it is afflicted with the *Death* status.  (Eject may not trigger this section - this needs further testing.)
- Pre-Counter: similar to counter but executed before it. Needs further testing. Seems to be used mostly for checking if the monster has the *Death* status and then change its animation. Ifs, variable assignments and stat changes can also be used. Launching an attack from this section crashes the game.

The order of execution when a monster is attacked is: **pre-counter** -> **death** (if killed) -> **counter**.  
Note: **pre-counter** code will **ONLY** be executed after an attack that kills a monster if the monster's **death** section has code in it (apart from "return").  
Note: if the **death** section is empty, it will function like a **_die_** opcode.  
Note: if the **death** section is *NOT* empty, it is mandatory for it to eventually execute a **_die_** opcode, otherwise the monster will continue fighting, even on 0 HP, making the battle unwinnable for the player and forcing them to run. If running is not an option, this results in a soft lock.  


1. TOC
{:toc}

# Opcodes

Monster AI sections are composed of one-byte opcodes, each followed by a variable number of the bytes used as parameters.  
These opcodes define the monster's behaviour in battle.  
Note: descriptions are written from the monster's perspective, so "opposing party" refers to the party of playable characters.  

## Opcode 0x00 (0) - return

### Summary

| Opcode | IfritAI name | Size | Short Description  |
|--------|--------------|------|--------------------|
| 0x00   | return       | 1    | End monster's turn |

This opcode is used to end the monster's turn, preventing further execution of code.  
It is mandatory for every battle script section to end with a **_return_**.

### Parameters

None

---

## Opcode 0x01 (1) - print

Displays a battle message.

### Summary

| Opcode | IfritAI name | Size | Short Description   |
|--------|--------------|------|---------------------|
| 0x01   | print        | 2    | Print text          |

### Parameters

| Position | Size | Name       | Type                     | Short Description     |
|----------|------|------------|--------------------------|-----------------------|
| 1        | 1    | **TextID** | [int](../OpCodeType#int) | The index of the text |

Texts are defined in [section 7](../FileFormat_DAT#section-7-informations--stats) of c0mxxx.dat files.  
Each text has an ID, starting from 0 and incrementing with each subsequent text.  
**TextID** corresponds to this ID.  
Note that battle message speed is ignored.

---

## Opcode 0x02 (2) - if

### Summary

The if opcode allow to execute code only on certain condition

| Opcode | IfritAI name | Size | Short Description |
|--------|--------------|------|-------------------|
| 0x02   | if           | 1    | Define condition  |

### Parameters

The if opcode is a really complex one with lots of different possibilities.  
It is composed of a subject that define how the other parameters are used.  
Then it uses 3 parameters for the condition: the left part of the condition, the right part, and the comparator.  
So it does something like this: \[ConditionLeftPart\] \[Comparator\] \[ConditionRightPart\], for ex: COMBAT SCENE == 76  
Then there is a jump param to define the jump size if the condition is not met

| Position | Size | Name                   | Type                                   | Short Description                                    |
|----------|------|------------------------|----------------------------------------|------------------------------------------------------|
| 1        | 1    | **SubjectID**          | [SubjectID](#subjectid)                | Define what the if will be about                     |
| 2        | 1    | **ConditionLeftPart**  | Vary                                   | The left condition                                   |
| 3        | 1    | **Comparator**         | [Comparator](../OpCodeType#comparator) | The comparator of the condition                      |
| 4        | 1    | **ConditionRightPart** | Vary                                   | The right condition                                  |
| 5        | 1    | **Padding**            | [Unused](../OpCodeType#unused)         | Always 0x00 (changing it has no impact)              |
| 6        | 2    | **Jump**               | [int](../OpCodeType#int)               | The number of byte to jump if the condition is false |

### SubjectID

#### General info

The **SubjectID** defines what will be the type of the left part and right part of the condition  
The _Short text_ is a description of the subject id.  
The _Left text_ is the meaning of the **ConditionLeftPart**. {} is to be replaced with the value hold by **ConditionLeftPart** depending of _Param left type_  
The _Param left type_ define the type to use to translate the **ConditionLeftPart**  
Same logic for the **ConditionRightPart**  
The _Param list_ can feed the param type with additional info.

#### Subject list

| SubjectID | Short text                | Left text                           | Param left type                                                    | Right text     | Param right type         | Param list |
|-----------|---------------------------|-------------------------------------|--------------------------------------------------------------------|----------------|--------------------------|------------|
| 0         | HP OF SPECIFIC TARGET     | HP_SPE of {}                        | [target_advanced_specific](../OpCodeType#target-advanced-specific) |                | percent                  |            |
| 1         | HP OF GENERIC TARGET      | HP_GEN of {}                        | [target_advanced_generic](../OpCodeType#target-advanced-generic)   |                | percent                  |            |
| 2         | RANDOM VALUE              | RANDOM VALUE BETWEEN 0 AND {}       | int_shift                                                          |                | int                      | [-1]       |
| 3         | COMBAT SCENE              | COMBAT SCENE                        |                                                                    |                | int                      |            |
| 4         | STATUS OF SPECIFIC TARGET | STATUS_SPE OF {}                    | target_advanced_specific                                           |                | status_ai                |            |
| 5         | STATUS OF GENERIC TARGET  | STATUS_GEN OF {}                    | target_advanced_generic                                            |                | status_ai                |            |
| 6         | NUMBER OF MEMBER          | NUMBER OF MEMBER OF {}              | target_advanced_generic                                            |                | int                      |            |
| 9         | ALIVE                     | ALIVE                               |                                                                    |                | target_advanced_specific |            |
| 10        | ATTACKER                  | ATTACKER                            | subject10                                                          |                | complex                  |            |
| 14        | GROUP LEVEL               | GROUP LEVEL OF {}                   | target_advanced_generic                                            |                | int                      |            |
| 15        | ALIVE IN SLOT             | ALLY IN SLOT {}                     | int_right                                                          | ALIVE          | alive                    |            |
| 16        | GENDER CHECK              | AT LEAST ONE ENEMY ALIVE HAS GENDER |                                                                    |                | gender                   |            |
| 17        | GFORCE OBTAINED           | Gforce to be stolen                 | const                                                              | Not yet stolen | const                    | [200, 204] |
| 18        | ODIN OBTAINED             | {} POSSESS ODIN                     | target_advanced_generic                                            |                | int                      |            |
| 19        | COUNTDOWN                 | COUNTDOWN                           |                                                                    |                | int                      |            |
| 20        | STATUS OF ALL IN TEAM     | STATUS OF ALL IN {}                 | target_advanced_generic                                            |                | status_ai                |            |
| \>20      | Var                       | var                                 | var_name                                                           |                | int                      |            |

If the **SubjectID** is > 20, it means the subject is of type var, the **ConditionLeftPart** is the ID of the var and the **ConditionRightPart** the value of the var to be compared

#### Additional info:

Here are additional info for some values

##### HP OF SPECIFIC TARGET

The **ConditionLeftPart** 0xCB (203) is persists across battles

- **Byte #1:** 0x00 (Self / Last command user) or 0x01 (Any ally / opponent)
- **Byte #2:**
    - 0xC8 (200): Own HP / Any opponent's HP
    - 0xC9 (201): Unused / Any ally's HP
    - 0xCB (203): Last command user's HP (persists across battles) / Unused
- **Byte #4:** Remaining HP percentage
    - 0x0A (10) = 100%
    - 0x09 (9)  = 90%
    - . . .

##### 2. **Random Number Check**

- **Byte #1:** 0x02
- **Byte #2:** Exclusive upper bound of range (0 to this value - 1)
- **Byte #4:** Number to compare against

##### 3. **Status Check**

###### At least 1 member:

- **Byte #1:** 0x04 (Self / Last command user) or 0x05 (Any ally / opponent)
- **Byte #2:**
    - 0xC8 (200): Self / Any opponent
    - 0xC9 (201): Unused / Any ally
    - 0xCB (203): Last command user / Unused
- **Byte #4:** Status ID

###### All members of party:
- **Byte #1:** 0x14 (20)
- **Byte #2:**
    - 0xC8 (200): Opposing part
    - 0xC9 (201): Own party
- **Byte #4:** Status ID

##### 4. **Alive Count Check**

- **Byte #1:** 0x06
- **Byte #2:**
    - 0xC8 (200): Opposing party
    - 0xC9 (201): Own party
- **Byte #4:** Number to compare against

##### 5. **Specific Entity Alive Check**

- **Byte #1:** 0x09
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** Entity ID

##### 6. **Last Action / Turn Count Check**

- **Byte #1:** 0x0A (10)
- **Byte #2:**
    - 0x00: Damage Type (Byte #4: 0x00 = Physical, 0x01 = Magical)
    - 0x01: Last command user ID (Byte #4 = Entity ID)
    - 0x02: Turn Counter that increases as soon as the ATB bar is full (Byte #4 = Number)
    - 0x03: Command (Byte #4: 0x01 = Attack, 0x02 = Magic, 0x04 = Item, 0x06 = Draw, 0xFE = GF)
    - 0x04: ID (Byte #4: Magic/Item/GF ID)
    - 0x05: Element (Byte #4 = Element ID)
    - 0xCB (203): Last command user party (Byte #4: 0xC8 = Own part, 0xC9 = Opposing party)  **TO BE TESTED**

##### 7. **Entity Alive Check (In specific slot)**

- **Byte #1:** 0x0F (15)
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** Target slot + 3 (e.g., 0x03 for slot 0)

##### 8. **Sex check**

- **Byte #1:** 0x10 (16)
- **Byte #4:**
    - 0xCA (202): Male
    - 0xCB (203): Female

##### 9. **GF Check (Not yet obtained)**

- **Byte #1:** 0x11 (17)
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** 0xCC (204)

##### 10. **Odin Acquisition Check (true if obtained)**

- **Byte #1:** 0x12 (18)
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** 0x00 / 0x01 (true / false)

##### 11. **Timer Check**

- **Byte #1:** 0x13 (19)
- **Byte #2:** 0xC8 (Unused?)

##### 12. **Variable Check**

- **Byte #1:** Variable ID
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** Value to compare against


Some info for memory help on variable check for local variable:
To work as expect, it needs to be 0xC8 (200). But values of 0xCB and value from 220 to 227 (like the local variable ID).

For local var. If var == subjectID, then v93 = BATTLE_VAR
if 0xC8, v92 = attacker_slot_id
if 0xCB, v92 = last_attacker_slot_id

---



## Opcode 0x03 (1) - declareCommandMagic

This Opcode is not used in any monster, but the code seems to indicate it declares a command type as magic. Don't know the impact

---

## Opcode 0x04 (4) - target

### Summary

This opcode defines a target, it must be used before any opcode that requires a target (like launching an ability).  
If the target is a specific playable character who isn't currently targetable, the character in the slot of the original target -1 will be targeted, if the original target was slot 0, the new target will be slot 1 instead.  
Note that the original target will still be targeted by opcodes **_draw_** and **_blowAway_**.

| Opcode | IfritAI name | Size | Short Description |
|--------|--------------|------|-------------------|
| 0x04   | target       | 2    | Print text        |

### Parameters

| Position | Size | Name            | Type                                      | Short Description |
|----------|------|-----------------|-------------------------------------------|-------------------|
| 1        | 1    | **Target** | [TargetBasic](../OpCodeType#target-basic) | The target        |

---

## Opcode 0x05 (5) - die

### Summary 

Causes monster that executes this opcode to die.

| Opcode | IfritAI name | Size | Short Description     |
|--------|--------------|------|-----------------------|
| 0x05   | die          | 1    | Causes monster to die |

### Parameters

None

---


## Opcode 0x07 (1) - declareCommandMonsterAttack

This Opcode is not used in any monster, but the code seems to indicate it declares a command type as monster attack. Don't know the impact

---

## Opcode 0x0B (11) - useRandom

### Summary

Picks one of 3 abilities to use randomly, then uses it.  
Requires **_target_** to have been used.

| Opcode | IfritAI name | Size | Short Description            |
|--------|--------------|------|------------------------------|
| 0x0B   | useRandom    | 4    | Use random ability between 3 |

### Parameters

| Position | Size | Name                    | Type                                                     | Short Description       |
|----------|------|-------------------------|----------------------------------------------------------|-------------------------|
| 1        | 1    | **MonsterLineAbility1** | [MonsterLineAbility](../OpCodeType#monster-line-ability) | The first ability line  |
| 2        | 1    | **MonsterLineAbility2** | [MonsterLineAbility](../OpCodeType#monster-line-ability) | The second ability line |
| 3        | 1    | **MonsterLineAbility3** | [MonsterLineAbility](../OpCodeType#monster-line-ability) | The third ability line  |

---

## Opcode 0x0C (12) - use

### Summary

Use one ability, requires **_target_** to have been used.

| Opcode | IfritAI name | Size | Short Description |
|--------|--------------|------|-------------------|
| 0x0C   | use          | 2    | Use one ability   |

### Parameters

| Position | Size | Name                   | Type                                                     | Short Description |
|----------|------|------------------------|----------------------------------------------------------|-------------------|
| 1        | 1    | **MonsterLineAbility** | [MonsterLineAbility](../OpCodeType#monster-line-ability) | The ability line  |

---


## Opcode 0x0D (13) - unknown13
Seems to jump to the op code 25 (doNothing) and just save the param.

---

## Opcode 0x0E (14) - var

### Summary

Sets local variable that will be only accessible by this monster during the battle.  
Can also be used to initialize a battle variable, in case the battle variable already has a value this opcode will be ignored.

| Opcode | IfritAI name | Size | Short Description               |
|--------|--------------|------|---------------------------------|
| 0x0E   | var          | 3    | Set local var to specific value |

### Parameters

| Position | Size | Name      | Type                                | Short Description             |
|----------|------|-----------|-------------------------------------|-------------------------------|
| 1        | 1    | **Var**   | [LocalVar](../OpCodeType#local-var) | The var to store the data     |
| 2        | 1    | **Value** | [int](../OpCodeType#int)            | The value var is set to       |

---

## Opcode 0x0F (15) - gvar

Sets global variable (accessible by all monsters).

### Summary

Sets global variable (accessible by all monsters)

| Opcode | IfritAI name | Size | Short Description       |
|--------|--------------|------|-------------------------|
| 0x0F   | gvar         | 3    | Set global var to value |

### Parameters

| Position | Size | Name      | Type                                 | Short Description             |
|----------|------|-----------|--------------------------------------|-------------------------------|
| 1        | 1    | **Var**   | [LocalVar](../OpCodeType#global-var) | The var to store the data     |
| 2        | 1    | **Value** | [int](../OpCodeType#int)             | The value var is set to       |

---

## Opcode 0x11 (17) - svar

### Summary

Sets savemap variable (not sure how it it stored).

| Opcode | IfritAI name | Size | Short Description        |
|--------|--------------|------|--------------------------|
| 0x11   | svar         | 3    | Set savemap var to value |

### Parameters

| Position | Size | Name      | Type                                    | Short Description             |
|----------|------|-----------|-----------------------------------------|-------------------------------|
| 1        | 1    | **Var**   | [SavemapVar](../OpCodeType#savemap-var) | The var to store the data     |
| 2        | 1    | **Value** | [int](../OpCodeType#int)                | The value var is set to       |

---

## Opcode 0x12 (18) - add

### Summary

Adds value to local variable that will be only accessible by this monster during the battle.

| Opcode | IfritAI name | Size | Short Description      |
|--------|--------------|------|------------------------|
| 0x12   | add          | 3    | Add value to local var |

### Parameters

| Position | Size | Name      | Type                                | Short Description           |
|----------|------|-----------|-------------------------------------|-----------------------------|
| 1        | 1    | **Var**   | [LocalVar](../OpCodeType#local-var) | The var to store the data   |
| 2        | 1    | **Value** | [int](../OpCodeType#int)            | The value to add to the var |

If **Value** is equal to 0xCB (203), then the value add is the slot of the last attacker.

---

## Opcode 0x13 (19) - gadd

### Summary

Adds value to global var (accessible by all monsters).

| Opcode | IfritAI name | Size | Short Description       |
|--------|--------------|------|-------------------------|
| 0x13   | gadd         | 3    | Add value to global var |

### Parameters

| Position | Size | Name      | Type                                  | Short Description           |
|----------|------|-----------|---------------------------------------|-----------------------------|
| 1        | 1    | **Var**   | [GlobalVar](../OpCodeType#global-var) | The var to store the data   |
| 2        | 1    | **Value** | [int](../OpCodeType#int)              | The value to add to the var |

---

## Opcode 0x15 (21) - sadd

### Summary

Adds value to savemap var (not sure where it is stored).

| Opcode | IfritAI name | Size | Short Description        |
|--------|--------------|------|--------------------------|
| 0x15   | sadd         | 3    | Add value to savemap var |

### Parameters

| Position | Size | Name      | Type                                    | Short Description           |
|----------|------|-----------|-----------------------------------------|-----------------------------|
| 1        | 1    | **Var**   | [SavemapVar](../OpCodeType#savemap-var) | The var to store the data   |
| 2        | 1    | **Value** | [int](../OpCodeType#int)                | The value to add to the var |

---

## Opcode 0x16 (22) - recover

### Summary

Sets remaining HP to max HP.

| Opcode | IfritAI name | Size | Short Description           |
|--------|--------------|------|-----------------------------|
| 0x16   | recover      | 1    | Sets remaining HP to max HP |

### Parameters

None

---

## Opcode 0x17 (23) - setEscape

### Summary

Allows/Disallows escaping in the current battle.

| Opcode | IfritAI name | Size | Short Description      |
|--------|--------------|------|------------------------|
| 0x17   | setEscape    | 2    | Sets ability to escape |

### Parameters

| Position | Size | Name                | Type                       | Short Description                         |
|----------|------|---------------------|----------------------------|-------------------------------------------|
| 1        | 1    | **EscapeActivated** | [Bool](../OpCodeType#bool) | True to allow escape, False to deactivate |

---

## Opcode 0x18 (24) - printSpeed

### Summary

Displays a battle message, respecting the _battle message speed_ setting.

| Opcode | IfritAI name | Size | Short Description                            |
|--------|--------------|------|----------------------------------------------|
| 0x18   | printSpeed   | 2    | Print text with battle message speed setting |

### Parameters

| Position | Size | Name       | Type                     | Short Description     |
|----------|------|------------|--------------------------|-----------------------|
| 1        | 1    | **TextID** | [int](../OpCodeType#int) | The index of the text |

Texts are defined in [section 7](../FileFormat_DAT#section-7-informations--stats) of c0mxxx.dat files.  
Each text has an ID, starting from 0 and incrementing with each subsequent text.  
**TextID** corresponds to this ID.

---

## Opcode 0x1C (28) - waitText

### Summary

Wait the previous message, with in parameters the number of text to wait.

| Opcode | IfritAI name | Size | Short Description                            |
|--------|--------------|------|----------------------------------------------|
| 0x18   | waitText     | 2    | Wait text after printing some                |

### Parameters

| Position | Size | Name       | Type                     | Short Description          |
|----------|------|------------|--------------------------|----------------------------|
| 1        | 1    | **NbText** | [int](../OpCodeType#int) | The number of text to wait |


---

## Opcode 0x1D (29) - leave

### Summary

Makes the monster in a specified encounter slot leave combat.

| Opcode | IfritAI name | Size | Short Description            |
|--------|--------------|------|------------------------------|
| 0x1D   | leave        | 2    | Makes a monster leave combat |

### Parameters

| Position | Size | Name       | Type                     | Short Description            |
|----------|------|------------|--------------------------|------------------------------|
| 1        | 1    | **Target** | [int](../OpCodeType#int) | Monster that's made to leave |

**Target** is the slot in which the monster currently is in the fight.  
Note that if 200 is used, the monster executing this opcode will be used as **Target**.

---

## Opcode 0x1F (31) - enter

### Summary

Makes the monster in a specified encounter slot enter combat, by setting it's Enabled, NOT Targetable and NOT Loaded flags to true.  
Whilst possible, it is not advisable to use **_enter_** on an encounter slot if the monster in that slot is currently in the fight.

| Opcode | IfritAI name | Size | Short Description            |
|--------|--------------|------|------------------------------|
| 0x1F   | enter        | 2    | Makes a monster enter combat |

### Parameters

| Position | Size | Name       | Type                     | Short Description             |
|----------|------|------------|--------------------------|-------------------------------|
| 1        | 1    | **Target** | [int](../OpCodeType#int) | Encounter slot of the monster |

**Target** is the monster's encounter slot, as defined in [scene.out](../BattleStructure).  

---


## Opcode 0x20 (32) - waitTextFaster

### Summary

This is not used by any monster, analyse oif the code is not complete, but it seems to be like waitText but 2 times faster.

Wait the previous message like wait text

| Opcode | IfritAI name | Size | Short Description                            |
|--------|--------------|------|----------------------------------------------|
| 0x20   | waitText     | 2    | Wait text after printing some                |

### Parameters

| Position | Size | Name       | Type                     | Short Description          |
|----------|------|------------|--------------------------|----------------------------|
| 1        | 1    | **NbText** | [int](../OpCodeType#int) | The number of text to wait |


---

## Opcode 0x24 (36) - fillAtb

### Summary

Fills the monster's ATB bar, readying it for its turn.

| Opcode | IfritAI name | Size | Short Description       |
|--------|--------------|------|-------------------------|
| 0x24   | fillAtb      | 1    | Fills monster's ATB bar |

### Parameters

None

---

## Opcode 0x25 (37) - setScanText

### Summary

Sets the extra scan text to a specific battle text.
This text can be found in the bottom left section of the scan screen, where info such as HP, monster name, level and elemental affinities is shown.

| Opcode | IfritAI name | Size | Short Description       |
|--------|--------------|------|-------------------------|
| 0x25   | setScanText  | 2    | Sets extra scan text    |

### Parameters

| Position | Size | Name       | Type                     | Short Description     |
|----------|------|------------|--------------------------|-----------------------|
| 1        | 1    | **TextID** | [int](../OpCodeType#int) | The index of the text |

Texts are defined in [section 7](../FileFormat_DAT#section-7-informations--stats) of c0mxxx.dat files.  
Each text has an ID, starting from 0 and incrementing with each subsequent text.  
**TextID** corresponds to this ID.

---

## Opcode 0x26 (38) - statChange

### Summary

Sets the multiplier for a chosen stat.  
The base stat itself remains unchanged, but for calculations during battle, the stat used is affected by the multiplier.  
For example, if **_statChange_** is used to increase a stat to 500% of its original value, setting the multiplier back to 100% will restore it to its base value.

| Opcode | IfritAI name | Size | Short Description        |
|--------|--------------|------|--------------------------|
| 0x26   | statChange   | 3    | Changes a stat           |

### Parameters

| Position | Size | Name           | Type                                    | Short Description             |
|----------|------|----------------|-----------------------------------------|-------------------------------|
| 1        | 1    | **Stat**       | [Stat](../OpCodeType#stat)              | The stat that will be changed |
| 2        | 1    | **Multiplier** | [int](../OpCodeType#int)                | The multiplier for said stat  |

Note that **Multiplier** is multiplied by 10, so for example if its set to 0x28 (40), the stat will be multiplied by 0x28 \* 0x0A = 0x190 (40 \* 10 = 400)

---

## Opcode 0x29 (41) - draw

### Summary

Makes previous ability draw and store a randomly selected magic from target (use after opcode **_useRandom_** or **_use_**).  
Since monsters can only hold one drawn magic at a time, using **_draw_** again will overwrite the previously stored magic.  
In the case where **_draw_** is used on a playable character that has no magic or a monster, the message showing what magic was stolen will appear only the first time and a nameless magic with no effect that looks and sounds like _Cure_ will be stored.  
If a monster uses **_draw_** on itself and then uses **_cast_**, the game will crash.

| Opcode | IfritAI name | Size | Short Description |
|--------|--------------|------|-------------------|
| 0x29   | draw         | 1    | Draws magic       |

### Parameters

None

---

## Opcode 0x2A (42) - cast

### Summary

Casts magic that's been stored by using the **_draw_** opcode.  
If no magic is stored, does nothing.  
Using this after the monster used **_draw_** on itself will crash the game.  
Note that casting magic with this opcode will not consume the stored magic.

| Opcode | IfritAI name | Size | Short Description |
|--------|--------------|------|-------------------|
| 0x2A   | cast         | 1    | Casts drawn magic |

### Parameters

None

---

## Opcode 0x2E (46) - blowAway

### Summary

Makes previous ability remove a randomly selected magic from the target's inventory (use after opcode **_useRandom_** or **_use_**).  
Note that if the blown-away magic was junctioned to a stat, Elemental Attack/Defense, or Status Attack/Defense, the affected attribute will lose its junction bonus.  
Does nothing if the target has no magic.

| Opcode | IfritAI name | Size | Short Description |
|--------|--------------|------|-------------------|
| 0x2E   | blowAway     | 1    | Blow away magic   |

### Parameters

None

---

## Opcode 0x2F (47) - targetable

### Summary

Sets this monster's NOT Targetable flag to _False_.

| Opcode | IfritAI name   | Size | Short Description          |
|--------|----------------|------|----------------------------|
| 0x2F   | targetable     | 1    | Makes monster targetable   |

### Parameters

None

---

## Opcode 0x30 (48) - untargetable

### Summary

Sets this monster's NOT Targetable flag to _True_.

| Opcode | IfritAI name     | Size | Short Description          |
|--------|------------------|------|----------------------------|
| 0x30   | untargetable     | 1    | Makes monster untargetable |

### Parameters

None

---

## Opcode 0x34 (52) - enable

### Summary

Sets this monster's Enabled flag to _True_.

| Opcode | IfritAI name     | Size | Short Description |
|--------|------------------|------|-------------------|
| 0x30   | untargetable     | 1    | Enables monster   |

### Parameters

| Position | Size | Name       | Type                     | Short Description             |
|----------|------|------------|--------------------------|-------------------------------|
| 1        | 1    | **Target** | [int](../OpCodeType#int) | Encounter slot of the monster |

**Target** is the monster's encounter slot, as defined in [scene.out](../BattleStructure).  
