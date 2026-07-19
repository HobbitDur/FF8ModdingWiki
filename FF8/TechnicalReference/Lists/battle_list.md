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

## Menu flags

Byte 0x05 of a [Battle command]({{site.baseurl}}/technical-reference/main/kernel/battle-commands/) — a battle-menu/UI descriptor, purely UI and never read by battle logic. Copied at battle setup into the character's per-slot command data (`ResetAndParseBattleAndFieldCharacter` / `linkedStockFieldCharData`) and consumed by `BattleMenu_ExecuteSelectedCommand` (0x4BC770) and the target-selection cursor. More on the surrounding battle UI: [Battle UI (HUD and command menu)]({{site.baseurl}}/technical-reference/battle/battle-ui/).

| Bits | Meaning |
|------|---------|
| 0x80 | Hide the ally status window while the target cursor is up. When clear (only Recover `0x20`, Revive `0x20`, Treatment `0x60`), targeting an ally opens the party HP/status panel |
| 0x40 | Status-window detail mode — the panel lists status ailments instead of HP digits (only meaningful when 0x80 is clear; used by Treatment) |
| 0x20 | Instant command — no submenu; confirming the command goes straight to target selection (Attack, Devour, Defend, Card, Doom, ...) |
| 0x1F | Submenu type, used only when 0x20 is clear (table below) |

Examples from the retail kernel: Attack = `0xA0` (instant, no ally panel), Magic = `0x80` (submenu 0), Draw = `0x83` (submenu 3), Combine = `0x88` (submenu 8), Recover/Revive = `0x20` (instant, ally HP panel shown), Treatment = `0x60` (instant, ailment panel shown).

### Submenu types (bits 0x1F)

The last four route through a shared "4-row special list" helper, `BattleMenu_OpenSpecialListWindow` (0x4C7D00), each with its own list-id.

| Id | Submenu | Opener function | Address |
|----|---------|------------------|---------|
| 0 | Magic list | `BattleMenu_OpenMagicWindow` | 0x4C8840 |
| 1 | GF list | `BattleMenu_OpenGFWindow` | 0x4C8280 |
| 2 | Item list | `BattleMenu_OpenItemWindow` (`BattleMenu_OpenItemWindow_Alt` when opened from a non-Item command) | 0x4C87A0 / 0x4C8550 |
| 3 | Draw window | `BattleMenu_OpenDrawWindow` | 0x4ADD10 |
| 4 | Shot ammo list | `BattleMenu_OpenShotWindow` | 0x4C8220 |
| 5 | Slot | `BattleMenu_OpenSlotWindow` | 0x4C7920 |
| 6 | Blue Magic list | `BattleMenu_OpenBlueMagicWindow` | 0x4C81C0 |
| 7 | Limit list (Fire Cross / Sorcery / Limit) | `BattleMenu_OpenLimitListWindow` | 0x4C8190 |
| 8 | Combine | `BattleMenu_OpenCombineWindow` | 0x4C81F0 |
| any other | none — falls through straight to target selection | `BattleMenu_OpenTargetSelection` | 0x4C7030 |

Magic list id 0 also carries a mode argument read from the command itself: Double opens it in ×2 mode, Triple in ×3 mode, everything else (including the plain Magic command) in ×1 mode.

### Status window flags

Entries picked from a **submenu** carry their own copy of bits 0x80/0x40 (the ally-status-window pair above): [Magic]({{site.baseurl}}/technical-reference/main/kernel/magic/) byte 0x09, [Junctionable GF]({{site.baseurl}}/technical-reference/main/kernel/junctionable-gfs/) byte 0x08, [Blue Magic]({{site.baseurl}}/technical-reference/main/kernel/blue-magic/) byte 0x08, [Shot]({{site.baseurl}}/technical-reference/main/kernel/shot-irvine-limit-breaks/) byte 0x09 and [Temporary-character limit breaks]({{site.baseurl}}/technical-reference/main/kernel/temporary-characters-limit-breaks/) byte 0x09 (the last two were long documented as the "inert high byte" of a 2-byte animation value — `Battle_applyDamage` indeed ignores it, but `BuildLimitCommandMenu` reads it into the limit list entry's status-window slot). When the player confirms a spell/GF/limit in the list, that byte is passed to the target cursor in the same slot a command's Menu flags byte goes (confirm path: list entry → target-cursor struct +36 → `sub_4B1E70` → `BattleHUD_StatusWinOpenRequest`/`DetailMode`; the low 6 bits are dead on this path).

Retail values are deliberate design, matching each spell's purpose:

| Value | Meaning | Retail users |
|-------|---------|--------------|
| 0x00  | Show the party HP panel while targeting | Cure, Cura, Curaga, Life, Full-life, Regen |
| 0x40  | Show the panel in ailment-detail mode (cycles each character's active statuses) | Esuna, Dispel, Protect, Shell, Reflect, Aura, Double, Triple, Haste, Float |
| 0x80  | Panel hidden | All offensive spells; all 16 GFs |
| 0xC0  | Panel hidden (bit 0x40 inert while 0x80 is set) | Slow, Stop, Blind, Confuse, Sleep, Silence |

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






