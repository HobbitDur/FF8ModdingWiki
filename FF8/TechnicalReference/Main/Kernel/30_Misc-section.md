---
layout: default
title: Misc
nav_order: 31
parent: Kernel
permalink: /technical-reference/main/kernel/misc/
---

# Misc Data Section

## General

| Offset | Sections | Section Size |
|--------|----------|--------------|
| 0x4CCC | 6        | Various      |


## Sections

| Offset | Ability                     | Length   |
|--------|-----------------------------|----------|
| 0x4CCC | Status Timers               | 14 bytes |
| 0x4CDA | ATB Speed Multiplier        | 1 byte   |
| 0x4CDB | Gilgamesh/Angelo summon interval ("Dead Timer") | 1 byte   |
| 0x4CDC | Status Limit Effects        | 32 bytes |
| 0x4CFC | Duel durations and initial sequences | 8 bytes  |
| 0x4D04 | Shot durations                 | 4 bytes  |


## Section Structure

The 14 status timers at 0x00–0x0D are loaded into the battle countdown as
`4 × (battleSpeed + 1) × value` ticks (`setupStatus2Timer`). Each idle battle frame,
`computeTimerStatus` subtracts `timer_speed_multiplier` from the timer — **2 by
default**, 3 under Haste, 1 under Slow, 0 under Stop — so at the ~15 fps battle rate about **30
ticks are consumed per second**. The real duration is therefore

```
seconds ≈ 4 × (battleSpeed + 1) × value / (2 × 15)
```

`battleSpeed` is the config **Battle Speed, `0` (fast) … `4` (slow)** — five settings, *not* a
0–255 value (`Battle_SetMaxAtbFromBattleSpeed`: `max_atb = 4000 × (battleSpeed + 1)`, the
same tick unit as the timers). At the midpoint (2) that is `value × 0.4` s; it scales from
`value × 0.2` s (fast, 0) to `value × 1.0` s (slow, 4). The ~15 fps rate is pinned by the Regen
tick, which heals every 30 frames (≈ 2 s). Timers only tick during **idle ATB time**, not during
action animations, so a real fight feels longer than this estimate; Haste makes them expire ~1.5×
faster and Slow ~2× slower.

| Offset | Length | Description                        |
|--------|--------|------------------------------------|
| 0x0000 | 1 byte | Sleep Timer                        |
| 0x0001 | 1 byte | Haste Timer                        |
| 0x0002 | 1 byte | Slow  Timer                        |
| 0x0003 | 1 byte | Stop Timer                         |
| 0x0004 | 1 byte | Regen Timer                        |
| 0x0005 | 1 byte | Protect Timer                      |
| 0x0006 | 1 byte | Shell Timer                        |
| 0x0007 | 1 byte | Reflect Timer                      |
| 0x0008 | 1 byte | Aura Timer                         |
| 0x0009 | 1 byte | Curse Timer                        |
| 0x000A | 1 byte | Doom Timer                         |
| 0x000B | 1 byte | Invincible Timer                   |
| 0x000C | 1 byte | Petrifying Timer                   |
| 0x000D | 1 byte | Float Timer                        |
| 0x000E | 1 byte | ATB Speed Multiplier — scales how fast **every** battler's ATB gauge fills: `cur_atb += 10 × this × (SPD+30) / 100`, applied **3× per rendered frame** (`Battle_TickAtbGaugesAndGfCountdown`, called from `isBattle_HUDdisplay`, itself called 3× per frame by `battle_cardgame_main_loop`). Retail value is **10**, not a %-of-normal multiplier despite the name. Because it ticks on the render loop rather than a fixed logic clock, real fill time depends on framerate — the PC port's well-known "ATB speeds up at high FPS" quirk. `max_atb = 4000 × (battleSpeed+1)` (`Battle_SetMaxAtbFromBattleSpeed`, same battleSpeed 0–4 as the status timers) |
| 0x000F | 1 byte | Gilgamesh/Angelo summon interval (a.k.a. "Dead Timer") — **not** a character-death countdown. Interval between the random Gilgamesh/Angelo/Phoenix auto-summon checks: `summonGilgaAngelStartFight` decrements it once per battle tick (called from `FFBattleDirector_battleLoop`); at 0 it rolls to summon Gilgamesh (12/255, if owned and not yet summoned this fight) or fire an Angelo/Phoenix auto-action, then reloads this value into `DEAD_TIMER_TO_SUMMON_GILGA`. Lower = checks more often |
The 32 status limit effects at 0x10–0x2F are how much each active status contributes to a
character's crisis/Limit-Break gauge, read by `Battle_ComputeCrisisLevelAndLimitFlag`. Every
active status (across both Status 1 and Status 2) adds its byte here into one running total
each frame:

```
crisis = (10*(statusSum + 4*(5*deadAllies + 40)) - 10*crisisLevelHPMultiplier*curHP/maxHP)
         / (rand(0..255) + 160) - 4          [clamped 0-4]
```

