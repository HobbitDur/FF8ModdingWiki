---
layout: default
title: Rinoa commands
nav_order: 26
parent: Kernel
permalink: /technical-reference/main/kernel/rinoa-commands/
---

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4A5C | 2        | 8 bytes      |

## Sections

| Offset | Ability    |
|--------|------------|
| 0x4A5C | Angelo     |
| 0x4A64 | Angel Wing |

## Section Structure

| Offset | Length  | Description                   |
|--------|---------|-------------------------------|
| 0x0000 | 2 bytes | Offset to ability name        |
| 0x0002 | 2 bytes | Offset to ability description |
| 0x0004 | 1 byte  | [Status window flags]({{site.baseurl}}/technical-reference/list/battle/#status-window-flags) — see [The limit-menu record](#the-limit-menu-record) |
| 0x0005 | 1 byte  | [TargetInfo]({{site.baseurl}}/technical-reference/list/kernel#target-info) |
| 0x0006 | 1 byte  | Unused — nothing reads it (IDA: 0 xrefs to the struct member); `0xFF` in both vanilla entries |
| 0x0007 | 1 byte  | Padding (unused; IDA: 0 xrefs) |

## The limit-menu record

`BuildLimitCommandMenu` (`0x48CCE0`) fills a 16-entry array of **5-byte records** at
`F_CHAR_DATA[slot] + 0x32`, one record per selectable limit entry, and every character's limit
list goes through the same builder and the same layout:

| Byte | Meaning |
|------|---------|
| +0 | entry id (index into the character's own limit table) |
| +1 | quantity / availability (`1` for Quistis and Rinoa, the ammo count for Shot) |
| +2 | Status window flags |
| +3 | TargetInfo |
| +4 | UI flags — `0x01` set when the entry's Attack flags have `0x80`, `0x02` out of stock (row greyed), `0x10` hidden |

Where `+2` comes from, per character:

| Character | Source of byte `+2` |
|-----------|---------------------|
| Quistis (Blue magic) | `K_BLUE_MAGIC[i].statusWindowFlags` — [Blue magic](../blue-magic/) `0x0008` |
| Seifer / Edea (Temp-char limits) | `K_TEMP_CHAR[i].statusWindowFlags` — [Temporary character limit breaks](../temporary-characters-limit-breaks/) `0x0009` |
| Irvine (Shot) | hardcoded `0x80` |
| **Rinoa (Combine)** | **this section, `0x0004`** — written by `BuildLimitMenuEntry_Rinoa` (`0x48CFB0`) |

The consumer is the same for all of them: `BattleMenu_ListWindow_Update` state 8 calls
`sub_4AB4F0(ctx, rec[3] /* TargetInfo */, rec[2] /* Status window */, rec[4], …)`, and
`sub_4AB190` stores byte `+2` in the target-cursor context at `+36`, which is what
`sub_4B1E70` reads to open the ally HP/status panel. So `0x0004` is the Status window byte,
not a separate flag set.

Both vanilla entries hold `0xA0`: bit `0x80` (hide the ally status panel — correct for Angelo
Cannon and Angel Wing, which target enemies) plus an `0x20` bit that no code reads and that no
other kernel entry sets anywhere.
