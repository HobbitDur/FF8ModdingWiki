---
layout: default
parent: Battle
title: Battle UI Timing and Input Sampling
permalink: /technical-reference/battle/battle-ui-timing-and-input/
---

This page documents how the PC 2000 battle module paces its frames, how the battle menu (HUD, command windows, Boost, Zell's Duel) is ticked, and how controller/keyboard input flows into the menu code. It explains why the battle menu feels locked to 15 fps on PC — input mashing for GF Boost and Zell's Duel registers far fewer presses than on PSX — and lists concrete patch points for fixing it.

1. TOC
{:toc}

## Summary

The PC battle module is frame-locked to **15.5 fps**. To preserve PSX pacing, the battle UI logic is ticked **4 times per rendered frame** (≈ 60 ticks/s), so all UI timers (ATB display, Zell's Duel countdown, Boost phases, text speed) run at the intended real-time speed. However, the hardware input poll (DirectInput keyboard/joystick) runs **once per rendered frame**, and the 4 UI ticks execute back-to-back within the same frame — they all see the same input snapshot. The result:

- Button **press edges** can only be produced on 1 of the 4 UI ticks → effective **15 Hz input sampling**.
- A press+release that fits inside one 64.5 ms frame window is **lost entirely**; two presses inside one window **merge into one**.
- Timers keep running at 60 ticks/s while inputs arrive at 15 Hz, so timed minigames (Zell's Duel, GF Boost) offer roughly **4× fewer input opportunities** than the same code pacing allows on PSX, where the pad is refreshed every vsync.

## Module frame rates

`Time_SetTargetFrameRate` converts a target fps into `FRAME_PERIOD_TICKS`; `Time_WaitNextFrame` sleeps at the end of each module loop iteration to hold the target (with a 2-frame overshoot amortization scheme). Each module sets its own rate at init:

| Module | Init function | Target fps | Constant pushed (double hi-dword) |
|--------|--------------|-----------|------------------------------------|
| Battle | `FFBattleInitSystem` | 15.5 | `0x402F0000` at `0x47CE3F` |
| Card game (same director) | `FFBattleInitSystem` | 60.5 | `0x404E4000` at `0x47CE38` |
| Field | `field_init_sub_46FD70` | 30.5 | `0x403E8000` at `0x46FDA9` |
| World map | `worldmap_init` | 30.5 | — |

The extra 0.5 is deliberate headroom so the limiter does not oscillate around the integer target. The card game running the exact same module loop at 60.5 fps shows the surrounding engine (gfx driver, input pump, task system) has no problem with 60 fps module loops.

## Anatomy of one battle frame

`battle_cardgame_main_loop` runs once per rendered frame (15.5 Hz in battle). Order of operations:

| Step | Code (in `battle_cardgame_main_loop`) | Purpose |
|------|----------------------------------------|---------|
| 1 | begin scene, clear, render queue setup | gfx frame start |
| 2 | pause check (`canBattleBePaused`) | sets `pause_game_battle` |
| 3 | 4× `Savemap_TickGameTimeAndCountdown` | game time advances 4 ticks per frame (60 ticks/s) |
| 4 | 3× (`isBattle_HUDupdate` + `isBattle_HUDdisplay`) with menu rendering **disabled** | **hidden catch-up UI ticks** |
| 5 | `IsWindowNOTActive` → `Input_ProcessInput` | **the only DirectInput poll of the frame** |
| 6 | `FFBattleDirector_battleLoop` | battle logic (ATB, actions, AI, tasks) — inside it `BdLink_GF_battle_input_and_texture_upload_called_in_loop` runs the per-frame render/task tick and calls `BattleUI_ArmInputFrame` once |
| 7 | 1× (`isBattle_HUDupdate` + `isBattle_HUDdisplay`) with menu rendering **enabled**, then `Battle_cursor_battle_win_and_pause_menu_render_related` | the visible UI tick + cursor/window rendering |
| 8 | swirl / present / `Time_WaitNextFrame` | frame end, sleep to 15.5 fps |

So the UI is ticked 4 times per frame (steps 4 and 7) — 62 ticks/s at 15.5 fps, matching the PSX 60 Hz tick budget — but the 4 ticks are **temporally clustered**: they run microseconds apart inside one 64.5 ms frame, not spread 16 ms apart as on PSX.

When the battle is paused, step 6 is skipped and the previous frame's battle scene is re-presented via `display_texture_related_sub_45D610(-1)` while the UI keeps ticking. This pause path is a working in-engine template for decoupling UI ticks from battle logic (see fix option B).

## The battle UI tick pair

Each UI tick is the pair `isBattle_HUDupdate` + `isBattle_HUDdisplay`, operating on the battle UI context (`BattleUI_CtxPtr`, 88-byte block at game_obj+912).

### isBattle_HUDupdate — fresh-input latch

Increments `BattleUI_TickCounter` and clears the context's *fresh input this tick* byte (ctx+33). It sets ctx+33 back to 1 only when:

- `BattleUI_NewInputFrameFlag` is pending — raised **once per battle frame** by `BattleUI_ArmInputFrame` (called from `BdLink_GF_battle_input_and_texture_upload_called_in_loop`), and
- at least `BattleUI_InputTickDivisor` ticks have elapsed since the last latch. The divisor is loaded from the static constant `CONST_BattleUI_TicksPerFrame` = **4**.

On a fresh-input tick it also copies the current window-context pad snapshot into ctx (buttons at ctx+4) and increments the input-frame counter (ctx+44). Consequently, exactly **1 of the 4 UI ticks per frame is a fresh-input tick** — a 15 Hz cadence that much of the menu code keys off.

### isBattle_HUDdisplay — pad ring advance + UI work

Every tick it:

1. Calls `Input_PadRing_AdvanceAndComputeEdges` (formerly `sub_49E9C0`): refreshes the PSX-format pad snapshot from the engine pad mask (`Input_PadRing_RefreshSnapshotFromEngine` → `Input_WritePsxPadButtons` → `Input_GetPadState`) and appends a new entry to the 8-entry ring buffer in `INPUT_BIG_STRUCT`, computing `keyon` (press edges) and `keyoff` (release edges) against the previous entry.
2. Snapshots pad state into the UI context: held (ctx+16), auto-repeat (ctx+18), pressed edges (ctx+20), each through `remap_pad_input`.
3. Runs the UI machinery: exit-combo check, analog-to-direction mapping, `BattleTask_UI_Dispatcher`, `BattleUI_UpdateAllWindows`, `Battle_TickAtbGaugesAndGfCountdown`.

The ring buffer advances 4×/frame, but because the engine pad mask only changes when `Input_ProcessInput` runs (once per frame, step 5), **at most one ring entry per frame can contain a press edge**. The three hidden ticks recompute edges against an unchanged mask and produce nothing.

## Input pipeline end to end

```
DirectInput keyboard/joystick
        │  Input_ProcessInput            ← once per rendered frame (15.5 Hz in battle)
        ▼
engine pad mask (Input_GetPadState)
        │  Input_WritePsxPadButtons      ← converts to PSX active-low 16-bit layout
        ▼
INPUT_BIG_STRUCT 8-entry ring            ← advanced once per UI tick (4×/frame)
  entry = {held, keyon, keyoff, autorepeat}
        │  read_pad_held_raw / read_pad_pressed_raw(port, age)
        ▼
remap_pad_input (ff8input.cfg mapping → PSX button order)
        ▼
Battle UI context  ctx+16 held / ctx+18 repeat / ctx+20 pressed
                   ctx+33 fresh-input latch (1 of 4 ticks)
```

The 16-bit PSX button mask layout (also used by `K_DUEL` sequences): hi byte `Select 0x01, Start 0x08, Up 0x10, Right 0x20, Down 0x40, Left 0x80`; lo byte `L2 0x01, R2 0x02, L1 0x04, R1 0x08, Triangle 0x10, Circle 0x20, Cross 0x40, Square 0x80` (before remap; after `remap_pad_input` the game's logical order applies).

## Effect on Zell's Duel

`BattleMenu_ZellDuel_Update` runs every UI tick (≈60/s):

- The duel timer `CURRENT_LIMITBREAK_FLOW` decrements once per tick while a 4-tick budget byte is non-zero; the budget refills on every fresh-input tick. Net effect: the countdown runs at **real-time speed (≈60/s)**, identical to PSX.
- Inputs are read per tick from `read_pad_pressed_raw` (edge word) OR'd with held D-pad bits, pushed into an 8-entry input ring, and matched (reversed, up to 5 buttons) against the three candidate `K_DUEL` sequences.

Since press edges materialize at most once per rendered frame, the player can land **one input per 64.5 ms** at best, and quick taps between two polls are dropped. The duel duration in seconds is unchanged, so the input-per-second ceiling is ~4× lower than the code's own tick pacing allows.

## Effect on GF Boost

`computeGFBoost_` also runs per UI tick, but its phase timers (`word_209CEF6`, safe/danger phase lengths of `15 × rand(2..6)` units) only decrement on **fresh-input ticks** (ctx+33), i.e. at 15/s instead of the intended 60/s:

- Boost phases last **4× longer in wall-clock time** (2–6 s instead of 0.5–1.5 s).
- Square-press edges are counted per tick but can only appear at 15 Hz → effective mash ceiling ≈ 7–8 registered presses/s, and fast taps are lost outright.

The +1-per-press / reset-on-danger-press / 75-start / 250-cap logic itself is identical to PSX.

## Fix approaches

### A. Input-fidelity hook (small, safe)

Keep the 15.5 fps loop, but stop losing presses. A hook (FFNx is the natural host) samples the real hardware on its own 60 Hz clock into a small history queue. Then either:

- feed each of the 4 clustered `Input_PadRing_AdvanceAndComputeEdges` calls a different 16.1 ms time-slice from the history (the 3 hidden ticks get the slices the vanilla game throws away), or
- simpler: accumulate "pressed since last poll" bits in the sampler and OR them into the mask that `Input_GetPadState` returns, so no press is ever shorter than one poll interval.

The time-sliced variant restores near-PSX behavior for both minigames without touching frame pacing, ATB, animation or effect speed: Zell's Duel consumes the ring per tick and matches sequences up to 8 entries deep, and Boost counts edges per tick, so distributing edges across the 4 ticks is exactly what both consumers expect. Latency stays one frame (unchanged), but nothing is lost or merged. Boost phase pacing stays 4× slow (it keys off the fresh-input latch), which can be fixed by also raising `BattleUI_NewInputFrameFlag` per tick — see B3.

### B. True 60 fps battle-module loop (full fix, heavier)

Run the module loop at 60.5 fps and spread the existing tick budget over time. Required pieces:

1. **Frame rate**: patch the `push 0x402F0000` at `0x47CE3F` to `push 0x404E4000` (15.5 → 60.5).
2. **UI ticks**: NOP the 3 hidden tick pairs in `battle_cardgame_main_loop` (calls at `0x47D09D`–`0x47D0B6`) and reduce the 4× `Savemap_TickGameTimeAndCountdown` (`0x47D076`–`0x47D085`) to 1× — one tick pair per 60 Hz frame keeps the 60 ticks/s budget, now correctly spread, each with a fresh input poll.
3. **Input frame arming**: `BattleUI_ArmInputFrame` is only reached when battle logic runs. Either force `BattleUI_NewInputFrameFlag` non-zero every frame and set `BattleUI_InputTickDivisor`/`CONST_BattleUI_TicksPerFrame` (dword at `0xB8A3E4`) to 1, so every tick is a fresh-input tick (this also restores PSX Boost phase pacing).
4. **Battle logic gating**: run `FFBattleDirector_battleLoop` + `BdLink_GF_battle_input_and_texture_upload_called_in_loop` only every 4th frame; on skipped frames re-present the scene the way the pause path already does (`display_texture_related_sub_45D610(-1)`, see `0x47D1FC`). Animations, ATB and effects then keep their 15 Hz logic rate while menu, cursor and input run at 60.
5. Audio/frame bookkeeping (`Sound_UpdateTransitions_PerFrame`, `Time_LastFrameElapsedMs`) already run per loop iteration and need no change.

Step 4 is the risky one (double-buffered render lists flip per battle frame — `dword_1D96A80`); the pause path proves re-presenting is safe, but interactions with the swirl, movie playback (`is_sleeping` path) and `mode_Battle_AnimationState != 3` phases need testing. Going further and interpolating the 3D at 60 fps is a separate, much larger project (see the notes on `MAG_*` effect gating on the magic runtime pages — procedural effect code is frame-count sensitive).

### What not to patch

- `CONST_BattleUI_TicksPerFrame` (= 4) alone: lowering it without raising the arm rate changes nothing — the latch is limited by `BattleUI_NewInputFrameFlag`, which is raised once per battle frame.
- The 15.5 constant alone: everything (ATB, animations, effects, game time, Boost, Duel timers) then runs 4× too fast; the UI tick budget stays 4/frame so UI timers would run at 240 ticks/s.

## Function and data addresses

| Name | Address | Description |
|---|---|---|
| `battle_cardgame_main_loop` | `0x47CF60` | Per-frame battle module loop (frame anatomy above) |
| `FFBattleInitSystem` | `0x47CE10` | Battle module init; sets 15.5 fps (card game 60.5) |
| `FFBattleDirector_battleLoop` | `0x47CCB0` | Battle logic state machine, once per frame |
| `BdLink_GF_battle_input_and_texture_upload_called_in_loop` | `0x500900` | Per-battle-frame task/render tick; arms the UI input frame |
| `Time_SetTargetFrameRate` | `0x4020C0` | fps → `FRAME_PERIOD_TICKS` |
| `Time_WaitNextFrame` | `0x4020F0` | End-of-frame limiter (sleep + overshoot amortization) |
| `IsWindowNOTActive` | `0x45B2E0` | Per-frame input pump wrapper (calls `Input_ProcessInput`) |
| `Input_ProcessInput` | `0x467D10` | DirectInput keyboard/joystick poll — once per rendered frame |
| `Input_GetPadState` | `0x468500` | Returns current engine 16-bit pad mask |
| `Input_WritePsxPadButtons` | `0x56D990` | Engine mask → PSX active-low pad bytes |
| `Input_PadRing_RefreshSnapshotFromEngine` (was `sub_49E720`) | `0x49E720` | Refreshes per-port pad snapshot from engine state |
| `Input_PadRing_AdvanceAndComputeEdges` (was `sub_49E9C0`) | `0x49E9C0` | Appends ring entry; computes keyon/keyoff edges |
| `read_pad_pressed_raw` / `read_pad_held_raw` | `0x49EDE0` / `0x49ED30` | Read edges/held from ring (`age` = entries back) |
| `remap_pad_input` | `0x4A2D60` | ff8input.cfg mapping to logical button order |
| `isBattle_HUDupdate` | `0x4A8E30` | UI tick part 1: fresh-input latch (ctx+33) |
| `isBattle_HUDdisplay` | `0x4A84E0` | UI tick part 2: pad ring advance, ctx snapshot, windows, ATB |
| `BattleUI_ArmInputFrame` (was `sub_4A9220`) | `0x4A9220` | Raises `BattleUI_NewInputFrameFlag`, sets tick divisor — 1×/battle frame |
| `BattleUI_SetInputFrameParams` (was `sub_4A8EF0`) | `0x4A8EF0` | Direct setter for divisor/flag/render ctx (unused caller-side) |
| `BattleMenu_ZellDuel_Update` | `0x4AF840` | Zell Duel state machine, per UI tick |
| `computeGFBoost_` | `0x56DD70` | GF Boost gauge, per UI tick |
| `Battle_TickAtbGaugesAndGfCountdown` | `0x4842B0` | ATB advance, called from the UI tick |
| `BattleUI_CtxPtr` | `0x1D6D490` | Pointer to 88-byte battle UI context (game_obj+912) |
| `BattleUI_TickCounter` | `0x1D6D4A4` | UI tick counter, incremented per UI tick |
| `BattleUI_NewInputFrameFlag` | `0x1D6D494` | Armed 1×/battle frame; consumed by the fresh-input latch |
| `BattleUI_InputTickDivisor` (was `dword_1D6D620`) | `0x1D6D620` | Min ticks between fresh-input latches (loaded with 4) |
| `BattleUI_LastInputLatchTick` (was `dword_1D6D628`) | `0x1D6D628` | Tick counter value at last latch |
| `CONST_BattleUI_TicksPerFrame` (was `dword_B8A3E4`) | `0xB8A3E4` | Static constant 4 = UI ticks per battle frame |
| `INPUT_BIG_STRUCT` | `0x1D2B110` | Input state: ports, 8-entry ring, DirectInput analog block (+0x188) |
| Battle fps constant patch point | `0x47CE3F` | `push 0x402F0000` (double 15.5 hi-dword) |
| Hidden UI tick call sites | `0x47D09D`–`0x47D0B6` | 3× update+display pairs, menu rendering disabled |
| Game-time 4× tick call sites | `0x47D076`–`0x47D085` | 4× `Savemap_TickGameTimeAndCountdown` |
| Pause re-present template | `0x47D1FC` | `display_texture_related_sub_45D610(-1)` |
