---
layout: default
title: Menu module runtime
parent: Menu
permalink: /technical-reference/menu/menu-module-runtime/
---

1. TOC
{:toc}

# Menu module runtime

This page describes how the menu system runs as an engine module: which module loops exist, how a menu is requested, and how results flow back to the engine. The menu data files themselves are covered by the other pages of this section (mngrp, mitem, mwepon...). How the engine switches modules is on [Engine startup and main loop]({{ site.baseurl }}/technical-reference/main/engine-startup-and-main-loop/).

## Menu resource loading

All menu resource files are loaded **once**, by `LoadMenuFiles` — registered as the engine-level `exit_main` callback, so it runs when the intro/credits module exits, right before the title screen appears. It calls `MenuReadFiles` (mngrp and friends), the pack-code, icon and vibration data loaders, and initializes the menu data pointer tables. This is why menu files are not reloaded between menus.

## Module loops using the menu system

Three registered module loops share the same init/exit (`menu_init` / `menu_exit`):

| Loop | Used for |
|------|----------|
| `FFTitleMenuModule_main_loop` | Title screen (menu ID 25); result bit 1 = New Game |
| `menu_or_tuto_main_loop_1` | In-game menu, tutorials, GF-obtained screens (mode 6/10/11 of the module handler) |
| `menu_endcombat_victory_main_loop` | Post-battle victory screens (EXP/AP/items), entered when the battle exits with the end-combat path |

All three run a 60 fps frame limiter (busy-wait on the high-resolution timer) — menus run at 60 fps while field/world run at 30.5 and battles at 15.

## Menu request interface

Two globals select what the menu module shows:

* `menu_id` (`0x1D2BB98`) — the menu to open. Observed values: 25 = title screen, 0x80000000 = the full in-game pause menu, `GF id + 5` = the "GF obtained" tutorial screens, and field scripts pass their menu ID through `MenuState_opcode_menu_id` (MENUNORMAL, MENUSHOP, MENUNAME... opcodes).
* `menu_sub_id` (`0xB87798`) — sub-parameter; for the pause menu it carries the save-enabled bits (`canSaveHere | 1` when opened from the field).

## The menu host state machine

`menu_host_run_frame` (formerly `SomethingWithReset`) drives one menu instance through `MENU_PHASE`:

| MENU_PHASE | Action |
|------------|--------|
| 0 | Setup: reset draw state, prepare the menu for `menu_id` |
| 1 | Load sub-machine (`dword_1D2A27C` 0→1→2): init menu state with (menu_id, menu_sub_id), run the loading steps, teardown |
| 2 | Fetch the menu result, return `result | 0x400`, reset to phase 0 |

The return value is 0 while the menu runs. **Bit 0x400 = menu closed**; the low bits are the menu system's result flags, which the module loop stores in `menu_result_flags` (`0x1D2BB9C`) before switching back to `FFModuleHandler_main_loop`. The module handler then interprets them (bit 0 = special action, bit 2 = start a battle immediately with the encounter ID in the high 16 bits — used by debug/battle-from-menu paths; on the title screen, bit 1 = New Game).

## Address table

| Name | Address | Description |
|------|---------|-------------|
| `LoadMenuFiles` | 0x470340 | One-time menu resource loading (engine exit_main) |
| `MenuReadFiles` | 0x4A1BF0 | mngrp & co. file loading |
| `menu_init_sub_4A2280` | 0x4A2280 | Module enter_main (timer + init) |
| `menu_init_sub_4972D0` | 0x4972D0 | Menu system init |
| `menu_exit_sub_4A22A0` | 0x4A22A0 | Module exit_main |
| `menu_or_tuto_main_loop_1` | 0x4A22C0 | In-game menu / tutorial module loop |
| `menu_endcombat_victory_main_loop` | 0x4A2690 | Post-battle victory screens loop |
| `FFTitleMenuModule_main_loop` | 0x4A24B0 | Title screen loop |
| `menu_host_run_frame` | 0x497380 | Menu host state machine (MENU_PHASE) |
| `MENU_PHASE` | 0x1D2A280 | Host phase (0 setup / 1 load / 2 result) |
| `menu_id` | 0x1D2BB98 | Requested menu ID |
| `menu_sub_id` | 0xB87798 | Menu sub-parameter (save-enable bits...) |
| `menu_result_flags` | 0x1D2BB9C | Result returned to the module handler |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
