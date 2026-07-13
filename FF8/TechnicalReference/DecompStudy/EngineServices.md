---
layout: default
title: Engine services (I/O, timing, input)
parent: Main
permalink: /technical-reference/main/engine-services/
---

1. TOC
{:toc}

# Engine services

Cross-cutting runtime services used by every module: archive/file I/O, frame timing, and input. Complements [Engine startup and main loop]({{ site.baseurl }}/technical-reference/main/engine-startup-and-main-loop/). All addresses are for FF8_EN.exe (2000 PC release), image base 0x400000.

## Archive I/O (FS/FI/FL)

Every file access goes through a **virtual file layer** (`FILE_HANDLE_TABLE`): `Archive_OpenVirtualFile` resolves a path either to a loose file on disk (CRT `_open`) or to an entry inside an FS archive, and read/seek/close operate on the virtual handle.

* An opened archive (`struc_flfifs`) holds the `.fl` path list (loaded as a token list), the open `.fs` data file and the `.fi` index buffer. An FI record is 12 bytes: `{u32 uncompressedSize, u32 fsOffset, u32 compression}`. FL lines are matched case-insensitively.
* Compression 1 = **LZSS** (`Archive_LZSSDecompress`, 12-bit window with base offset 0xFEE, run length 3–18, out-of-window bytes read as zero, stream prefixed by a u32 size). A compressed file is decompressed **whole** on first read and cached on the handle.
* A static configuration table (800-byte stride, kind ids in `ARCHIVE_KIND_TABLE`) maps path substrings to archives. Kind 0 (FIELD) is special: field sub-archives are **nested** — the requested sub-archive's `.fi/.fl/.fs` are extracted from `field.fs` into `<CurrentDir>\temp.fi/.fl/.fs` (cached per subfolder) and then opened as a normal archive. Other kinds open their archive directly.
* Path table: `CopyDataPathsStrings` builds 260-byte-stride entries — app root, `Data\`, then per-folder paths (Sound, Music, Menu, Battle, Field, world Data root `PATH_DATA_DIR`). World paths pass through `getWorldFsPath`, which implements the 2-character `;x` elision used to strip language tags from stored paths.

| Function | Address |
|----------|---------|
| `Archive_OpenVirtualFile` / `Archive_SeekVirtualFile` / `Archive_ReadVirtualFile` / `Archive_CloseVirtualFile` | 0x51B4E0 / 0x51BDC0 / 0x51BE40 / 0x51BF50 |
| `Archive_OpenFsArchive` | 0x40EFAA |
| `Archive_FindFileEntry` (FL match → FI record) | 0x40F06B |
| `Archive_ReadFileData` (raw or LZSS) | 0x40F52C |
| `Archive_LZSSDecompress` | 0x40F852 |
| `Archive_LoadFlPathList` / `Archive_FL_GetPathByIndex` | 0x428B6E / 0x428C1A |
| `IO_OpenFile` (disk-or-archive resolution) | 0x40E33A |
| `File_WriteBufferToDisk` (temp.* extraction) | 0x40EB71 |

## Frame timing

The engine has two timer backends selected by `USE_TIME_RDTSC`: the raw CPU **RDTSC** counter, or `timeGetTime` (1 kHz). RDTSC is only enabled when `CPU_DetectProcessor` (full CPUID identification at startup) reports an Intel P5/P6 or AMD K6/K7 class CPU; its frequency is calibrated against QueryPerformanceCounter during a 100 ms busy-wait at realtime priority (`CPU_MeasureTscFrequency`) and stored in `game_obj->countspersecond`.

Frame pacing:

* `Time_SetTargetFrameRate(fps)` — each module sets its own rate (world = 30.5 fps, field/battle = via their init) as `FRAME_PERIOD_TICKS = countspersecond / fps`.
* `Time_WaitNextFrame` — the limiter: sleeps off the remainder of the period when the frame was fast, or returns "over budget" carrying the overshoot (clamped to one period) and amortizing it over the next two frames.
* The menu/title modules bypass the limiter and busy-wait on a fixed 60 fps period (`FRAME_PERIOD_TICKS_60FPS`).

## Input

`Input_ProcessInput` (pumped every frame from `IsWindowNOTActive`) polls DirectInput keyboard (256 DIK bytes), mouse, and up to two joysticks, then builds a 32-bit state per pad through the remap table at 0x1CD0208 (112 bytes per pad = 3 alternative binding banks × 32 codes; code < 0xDE = DIK scancode, 0x6A–0x6C = mouse buttons, 0xE0+n = joystick button, 0xFC–0xFF = stick Y−/Y+/X−/X+). Rising edges are computed as `cur & ~(prev & cur)`, with a keyboard-style auto-repeat layer on top.

The resulting 16-bit game pad mask **is the PSX digital pad layout** (verified by `Input_WritePsxPadButtons`, which converts it active-low into an emulated PSX pad buffer):

| Bit | Button | Bit | Button |
|-----|--------|-----|--------|
| 0x0001 | L2 | 0x0100 | Select |
| 0x0002 | R2 | 0x0800 | Start |
| 0x0004 | L1 | 0x1000 | Up |
| 0x0008 | R1 | 0x2000 | Right |
| 0x0010 | Triangle (Cancel) | 0x4000 | Down |
| 0x0020 | Circle (Menu) | 0x8000 | Left |
| 0x0040 | Cross (Confirm) | | |
| 0x0080 | Square (Examine) | | |

`remap_pad_input` further remaps bits 0–11 through the player's button config in the savemap settings; the D-pad nibble 0xF000 passes through unchanged. The world map keeps its own double-buffered copy (`world_input_states[2]` + `world_input_frame_parity`) with hold-to-repeat after 30 time units.

Debug key combos (raw DIK state, held 5 frames): **Ctrl+R** = soft reset, **Ctrl+Q** = quit. The bounds-check of that code still contains the developer string "William please check this".

| Function | Address |
|----------|---------|
| `Input_ProcessInput` | 0x467D10 |
| `Input_PollKeyboard` / `Input_PollMouse` / `Input_PollJoysticks` | 0x468D80 / 0x468B60 / 0x4692B0 |
| `Input_GetPadState` / `Input_UpdateAutoRepeat` | 0x468500 / 0x468540 |
| `Input_WritePsxPadButtons` | 0x56D990 |
| `World_PollInputBeginFrame` | 0x559240 |
| `InputKeyboardResetCombination` (Ctrl+R / Ctrl+Q) | 0x4A2E50 |
| `Time_SetTargetFrameRate` / `Time_WaitNextFrame` | 0x4020C0 / 0x4020F0 |
| `CPU_DetectProcessor` / `CPU_MeasureTscFrequency` | 0x569E70 / 0x56AD8E |
