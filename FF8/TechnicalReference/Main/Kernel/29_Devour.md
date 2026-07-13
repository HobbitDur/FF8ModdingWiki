---
layout: default
title: Devour
nav_order: 30
parent: Kernel
permalink: /technical-reference/main/kernel/devour/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4C0C | 16       | 12 bytes     |

## Sections

| Offset | Ability                     |
|--------|-----------------------------|
| 0x4C0C | Tastes okay...              |
| 0x4C18 | Delicious!!!                |
| 0x4C24 | Refreshing!                 |
| 0x4C30 | It`s rotten...              |
| 0x4C3C | Tastes funny...             |
| 0x4C48 | Can`t see anything          |
| 0x4C54 | Tastes awful!!!             |
| 0x4C60 | Barf...Bwahhh!!!            |
| 0x4C6C | Shouldn`t have...eaten...it |
| 0x4C78 | No good!                    |
| 0x4C84 | Gained strength             |
| 0x4C90 | Feel healthier              |
| 0x4C9C | Clear head!                 |
| 0x4CA8 | Increased morale!           |
| 0x4CB4 | Light on my feet!           |
| 0x4CC0 | All systems go!             |		 

## Section Structure

| Offset | Length  | Description                                                                                                                                   |
|--------|---------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to devour description                                                                                                                  |
| 0x0002 | 1 byte  | Damage or heal HP and Status _<br/><br/> 0x1E - Cure   <br/> 0x1F - Damage_                                                                   |
| 0x0003 | 1 byte  | HP Heal/DMG Quantity Flag _<br/><br/> 0x00 - 0% <br/> 0x01 - 6.25% <br/> 0x02 - 12.50% <br/> 0x04 - 25%<br/> 0x08 - 50%<br/> 0x10 - 100%_     |
| 0x0004 | 4 bytes | [Status 2]({{site.baseurl}}/technical-reference/list/status-flags#status-2) (statuses 16-47)                                                                                                                     |
| 0x0008 | 2 bytes | [Status 1]({{site.baseurl}}/technical-reference/list/status-flags#status-1) (statuses 0-15)                                                                                                                      |
| 0x000A | 1 byte  | Raised Stat Flag _<br/><br/> 0x00 - None <br/> 0x01 - STR <br/> 0x02 - VIT <br/> 0x04 - MAG<br/> 0x08 - SPR<br/> 0x10 - SPD<br/> 0x20 - LUCK_ |
| 0x000B | 1 byte  | Raised Stat HP Quantity                                                                                                                       |