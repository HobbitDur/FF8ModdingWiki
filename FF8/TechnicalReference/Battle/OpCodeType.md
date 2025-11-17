---
layout: default
parent: Battle
title: Opcode Type List
author: nihil, hobbitdur
permalink: /technical-reference/battle/opcode-type-list/
---

# Type list

## int

This type take literally the value of the parameter.
If the parameter is more than 1 byte, the int is in little endian
When speaking of int, we consider an unsigned int, so value are between 0 and 255 except state otherwise

## unused

Means the value is not used and could be changed by any value without any impact on the game

## Comparator

| Opcode dec | Opcode hex | Comparator pretty | Comparator IfritAI |
|------------|------------|-------------------|--------------------|
| 0          | 0x00       | ==                | ==                 |
| 1          | 0x01       | <                 | <                  |
| 2          | 0x02       | \>                | \>                 |
| 3          | 0x03       | ≠                 | !=                 |
| 4          | 0x04       | ≤                 | <=                 |
| 5          | 0x05       | ≥                 | \>=                |

## Target advanced specific

| Opcode dec | Opcode hex | Text          |
|------------|------------|---------------|
| 200        | 0xC8       | SELF          |
| 203        | 0xCB       | LAST ATTACKER |

## Target advanced generic

| Opcode dec | Opcode hex | Text       |
|------------|------------|------------|
| 200        | 0xC8       | ENEMY TEAM |
| 201        | 0xC9       | ALLY TEAM  |

## Target basic

| Opcode dec | Opcode hex | Text                  | Comment                               |
|------------|------------|-----------------------|---------------------------------------|
| 200        | 0xC8       | SELF                  |                                       |
| 201        | 0xC9       | RANDOM ENEMY          |                                       |
| 202        | 0xCA       | RANDOM ALLY           |                                       |
| 203        | 0xCB       | LAST ATTACKER         |                                       |
| 204        | 0xCC       | ALL ENEMIES           |                                       |
| 205        | 0xCD       | ALL ALLIES            |                                       |
| 206        | 0xCE       | UNKNOWN               |                                       |
| 207        | 0xCF       | RANDOM NONSELF ALLY   |                                       |
| 208        | 0xD0       | RANDOM ENEMY EACH HIT | Meteor, Omega Weapon with Terra Break |
| 209        | 0xD1       | NEW ALLY              | Shiva                                 |

# Monster line ability

In FF8, monster have 3 level of difficultyjehafeahhfxcdfgxf, by default at level 10, 20 and 30.   
For each level, the ability change.

An ability line correspond to a list of 3 abilities, with the first being at low level, second at medium level and third at high level.

A monster can have theoretically up to 255 ability line, even tho in practise 10 is already a lot.

So the value is the ID of the ability line, starting from 0. The line contains 3 [monster ability]({{site.baseurl}}/FF8/TechnicalReference/Lists/Ability_list#monster-ability)

# Local var

Local variable of unsigned byte type, used by AIs.    
Here the list of all available local vars and their respective IDs:

| Opcode dec | Opcode hex | IfritAI name |
|------------|------------|--------------|
| 220        | 0xDC       | varA         |
| 221        | 0xDD       | varB         |
| 222        | 0xDE       | varC         |
| 223        | 0xDF       | varD         |
| 224        | 0xE0       | varE         |
| 225        | 0xE1       | varF         |
| 226        | 0xE2       | varG         |
| 227        | 0xE3       | varH         |
| 228        | 0xE4       | varI         |

When used as a parameter for the opcode [**_target_**](../battle-scripts/#opcode-0x04-4---target):

| Value | Resulting target |
|-------|------------------|
| 0     | Battle slot 0    |
| 1     | Battle slot 1    |
| 2     | Battle slot 2    |
| 3     | Battle slot 3    |
| 4     | Battle slot 4    |
| 5     | Battle slot 5    |
| 6     | Battle slot 6    |
| 7     | Battle slot 7    |

_Battle slots_ from 0 to 2 represent the playable characters in menu order, 3 to 7 represent monsters, in [scene.out](../battle-structure-sceneout/) declaration order.  

# Savemap var

Not sure what does it correspond, but this is info that can be re-used between fight

# Global map

This are variable that can be reused anywhere in the game. Here the list known and when it is used for AI

| Opcode dec | Opcode hex | var_name     | Used for                                        |
|------------|------------|--------------|-------------------------------------------------|
| 81         | 0x51       | GlobalVar81  | TonberryDefeated                                |
| 82         | 0x52       | GlobalVar82  | TonberrySrIsDefeated                            |
| 83         | 0x53       | GlobalVar83  | UfoIsDefeated                                   |
| 84         | 0x54       | GlobalVar84  | FirstBugSeen                                    |
| 85         | 0x55       | GlobalVar85  | FirstBombSeen                                   |
| 86         | 0x56       | GlobalVar86  | FirstT-RexaurSeen                               |
| 87         | 0x57       | GlobalVar87  | LimitBreakIrvine                                |
| 96         | 0x60       | GlobalVar96  | WedgeAppeared, omegaWeaponFightedButNotDefeated |
| 97         | 0x61       | GlobalVar97  |                                                 |
| 98         | 0x62       | GlobalVar98  | ElvoretAppeared                                 |
| 102        | 0x66       | GlobalVar102 | FirstBugSeen                                    |

## Stat

| Opcode dec | Opcode hex | Text     |
|------------|------------|----------|
| 0          | 0x00       | Strength |
| 1          | 0x01       | Vitality |
| 2          | 0x02       | Magic    |
| 3          | 0x03       | Spirit   |
| 4          | 0x04       | Speed    |
| 5          | 0x05       | Evade    |

