---
layout: default
title: Battle items
nav_order: 9
parent: Kernel
permalink: /technical-reference/main/kernel/battle-items/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x3930 | 33       | 24 bytes     |

## Sections

| Offset | Ability        |
|--------|----------------|
| 0x3930 | Dummy/Unused   |
| 0x3948 | Potion         |
| 0x3960 | Potion+        |
| 0x3978 | Hi-Potion      |
| 0x3990 | Hi-Potion+     |
| 0x39A8 | X-Potion       |
| 0x39C0 | Mega-Potion    |
| 0x39D8 | Phoenix Down   |
| 0x39F0 | Mega Phoenix   |
| 0x3A08 | Elixir         |
| 0x3A20 | Megalixir      |
| 0x3A38 | Antidote       |
| 0x3A50 | Soft           |
| 0x3A68 | Eye Drops      |
| 0x3A80 | Echo Screen    |
| 0x3A98 | Holy Water     |
| 0x3AB0 | Remedy         |
| 0x3AC8 | Remedy+        |
| 0x3AE0 | Hero-trial     |
| 0x3AF8 | Hero           |
| 0x3B10 | Holy War-trial |
| 0x3B28 | Holy War       |
| 0x3B40 | Shell Stone    |
| 0x3B58 | Protect Stone  |
| 0x3B70 | Aura Stone     |
| 0x3B88 | Death Stone    |
| 0x3BA0 | Holy Stone     |
| 0x3BB8 | Flare Stone    |
| 0x3BD0 | Meteor Stone   |
| 0x3BE8 | Ultima Stone   |
| 0x3C00 | Gysahl Greens  |
| 0x3C18 | Phoenix Pinion |
| 0x3C30 | Friendship     |

## Section Structure

| Offset | Length  | Description                 |
|--------|---------|-----------------------------|
| 0x0000 | 2 bytes | Offset to item  name        |
| 0x0002 | 2 bytes | Offset to item  description |
| 0x0004 | 2 bytes | Magic ID                    |
| 0x0006 | 1 byte  | Attack type                 |
| 0x0007 | 1 byte  | Attack power                |
| 0x0008 | 1 byte  | Category (unused) — not a bitfield; 3 mutually-exclusive category codes that never combine: `0x00` pure curatives (Potion..Megalixir), `0x40` status-cure/support items (Antidote, Remedy, Hero, Holy War, Shell/Protect/Aura Stone), `0x80` offensive/special items (the 6 elemental stones, Gysahl Greens, Phoenix Pinion, Friendship). Copied into the runtime battle-item inventory by `updateBattleItemData`, but nothing reads that copy back and nothing reads this kernel byte directly either (item-use AI keys on item id, the item-menu draw path only uses the selectability byte, `computeCommandAction` resolves item effects from `attackType`/`specialActionID`) — real, deliberate category data that is inert in the shipped PC engine |
| 0x0009 | 1 byte  | Target info                 |
| 0x000A | 1 byte  | Attack flags + selectability (IDA `attackFlagsAndSelectability`) — a dual-purpose byte. In battle it is the item's **Attack flags**: `Battle_applyDamage` loads it into `ATTACK_FLAG` (low 2 bits = damage-type pair: retail curatives use `2` = Item/Medicine so MedData doubles their healing, offensive stones use `1` = Magical so Shell halves them; bit `0x80` also gates the revive path). In the menu, `updateBattleItemData` reads the same byte: **bit 0x80 set → item selectable/usable in battle**; **bit 0x20 clear → entry dimmed**. Retail values: curatives `0xE2`, Hero/Holy War/Gysahl-type `0xA2`, offensive stones `0xA1` |
| 0x000B | 1 byte  | Target hit animation — `Battle_applyDamage` loads it into `HIT_TYPE_TARGET_ANIMATION_TO_PLAY` (the flags/animation byte order is swapped vs. Magic, like Duel/Rinoa-2). Retail: `0` for curative/support items, `5` for the five offensive stones — same convention as Magic 0x06 |
| 0x000C | 1 bytes | Padding — `0x00` for all 33 items; its only xref is pointer arithmetic in `getTextBattleItem`'s non-battle-item branch, not a semantic read |
| 0x000D | 1 byte  | Status attack accuracy       |
| 0x000E | 2 bytes | [Status 1]({{site.baseurl}}/technical-reference/list/status-flags#status-1) (statuses 0-15)    |
| 0x0010 | 4 bytes | [Status 2]({{site.baseurl}}/technical-reference/list/status-flags#status-2) (statuses 16-47)   |
| 0x0014 | 1 byte  | Hit rate — physical accuracy vs. the target's Evade (`Battle_applyDamage` → `HIT_ATTACK_HITPERCENT`, the Hit%-stat slot); `0xFF` = always hits |
| 0x0015 | 1 byte  | Random-select flag — bit 0 marks the item eligible for random battle-item selection (`sub_483CA0` picks a random inventory item with this bit set) |
| 0x0016 | 1 bytes | Hit Count                   |
| 0x0017 | 1 bytes | Element                     |
