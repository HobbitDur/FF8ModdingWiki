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

## Menu programs and the dispatch table

Inside the host, menus run as **programs** on a small stack machine. The requested menu ID (a *hosted id*) is mapped by `Menu_StartHostedProgram` (0x4B3140) to a *program id* — an index into **`Menu_ProgramTable`** (0xB87ED8, 33 entries of `{init_function, mngrp_group}`). Programs invoke children with `Menu_InvokeProgram` (0x4BDB30), which pushes the program stack and loads the child's mngrp file group.

Hosted ids: 0/default = main menu (param = "can save here") · 1 = party select · 2/3/4 = name entry Squall/Rinoa/Angelo · 5–20 = name entry GF 0–15 (post-battle GF naming = GF id + 5) · 22 = save-point menu (param = save flags) · 23 = shop (param = shop index; 21 opens the junk shop) · 24 = game-over Continue · 25 = title · 26 = tutorial · 27/28 = name Boko/Griever · 29 = tutorial direct page.

Program table (index = program id): 0 root idle · 1 main menu · 2 item · 3 magic · 4 GF · 5 status · 6 game-over title variant · 7 card album · 8 config · 9/10 party select · 11 shop · 12 junk shop (weapon remodel) · 13 save menu · 14 Tonberry Call Shop · 15 name entry · 16 title · 17 junction · 18 junction demo · 19 refine (incl. Card Mod) · 20 tutorial · 21 Information hypertext browser ([TextBox pages](../mngrp-textbox-section/)) · 22 game-controls image browser (raw 63-65) · 23 SeeD written test · 24 GF demo · 25/26/31 [tutorial book viewers](../mmag/) (battle tutorial / card rules / card icons) · 27 Chocobo World screen ([mmag2.bin](../mmag2/)) · 28 limit-break demos · 29 character-switch demo · 30 tutorial direct · 32 partyRest (no UI). The main menu maps its entries to submenu program ids through a small byte table (low 5 bits per entry).

## Text engine (TEXT_LAYER)

All menu and dialog text renders through 8 window slots of 60 bytes at **`TEXT_LAYER`** (0x1D2B330): rect, encoded-text pointer + current line, typewriter speed/progress, color/flags, render target, open-animation scale (0–4096), choice block (first/last/current/cancel line), page-arrow blink, wait counter and draw callback. The world map's 13 message windows allocate from the same pool.

* **Flow**: `Text_SetLayerText[WithChoices]` assigns text → `Text_Window_UpdateStateMachine` (0x49FEB0) advances typewriter and choice cursor each tick → `Text_DrawWindowLayer`/`Text_RenderGlyphs` emit frame, cursor and glyph sprites.
* **Glyphs**: sysfnt font texture, 12×12 cells, 21 per row (`u = 12·(g%21)`, `v = 12·(g/21)`); proportional widths from packed nibbles in `font_char_width_table`; extended pages via lead bytes 0x19–0x1B, second sheet for 0x1C–0x1F. Line height 16 px.
* **Control codes**: 0x00 end · 0x01/0x07 end of page (wait confirm) · 0x02 newline (+32 px indent on choice lines) · 0x05+n icon from aicon.sp1 (0x20–0x2F = button icons, remapped by key config) · 0x06+n color (low nibble = CLUT, high = blink variants) · 0x08+p typewriter speed (32 instant, 33 pause, else 4096/(p−33)) · 0x09 wait. Variable inserts (names, numbers) are pre-expanded by `ProcessBattleTextExpansion`.

## mngrp group loading

At session begin the host loads `mngrphd.bin` (the offset index into [mngrp.bin]({{ site.baseurl }}/technical-reference/menu/menu-mngrp-bin/)). `Menu_LoadMngrpGroupAsync(group)` then loads the program's file group and its shared text sub-file into menu VRAM (+0x2E000), where `getMenuString(1, section, index, variant)` reads the two-level word-offset (tkmnmes) format. Requests go through an 8-entry async ring (0x1D750D0); TIM sub-files are flagged by `Menu_RegisterTexUpload` for VRAM upload after the read.

Each 20-byte ring entry is `{status, file_id, group_id, dest, callback, cb_arg}`. `Menu_FileLoadQueue_Process` pops entries: a `file_id` ≥ 0 is a **raw mngrphd entry index** (entry = `mngrphd + 8·file_id`); `file_id` = -1 loads the whole named file of `Menu_GroupFileTable[group]` (the PSX menuXXX.ovl names, mngrp.bin for group 17). Bit 0 of the mngrphd seek selects the copy mode: set → raw copy from `seek − 1` (all 118 PC entries); clear → LZS decompression via `File_LoadRange_LZSDecompress` (PSX leftover, unused on PC). Groups 1/8/11/12 share text kind 1 (tkmnmes2, entry 1), the other groups kind 2 (tkmnmes3, entry 2); group 0 text (tkmnmes1, entry 0) lives in its own 0x800 buffer.

### mngrp section consumers (raw mngrphd entry indices)

