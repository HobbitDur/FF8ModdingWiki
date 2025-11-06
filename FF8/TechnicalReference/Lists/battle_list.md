---
layout: default
title: Battle
parent: List
permalink: /technical-reference/list/battle/
---


# Encounter data

| Value | Description                                                          |
|-------|----------------------------------------------------------------------|
| 0x0   | Regular battle.                                                      |
| 0x1   | No escape?                                                           |
| 0x2   | Disable victory fanfare (battle music keeps playing after win/loss). |
| 0x4   | Inherit countdown timer from field.                                  |
| 0x8   | No Item/XP Gain?                                                     |
| 0x10  | Use current music as battle music.                                   |
| 0x20  | Force preemptive attack.                                             |
| 0x40  | Force back attack.                                                   |
| 0x80  | Unknown.                                                             |

# Monster info byte flag


## Byte 0

| Bit Position | Flag (Hex) | Description |
|--------------|------------|-------------|
| 0 (LSB)      | 0x01       | UNKNOWN0    |
| 1            | 0x02       | UNKNOWN1    |
| 2            | 0x04       | UNKNOWN2    |
| 3            | 0x08       | UNKNOWN3    |
| 4            | 0x10       | UNKNOWN4    |
| 5            | 0x20       | UNKNOWN5    |
| 6            | 0x40       | UNKNOWN6    |
| 7 (MSB)      | 0x80       | UNKNOWN7    |


## Byte 1

| Bit Position | Flag (Hex) | Description           |
|--------------|------------|-----------------------|
| 0 (LSB)      | 0x01       | Zombie                |
| 1            | 0x02       | Fly                   |
| 2            | 0x04       | zz1                   |
| 3            | 0x08       | LvUp-Down Immunity    |
| 4            | 0x10       | HP Hidden             |
| 5            | 0x20       | Auto-Reflect          |
| 6            | 0x40       | Auto-Shell            |
| 7 (MSB)      | 0x80       | Auto-Protect          |

## Byte 2

| Bit Position | Flag (Hex) | Description             |
|--------------|------------|-------------------------|
| 0 (LSB)      | 0x01       | Increase SurpriseRNG    |
| 1            | 0x02       | Decrease SurpriseRNG    |
| 2            | 0x04       | SurpriseAttack Immunity |
| 3            | 0x08       | unused                  |
| 4            | 0x10       | unused                  |
| 5            | 0x20       | unused                  |
| 6            | 0x40       | Gravity Immunity        |
| 7 (MSB)      | 0x80       | Always obtains card     |

## GF/ Magic / Item Type damage

| Value | Description                     |
|-------|---------------------------------|
| 0x00  | Magic unmissable                |
| 0x01  | % Current HP                    |
| 0x02  | GF damage                       |
| 0x04  | Diablos damage                  |
| 0x05  | GF damage ignore SPR            |
| 0x06  | Magic ignore SPR and unmissable |
| 0x07  | Curative magic                  |
| 0x09  | White wind (Quistis blue magic) |
| 0x0A  | Magic damage                    |
| 0x0A  | Depends HIT% (100*Power-Hit%)   |
| 0x0C  | Target Current HP - 1 (Moomba)  |
| 0x0D  | Based on GF level (Cactuar)     |
| 0x0E  | Curative item                   |
| 0x0F  | Angelo recover                  |
| 0x11  | ?                               |
| 0x12  | 1 HP (Excalipoor)               |


enum GFMagicDamageType : __int8 {
    GF_MAGIC_DAMAGE_TYPE_MAGIC_UNMISSABLE               = 0x00, // Magic unmissable
    GF_MAGIC_DAMAGE_TYPE_PERCENT_CURRENT_HP             = 0x01, // % Current HP
    GF_MAGIC_DAMAGE_TYPE_GF_DAMAGE                      = 0x02, // GF damage
    GF_MAGIC_DAMAGE_TYPE_DIABLOS_DAMAGE                 = 0x04, // Diablos damage
    GF_MAGIC_DAMAGE_TYPE_GF_DAMAGE_IGNORE_SPR           = 0x05, // GF damage ignore SPR
    GF_MAGIC_DAMAGE_TYPE_MAGIC_IGNORE_SPR_AND_UNMISSABLE = 0x06, // Magic ignore SPR and unmissable
    GF_MAGIC_DAMAGE_TYPE_MAGIC_DAMAGE                   = 0x0A, // Magic damage
    GF_MAGIC_DAMAGE_TYPE_UNKNOWN                        = 0x11  // (Unknown)
};






