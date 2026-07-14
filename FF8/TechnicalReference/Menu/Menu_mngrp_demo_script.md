---
layout: default
parent: Menu
title: Mngrp Tutorial Demo Scripts
permalink: /technical-reference/menu/mngrp-demo-script/
---

# Tutorial demo scripts

The tutorial menu ("TUTORIAL" in the main menu) offers demo entries that play back a guided demonstration of a
menu screen: the Junction demos, the GF demo, the Squall/Zell/Rinoa limit break demos and the character switch
demo. Each demo runs the **real menu program** on a **fake savegame**, driven by a small **script that fakes
controller input** and shows caption windows.

All the data lives in [mngrp.bin](../mngrpbin-file-format/) sections (raw [mngrphd](../mngrphdbin-file-format/)
entries 160-179 and 204-205).

## Demo record table

The nine demos come from a table of 12-byte records in the executable (`Menu_TutorialDemoRecords`, 0xB88360):

| Offset | Type  | Value          | Description                                                        |
|--------|-------|----------------|----------------------------------------------------------------------|
| 0      | Byte  | demo_id        | Tutorial menu entry id (5-13)                                      |
| 1      | Byte  | program_id     | Menu program invoked: 18 = junction demos, 24 = GF demo, 28 = limit break demos, 29 = character switch |
| 2      | Byte  | variant        | Sub-mode for the program (limit breaks: 0 = Squall, 1 = Zell, 4 = Rinoa; junction: 0-3) |
| 3      | Byte  | mock_gf_file   | Raw mngrphd index of the mock GF records (177 or 179)              |
| 4      | Byte  | mock_save_file | Raw mngrphd index of the mock save data (176 or 178)               |
| 5      | Byte  | text_file      | Raw mngrphd index of the caption text, a [string section](../mngrp-string-section/) (160-167, 204) |
| 6      | Byte  | script_file    | Raw mngrphd index of the demo script (168-175, 205)                |
| 7      | Byte  | flag           | 1 = build the demo party from the real save's available characters (set only for the character switch demo) |
| 8      | Byte  | help_id        | Description string id in the tutorial menu (62-70)                 |
| 9-11   | Bytes | padding        |                                                                    |

The four files are loaded to menu VRAM +0x2A000 / +0x29000 / +0x1B000 / +0x1F000 respectively, then the
program starts with the demo script active.

## Mock save data

Before a demo starts, the tutorial menu **backs up the real save** into menu VRAM (characters +0x27490, GFs
+0x27050, settings +0x27AE0, party block +0x27AF4), then overwrites the live savemap with the mock files:

* **Mock characters** (raw 176/178): **8 records of 152 bytes**, the savemap character record format
  (Squall...Edea). On load the current HP is forced to 9999 and status effects are cleared.
* **Mock GF records** (raw 177/179): **16 records of 68 bytes**, the savemap GF record format (name in FF8 text,
  experience, HP, abilities...). HP is forced to 9999 and each **GF name is replaced by the name from the real
  save's backup**, so the development names left in the file (misspellings such as "Quetcoatl") never show
  in game.

Variant A (176/177) is used by the junction, magic junction, GF and limit break demos; variant B (178/179) by the
elemental junction, status junction and character switch demos. When the demo ends, the backup is copied back
over the savemap.

## Script format

A demo script is a stream of **UInt16 little-endian words**. The high nibble is the opcode, the low 12 bits the
operand:

| Opcode | Name               | Effect                                                                                     |
|--------|--------------------|----------------------------------------------------------------------------------------------|
| 0x1    | HOLD_BUTTON        | OR `1 << (operand & 0xFF)` into the synthesized pad word for this frame                    |
| 0x2    | WAIT_WINDOW_READY  | Wait until the caption window is ready                                                     |
| 0x3    | SHOW_TEXT          | Open a caption window centered on (X, Y) with string `text_index` of the caption section   |
| 0x4    | HIDE_TEXT          | Close the caption window                                                                   |
| 0x5    | SET_TEXT_INDEX     | text_index = operand                                                                       |
| 0x6    | SET_TEXT_X         | Caption center X = operand                                                                 |
| 0x7    | SET_TEXT_Y         | Caption center Y = operand                                                                 |
| 0x8    | WAIT_CONFIRM       | Wait for the player: confirm advances, cancel aborts the whole demo                        |
| 0x9    | WAIT               | Wait operand frames                                                                        |
| 0xA    | WAIT_ANIM          | Wait until the window open/close animation finishes                                        |
| 0xF    | END                | Stop the demo script (input returns to the player)                                        |

Each frame, the interpreter replaces the pad read: the word built by HOLD_BUTTON opcodes is written into the
engine's pad state, so the hosted menu program navigates as if the player pressed those buttons. Ops 0x1 and
0x4-0x7 execute immediately (several per frame); the wait ops yield until their condition is met.

### Example (start of the Junction demo script, raw section 168)

```
0000: 60C0  SET_TEXT_X 192
0002: 7068  SET_TEXT_Y 104
0004: 5000  SET_TEXT_INDEX 0
0006: 903C  WAIT 60
0008: 3000  SHOW_TEXT
000A: 2000  WAIT_WINDOW_READY
000C: 8000  WAIT_CONFIRM
000E: 4000  HIDE_TEXT
0010: A000  WAIT_ANIM
0012: 903C  WAIT 60
0014: 5001  SET_TEXT_INDEX 1
...
```

## Engine addresses (FF8 PC 2000, FF8_EN.exe)

| Address   | Name                          | Role                                                        |
|-----------|-------------------------------|---------------------------------------------------------------|
| 0x4BE100  | Menu_ReadPad_OrRunDemoScript  | Per-frame input hook: runs the script VM when a demo is active, otherwise reads the real pad |
| 0x4BE050  | Menu_DemoScript_Start         | Arms the VM with a script buffer and a caption text section |
| 0xB88360  | Menu_TutorialDemoRecords      | The 9 × 12-byte demo records                                |
| 0xB88570  | Menu_TutorialPageList         | Tutorial page-browser TIM list {63, 64, 65, -1}             |
| 0x1D76BC0 | Menu_DemoScript_IP            | Current script word pointer                                 |
| 0x1D76AB4 | Menu_DemoScript_TextSection   | Caption string section pointer                              |
| 0x1D77078 | Menu_DemoScript_Active        | 1 while a demo script drives the input                      |
| 0x1D76B40 | Menu_DemoScript_Cancelled     | Set when the player cancels the demo                        |
| 0x4C99E0  | Menu_Demo_ApplyMockSave       | Copies the mock character/GF records over the live savemap  |
| 0x4CADA0  | Menu_Demo_RestoreRealSave     | Restores the real save backup when the demo ends            |
| 0x1D771AC | Menu_Demo_UseRealRosterFlag   | Record flag byte: demo party from the real roster           |
