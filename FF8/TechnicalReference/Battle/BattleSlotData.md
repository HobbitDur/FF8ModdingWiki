---
layout: default
parent: Battle
title: Battle Slot Data
permalink: /technical-reference/battle/battle-slot-data/
---

`BATTLE_SLOT_DATA` is the central per-slot runtime structure used by ATB, status, damage, targeting, command menus and enemy AI.

1. TOC
{:toc}

## Slot array

| Field | Value |
|-------|-------|
| Base address | `0x1D27B10` |
| Stride | `0xD0` bytes |
| Count | 11 slots (`0..10`) |

| Slot range | Use |
|------------|-----|
| `0..2` | Party members |
| `3..7` | Enemies (up to 5 active) |
| `8..10` | GF-related runtime slots |

Slot addresses are computed as:

```
slot_address = 0x1D27B10 + slot_id * 0xD0
```

Example: slot 3 is `0x1D27B10 + 3 * 0xD0 = 0x1D27D80`.

## High-signal offsets

| Offset | Size | Field | Notes / primary writer |
|--------|------|-------|------------------------|
| `+0x00` | 4 | `monster_info_section` | Enemy-only pointer (`0x48BBD0`) |
| `+0x04` | 4 | `monster_ai_section` | Enemy-only pointer used by the AI VM |
| `+0x08` | 4 | `status_2` | Authoritative status_2 (`0x493840`) |
| `+0x0C` | 4 | `status_2_copy` | UI / mirror copy (`0x47E2D0`) |
| `+0x10` | 4 | `max_atb` | Initialized by `0x484490` |
| `+0x14` | 4 | `cur_atb` | Updated by `0x4842B0` |
| `+0x18` | 4 | `current_hp` | Written by `Battle_ApplyDamageOrHeal` (`0x494410`) |
| `+0x1C` | 4 | `max_hp` | Initialized by party/enemy setup |
| `+0x44` | 16 | `elem_def[8]` | `int16[8]`; party from junctions, enemy from `.dat` info |
| `+0x54` | 32 | `timer[16]` | Status timers |
| `+0x7C` | 2 | `flag_data` | Active/ready state bitfield |
| `+0x7E` | 2 | `immunity_flag_data` | Gravity immunity and related flags |
| `+0x80` | 2 | `status_1` | Authoritative status_1 (`0x493840`) |
| `+0x82` | 2 | `status_1_copy` | UI / mirror copy (`0x47E2D0`) |
| `+0x84` | 2 | `target_info_mask` | Also used in GF shield HP tracking |
| `+0x86` | 2 | `hit_status_1` | Party init (`0x48B310`) |
| `+0x90` | 0x28 | `mental_res` | Byte-addressed mental resistances |
| `+0xBB` | 1 | `com_file_id` | `0xFF` = empty slot |
| `+0xBC` | 1 | `level` | Runtime battle level |
| `+0xC1` | 1 | `spd` | Authoritative speed used by ATB |
| `+0xCA` | 1 | `crisis_level` | Limit Break crisis level (`0x4941F0`) |

## Status fields

`status_1` is a 16-bit field at `+0x80`.

| Bit | Mask | Status | Evidence |
|-----|------|--------|----------|
| 0 | `0x0001` | Death / KO | Set by `Battle_ApplyDamageOrHeal` when HP reaches 0 |
| 2 | `0x0004` | Petrify | Tested with Death as `status_1 & 5` |
| 6 | `0x0040` | Zombie | Set by enemy info initialization when the monster has the zombie flag |

`status_2` is a 32-bit field at `+0x08`.

| Bit | Mask | Status | Evidence |
|-----|------|--------|----------|
| 0 | `0x00000001` | Sleep | ATB and arbitration gating |
| 1 | `0x00000002` | Haste | ATB increment base becomes 15 |
| 2 | `0x00000004` | Slow | ATB increment base becomes 5 |
| 3 | `0x00000008` | Stop | Blocks readiness and is handled during damage/status application |
| 5 | `0x00000020` | Protect | Auto-status init from party abilities |
| 6 | `0x00000040` | Shell | Auto-status init from party abilities |
| 7 | `0x00000080` | Reflect | Auto-status init from party abilities |
| 14 | `0x00004000` | Confuse-like | Target eligibility mask |
| 16 | `0x00010000` | Eject | Checked and cleared by status commit code |
| 30 | `0x40000000` | Has Magic | Set during party init |
| 31 | `0x80000000` | GF Summoning | Signed status check in GF summon cleanup |

## Composite masks

| Mask | Usage |
|------|-------|
| `status_1 & 0x05` | Death or Petrify |
| `status_2 & 0x0009` | Sleep or Stop |
| `status_2 & 0x4009` | Sleep, Stop or confuse-like target rejection |
| `status_2 & 0x180800` | Invulnerability flags; exact bit identities need more work |
| `status_2 & 0x2004009` | Extended target ineligibility |
| `status_1 & 0x25` | Death, Petrify or Berserk |

## ATB update

`BattleATB_TickAndReady` (`0x4842B0`) is called every active battle frame from `BattleUI_InputPollAndMenuState` (`0x4A8772`).

Per slot, the ATB increment is:

```
base = 10
base = 15 if status_2 & 0x2  (Haste)
base = 5  if status_2 & 0x4  (Slow)

cur_atb += base * K_MISC.atb_speed_multiplier * (spd + 30) / 100
```

A slot is processed only when it is active, alive, not petrified, not asleep/stopped and not already in a ready state. When `cur_atb >= max_atb`, `cur_atb` is clamped and the slot transitions either to an auto-command path or normal command menu readiness.

| Condition | Result |
|-----------|--------|
| `status_1 & 0x20` or `status_2 & 0x2004000` | Auto-command path via `Battle_ProcessAutoCommand` |
| Otherwise | Normal menu path via `BattleUI_EnqueueCommand(slot, 17, 128, 0)` |

For party slots, the ATB values are mirrored to `BATTLE_ATB_UI_MIRROR` (`0x1CFF180`) for gauge display.

## flag_data notes

`flag_data` is heavily used by active/ready state logic. Confirmed initialization values:

| Context | Value |
|---------|-------|
| Party init (`0x48B5F0`) | `*(_DWORD *)&slot.flag_data = 0x8801` |
| Enemy init (`0x48BBD0`) | `*(_DWORD *)&slot.flag_data = 0x0011` |

Note: treat `flag_data` as an opaque bitfield unless the exact writer/reader has been confirmed.
