---
layout: default
title: Battle commands
nav_order: 2
parent: Kernel
permalink: /technical-reference/main/kernel/battle-commands/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x00E4 | 39       | 8 bytes      |

## Sections

| Offset | Ability    |
|--------|------------|
| 0x00E4 | Dummy      |
| 0x00EC | Attack     |
| 0x00F4 | Magic      |
| 0x00FC | GF         |
| 0x0104 | Item       |
| 0x010C | Renzokuken |
| 0x0114 | Draw       |
| 0x011C | Devour     |
| 0x0124 | Unnamed    |
| 0x012C | Cast       |
| 0x0134 | Stock      |
| 0x013C | Duel       |
| 0x0144 | Mug        |
| 0x014C | Unnamed    |
| 0x0154 | Shot       |
| 0x015C | Blue Magic |
| 0x0164 | Slot       |
| 0x016C | Fire Cross |
| 0x0174 | Sorcery    |
| 0x017C | Combine    |
| 0x0184 | Limit      |
| 0x018C | Limit      |
| 0x0194 | Limit      |
| 0x019C | Defend     |
| 0x01A4 | Mad Rush   |
| 0x01AC | Treatment  |
| 0x01B4 | Recovery   |
| 0x01BC | Revive     |
| 0x01C4 | Darkside   |
| 0x01CC | Card       |
| 0x01D4 | Doom       |
| 0x01DC | Kamikaze   |
| 0x01E4 | Absorb     |
| 0x01EC | LV Down    |
| 0x01F4 | LV Up      |
| 0x01FC | Single     |
| 0x0204 | Double     |
| 0x020C | Triple     |
| 0x0214 | Minimog    |

## Section Structure

| Offset | Length  | Description                                                                |
|--------|---------|----------------------------------------------------------------------------|
| 0x0000 | 2 bytes | Offset to ability name                                                     |
| 0x0002 | 2 bytes | Offset to ability description                                              |
| 0x0004 | 1 byte  | [Ability data ID](#ability-data-id-0x04)                                   |
| 0x0005 | 1 byte  | [Menu flags]({{site.baseurl}}/technical-reference/list/battle/#menu-flags) |
| 0x0006 | 1 byte  | [TargetInfo]({{site.baseurl}}/technical-reference/list/kernel#target-info) |
| 0x0007 | 1 byte  | Padding                                                                    |

### Ability data ID (0x04)

Index into [Command ability in battle](../command-abilities-in-battle/) (kernel section 11) supplying this command's fixed built-in effect (magic/effect id,
attack type, power, hit count, element, status, animation), via `computeCommandAction`.

`0xFF` = no fixed effect: the action is chosen at runtime from the player's selection (Attack, Magic, Draw, GF, Item all use `0xFF`). Fixed-effect commands (
Card, Devour, Defend, Mad Rush, Treatment, Recover, Revive, Doom, Absorb, LV Up/Down) carry a real index. At setup, if the linked entry's attack flags have the
Revive bit, the command is flagged as a revive.


