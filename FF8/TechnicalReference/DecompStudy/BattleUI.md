---
layout: default
title: Battle UI (HUD and command menu)
parent: Battle
permalink: /technical-reference/battle/battle-ui/
---

1. TOC
{:toc}

# Battle UI — HUD and in-battle menus

The 2D window layer drawn over a battle: party HUD, command window, sub-windows, target selection and captions. The battle logic behind it is on [Battle module runtime]({{ site.baseurl }}/technical-reference/battle/module-runtime/). Addresses for FF8_EN.exe, image base 0x400000.

## Windowing core

The battle UI is a tiny widget system: a **9-slot window table** at 0x1D76628 (20 bytes per slot: update callback, draw callback, overlay callback, redraw state). Fixed slot assignments:

| Slot | Window |
|------|--------|
| 1 | Turn pre-handler |
| 2 | Active sub-window (magic / GF / item / draw / target / specials) |
| 3 | Command companion layer |
| 4 | Command window |
| 5 | Party status panel (Select key detail view) |
| 6 | Zell Duel input window |
| 7 | Party HUD rows |
| 8 | Description/caption window (drawn even when the HUD is hidden) |

Draws are **cached**: a window with redraw state 2 only re-renders when explicitly invalidated (`BattleUI_InvalidateWindowsUpTo`) — HP or ATB changes trigger that invalidation. `BattleUI_UpdateAllWindows` / `DrawAllWindows` / `DrawAllWindowOverlays` run the three passes each frame (the overlay pass draws the target cursor above everything).

## Party HUD (window 7)

Three 13-px rows in the (122,165,190,51) region, backed by `BATTLE_CHARA_UI` (0x1D76928, 3 × 108-byte structs — HP roll state, digit glyphs, gauge widths, per-character cursor memory):

* **HP digits** (x+97): displayed HP *rolls* toward the real value at maxHP/96 per tick; CLUT color white normally, **yellow below 25 % HP, red at 0**.
* **ATB bar** (x+135): a 48-px gradient quad; colors come from two table pairs (0xB8790C/1C filling, 0xB8792C/3C ready) modulated by the status word — and when the gauge is full and it's that character's turn, the bar pulses with a triangle wave on the frame counter (the "ready blink").
* **GF summon overlay**: while a GF is called, an overlay slides over the row showing the GF name, GF HP and the compatibility-driven countdown bar.
* The status panel (window 5, (218,164) 94×52) shows detailed cur/max HP with digit glyph helpers; Select cycles status detail modes.

## Command window (slot 4)

