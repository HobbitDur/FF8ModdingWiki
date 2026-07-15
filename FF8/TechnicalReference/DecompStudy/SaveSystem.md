---
layout: default
title: Save system (PC)
parent: Main
permalink: /technical-reference/main/save-system/
---

1. TOC
{:toc}

# Save system — PC runtime and file format

How FF8 PC saves work: the memcard-emulation layer, the exact file format with checksum, the load-menu preview block, new-game initialization and Chocobo World transfer. Addresses for FF8_EN.exe, image base 0x400000.

## PSX memcard emulation

The PC build keeps the PSX memory-card code and shims file names: internal PSX name `BASLUSP008920426NN` maps to `{GameDir}\SAVE\SLOT1|SLOT2\saveNN` (NN = 01..30), and `BASLUSP00892C0426` maps to `{GameDir}\save\chocorpg`. Two emulated "cards" (port 0 = SLOT1, port 16 = SLOT2), 30 saves each. The save/load "memory card" screen is one shared state machine (`Save_CardScreen_Update`) running in load mode (title Continue) or save mode (save points).

## Save file format

On disk a save is `[u32 compressedSize][LZSS stream]` (standard FF8 LZSS), decompressing to a full **8192-byte PSX save block**:

| File offset | Content |
|-------------|---------|
| 0–383 | PSX header: `"SC"`, icon info, SJIS title (playtime "HH:MM" patched in as full-width digits), icon CLUT/frames |
| 384–5411 | **savemap block** — verbatim copy of 5028 bytes from `SG_CHECKSUM` |
| 5412–8191 | zero padding |

* **Checksum**: CRC-16/CCITT (poly 0x1021, init 0xFFFF, final NOT; table-driven, `Save_ComputeChecksumCRC16CCITT`) over savemap+80..+5023 (4944 bytes), stored at savemap+0 **and** duplicated at savemap+5024. No other obfuscation or encryption.
* **Two-phase commit**: the file is first written raw with magic 0xFFFF (and a "write error" SJIS title from the header templates), then the first 512 bytes are rewritten with magic **0x08FF** + final title and the whole file is LZSS-recompressed in place (`Save_RecompressSaveFileLZSS`). A save interrupted between phases is detectable by its 0xFFFF magic.
* **Load**: requires `CRC(buf+80, 4944)` to equal both stored copies; then 5028 bytes are copied to `SG_CHECKSUM`, the RNG is reseeded from save statistics, and `engine_restore_game_status` recomputes derived character/GF stats. No version or region checks beyond the magic.
* The PSX read-back verify states survive in the code but are **dead on PC**, and a leftover **debug quick-loader** (`Save_DebugLoadSaveFileByPath_UNUSED`) loads a raw file by path expecting magic 0x0FF8 with no CRC check.

## Preview block (savemap+0..127)

What the load menu shows, refreshed at save time by `Save_BuildSaveFileImage`:

