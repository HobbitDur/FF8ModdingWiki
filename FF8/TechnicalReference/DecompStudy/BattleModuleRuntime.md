---
layout: default
title: Battle module runtime
parent: Battle
permalink: /technical-reference/battle/module-runtime/
---

1. TOC
{:toc}

# Battle module runtime

How a battle runs in the engine: module lifecycle, the battle state machine, the ATB system, and the command pipeline. Damage and stat math is on the [battle formulas]({{ site.baseurl }}/technical-reference/battle/formulas/) page; monster AI, models and stages have their own pages. Addresses for FF8_EN.exe, image base 0x400000.

## Lifecycle

`wanted_game_mode = 3` makes the module handler enter **`FFBattleTransitionModule`**, which plays the swirl (normal or boss variant) and then registers the battle module: `FFBattleInitSystem` / `FFBattleExitSystem` / `battle_cardgame_main_loop` (shared with the card game).

* **Init** zeroes the 0x1344-byte battle runtime state, sets the logic rate (battle = 15 fps logic, card game = 60) and switches the viewport.
* **Main loop** handles pause, updates and draws the HUD **three times per frame** while the UI phase is active, then calls **`FFBattleDirector_battleLoop`**.
* The director's `GLOBAL_BATTLE_MOD_STATE` sub-machine: countdown/load → transition → `btitle.ovl` (battle title) → in-battle. In-battle setup: stage `.x` load → `scene.out` encounter read into `CURRENT_ENCOUNTER_DATA_SCENE_OUT` → party parse → monster `.dat` loads → FIGHTING.
* **Exit**: when the end fade completes, the stage unloads and `Battle_ExitWritebackPartyItemsAndResult` writes HP/statuses back to the savemap, merges the battle inventory into the item list, and routes by the result byte (1/3 = game over, 2 = escaped, 4 = victory, 5 = other). Victory goes to the `menu_endcombat_victory` module (EXP/AP/item screens); everything else returns to the module handler.

## Battle phase global

`mode_Battle_AnimationState` (word): 0 = idle, 1 = field fading out before the module switch, 3 = battle active (HUD + ATB ticking enabled), 4 = battle won → victory/rewards module (the world module busy-waits on 4 when a battle was triggered from the world map).

## Per-frame order (FIGHTING)

Game-over/victory/escape checks → run-away animation tasks → the 3 player command queues → action buffer → Odin intro → **`BattleTurn_ProcessActionQueue`** (action execution) → timers/Gilgamesh → battle text → HUD phase (ticks ATB) → monster AI (fills the same action pools).

## Combatants

`BATTLE_SLOT_DATA`: 8 slots of 208 bytes (`FF8BattleSlotData`) — slots 0–2 party, 3–7 monsters. Key fields: +16 `max_atb`, +20 `cur_atb`, +24/+28 current/max HP, +124 flags (bit 3 = ready-to-act), +128 status word (bit 0 death), +144 mental resistances, +188 level, +189 stat array ([4] = SPD), +202 crisis level. A parallel 156-byte visual struct holds position/animation state.

## ATB system

* **Gauge size**: `max_atb = 4000 × (BattleSpeed setting + 1)` (config 0 = fastest).
* **Starting fill**: `cur_atb = max_atb/100 × (SPD/4 + rand(0..127) + 1 − 35)`, clamped to [0, max]. The Initiative ability starts the gauge full.
* **Tick** (3× per frame while the HUD updates): `cur_atb += rate × atb_multiplier × (SPD + 30) / 100`, where rate = 10 normally, 15 hasted, 5 slowed, and `atb_multiplier` comes from kernel Misc data. No fill while dead/petrified/stopped/sleeping.
* Gauge full → berserk/confusion/Angel Wing act automatically; otherwise the command window opens and the slot is flagged ready.
* A summoned **GF countdown** decrements by 2 per tick (3 hasted, 1 slowed).

## Crisis level and the Limit command

`Battle_ComputeCrisisLevelAndLimitFlag`:

```
crisis = (10×(statusSum + 4×(5×deadAllies + 40)) − 10×HPmod×curHP/maxHP)
         / (rand(0..255) + 160) − 4        → clamped to 0..4
```

`statusSum` sums kernel Misc limit-effect bytes over the character's set status bits — **Aura** is by far the largest contributor; `HPmod` is the character's crisis-HP multiplier from kernel data; Curse (or a map seal) forces 0. The Limit command is then shown this turn when `60 × crisis ≥ rand(0..255)` — about 23% / 47% / 70% / 94% for levels 1–4.

## Command pipeline and targeting

Command menu → 12-byte selection buffer → `Battle_FlushMenuSelectionsToCommandQueue` → `BATTLE_PLAYER_COMMAND_QUEUE` (3 × 8-byte entries: slot, command type, magic/item id, target mask, active) → each frame `processCommandBattleInputFromPlayer` allocates into the **three-priority shared action pools** (11 slots, the same allocator the monster AI uses — GF/limits into pool 1, magic/items/attacks into pool 2) → `BattleTurn_ProcessActionQueue` executes per target.

**Target mask** (word): bit N = combatant slot N (0–2 party, 3–7 monsters), bit 15 = multi-target; "all enemies" = 0x80F8. Kernel target-info bits refine selection: 0x20 single random, 0x10 whole side, 0x40 enemy side.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `FFBattleTransitionModule` | 0x559890 | Plays the battle swirl and registers the battle module |
| `FFBattleInitSystem` | 0x47CE10 | Battle module init |
| `FFBattleExitSystem` | 0x47CEF0 | Battle module exit |
| `battle_cardgame_main_loop` | 0x47CF60 | Shared battle/card-game main loop |
| `FFBattleDirector_battleLoop` | 0x47CCB0 | Battle director state machine |
| `Battle_ExitWritebackPartyItemsAndResult` | 0x4868C0 | Writes HP/statuses/items back to the savemap on exit |
| `BattleMenu_CommandWindow_Init` | 0x4BCBE0 | Command window init state (referred to as `Battle_CommandMenuInit` elsewhere on this page) |
| `BattleMenu_CommandWindow_Update` | 0x4BB9E0 | Command window state machine (referred to as `Battle_CommandMenuUpdateHandler` elsewhere on this page) |
| `Battle_TickAtbGaugesAndGfCountdown` | 0x4842B0 | Per-tick ATB gauge and GF countdown update |
| `Battle_CalculateInitialATB` | 0x4844D0 | Starting ATB fill formula |
| `Battle_SetMaxAtbFromBattleSpeed` | 0x484490 | Sets `max_atb` from the Battle Speed setting |
| `Battle_ComputeCrisisLevelAndLimitFlag` | 0x4941F0 | Crisis level and Limit-availability formula |
| `Battle_RollLimitCommandFromCrisisLevel` | 0x494190 | Rolls whether Limit is shown this turn |
| `Battle_FlushMenuSelectionsToCommandQueue` | 0x4BB610 | Flushes the menu selection buffer to the player command queue |
| `BATTLE_SLOT_DATA` | 0x1D27B10 | Global variable/data, not a function — 8×208 B combatant slot array |
| `mode_Battle_AnimationState` | 0x1CDBFE0 | Global variable/data, not a function — battle phase word |
| Result byte | 0x1CFF6E7 | Global variable/data, not a function — battle exit result code |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
