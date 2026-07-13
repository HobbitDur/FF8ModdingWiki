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
- Counter: executes after the monster is affected by a battle command. Note that this means its impossible to change a monsters stats/elemental resists before it takes damage, and that it cannot detect _Sleep_.
- Death: executes when the monster’s HP reaches 0 or it is afflicted with the *Death* status.  (Eject may not trigger this section - this needs further testing.)
- Pre-Counter: similar to counter but executed before it. Unlike the other sections, pre-counter runs **synchronously inside the damage-application code**, at the exact moment the hit is being resolved: the engine has already computed the damage and picked the default hit/death reaction animation, but has not yet committed the hit data. This unique timing is what gives pre-counter its special powers: it is the only section where **_setHitAnim_** works (it overrides the reaction animation for the very hit being processed — the classic vanilla use is checking for the *Death* status and swapping in a custom death animation), and it is also why launching an attack from this section crashes the game (the engine is in the middle of resolving another action). Ifs, variable assignments and stat changes can also be used safely here.

The order of execution when a monster is attacked is: **pre-counter** -> **death** (if killed) -> **counter**.  
This order is now fully explained by the engine's scheduling (verified via decompile, 2026-07): pre-counter runs *synchronously in the middle of the hit*, while death and counter are *queued* — during damage application each victim is stamped with a pending reaction (counter if it survived, death if it died with scripted death), and once the attacker's action fully completes, those reactions are queued **in the order the targets were hit**. For a multi-hit attack, pre-counter runs once, on the final hit.  
Note: **pre-counter** code will **ONLY** be executed after an attack that kills a monster if the monster's **death** section has code in it (apart from "return"). *Mechanism (traced 2026-07):* at monster load, the engine checks **the first bytecode byte of the death section** — if it is not the `return`/`stop` opcode (`0x00`), a "scripted death" flag is set. On a killing blow, both the death script *and* the pre-counter call go through that flag's branch. On ordinary (non-killing) hits, pre-counter is **not** gated by this flag at all and runs for every monster. Byte-exact quirk: only the *first* byte of the death section is checked, so a death section starting with `return` followed by more code is treated as empty (the extra code is unreachable anyway).  
Note: if the **death** section is empty, it will function like a **_die_** opcode.  
Note: if the **death** section is *NOT* empty, it is mandatory for it to eventually execute a **_die_** opcode, otherwise the monster will continue fighting, even on 0 HP, making the battle unwinnable for the player and forcing them to run. If running is not an option, this results in a soft lock. *Mechanism:* when a scripted-death monster is killed, the engine applies the Death status, runs pre-counter, then **removes the Death status again** and defers the actual death to the queued death section — the monster really is alive at 0 HP until its script executes **_die_**.  

The PC runtime interpreter, section dispatch functions, the scheduling queue, and a full deep-dive on pre-counter are documented in [Enemy AI VM Runtime](../enemy-ai-vm-runtime/). Beyond the 5 scripted sections, the same dispatcher also handles 4 engine-internal "sections" that contain no monster bytecode: Doom expiry (5), Regen ticks (6), the Odin/Gilgamesh/Phoenix auto-summons (7) and Angelo auto-actions (8) — see the same page.

1. TOC
{:toc}

# Opcodes

Monster AI sections are composed of one-byte opcodes, each followed by a variable number of the bytes used as parameters.  
These opcodes define the monster's behaviour in battle.  
Note: descriptions are written from the monster's perspective, so "opposing party" refers to the party of playable characters.  

## Opcode 0x00 (0) - return

### Summary

| Opcode | IfritAI name | Size | Short description  |
|--------|--------------|------|--------------------|
| 0x00   | return       | 1    | End monster's turn |

This opcode is used to end the monster's turn, preventing further execution of code.  
It is mandatory for every battle script section to end with a **_return_**.  
Note: the underlying engine calls this opcode `stop` internally; IfritAI and this wiki use the friendlier name **_return_**.

### Parameters

None

---

## Opcode 0x01 (1) - print

Displays a battle message.

### Summary

| Opcode | IfritAI name | Size | Short description   |
|--------|--------------|------|---------------------|
| 0x01   | print        | 2    | Print text          |

### Parameters