`BattleMenu_CommandWindow_Update` is a 25-state machine: init (reads the character's 4 junctioned command entries from `F_CHAR_DATA[].commandData`, names resolved from kernel.bin) → scale-in animation (+409/frame to 4096) → input states → optional inline Double/Triple sub-list → flush selection to the [command queue]({{ site.baseurl }}/technical-reference/battle/module-runtime/) → executed/character-switch states. Cursor position is remembered per character when the config "cursor memory" flag is set.

**Limit display**: pressing LEFT on a command whose kernel flag allows it slides in the limit command with an eased crossfade; a blinking arrow icon marks crisis; Renzokuken's R1 caption and timing gauges are drawn by the caption window (slot 8) from the combo message pointer.

## Sub-windows (slot 2)

Magic list (with Draw-stock counts), GF list, two-column item list, the Draw window (draw/cast choice), and four special list types share a generic scrolling-list engine (`BattleMenu_ListWindow_*`, 0x4FDD90). Zell's Duel input replaces slot 6. Target selection (`BattleMenu_OpenTargetSelection`, 8 states) polls a target bitmask, supports the ALL toggle for spells flagged multi-target, and confirms into the pending-selection buffer.

`BattleMenu_ExecuteSelectedCommand` is what opens each of these sub-windows; the full bit layout and id-to-function table lives in [Menu flags]({{site.baseurl}}/technical-reference/list/battle/#menu-flags).

## Text and graphics sources

* Command/magic/item names and descriptions come from **kernel.bin** text sections at runtime (`getAddressAbilityName`, `getMagicText`, `getBattleCommandDescription`); monster names come from scene.out; top captions are queued as print-text battle tasks with config-controlled speed; variables are expanded by `ProcessBattleTextExpansion`.
* The battle UI does **not** use the menu module's TEXT_LAYER: digits, labels, gauge frames and arrows are sprites from the **AICON/SP1 icon atlas**, with colors selected as CLUT-row offsets.
* The **blue window gradient** is built from textured 8-px strips vertex-tinted by the player's configured window color (`BattleUI_DrawWindowGradientStrips`).
* Damage/heal number popups are *not* part of this 2D layer — they are 3D-projected billboards on the battle-effect/task side; the HUD only rolls its HP digits.

## Frame rate and input sampling — why Duel and Boost are worse than on PSX

The PC battle module is **frame-locked at 15 fps**: `FFBattleInitSystem` sets the target rate to the double constant 15.0 (60.0 for the card game), and one loop iteration does render + logic + **one DirectInput poll**. On PSX the 3D battle also ran at ~15 fps, but the pad was sampled and the menu overlay updated on the 60 Hz vblank, independent of the render rate.

The port compensates for the *logic* but not for the *input*:

* `battle_cardgame_main_loop` calls `isBattle_HUDupdate` **4 times per rendered frame** (3 hidden ticks with rendering disabled + 1 visible) → UI timers, typewriter text, gauges and the Duel countdown all run at 4 × 15 = **60 ticks/s**, i.e. correct real-time PSX speed.
* But `isBattle_HUDupdate` clears the "fresh input" flag (ctx+33) every tick and only sets it when `BattleUI_NewInputFrameFlag` is pending — and that flag is raised **once per rendered frame** by the input poll. So 3 of the 4 ticks see stale input: **effective input sampling in battle is 15 Hz** (one new pad snapshot every 66.7 ms), versus 60 Hz on PSX.

Consequences, straight from the code:

* **Zell's Duel** (`BattleMenu_ZellDuel_Update`): the countdown decrements once per tick through a 4-tick budget refilled on each fresh-input event — so the timer runs at the correct 60/s. The inputs, however, are edge words pushed into an 8-entry ring only when a *new* snapshot shows them: at most one new input event per 66.7 ms, presses shorter than a frame are lost, and two quick presses merge into one snapshot. Same duel time, **a quarter of the input opportunities** → far fewer commands per Duel than on PSX.
* **GF Boost** (`computeGFBoost`): the gauge (+1 per Square press edge in the "safe" phase, reset to 75 in the "danger" phase, start 75, cap 250, untouched = 100) suffers twice. Press edges are capped by the 15 Hz sampling (~7–8 effective mashes/s instead of ~30). And the safe/danger **phase timers only decrement on fresh-input frames** (15/s) while their durations (`15 × (rand(1..3) + rand(1..3))` units) were tuned for 60/s — so on PC each phase lasts 2–6 seconds instead of 0.5–1.5 s. The Duel timer got the 4-tick real-time fix; the Boost phase pacing did not.

In short: the menu isn't "running at 15 fps" logically — it ticks at 60 Hz — but it can only *see the controller* at 15 Hz, and Boost's phase pacing was left on the per-frame clock. Fixing Duel/Boost responsiveness would mean polling input per tick (or per 16.7 ms) and feeding `BattleUI_NewInputFrameFlag`/ctx+33 accordingly, plus restoring Boost's phase decrement to per-tick.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `BattleUI_RegisterWindow` | 0x4B9AD0 | Registers a window's update/draw/overlay callbacks in the 9-slot table |
| `BattleUI_UpdateAllWindows` | 0x4B9C80 | Per-frame update pass over all windows |
| `BattleUI_DrawAllWindows` | 0x4B9DB0 | Per-frame draw pass over all windows |
| `BattleUI_InvalidateWindowsUpTo` | 0x4B9C40 | Forces redraw of cached windows |
| `BattleUI_DrawWindowGradientStrips` | 0x4B6530 | Draws the tinted blue window gradient |
| `BattleHUD_Init` | 0x4B1B00 | Initializes the party HUD |
| `BattleHUD_RefreshCharaRow` | 0x4B1BB0 | Updates a party HUD row's rolling HP/gauge state |
| `BattleHUD_DrawPartyRows` | 0x4B1740 | Draws all party HUD rows |
| `BattleHUD_DrawCharaRow` | 0x4B0F10 | Draws a single party HUD row |
| `BattleHUD_DrawGFSummonOverlay` | 0x4B08F0 | Draws the GF summon overlay on the HUD |
| `BattleHUD_GetATBGaugeColor` | 0x4B14C0 | Picks ATB gauge gradient colors |
| `BattleMenu_CommandWindow_Update` | 0x4BB9E0 | Command window state machine |
| `BattleMenu_CommandWindow_Init` | 0x4BCBE0 | Command window init state |
| `BattleMenu_CommandWindow_Draw` | 0x4BCE10 | Command window draw |
| `BattleMenu_ExecuteSelectedCommand` | 0x4BC770 | Opens the sub-window for the selected command |
| `BattleMenu_OpenMagicWindow` | 0x4C8840 | Opens the magic list sub-window |
| `BattleMenu_OpenGFWindow` | 0x4C8280 | Opens the GF list sub-window |
| `BattleMenu_OpenItemWindow` | 0x4C87A0 | Opens the item list sub-window |
| `BattleMenu_OpenDrawWindow` | 0x4ADD10 | Opens the Draw sub-window |
| `BattleMenu_OpenTargetSelection` | 0x4C7030 | Opens target selection |
| `BattleMenu_ListWindow_Update` | 0x4FDD90 | Generic scrolling-list engine shared by sub-windows |
| `BattleMsg_ComboCaption_Draw` | 0x4C8DC0 | Draws the Renzokuken combo caption/timing gauges |
| `BattleMenu_ZellDuel_Update` | 0x4AF840 | Zell's Duel input window state machine |
| `computeGFBoost` | 0x56DD70 | GF Boost mini-game gauge/phase logic |
| `BattleUI_WindowTable` | 0x1D76628 | Global variable/data, not a function — 9-slot window table (20 B/slot) |
| `BATTLE_CHARA_UI` | 0x1D76928 | Global variable/data, not a function — party HUD state (3×108 B) |
| ATB color tables | 0xB8790C–0xB8793C | Global variable/data, not a function — ATB gauge gradient color pairs |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
