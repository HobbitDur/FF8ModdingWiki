---
layout: default
title: Weapons
nav_order: 6
parent: Kernel
permalink: /weapons/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x35B8 | 33       | 12 bytes     |

## Sections

| Offset | Character | Weapon Name     |
|--------|-----------|-----------------|
| 0x35B8 | Squall    | Revolver        |
| 0x35C4 | Squall    | Shear Trigger   |
| 0x35D0 | Squall    | Cutting Trigger |
| 0x35DC | Squall    | Flame Saber     |
| 0x35E8 | Squall    | Twin Lance      |
| 0x35F4 | Squall    | Punishment      |
| 0x3600 | Squall    | Lion Heart      |
| 0x360C | Zell      | Metal Knuckle   |
| 0x3618 | Zell      | Maverick        |
| 0x3624 | Zell      | Gauntlet        |
| 0x3630 | Zell      | Ehrgeiz         |
| 0x363C | Irvine    | Valiant         |
| 0x3648 | Irvine    | Ulysses         |
| 0x3654 | Irvine    | Bismark         |
| 0x3660 | Irvine    | Exeter          |
| 0x366C | Quistis   | Chain Whip      |
| 0x3678 | Quistis   | Slaying Tail    |
| 0x3684 | Quistis   | Red Scorpion    |
| 0x3690 | Quistis   | Save the Queen  |
| 0x369C | Rinoa     | Pinwheel        |
| 0x36A8 | Rinoa     | Valkyrie        |
| 0x36B4 | Rinoa     | Rising Sun      |
| 0x36C0 | Rinoa     | Cardinal        |
| 0x36CC | Rinoa     | Shooting Star   |
| 0x36D8 | Selphie   | Flail           |
| 0x36E4 | Selphie   | Morning Star    |
| 0x36F0 | Selphie   | Crescent Wish   |
| 0x36FC | Selphie   | Strange Vision  |
| 0x3708 | Seifer    | Hyperion        |
| 0x3714 | Edea      | None            |
| 0x3720 | Laguna    | Machine Gun     |
| 0x372C | Kiros     | Katal           |
| 0x3738 | Ward      | Harpoon         |

## Section Structure

| Offset | Length  | Description                                                                                                                                                                                                                  |
|--------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to weapon name                                                                                                                                                                                                        |
| 0x0002 | 1 byte  | Renzokuken finishers<br/><br/> 0x01 = Rough Divide<br/> 0x02 = Fated Circle<br/> 0x04 = Blasting Zone<br/> 0x08 = Lion Heart                                                                                                 |
| 0x0003 | 1 byte  | Unknown                                                                                                                                                                                                                      |
| 0x0004 | 1 byte  | Character ID<br/><br/> 0x00 - Squall<br/> 0x01 - Zell<br/> 0x02 - Irvine<br/> 0x03 - Quistis<br/> 0x04 - Rinoa<br/> 0x05 - Selphie<br/> 0x06 - Seifer<br/> 0x07 - Edea<br/> 0x08 - Laguna<br/> 0x09 - Kiros<br/> 0x0A - Ward |
| 0x0005 | 1 bytes | Attack Type                                                                                                                                                                                                                  |
| 0x0006 | 1 byte  | Attack Power                                                                                                                                                                                                                 |
| 0x0007 | 1 byte  | Attack Parameter                                                                                                                                                                                                             |
| 0x0008 | 1 byte  | STR Bonus                                                                                                                                                                                                                    |
| 0x0009 | 1 byte  | Weapon Tier                                                                                                                                                                                                                  |
| 0x000A | 1 byte  | Crit Bonus                                                                                                                                                                                                                   |
| 0x000B | 1 byte  | Melee Weapon?                                                                                                                                                                                                                |