| Position | Size | Name       | Type                     | Short description     |
|----------|------|------------|--------------------------|-----------------------|
| 1        | 1    | **TextID** | [int](../opcode-type-list#int) | The index of the text |

Texts are defined in [section 7](../model-sections/information-stats/) of c0mxxx.dat files.  
Each text has an ID, starting from 0 and incrementing with each subsequent text.  
**TextID** corresponds to this ID.  
Note that battle message speed is ignored.

---

## Opcode 0x02 (2) - if

### Summary

The if opcode allow to execute code only on certain condition

| Opcode | IfritAI name | Size | Short description |
|--------|--------------|------|-------------------|
| 0x02   | if           | 1    | Define condition  |

### Parameters

The if opcode is a really complex one with lots of different possibilities.  
It is composed of a subject that define how the other parameters are used.  
Then it uses 3 parameters for the condition: the left part of the condition, the right part, and the comparator.  
So it does something like this: \[ConditionLeftPart\] \[Comparator\] \[ConditionRightPart\], for ex: COMBAT SCENE == 76  
Then there is a jump param to define the jump size if the condition is not met

| Position | Size | Name                   | Type                                   | Short description                                    |
|----------|------|------------------------|----------------------------------------|------------------------------------------------------|
| 1        | 1    | **SubjectID**          | [SubjectID](#subjectid)                | Define what the if will be about                     |
| 2        | 1    | **ConditionLeftPart**  | Vary                                   | The left condition                                   |
| 3        | 1    | **Comparator**         | [Comparator](../opcode-type-list#comparator) | The comparator of the condition                      |
| 4        | 1    | **ConditionRightPart** | Vary                                   | The right condition                                  |
| 5        | 1    | **Padding**            | [Unused](../opcode-type-list#unused)         | Always 0x00 (changing it has no impact)              |
| 6        | 2    | **Jump**               | [int](../opcode-type-list#int)               | The number of byte to jump if the condition is false |

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
| 0         | HP OF SPECIFIC TARGET     | HP_SPE of {}                        | [target_advanced_specific](../opcode-type-list#target-advanced-specific) |                | percent                  |            |
| 1         | HP OF GENERIC TARGET      | HP_GEN of {}                        | [target_advanced_generic](../opcode-type-list#target-advanced-generic)   |                | percent                  |            |
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

## Opcode 0x03 (3) - prepareMagic

### Summary

Stores a magic ID in the monster's *stored action*, so that it may be used by the opcode **_silentUse_**.  

| Opcode | IfritAI name | Size | Short description             |
|--------|--------------|------|-------------------------------|
| 0x03   | prepareMagic | 1    | Stores magic ID for later use |

### Parameters

| Position | Size | Name            | Type                                          | Short description |
|----------|------|-----------------|-----------------------------------------------|-------------------|
| 1        | 1    | **Magic ID**    | [Magic](../../list/magic-list/#magic)         | Magic ID          |

---

## Opcode 0x04 (4) - target

### Summary

This opcode defines a target, it must be used before any opcode that requires a target (like launching an ability).  
If the target is a specific playable character who isn't currently targetable, the character in the slot of the original target -1 will be targeted, if the original target was slot 0, the new target will be slot 1 instead.  
Note that the original target will still be targeted by opcodes **_draw_** and **_blowAway_** (TO BE TESTED: silentUse).

| Opcode | IfritAI name | Size | Short description |
|--------|--------------|------|-------------------|
| 0x04   | target       | 2    | Print text        |

### Parameters

| Position | Size | Name            | Type                                            | Short description |
|----------|------|-----------------|-------------------------------------------------|-------------------|
| 1        | 1    | **Target**      | [TargetBasic](../opcode-type-list#target-basic) | The target        |

OR

| Position | Size | Name            | Type                                      | Short description     |
|----------|------|-----------------|-------------------------------------------|-----------------------|
| 1        | 1    | **Var**         | [LocalVar](../opcode-type-list#local-var) | Var containing target |

OR

| Position | Size | Name            | Type                                                      | Short description     |
|----------|------|-----------------|-----------------------------------------------------------|-----------------------|
| 1        | 1    | **Monster ID**  | [c0mxxx.dat files ID](../monster-files-c0mxxxdat/) + 0x10 | Monster ID            |

---

## Opcode 0x06 (6) - usePrepared

### Summary 

Uses the monster's *stored action*.  

| Opcode | IfritAI name | Size | Short description     |
|--------|--------------|------|-----------------------|
| 0x06   | usePrepared  | 1    | Uses stored action    |

### Parameters

None

---

## Opcode 0x07 (7) - prepareMonsterAbility

### Summary

Stores an monster ability ID in the monster's *stored action*, so that it may be used by the opcode **_silentUse_**.  

| Opcode | IfritAI name          | Size | Short description                       |
|--------|-----------------------|------|-----------------------------------------|
| 0x07   | prepareMonsterAbility | 1    | Stores monster ability ID for later use |

### Parameters

| Position | Size | Name                      | Type                                               | Short description  |
|----------|------|---------------------------|----------------------------------------------------|--------------------|
| 1        | 1    | **Monster Ability ID**    | [Monster Ability ID](../../list/ability-list/#monster-ability) | Monster Ability ID |

---

## Opcode 0x08 (8) - die

### Summary 

Causes monster that executes this opcode to die.

| Opcode | IfritAI name | Size | Short description     |
|--------|--------------|------|-----------------------|
| 0x08   | die          | 1    | Causes monster to die |

### Parameters

None

---

## Opcode 0x0B (11) - useRandom

### Summary

Picks one of 3 abilities to use randomly, then uses it.  
Requires **_target_** to have been used.

| Opcode | IfritAI name | Size | Short description            |
|--------|--------------|------|------------------------------|
| 0x0B   | useRandom    | 4    | Use random ability between 3 |

### Parameters

| Position | Size | Name                    | Type                                                     | Short description       |
|----------|------|-------------------------|----------------------------------------------------------|-------------------------|
| 1        | 1    | **MonsterLineAbility1** | [MonsterLineAbility](../opcode-type-list#monster-line-ability) | The first ability line  |
| 2        | 1    | **MonsterLineAbility2** | [MonsterLineAbility](../opcode-type-list#monster-line-ability) | The second ability line |
| 3        | 1    | **MonsterLineAbility3** | [MonsterLineAbility](../opcode-type-list#monster-line-ability) | The third ability line  |

---

## Opcode 0x0C (12) - use

### Summary

Use one ability, requires **_target_** to have been used.

| Opcode | IfritAI name | Size | Short description |
|--------|--------------|------|-------------------|
| 0x0C   | use          | 2    | Use one ability   |

### Parameters

| Position | Size | Name                   | Type                                                     | Short description |
|----------|------|------------------------|----------------------------------------------------------|-------------------|
| 1        | 1    | **MonsterLineAbility** | [MonsterLineAbility](../opcode-type-list#monster-line-ability) | The ability line  |

---


## Opcode 0x0D (13) - noOp13

*(Previously documented as `unknown13`; renamed once its behavior was confirmed.)*

Confirmed via decompile (2026-07): reads its 1-byte parameter into a scratch variable that nothing consumes, then continues to the next opcode (it shares its exit path with **_doNothing_**). It is a true 2-byte no-op with no side effect. Not used by any monster in the vanilla game.

| Opcode | IfritAI name | Size | Short description |
|--------|--------------|------|-------------------|
| 0x0D   | noOp13       | 2    | No-op; parameter is read then discarded |

---

## Opcode 0x0E (14) - var

### Summary

Sets local variable that will be only accessible by this monster during the battle.  
Can also be used to initialize a battle variable, in case the battle variable already has a value this opcode will be ignored.

| Opcode | IfritAI name | Size | Short description               |
|--------|--------------|------|---------------------------------|
| 0x0E   | var          | 3    | Set local var to specific value |

### Parameters

| Position | Size | Name      | Type                                | Short description             |
|----------|------|-----------|-------------------------------------|-------------------------------|
| 1        | 1    | **Var**   | [LocalVar](../opcode-type-list#local-var) | The var to store the data     |
| 2        | 1    | **Value** | [int](../opcode-type-list#int)            | The value var is set to       |

If **Value** is 203, the ID of the _Last Attacker_ will be stored in the variable. 

---

## Opcode 0x0F (15) - bvar

Sets battle variable (accessible by all monsters).

### Summary

Sets global variable (accessible by all monsters)

| Opcode | IfritAI name | Size | Short description       |
|--------|--------------|------|-------------------------|
| 0x0F   | bvar         | 3    | Set battle var to value |

### Parameters

| Position | Size | Name      | Type                                 | Short description             |
|----------|------|-----------|--------------------------------------|-------------------------------|
| 1        | 1    | **Var**   | [LocalVar](../opcode-type-list#global-var) | The var to store the data     |
| 2        | 1    | **Value** | [int](../opcode-type-list#int)             | The value var is set to       |

---

## Opcode 0x11 (17) - gvar

### Summary

Sets savemap variable (not sure how it it stored).

| Opcode | IfritAI name | Size | Short description        |
|--------|--------------|------|--------------------------|
| 0x11   | gvar         | 3    | Set savemap var to value |

### Parameters

| Position | Size | Name      | Type                                    | Short description             |
|----------|------|-----------|-----------------------------------------|-------------------------------|
| 1        | 1    | **Var**   | [SavemapVar](../opcode-type-list#savemap-var) | The var to store the data     |
| 2        | 1    | **Value** | [int](../opcode-type-list#int)                | The value var is set to       |

---

## Opcode 0x12 (18) - add

### Summary

Adds value to local variable that will be only accessible by this monster during the battle.

| Opcode | IfritAI name | Size | Short description      |
|--------|--------------|------|------------------------|
| 0x12   | add          | 3    | Add value to local var |

### Parameters

| Position | Size | Name      | Type                                | Short description           |
|----------|------|-----------|-------------------------------------|-----------------------------|
| 1        | 1    | **Var**   | [LocalVar](../opcode-type-list#local-var) | The var to store the data   |
| 2        | 1    | **Value** | [int](../opcode-type-list#int)            | The value to add to the var |

If **Value** is equal to 0xCB (203), then the added value is equal to the last attacker's slot.

---

## Opcode 0x13 (19) - badd

### Summary

Adds value to battle var (accessible by all monsters).

| Opcode | IfritAI name | Size | Short description       |
|--------|--------------|------|-------------------------|
| 0x13   | badd         | 3    | Add value to battle var |

### Parameters

| Position | Size | Name      | Type                                  | Short description           |
|----------|------|-----------|---------------------------------------|-----------------------------|
| 1        | 1    | **Var**   | [GlobalVar](../opcode-type-list#global-var) | The var to store the data   |
| 2        | 1    | **Value** | [int](../opcode-type-list#int)              | The value to add to the var |

---

## Opcode 0x15 (21) - gadd

### Summary

Adds value to savemap var (not sure where it is stored).

| Opcode | IfritAI name | Size | Short description        |
|--------|--------------|------|--------------------------|
| 0x15   | gadd         | 3    | Add value to savemap var |

### Parameters

| Position | Size | Name      | Type                                    | Short description           |
|----------|------|-----------|-----------------------------------------|-----------------------------|
| 1        | 1    | **Var**   | [SavemapVar](../opcode-type-list#savemap-var) | The var to store the data   |
| 2        | 1    | **Value** | [int](../opcode-type-list#int)                | The value to add to the var |

---

## Opcode 0x16 (22) - recover

### Summary

Sets remaining HP to max HP.

| Opcode | IfritAI name | Size | Short description           |
|--------|--------------|------|-----------------------------|
| 0x16   | recover      | 1    | Sets remaining HP to max HP |

### Parameters

None

---

## Opcode 0x17 (23) - setEscape

### Summary

Allows/Disallows escaping in the current battle.  
**Correction:** the underlying engine name for this opcode is `cannotEscape` (reference data comment: "Deactivate Run away"), which implies the boolean below is the opposite polarity of what was previously documented here. This needs to be confirmed in-game: it is likely that `True` **blocks** escape rather than allowing it.

| Opcode | IfritAI name | Size | Short description      |
|--------|--------------|------|------------------------|
| 0x17   | setEscape    | 2    | Sets ability to escape |

### Parameters

| Position | Size | Name                | Type                       | Short description                          |
|----------|------|---------------------|----------------------------|--------------------------------------------|
| 1        | 1    | **EscapeActivated** | [Bool](../opcode-type-list#bool) | Previously documented as "True to allow escape, False to disallow it" — likely backwards, see correction above. **TO BE TESTED.** |

---

## Opcode 0x18 (24) - printSpeed

### Summary

Displays a battle message, respecting the _battle message speed_ setting.

| Opcode | IfritAI name | Size | Short description                            |
|--------|--------------|------|----------------------------------------------|
| 0x18   | printSpeed   | 2    | Print text with battle message speed setting |

### Parameters

| Position | Size | Name       | Type                     | Short description     |
|----------|------|------------|--------------------------|-----------------------|
| 1        | 1    | **TextID** | [int](../opcode-type-list#int) | The index of the text |

Texts are defined in [section 7](../model-sections/information-stats/) of c0mxxx.dat files.  
Each text has an ID, starting from 0 and incrementing with each subsequent text.  
**TextID** corresponds to this ID.

---

## Opcode 0x1C (28) - waitText

### Summary

Waits for a specified amount of texts to finish displaying before resuming the battle.

| Opcode | IfritAI name | Size | Short description                     |
|--------|--------------|------|---------------------------------------|
| 0x18   | waitText     | 2    | Waits for text/s to finish displaying |

### Parameters

| Position | Size | Name       | Type                     | Short description               |
|----------|------|------------|--------------------------|---------------------------------|
| 1        | 1    | **NbText** | [int](../opcode-type-list#int) | The number of texts to wait for |


---

## Opcode 0x1D (29) - leave

### Summary

Makes the monster in a specified encounter slot leave combat.

| Opcode | IfritAI name | Size | Short description            |
|--------|--------------|------|------------------------------|
| 0x1D   | leave        | 2    | Makes a monster leave combat |

### Parameters

| Position | Size | Name       | Type                     | Short description            |
|----------|------|------------|--------------------------|------------------------------|
| 1        | 1    | **Target** | [int](../opcode-type-list#int) | Monster that's made to leave |

**Target** is the slot in which the monster currently is in the fight.  
Note that if 200 is used, the monster executing this opcode will be used as **Target**.

---

## Opcode 0x1F (31) - enter

### Summary

Makes the monster in a specified encounter slot enter combat, by setting it's Enabled, NOT Targetable and NOT Loaded flags to true.  
Whilst possible, it is not advisable to use **_enter_** on an encounter slot if the monster in that slot is currently in the fight.

| Opcode | IfritAI name | Size | Short description            |
|--------|--------------|------|------------------------------|
| 0x1F   | enter        | 2    | Makes a monster enter combat |

### Parameters

| Position | Size | Name       | Type                     | Short description             |
|----------|------|------------|--------------------------|-------------------------------|
| 1        | 1    | **Target** | [int](../opcode-type-list#int) | Encounter slot of the monster |

**Target** is the monster's encounter slot, as defined in [scene.out](../battle-structure-sceneout/).  

---


## Opcode 0x20 (32) - waitTextFast

### Summary

This is not used by any monster, analyse of the code is not complete, but it seems to be like waitText but 2 times faster.

Wait the previous message like wait text

| Opcode | IfritAI name | Size | Short description                     |
|--------|--------------|------|---------------------------------------|
| 0x20   | waitTextFast | 2    | Waits for text/s to finish displaying, twice as fast as waitText |

### Parameters

| Position | Size | Name       | Type                     | Short description               |
|----------|------|------------|--------------------------|---------------------------------|
| 1        | 1    | **NbText** | [int](../opcode-type-list#int) | The number of texts to wait for |


---

## Opcode 0x24 (36) - fillAtb

### Summary

Fills the monster's ATB bar, readying it for its turn.

| Opcode | IfritAI name | Size | Short description       |
|--------|--------------|------|-------------------------|
| 0x24   | fillAtb      | 1    | Fills monster's ATB bar |

### Parameters

None

---

## Opcode 0x25 (37) - setScanText

### Summary

Sets the extra scan text to a specific battle text.
This text can be found in the bottom left section of the scan screen, where info such as HP, monster name, level and elemental affinities is shown.

| Opcode | IfritAI name | Size | Short description       |
|--------|--------------|------|-------------------------|
| 0x25   | setScanText  | 2    | Sets extra scan text    |

### Parameters

| Position | Size | Name       | Type                     | Short description     |
|----------|------|------------|--------------------------|-----------------------|
| 1        | 1    | **TextID** | [int](../opcode-type-list#int) | The index of the text |

Texts are defined in [section 7](../model-sections/information-stats/) of c0mxxx.dat files.  
Each text has an ID, starting from 0 and incrementing with each subsequent text.  
**TextID** corresponds to this ID.

---

## Opcode 0x28 (40) - statChange

### Summary

Sets the multiplier for a chosen stat.  
The base stat itself remains unchanged, but for calculations during battle, the stat used is affected by the multiplier.  
For example, if **_statChange_** is used to increase a stat to 500% of its original value, setting the multiplier back to 100% will restore it to its base value.

| Opcode | IfritAI name | Size | Short description        |
|--------|--------------|------|--------------------------|
| 0x28   | statChange   | 3    | Changes a stat           |

### Parameters

| Position | Size | Name           | Type                                    | Short description             |
|----------|------|----------------|-----------------------------------------|-------------------------------|
| 1        | 1    | **Stat**       | [Stat](../opcode-type-list#stat)              | The stat that will be changed |
| 2        | 1    | **Multiplier** | [int](../opcode-type-list#int)                | The multiplier for said stat  |

Note that **Multiplier** is multiplied by 10, so for example if its set to 0x28 (40), the stat will be multiplied by 0x28 \* 0x0A = 0x190 (40 \* 10 = 400)

---

## Opcode 0x29 (41) - draw

### Summary

Makes previous ability draw and store a randomly selected magic from target (use after opcode **_useRandom_** or **_use_**).  
Since monsters can only hold one drawn magic at a time, using **_draw_** again will overwrite the previously stored magic.  
In the case where **_draw_** is used on a playable character that has no magic or a monster, the message showing what magic was stolen will appear only the first time and a nameless magic with no effect that looks and sounds like _Cure_ will be stored.  
If a monster uses **_draw_** on itself and then uses **_cast_**, the game will crash.

| Opcode | IfritAI name | Size | Short description |
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

| Opcode | IfritAI name | Size | Short description |
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

| Opcode | IfritAI name | Size | Short description |
|--------|--------------|------|-------------------|
| 0x2E   | blowAway     | 1    | Blow away magic   |

### Parameters

None

---

## Opcode 0x2F (47) - targetable

### Summary

Sets this monster's NOT Targetable flag to _False_.

| Opcode | IfritAI name   | Size | Short description          |
|--------|----------------|------|----------------------------|
| 0x2F   | targetable     | 1    | Makes monster targetable   |

### Parameters

None

---

## Opcode 0x30 (48) - untargetable

### Summary

Sets this monster's NOT Targetable flag to _True_.

| Opcode | IfritAI name     | Size | Short description          |
|--------|------------------|------|----------------------------|
| 0x30   | untargetable     | 1    | Makes monster untargetable |

### Parameters

None

---

## Opcode 0x34 (52) - enable

### Summary

Sets this monster's Enabled flag to _True_.

| Opcode | IfritAI name | Size | Short description |
|--------|--------------|------|-------------------|
| 0x34   | enable       | 1    | Enables monster   |

### Parameters

| Position | Size | Name       | Type                     | Short description             |
|----------|------|------------|--------------------------|-------------------------------|
| 1        | 1    | **Target** | [int](../opcode-type-list#int) | Encounter slot of the monster |

**Target** is the monster's encounter slot, as defined in [scene.out](../battle-structure-sceneout/).

---

## Additional opcodes (not yet fully written up)

The 30 opcodes above are the ones that had a full write-up. IfritAI's reference data (`ai_vanilla.json`) confirms 59 opcodes total exist, so the following 25 were missing from this page entirely. They're real, working opcodes — just not documented in as much depth yet. Descriptions below are confirmed against the decompiled engine code (2026-07); anyone expanding these into full sections (with worked examples, like the ones above) would be doing the wiki a favor.

Six of these opcodes were previously misnamed (or named before their behavior was understood) in IfritAI's reference data and have been **renamed** after this verification pass — see the callouts below:

| Old name | New name | Why |
|----------|----------|-----|
| `remain` | `vanish` | The code silently removes the monster from battle — the opposite of "remaining" |
| `addMaxHP` | `addCurrentHP` | The code writes current HP, never max HP |
| `anim` | `setHitAnim` | It doesn't play an animation — it sets the hit/death **reaction** animation of the current hit (pre-counter only) |
| `unknown13` | `noOp13` | Behavior is now known: a verified no-op |
| `enterAlt` | `enterWithAnim` | "Alt" said nothing; the actual difference from `enter` is the played entrance animation |
| `targetAllySlot` | `targetBattleSlot` | The parameter is a raw battle slot, and nothing restricts it to allies |

| Opcode | IfritAI name | Size | Description | Notes |
|--------|--------------|------|--------------|-------|
| 0x05 (5) | prepareAnim | 1 | Sets the animation-sequence ID ([section 5](../model-sections/animation-sequences/)) that will be used when the stored action is launched with **_usePrepared_**. Note that **_use_**/**_useRandom_** overwrite this with the ability's own animation from section 7, so it only has an effect on the prepare→usePrepared path | Used by monsters 11, 12, 91, 109, 122, 124, 126 |
| 0x09 (9) | **setHitAnim** *(renamed from `anim`)* | 1 | Sets the hit/death **reaction** animation (a [section 5](../model-sections/animation-sequences/) sequence ID) that this monster plays for the **hit currently being resolved**. How it works: when a hit lands, the engine first derives the default reaction animation from the attack's kernel data (its `animationTriggered` byte, with miss = dodge and crit = stagger overrides), *then* runs the monster's pre-counter section, *then* commits the value into the hit data. An opcode 9 call inside pre-counter therefore lands in exactly the right window to override the reaction. Outside pre-counter (Init/Turn/Counter/Death) the value is recomputed before being read, so it does nothing — which is why earlier testing from the Turn section showed "no impact in game". The engine's own default for a normal death is sequence **3**, which is why almost every vanilla usage is `setHitAnim(3)` guarded by a Death-status check (force the standard death animation), while special monsters use custom sequences (12–16, 36, 49, 59) for unique death/hit reactions | **Renamed 2026-07.** Used by ~25 vanilla monsters, exclusively in the pre-counter section |
| 0x19 (25) | doNothing | 1 | Reads and discards one padding byte; a true no-op | |
| 0x1A (26) | printAndLock | 1 | Displays a battle message and blocks further script execution until that message finishes displaying | |
| 0x1B (27) | **enterWithAnim** *(renamed from `enterAlt`)* | 2 | Makes the monster in encounter slot `{param1}` enter combat **with an entrance action/animation played immediately** (battle slot = param1 + 3). Internally it queues and executes the same command family as the Phoenix-Pinion/kamikaze effects (sub-type 3), raises the same internal flag as **_prepareSummon_**, then makes the monster present (loaded, visible, targetable) once the entrance animation unlocks. This is the "scripted reinforcement with fanfare" variant of **_enter_**: compare `c0m074` (Biggs), which uses `enterWithAnim(1, 0)` for Wedge's dramatic entrance but plain `enter(2)` for a silent reinforcement | **Renamed 2026-07.** Param2 is passed down as the command's target-slot sub-parameter; its exact role is still unconfirmed |
| 0x1E (30) | specialAction | 1 | Queues a special action by ID, indexing the special action list | |
| 0x22 (34) | printAlt | 2 | Displays a battle message with a configurable wait/delay time (2nd parameter). Not used by any monster script | |
| 0x23 (35) | jump | 2 | The raw unconditional jump — this is what implements **_if_**'s else/endif branches under the hood | See [Enemy AI VM Runtime](../enemy-ai-vm-runtime/) |
| 0x26 (38) | targetStatus | 4 | Builds a target mask from all actors matching a status condition (target type, comparator, status ID) | |
| 0x27 (39) | autoStatus | 2 | Sets or clears a status flag on self. Status IDs ≥ 16 write to the status_2 field (offset by 16), IDs < 16 write to status_1 | |
| 0x2B (43) | **targetBattleSlot** *(renamed from `targetAllySlot`)* | 1 | Targets a **battle slot** directly: sets the pending target mask to `1 << param`, with **no +3 conversion** — so the parameter is a raw battle slot (0–2 = characters, 3+ = monsters), *not* an encounter slot as previously believed, and nothing in the code restricts it to allies. The old "seems to require assignSlot" note is now fully explained by its only vanilla user, `c0m124` (Mobile Type 8): the script first pins its two probes with `assignSlot(4, 4)` and `assignSlot(5, 5)` (encounter slot into that *same-numbered* battle slot — which is why the parameter was mistakable for an encounter slot), then uses `targetBattleSlot(4)` / `targetBattleSlot(5)` to aim its revival abilities at them. Without the assignSlot pinning, the probes' battle slots wouldn't be predictable and the hardcoded values would miss | **Renamed 2026-07** |
| 0x2C (44) | **vanish** *(renamed from `remain`)* | 0 | Silently removes this monster from battle: sets Death status, Not Targetable, and clears the "enabled" flag — with no death sequence/message. The old name `remain` described the opposite of what the code does | **Renamed 2026-07.** Only known to be used by monster IDs 87 and 91 — worth checking those scripts to see if it's used to hide a "shell" slot while another part of the same monster keeps fighting |
| 0x2D (45) | elemDmgMod | 3 | Writes a 16-bit value into a per-monster local-var slot indexed by element ID; some later damage calculation presumably reads it back as a resistance modifier. IfritAI encodes the authored percentage as `900 - percent` when compiling — this transform is unverified against actual in-game damage output | |
| 0x31 (49) | giveGF | 1 | Gives the player a specific GF and records it in the save data | Used by Tomberry |
| 0x32 (50) | prepareSummon | 0 | Sets an internal "preparing a summon" flag; no parameters | |
| 0x33 (51) | activate | 0 | Queues an "activate" battle task; no parameters | |
| 0x35 (53) | loadAndTargetable | 1 | Finalizes a monster's entrance: once the current animation unlocks, clears the NOT Loaded, NOT Visible **and** NOT Targetable flags on the given battle slot, recomputes the enable masks and starts the slot's periodic effects (Regen ticks etc.). Parameter value 209 means "the slot filled by the most recent **_enter_**/**_assignSlot_**" | Typical pattern: `assignSlot` → … → `loadAndTargetable(209)` |
| 0x36 (54) | gilgamesh | 0 | Sets the savegame flag that marks Gilgamesh as available | |
| 0x37 (55) | giveCard | 1 | Adds a specific Triple Triad card to the battle's card-drop list | |
| 0x38 (56) | giveItem | 1 | Adds a specific item to the battle's item drop/steal list | |
| 0x39 (57) | gameOver | 0 | Forces a Game Over | |
| 0x3A (58) | targetableSlot | 1 | Clears **only** the NOT Targetable flag on the given **battle slot** (unlike **_loadAndTargetable_**, it does not touch NOT Loaded / NOT Visible), then queues an enable-mask recompute. The "unexpected results" reported when testing it likely come from using it on a slot that isn't loaded/visible yet, or from passing an encounter slot where a battle slot is expected | |
| 0x3B (59) | assignSlot | 2 | Brings the monster from encounter slot `{param1}` into battle slot `{param2}` — identical to **_enter_** except the destination battle slot is explicit. Battle slot `0` = auto-search the first free monster slot (confirmed in code; fails with slot 255 if none is free). Loads the monster's skeleton/weapon/animations, records the slot as "last entered" (consumable by `loadAndTargetable(209)`), and makes it present once the animation unlocks | Used by monsters 124 and 126 |
| 0x3C (60) | **addCurrentHP** *(renamed from `addMaxHP`)* | 1 | Adds a signed 16-bit value directly to the monster's **current** HP. The old name and its own description ("Increase max HP (but not current)") both claimed it touched max HP — the decompiled code only ever writes `current_hp`, never `max_hp` | **Renamed 2026-07.** Negative values presumably work as direct damage; worth confirming there's no clamp to max HP |
| 0x3D (61) | proofOfOmega | 0 | Gives the player "Proof of Omega". The item ID (127) is hardcoded in the engine function, not passed as a script parameter | Only used by monster ID 114 (Omega Weapon) |
