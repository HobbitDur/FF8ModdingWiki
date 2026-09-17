---
layout: default
title: Devour List
parent: List
permalink: /technical-reference/list/devour-list/
---

## Devour Effects

| ID   | Name                    |
|------|-------------------------|
| 0    | HP Recovery             |
| 1    | Full HP Recovery        |
| 2    | HP & Status Rec.        |
| 3    | Damage & Zombie         |
| 4    | Damage(m) & Poison      |
| 5    | Damage & Dark           |
| 6    | Damage(s) & Poison      |
| 7    | Damage                  |
| 8    | Dmg & Random Status     |
| 9    | No Change               |
| 10   | Strength +1             |
| 11   | Defense +1              |
| 12   | Magic +1                |
| 13   | Spirit +1               |
| 14   | Speed +1                |
| 15   | Max HP +10              |
| 255  | Immune                  |

## The other devour byte

The table above is the **effect ID** (monster bytes 251-253, one per level tier), which drives everything a player sees. A monster also carries a
**devour category** in byte 255, and the two are easy to confuse:

| | Effect ID (bytes 251-253) | Devour category (byte 255) |
|---|---|---|
| What it selects | the row of the table above: statuses, heal/damage amounts, the permanent stat bonuses | a classification of the monster (0 prime beast, 3 plant, 7 machine, 8 inedible...) |
| What the player sees | everything | nothing |
| How the engine uses it | the kernel devour table | `computeDevour` stores it and `Battle_DamageGettingRelated` returns it as the devour hit's **damage** — 0-7 points on a monster that is being ejected anyway, and 8 on a failure, hidden behind the miss flag |

So the category is read, but its only vanilla effect is invisible. The value table and the reasoning behind it are in
[Informations & stats]({{site.baseurl}}/technical-reference/battle/model-sections/information-stats/#byte-255-devour-category).