| Entry | Consumer |
|-------|----------|
| 0/1/2 | tkmnmes1/2/3: group-0 text buffer / shared text kind 1 / kind 2 |
| 3 | Chocobo World menu data (`ChocoboWorld_Prog27Menu_Update`) |
| 7 | Magazine picture sprites (SP2 quad-list format), loaded by the tutorial, magazine and save-point card viewers |
| 9, 10 | face1/face2: the two main-menu UI texture pages, reloaded on every sub-screen exit |
| 12 | magita.tim: tutorial/magazine/item-use background texture |
| 20/24/28/44/48/71/180 | Magazine category bases; page = base + mmag.bin entry byte 23 (Weapons Monthly 1st / Pet Pals / Weapons Monthly monthly / Occult Fan / Cards / Combat King & TT tutorial / Chocobo World) |
| 48 + page | Card Album pages 0-9 (mc00–mc09) |
| 87 | Book/magazine viewer text |
| 90 | Chocobo World intro story (save-point screen) |
| 95 | SeeD written test generic text |
| 96 + test | SeeD written test questions; the engine caps test < 30, so entry 126 ("Test seed 31") is unreachable |
| 127 | TextBox map, loaded to 0x1D82E4C for the info browser |
| 128 + group | TextBox sections 0-5 (info browser pages) |
| 160–167 | Tutorial demo text (junction ×4, GF, Squall/Zell/Rinoa limit breaks) |
| 168–175 | Tutorial demo scripts, paired one-to-one with 160–167 |
| 176/177, 178/179 | Tutorial demo mock save data + mock GF records (two variants A/B) |
| 180 + page | Chocobo World pages from mmag2.bin entries |
| 188–192 | m000–m004.bin refine recipes → buffer 0x1D8A864 |
| 196–200 | m000–m004.msg refine text → buffer 0x1D85864 |
| 204, 205 | Character switch tutorial text + demo script |

### Tutorial demo records

Full format on the [tutorial demo scripts page]({{ site.baseurl }}/technical-reference/menu/mngrp-demo-script/).
The tutorial menu's demo entries come from a table of 12-byte records at 0xB88360:
`{demo_id, program_id, variant, mock_gf_file, mock_save_file, text_file, script_file, flag, help_id, pad[3]}` —
the four file bytes are raw mngrphd entry indices, loaded to menu VRAM +0x2A000 / +0x29000 / +0x1B000 / +0x1F000
respectively before invoking `program_id` (18 = junction demos, 24 = GF demo, 28 = limit break demos with
`variant` 0/1/4 for Squall/Zell/Rinoa, 29 = character switch). The mock save/GF files give the demo its fake
party ("Quetcoatl", Shiva, Ifrit… with 2000 HP, 9999 gil and a preset inventory). The tutorial page-browser list
at 0xB88570 is `{63, 64, 65, -1}` — the three PSX controller diagram TIMs.

Per-menu inits also load extras outside mngrp (magsort.bin, pet_exp.bin, shop.bin, price.bin, mitem.bin…) as standalone files. The standalone copies of tkmnmes and m00X that also exist in the menu archive are loaded by `MenuReadFiles` but never read.

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
| `Menu_RunHostedMenuFrame` (ex `menu_host_run_frame`) | 0x497380 | Menu host state machine (MENU_PHASE) |
| `Menu_StartHostedProgram` | 0x4B3140 | Hosted id → program id mapping |
| `Menu_InvokeProgram` | 0x4BDB30 | Push child program + load its mngrp group |
| `Menu_ProgramTable` | 0xB87ED8 | 33 × {init_fn, mngrp_group} dispatch table |
| `Menu_LoadMngrpGroupAsync` | 0x4AC200 | Group + shared text loading |
| `Menu_LoadMngrpFileAsync` | 0x4AC030 | Queue one mngrp section load by raw mngrphd index |
| `Menu_FileLoadQueue_Process` | 0x4AC0A0 | Pops the async ring, raw copy vs LZS path |
| `Menu_FileLoadQueue` | 0x1D750D0 | 8 × 20-byte async load ring |
| `Menu_GroupFileTable` | 0x1D751C0 | 19 × {dest, name} group file table (menuXXX.ovl / mngrp.bin / init.out) |
| `Menu_InitGroupFileTable` | 0x4ABD80 | Fills Menu_GroupFileTable |
| `File_LoadRange_LZSDecompress` | 0x52D770 | Load file range + LZS decompress (mngrphd seek bit 0 clear) |
| `LZS_DecompressBuffer` | 0x5305D0 | LZS decompressor (4-byte size header, 12-bit window) |
| `getMenuString` | 0x4BD630 | Two-level positional string lookup (ignores count words; entry = 2·index+variant) |
| `mngrphd_binBuffer` | 0x1D2BB18 | Loaded mngrphd.bin (256 × {seek, size}) |
| `TEXT_LAYER` | 0x1D2B330 | 8 × 60-byte text window slots |
| `Text_Window_UpdateStateMachine` | 0x49FEB0 | Typewriter/choice state machine |
| `Text_RenderGlyphs` | 0x4A1570 | Glyph sprite emission |
| `MENU_PHASE` | 0x1D2A280 | Host phase (0 setup / 1 load / 2 result) |
| `menu_id` | 0x1D2BB98 | Requested menu ID |
| `menu_sub_id` | 0xB87798 | Menu sub-parameter (save-enable bits...) |
| `menu_result_flags` | 0x1D2BB9C | Result returned to the module handler |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
