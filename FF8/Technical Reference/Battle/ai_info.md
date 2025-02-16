---
layout: default
parent: Battle
title: Opcode List
author: nihil, hobbitdur
---

This section will list all opcode of the game, with a type list of parameters
The point of view is of the monster. So when saying "Enemy team" means the squall team.

1. TOC
{:toc}

# Opcode list

## Opcode 0x00 (0) - return

### Summary

| Opcode | IfritAI name | Size | Short Description         |
|--------|--------------|------|---------------------------|
| 0x00   | return       | 1    | Exit the AI for this turn |

This function will stop the code execution and leave the AI turn.  
It can be used to either stop in a condition or used at the end of the AI code.  
It is mandatory to have one **_return_** for every end of execution.

### Parameters

None

---

## Opcode 0x01 (1) - print

### Summary

| Opcode | IfritAI name | Size | Short Description   |
|--------|--------------|------|---------------------|
| 0x01   | print        | 2    | Print text          |

### Parameters

| Position | Size | Name       | Yype                     | Short Description     |
|----------|------|------------|--------------------------|-----------------------|
| 1        | 1    | **TextID** | [int](../OpCodeType#int) | The index of the text |

Text in combat are defined in [section 7](../FileFormat_DAT#section-7-informations--stats) of c0mxxx.dat files.  
Each text as an ID starting from 0 to the number of text - 1.  
**TextID** correspond to this ID

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
So it does something like this: \[LeftCondition\] \[Comparator\] \[RightCondition\], for ex: COMBAT SCENE == 76  
Then there is a jump param to define the jump size if the condition is not met  

| Position | Size | Name               | Yype                                   | Short Description                                    |
|----------|------|--------------------|----------------------------------------|------------------------------------------------------|
| 1        | 1    | **SubjectID**      | [SubjectID](#subjectid)                | Define what the if will be about                     |
| 2        | 1    | **LeftCondition**  | Vary                                   | The left condition                                   |
| 3        | 1    | **Comparator**     | [Comparator](../OpCodeType#comparator) | The comparator of the condition                      |
| 4        | 1    | **RightCondition** | Vary                                   | The right condition                                  |
| 5        | 1    | **Padding**        | [Unused](../OpCodeType#unused)         | Always 0x00 (changing it has no impact)              |
| 6        | 2    | **Jump**           | [int](../OpCodeType#int)               | The number of byte to jump if the condition is false |

### SubjectID
The **SubjectID** defines what will be the type of the left and right condition  
The _Short text_ is a description of the subject id.  
The _Left text_ is the meaning of the **LeftCondition**. {} is to be replaced with the value hold by **LeftCondition** depending of _Param left type_  
The _Param left type_ define the type to use to translate the **LeftCondition**  
Same logic for the **RightCondition**  
The _Param list_ can feed the param type with additional info.  

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

If the **SubjectID** is > 20, it means the subject is of type var, the **LeftCondition** is the ID of the var and the **RightCondition** the value of the var to be compared  

#### Additional info:

##### HP OF SPECIFIC TARGET
The **LeftCondition** 0xCB (203) is persists across battles

- **Byte #1:** 0x00 (Self / Last command user) or 0x01 (Any ally / opponent)
- **Byte #2:**
    - 0xC8 (200): Own HP / Any opponent's HP
    - 0xC9 (201): Unused / Any ally's HP
    - 0xCB (203): Last command user's HP (persists across battles) / Unused
- **Byte #4:** Remaining HP percentage
    - 0x0A (10) = 100%
    - 0x09 (9)  = 90%
    - . . .

### 2. **Random Number Check**

- **Byte #1:** 0x02
- **Byte #2:** Exclusive upper bound of range (0 to this value - 1)
- **Byte #4:** Number to compare against

### 3. **Status Check**

### At least 1 member:

- **Byte #1:** 0x04 (Self / Last command user) or 0x05 (Any ally / opponent)
- **Byte #2:**
    - 0xC8 (200): Self / Any opponent
    - 0xC9 (201): Unused / Any ally
    - 0xCB (203): Last command user / Unused
- **Byte #4:** Status ID

  ### All members of party:
- **Byte #1:** 0x14 (20)
- **Byte #2:**
    - 0xC8 (200): Opposing part
    - 0xC9 (201): Own party
- **Byte #4:** Status ID

### 4. **Alive Count Check**

- **Byte #1:** 0x06
- **Byte #2:**
    - 0xC8 (200): Opposing party
    - 0xC9 (201): Own party
- **Byte #4:** Number to compare against

### 5. **Specific Entity Alive Check**

- **Byte #1:** 0x09
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** Entity ID

### 6. **Last Action / Turn Count Check**

- **Byte #1:** 0x0A (10)
- **Byte #2:**
    - 0x00: Damage Type (Byte #4: 0x00 = Physical, 0x01 = Magical)
    - 0x01: Last command user ID (Byte #4 = Entity ID)
    - 0x02: Turn Counter that increases as soon as the ATB bar is full (Byte #4 = Number)
    - 0x03: Command (Byte #4: 0x01 = Attack, 0x02 = Magic, 0x04 = Item, 0x06 = Draw, 0xFE = GF)
    - 0x04: ID (Byte #4: Magic/Item/GF ID)
    - 0x05: Element (Byte #4 = Element ID)
    - 0xCB (203): Last command user party (Byte #4: 0xC8 = Own part, 0xC9 = Opposing party)  **TO BE TESTED**

### 7. **Entity Alive Check (In specific slot)**

- **Byte #1:** 0x0F (15)
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** Target slot + 3 (e.g., 0x03 for slot 0)

### 8. **Sex check**

- **Byte #1:** 0x10 (16)
- **Byte #4:**
    - 0xCA (202): Male
    - 0xCB (203): Female

### 9. **GF Check (Not yet obtained)**

- **Byte #1:** 0x11 (17)
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** 0xCC (204)

### 10. **Odin Acquisition Check (true if obtained)**

- **Byte #1:** 0x12 (18)
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** 0x00 / 0x01 (true / false)

### 11. **Timer Check**

- **Byte #1:** 0x13 (19)
- **Byte #2:** 0xC8 (Unused?)

### 12. **Variable Check**

- **Byte #1:** Variable ID
- **Byte #2:** 0xC8 (Unused?)
- **Byte #4:** Value to compare against

---

## Opcode 0x04 (4) - IfritAI name: target (1 arg)

Defines target of battle ability

- **Byte #1:** Basic target

---

## Opcode 0x0B (11) - IfritAI name: useRandom (3 arg)

Picks one of 3 abilities to use randomly, then uses it

- **Byte #1 - Byte #3:** Monster ability ID (from the dat file)

---

## Opcode 0x0C (12) - IfritAI name: use (1 arg)

Uses ability

- **Byte #1:** Monster ability ID (from the dat file)

---

## Opcode 0x0E (14) - IfritAI name: var (2 args)

Sets local variable (accessible by this monster)

- **Byte #1:** Variable
- **Byte #2:** Unsigned byte value to assign

---

## Opcode 0x0F (15) - IfritAI name: gvar (2 args)

Sets global variable (accessible by all monsters)

- **Byte #1:** Variable
- **Byte #2:** Unsigned byte value to assign

---

## Opcode 0x11 (17) - IfritAI name: svar (2 args)

Sets savefile variable

- **Byte #1:** Variable
- **Byte #2:** Unsigned byte value to assign

---

## Opcode 0x12 (18) - IfritAI name: add (2 args)

Adds value to local variable (accessible by this monster)

- **Byte #1:** Variable
- **Byte #2:** Unsigned byte value to add

---

## Opcode 0x13 (19) - IfritAI name: gadd (2 args)

Adds value to battle variable (accessible by all monsters)

- **Byte #1:** Variable
- **Byte #2:** Unsigned byte value to add

---

## Opcode 0x15 (21) - IfritAI name: sadd (2 args)

Adds value to savefile variable

- **Byte #1:** Variable
- **Byte #2:** Unsigned byte value to add

---

## Opcode 0x16 (22) - IfritAI name: recover

Sets remaining HP to max HP

---

## Opcode 0x17 (23) - IfritAI name: setEscape (1 arg)

Sets ability to escape true / false

- **Byte #1:** Boolean value

---

# Opcode 0x2E (46) - IfritAI name: blowAway

Makes previous ability blow away magic from target (use after opcode 0x0B or 0x0C, useRandom or use)

---