| Offset | Size | Field |
|--------|------|-------|
| +0 | u16 | CRC-16 checksum |
| +2 | u16 | magic 0x08FF (0xFFFF = interrupted save) |
| +4 | u16 | location name ID |
| +6 / +8 | u16 | leader current / max HP |
| +10 | u16 | save count |
| +12 | u32 | gil (Laguna's gil when the flag says so) |
| +16 | u32 | playtime in seconds (display cap 99:59) |
| +20 | u8 | leader level |
| +21 | u8×3 | party portrait IDs (0xFF = empty) |
| +24/+36/+48/+60 | 12 B each | Squall / Rinoa / Angelo / Boko names |
| +72 | u32 | current disc |
| +76 | u32 | save ordinal (monotonic; the newest save gets the default cursor) |

## New game and playtime

* **New game**: `Savemap_Clear` zeroes the savemap, then `Savemap_LoadNewGameDefaults_InitOut` loads the file **`init.out`** directly into savemap+80 — that file *is* the new-game savemap and can be edited to change starting inventory, stats, flags…
* **Playtime**: `Savemap_TickGameTimeAndCountdown`, called from every module main loop, adds 2191 per frame to an accumulator; every 0x20000 overflow = +1 second (131072/2191 ≈ 59.82 Hz — the NTSC vsync rate, so playtime advances at PSX speed regardless of module frame rate). The script COUNTDOWN uses the same mechanism.

## Why the load screen looks slow (the progress bar)

The data is loaded almost instantly — the visible slowness is entirely inherited PSX memory-card theater:

* **All I/O is synchronous behind an async façade.** `Save_EmuMC_ReadFile` performs the whole read (including LZSS decompression of the full 8 KB) in one call, then the PSX-style event shim reports completion — so every "async card operation" is already finished by the first poll.
* **The card screen is a frame-locked state machine** (60 fps menu loop, one state transition per frame). Scanning a slot walks its 30 save files one at a time: issue preview read (state 25) → poll completion (state 27) → card status re-check (state 26) → next file. Even with instant I/O that's 2–3 frames per file ≈ 1–1.5 s for a slot.
* **The progress bar is an animation, not a measurement.** It advances at a fixed **64/4096 per frame** — a minimum of 64 frames (~1.07 s) to fill — and is merely *capped* by the scan position (`(fileIndex+2)×256`). Faster I/O cannot make it faster.
* Leftover PSX pacing shims add structure but little time on PC: the card-test state machine counts down 180 polls (`EmuMC_PollCardStatePaced`, from the PSX card-detection timing), per-file completion has a 60-frame timeout, and `EmuMC_WaitCardEvents180` spins up to 180 iterations — all designed around a real memory card that read 128-byte frames one interrupt at a time.
* Loading the selected save itself (state 74–76: one 5120-byte read + CRC check + memcpy into the savemap) completes in a couple of frames — the multi-second experience is the slot scan plus the bar animation.

A speed-up patch would (a) let the bar cap jump immediately (scan several files per frame — the state machine can safely process multiple files per tick since I/O is synchronous) and (b) raise the bar's 64/frame fill rate.

## Chocobo World

`save\chocorpg` is `[u32 size][LZSS]` of 514 bytes: u16 magic 0x08FF + 512 bytes of Pocketstation world data. The savemap keeps a 64-byte mirror (`SG_CHOCOBO_WORLD_DATA`, savemap+4960) with a once-randomized world ID. Export writes a 128-byte region into chocorpg (converting Boko's level, clearing collected item counters); import decodes item-class counts into (item, quantity) pairs added to the inventory and merges event/level data back. The transfer screen is menu program 27, invoked from the card screen.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `Save_CardScreen_Update` | 0x4E3090 | Save/load memory-card screen state machine |
| `Save_BuildSaveFileImage` | 0x4E2EF0 | Builds the preview-block image at save time |
| `Save_ComputeChecksumCRC16CCITT` | 0x500310 | CRC-16/CCITT checksum |
| `Save_EmuMC_WriteFile` | 0x4C5500 | Emulated memcard file write |
| `Save_EmuMC_ReadFile` | 0x4C5B00 | Emulated memcard file read |
| `Save_EmuMC_CreateFile` | 0x4C4FA0 | Emulated memcard file create |
| `Save_DebugLoadSaveFileByPath_UNUSED` | 0x4E2DE0 | Leftover debug quick-loader, dead code path |
| `Save_EmuMC_OpenMapNameToPCPath` | 0x4C6BD0 | Maps PSX save name to PC path |
| `Save_RecompressSaveFileLZSS` | 0x4C6E50 | Second-phase LZSS recompression of the save file |
| `Archive_LZSSCompress` | 0x40FE1D | LZSS compressor |
| `Savemap_Clear` | 0x56D9F0 | Zeroes the savemap |
| `Savemap_LoadNewGameDefaults_InitOut` | 0x56DA10 | Loads `init.out` into the new-game savemap |
| `Savemap_TickGameTimeAndCountdown` | 0x4701B0 | Playtime/countdown accumulator tick |
| `ChocoboWorld_CheckChocorpgGetId` | 0x4C63C0 | Chocobo World transfer / world ID handling |
| `engine_restore_game_status` | 0x495EF0 | Recomputes derived character/GF stats after load |
| `SG_CHECKSUM` | 0x1CFDC58 | Global variable/data, not a function — live savemap buffer |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000).