Higher values push the crisis level (and so Limit Break availability) up faster; `0` means
that status doesn't affect it at all. There's no term that lowers crisis level — every listed
status only ever pushes it up, which is why Death/Poison/etc. all have a value here despite
being harmful.

| 0x0010 | 1 byte | Death Limit Effect                 |
| 0x0011 | 1 byte | Poison Limit Effect                |
| 0x0012 | 1 byte | Petrify Limit Effect               |
| 0x0013 | 1 byte | Darkness Limit Effect              |
| 0x0014 | 1 byte | Silence Limit Effect               |
| 0x0015 | 1 byte | Berserk Limit Effect               |
| 0x0016 | 1 byte | Zombie Limit Effect                |
| 0x0017 | 1 byte | Limit effect for the unused Status-1 bit 7 slot |
| 0x0018 | 1 byte | Sleep Limit Effect                 |
| 0x0019 | 1 byte | Haste Limit Effect                 |
| 0x001A | 1 byte | Slow Limit Effect                  |
| 0x001B | 1 byte | Stop Limit Effect                  |
| 0x001C | 1 byte | Regen Limit Effect                 |
| 0x001D | 1 byte | Protect Limit Effect               |
| 0x001E | 1 byte | Shell Limit Effect                 |
| 0x001F | 1 byte | Reflect Limit Effect               |
| 0x0020 | 1 byte | Aura Limit Effect                  |
| 0x0021 | 1 byte | Curse Limit Effect                 |
| 0x0022 | 1 byte | Doom Limit Effect                  |
| 0x0023 | 1 byte | Invincible Limit Effect            |
| 0x0024 | 1 byte | Petrifying Limit Effect            |
| 0x0025 | 1 byte | Float Limit Effect                 |
| 0x0026 | 1 byte | Confusion Limit Effect             |
| 0x0027 | 1 byte | Drain Limit Effect                 |
| 0x0028 | 1 byte | Eject Limit Effect                 |
| 0x0029 | 1 byte | Double Limit Effect                |
| 0x002A | 1 byte | Triple Limit Effect                |
| 0x002B | 1 byte | Defend Limit Effect                |
| 0x002C | 1 byte | Immune Physical attack limit effect |
| 0x002D | 1 byte | Immune Magic attack limit effect    |
| 0x002E | 1 byte | Charged Limit Effect               |
| 0x002F | 1 byte | Back Attack Limit Effect           |
| 0x0030 | 1 byte | Duel duration CL1 |
| 0x0031 | 1 byte | Duel initial sequence CL1 |
| 0x0032 | 1 byte | Duel duration CL2 |
| 0x0033 | 1 byte | Duel initial sequence CL2 |
| 0x0034 | 1 byte | Duel duration CL3 |
| 0x0035 | 1 byte | Duel initial sequence CL3 |
| 0x0036 | 1 byte | Duel duration CL4 |
| 0x0037 | 1 byte | Duel initial sequence CL4 |
| 0x0038 | 1 byte | Shot duration CL1 |
| 0x0039 | 1 byte | Shot duration CL2 |
| 0x003A | 1 byte | Shot duration CL3 |
| 0x003B | 1 byte | Shot duration CL4 |

## Duel / Shot crisis-level fields (0x30–0x3B)

These drive **Zell's "Duel"** and **Irvine's "Shot"**. The native crisis level is
**1–4** while a Limit Break is available; **0** means no Limit Break.

- **Duel duration (CL1–4)** — `linkedToZellDuel` (`0x48E5A0`, read at `0x48E5C2`)
  passes `K_MISC[0x2E + 2 * crisis_level]` to `BattleMenu_ZellDuel_Open` as the
  input-window duration. This selects offsets **0x30, 0x32, 0x34, 0x36**.
- **Duel initial sequence (CL1–4)** — `computeCommandAction` (`0x48DF0D`)
  assigns `K_MISC[0x2F + 2 * crisis_level]` to `ZELL_DUEL_CURRENT_SEQ`, which then
  indexes the [Duel move graph](../duel-parameters/) (section 24). This selects
  offsets **0x31, 0x33, 0x35, 0x37**. It is a move-graph index, not an actor's Seq anim.
- **Shot duration (CL1–4)** — offsets **0x38–0x3B** select Irvine's shooting-window duration.

Duration bytes are displayed as **raw / 15 seconds** at normal game speed: the game
loads `4 * raw` countdown ticks and displays 60 ticks per second. The countdown can
pause while its input window is inactive. These are distinct from status-effect timers.

The corresponding IDA members are `duel_duration_crisis_1` … `_4`,
`duel_initial_sequence_crisis_1` … `_4`, and `shot_duration_crisis_1` … `_4`.

## Function addresses

| Function | Address |
|---|---|
| `setupStatus2Timer` | 0x4832f0 |
| `Battle_SetMaxAtbFromBattleSpeed` | 0x484490 |
| `Battle_TickAtbGaugesAndGfCountdown` | 0x4842b0 |
| `computeTimerStatus` | 0x483470 |