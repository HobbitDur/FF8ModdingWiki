---
layout: default
title: Support modules and engine services
parent: Main
permalink: /technical-reference/main/support-modules/
---

1. TOC
{:toc}

# Support modules and engine services

This page collects the small modules and one-time services around the main game modules: engine initialization, the CD-check module, new-game/load state setup, and the movie path. The module system itself is described on [Engine startup and main loop]({{ site.baseurl }}/technical-reference/main/engine-startup-and-main-loop/).

## Engine initialization (PubIntroInit)

`PubIntroInit` is the engine `init` callback, run once from the window-creation path:

1. Reads the sound, MIDI and graphics device GUIDs and options from the registry.
2. Creates the single-instance mutex — if the mutex already exists (error 183), the game exits immediately; this is why a second FF8 instance closes silently.
3. Initializes the renderer (`init_graphics`), the emulated PSX VRAM buffer, DirectInput (loading user key bindings or the defaults), DirectSound and the music system (paths from the registry).

`pubintro_cleanup` (the `cleanup` callback) tears all of this down at exit.

## CD-check module

Registered whenever the disc number stored in the savemap does not match the detected disc (checked by the module handler on every field entry, and used on disc-change field jumps). The module preloads `wm2field.tbl`, then `cdcheck_main_loop` runs `InsertDiscSequence` each frame — the "Please insert disc N" screen — until the right disc is present, then switches back to the module handler.

On PC there is no actual CD query: `InsertDiscSequence` probes for the marker files **`DISK1` … `DISK4`** (game-root relative) with a plain file open; the index of the first file found is the "inserted disc". The screen itself is a state machine: fade out → wait until the input flags release → load `ff8\data\eng\disc` (the insert-disc image, drawn 580×406 at 30,37) → fade in → poll the DISK files every 300 frames → fade out and return once `DISKn` matches the required disc. This is why the Steam/2013 repacks simply ship all four DISK files — the check then always passes instantly.

## SeeD salary system

`Field_PaySeedSalary` (called by the field script VM every 0x6000 step-units, see [Field module runtime]({{ site.baseurl }}/technical-reference/field/field-module-runtime/)) implements the salary and the famous rank decay:

* `rank_points += (total_kills − kills_at_last_payment − 10)` — the fixed −10 is the decay per pay period; killing enemies offsets it. Clamped to [100, 3100] (rank 1 to rank 31/A).
* Salary = `SEED_SALARY_TABLE[rank_points / 100] × 10` gil, added to party gil (cap 99,999,999).
* `miscFlag` bits 0x10/0x1000 suppress the salary alert popup and its two sounds (0x5B/0x5C).

The hardcoded table (`SEED_SALARY_TABLE`, 32 word entries — value × 10 = gil):

| Rank | Salary | Rank | Salary | Rank | Salary | Rank | Salary |
|------|--------|------|--------|------|--------|------|--------|
| 1 | 500 | 9 | 7000 | 17 | 13500 | 25 | 17500 |
| 2 | 1000 | 10 | 8000 | 18 | 14000 | 26 | 18000 |
| 3 | 1500 | 11 | 9000 | 19 | 14500 | 27 | 18500 |
| 4 | 2000 | 12 | 10000 | 20 | 15000 | 28 | 19000 |
| 5 | 3000 | 13 | 11000 | 21 | 15500 | 29 | 19500 |
| 6 | 4000 | 14 | 12000 | 22 | 16000 | 30 | 20000 |
| 7 | 5000 | 15 | 12500 | 23 | 16500 | 31 (A) | 30000 |
| 8 | 6000 | 16 | 13000 | 24 | 17000 | | |

The table sits directly after the field opcode handler table, at `0xB8E474`.

## New game / load setup (newgame_startgame)

`newgame_startgame(is_new_game)` prepares the savemap before the module handler starts:

For a **new game** it clears the savemap variable block and writes the defaults:
* the "FF-8" magic text at the start of the block;
* current disc = 1;
* two world-map draw-point bytes set to 127 and one draw-state byte to 5;
* `miscFlag` bits 3 and 4 set — bit 3 is "SeeD salary disabled", so a new game starts without a salary until the field scripts enable it;
* SeeD rank points = 500.

For **both paths** (new game and load) it then:
* resets the per-slot timer array and draw-point respawn state;
* clears the queued-music fields (set to −1);
* restores the encounter flags from the savemap;
* restores `MAP_SEAL` only when `miscFlag` bit 0x800 is set;
* restores the current car-rental state and current disc;
* applies the salary-enabled state (`setSalaryActive(!(miscFlag & 8))`);
* registers two menu callbacks used by the pause menu.

## Movie playback path

Movies do not use a dedicated module: the `START_MOVIE`/`MOVIE` globals switch the active module loop into a Bink update path (`update_movie_sample_bink`) — visible in `FFStartModule` (intro movies) and in the field module loop (in-field FMVs, where the field camera follows the movie camera and the `.msk` depth mask applies). The `is_sleeping`/`UpdateRateRelated` pair in the module shells throttles rendering while a movie decodes.

## Frame-rate summary

Logic rates set by each module's init (`engine_set_time`):

| Module | Rate |
|--------|------|
| Intro / title / menus / victory screens | 60 fps (frame limiter in the loop) |
| Field | 30.5 fps |
| World map | 30.5 fps |
| Battle | 15 fps |
| Card game | 60 fps |

## Address table

| Name | Address | Description |
|------|---------|-------------|
| `PubIntroInit` | 0x401890 | Engine init: registry, mutex, gfx, input, sound, music |
| `pubintro_cleanup` | 0x401A00 | Engine cleanup |
| `cdcheck_init` | 0x52DC00 | CD-check module enter_main |
| `cdcheck_main_loop` | 0x52DCF0 | Hosts InsertDiscSequence until correct disc |
| `cdcheck_exit_sub_52DCA0` | 0x52DCA0 | CD-check module exit |
| `InsertDiscSequence` | 0x52F9E0 | "Insert disc" screen + DISK1-DISK4 file polling |
| `Field_PaySeedSalary` | 0x52B140 | Salary payment + rank decay (−10/period) |
| `SEED_SALARY_TABLE` | 0xB8E474 | 32 salary words (× 10 = gil) |
| `newgame_startgame` | 0x52CA90 | Savemap defaults / restore on new game or load |
| `setSalaryActive` | 0x4B86C0 | Enables/disables the SeeD salary system |
| `MAP_SEAL` | 0x1CFF6E8 | Sealed-abilities state (restored when miscFlag bit 0x800) |
| `update_movie_sample_bink` | 0x55A620 | Bink movie frame update |
| `main_init_sub_470690` | 0x470690 | Module-handler enter_main (clears draw flag) |
| `main_exit_sub_4706A0` | 0x4706A0 | Module-handler exit_main |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
