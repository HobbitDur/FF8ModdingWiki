---
layout: default
title: GTE emulation layer
parent: Main
permalink: /technical-reference/main/gte-emulation/
---

1. TOC
{:toc}

# GTE emulation layer

The PC port keeps the PlayStation's geometry pipeline: instead of rewriting the renderers for a
CPU, it ships a **software emulation of the PSX GTE** (Geometry Transformation Engine, COP2) and
lets the original PSX-shaped code run on top. The emulation is faithful down to the register
numbering, the instruction encodings and the FLAG register's saturation bits.

Every renderer in the game sits on this layer — battle models, spell and GF effects, field
characters, the world map. Reading any of them means reading GTE code, so this page is the
prerequisite for pages like [Magic effect anatomy]({{ site.baseurl }}/technical-reference/battle/magic-effect-anatomy/)
and the [Cure case study]({{ site.baseurl }}/technical-reference/battle/cure-case-study/).

> **Executable.** Addresses here are `FF8_EN.exe`, image base `0x400000`. The 2000 PC and 2013
> Steam English executables are the same binary, so these agree with both the battle case studies
> and the rest of DecompStudy.

## Why it matters

Two practical consequences:

- **The old names in this cluster are wrong.** Before the GTE was identified, the register file
  was read as camera state, so it acquired names like `CAM_POSITION`, `CAMERA_POS_X`,
  `Cam_xyz2_y_float`, `World_CameraZoom`, `setCamPos`. None of them are camera data. They are the
  MAC accumulator, the rotation matrix, the projection distance and a result read. Treat any
  surviving `Cam*`/`camera*` name near the addresses below as suspect.
- **The code reads as PSX assembly, not as C.** A function that looks like an opaque sequence of
  `sub_45Exxx` calls is usually a short, ordinary GTE program: load a matrix, load a vector, run an
  op, read the result.

## Register files

Both files are plain dword arrays, indexed exactly as the hardware numbers them. Each register's
index is confirmed arithmetically from its address, not assumed.

### Data registers (cop2d) — base `0x1CA8A10`

| Reg | Name | Role |
|---|---|---|
| dr0–5 | `GTE_VXY0` `GTE_VZ0` `GTE_VXY1` `GTE_VZ1` `GTE_VXY2` `GTE_VZ2` | the three input vectors |
| dr7 | `GTE_OTZ` | average depth, for ordering-table insertion |
| dr8 | `GTE_IR0` | depth-cue / interpolation factor |
| dr9–11 | `GTE_IR1` `GTE_IR2` `GTE_IR3` | the accumulator vector (saturated) |
| dr12–14 | `GTE_SXY0` `GTE_SXY1` `GTE_SXY2` | screen-coordinate FIFO (packed `(y<<16)\|x`) |
| dr16–19 | `GTE_SZ0` … `GTE_SZ3` | screen-depth FIFO |
| dr24 | `GTE_MAC0` | scalar result (NCLIP area, depth) |
| dr25–27 | `GTE_MAC123` | vector result — **the struct formerly named `CAM_POSITION`** |

### Control registers (cop2c) — base `0x1CA927C`

| Reg | Name | Role |
|---|---|---|
| ctrl0–4 | `GTE_CTRL_MATRICES` | rotation matrix R (packed word pairs) |
| ctrl5–7 | `GTE_TRX` `GTE_TRY` `GTE_TRZ` | translation vector |
| ctrl8–12 | (light matrix) | second general matrix — **bone matrices live here**, see below |
| ctrl13–15 | (BK) | background colour vector |
| ctrl16–23 | (colour matrix, FC) | unused by the code studied so far |
| ctrl24/25 | `GTE_OFX_hi` `GTE_OFY_hi` | screen offset (the `_hi` symbols are the integer halves of ctrl24/25) |
| ctrl26 | `GTE_H_Zoom` | **projection distance H** (was `World_CameraZoom`) |
| ctrl27/28 | `GTE_DQA` `GTE_DQB` | depth-cue coefficients |
| ctrl29/30 | `GTE_ZSF3` `GTE_ZSF4` | Z-average scale factors (tri / quad) |
| ctrl31 | `GTE_FLAG` | saturation + error flags |

Writes go through `GTE_WriteControlReg`. Writing R (ctrl0–4) additionally refreshes a **float
mirror** of the rotation matrix at `0x1CA9234`–`0x1CA9254`, which the float implementations of
RTPS/RTPT/OP multiply directly. The mirror stores each row **reversed** (`Rf13, Rf12, Rf11`, then
`Rf23, Rf22, Rf21`, then `Rf33, Rf32, Rf31`) — a detail worth remembering when reading those
functions, since maintaining that mirror is why the control-register writer is ~850 bytes long.

## The MVMVA command word

`GTE_MVMVA` (multiply vector by matrix and vector add) is the workhorse, and it takes **the literal
COP2 instruction word** as its argument — the encoding the PSX would have executed. The emulator
decodes the hardware bitfields:

| Bits | Field | Meaning |
|---|---|---|
| `>>17 & 3` | mx | matrix select → `GTE_CTRL_MATRICES[8*mx]` (0 = rotation, 1 = light, 2 = colour) |
| `>>15 & 3` | v | vector select (0–2 = V0/V1/V2, 3 = the IR accumulator) |
| `>>13 & 3` | cv | translation add (0 = TR, 1 = BK, 3 = none) |
| `& 0x80000` | sf | shift — the `>>12` fixed-point scale |
| `& 0x3F` | fn | function code `0x12` = MVMVA |

The exe ships a **wrapper table** of nine one-line stubs, one per preset command — the equivalent of
the PsyQ SDK's MVMVA macros. The commands are enumerated as `GTECommand`:

| Wrapper | Command | Operation |
|---|---|---|
| `GTE_MVMVA_RotV0_Tr` (and a duplicate `_2`) | `GTE_CMD_MVMVA_ROT_V0_TR` = `0x480012` | R×V0 + TR — the standard world transform |
| `GTE_MVMVA_RotV0` | `..._ROT_V0` = `0x486012` | R×V0 |
| `GTE_MVMVA_RotIR` | `..._ROT_IR` = `0x49E012` | R×IR — chained rotations |
| `GTE_MVMVA_LightV0_Bk` | `..._LIGHT_V0_BK` = `0x4A2012` | L×V0 + BK |
| `GTE_MVMVA_LightV1_Bk` | `..._LIGHT_V1_BK` = `0x4AA012` | L×V1 + BK |
| `GTE_MVMVA_LightV2_Bk` | `..._LIGHT_V2_BK` = `0x4B2012` | L×V2 + BK |
| `GTE_MVMVA_LightIR` | `..._LIGHT_IR` = `0x4BE012` | L×IR |
| `GTE_MVMVA_ColorV0` | `..._COLOR_V0` = `0x4C6012` | C×V0 |

> **IDA trap.** Two of these constants (`0x480012` and `0x4C6012`) are valid addresses inside
> `.text`, so IDA renders them as **false offsets** (`offset off_480012`, and the worse
> `offset loc_4C600F+3` — a phantom reference into the middle of an instruction). They are
> immediates, not pointers. Applying the `GTECommand` enum to the operand fixes the display and
> stops re-analysis from guessing again.

## Operations

| Op | What it does |
|---|---|
| **RTPS** | Rotate/Translate/Perspective for one vertex: `IR = clamp(R×V0 + TR)` → SZ FIFO push → `screen = IR × (H/2 / SZ3) × 8 + OF` (clamped to ±`0x1FF8`) → SXY FIFO push → `IR0 = clamp((H×8/SZ3)×DQA + DQB, 0..0x1000)`, the depth-cue factor. |
| **RTPT** | The three-vertex version — fills the whole SXY FIFO in one call. |
| **NCLIP** | `MAC0 = SX0(SY1−SY2) + SX1(SY2−SY0) + SX2(SY0−SY1)` — twice the signed screen area. `> 0` means front-facing. **The universal backface cull.** |
| **AVSZ3 / AVSZ4** | `OTZ = ZSF × (ΣSZ) >> 12` — the average depth used to pick an ordering-table bucket. |
| **OP** | Outer (cross) product: `MAC/IR = D × IR`, where D is the rotation matrix **diagonal** (loaded via `GTE_SetRotDiagonal`). |

All of them reproduce the hardware FLAG bits on overflow: `0x81000000` (MAC1/IR1), `0x80800000`
(IR2), `0x400000` (IR3), plus RTPS's `0x80040000` / `0x80004000` / `0x80002000` for SZ and screen
saturation.

## Reading renderer code

Three idioms cover most of it:

- **Vertex transform.** `GTE_SetRotMatrix_W` + `GTE_SetTransVector_W` load a bone matrix, then
  `GTE_MVMVA_RotV0_Tr` transforms a point and `GTE_ReadMAC123` collects it. Many model renderers
  instead load bone matrices into the **light-matrix bank** (ctrl8–12) and transform with
  `GTE_MVMVA_LightV0_Bk` — the light matrix is simply a second general-purpose matrix, nothing to
  do with lighting there.
- **Polygon emission.** Triangles: `GTE_LoadV012` → RTPT → NCLIP → cull if `MAC0 <= 0` → AVSZ3 →
  insert at the OT bucket. Quads: RTPT for the first three vertices, then one RTPS plus
  `GTE_ReadSXY2` for the fourth, then AVSZ4. `GTE_StoreSXY012_PolyFT3`/`_PolyGT3` write the screen
  coordinates straight into a GPU packet at the FT3/GT3 vertex strides.
- **Matrix building.** `GTE_LoadIRFromMatrixColumn` / `GTE_StoreIRToMatrixColumn` walk a matrix
  column-wise (stride 3) through `GTE_MVMVA_RotIR`, composing rotations without touching memory in
  between.

The ordering table itself lives at `g_Battle_FrameRenderListBase + 68`: 4095 four-byte buckets,
ending at `+16447`. The one-past-the-end bucket `+16448` is used deliberately — it is where the
battle blob shadow inserts, i.e. behind everything.

## Function reference

| Address | Name | Role |
|---|---|---|
| 0x45D7F0 | `GTE_WriteControlReg` | control-register write; also maintains the float R mirror |
| 0x460860 | `GTE_MVMVA` | the MVMVA emulator (takes a `GTECommand` word) |
| 0x4607D0–0x46085B | `GTE_MVMVA_*` | the nine preset-command wrappers |
| 0x45FAA0 | `GTE_RTPS` | rotate/translate/perspective, one vertex |
| 0x45FE10 | `GTE_RTPT` | …three vertices |
| 0x45EE10 | `GTE_NCLIP` | signed screen area (backface cull) |
| 0x45E5C0 / 0x45E610 | `GTE_AVSZ3` / `GTE_AVSZ4` | average depth for OT insertion |
| 0x45E820 | `GTE_OP` | outer/cross product |
| 0x45DE00 / 0x56BAE0 | `GTE_SetRotMatrix` / `_W` | load R (ctrl0–4) |
| 0x45DEF0 / 0x56BB30 | `GTE_SetTransVector` / `_W` | load TR (ctrl5–7) |
| 0x45DE50 | `GTE_SetLightMatrix` | load the light matrix (ctrl8–12) |
| 0x45DCF0 | `GTE_SetBackgroundVector` | load BK (ctrl13–15) |
| 0x45DC70 | `GTE_SetRotDiagonal` | load the R diagonal (for `GTE_OP`) |
| 0x45DF80 | `GTE_LoadV0` | load V0 from an `FF8Coordinate` |
| 0x45DFE0 | `GTE_LoadV012` | load all three vectors (RTPT input) |
| 0x45E060 | `GTE_LoadV0FromDwords` | load V0 from dword triple |
| 0x45DC40 | `GTE_LoadIR123` | load the IR accumulator |
| 0x45E180 / 0x45E470 | `GTE_LoadIRFromMatrixColumn` / `GTE_StoreIRToMatrixColumn` | column-wise matrix walk |
| 0x45E450 | `GTE_ReadMAC123` | read the vector result (**was `setCamPos`** — it reads, not sets) |
| 0x45E3C0 / 0x45E3D0 | `GTE_ReadMAC0` / `GTE_ReadOTZ` | read scalar results |
| 0x45E210 | `GTE_ReadFLAG` | read the flag register |
| 0x45E260 / 0x45E270 / 0x45E2A0 | `GTE_ReadSXY2` / `GTE_ReadSXY012_Split` / `GTE_ReadSXY012` | read the screen FIFO |
| 0x45E3E0 | `GTE_StoreIR123` | store the accumulator to memory |
| 0x45E2E0 / 0x45E300 / 0x45E320 / 0x45E340 | `GTE_StoreSXY012_PolyFT3` / `_PolyGT3` (+`_2`) | write screen coords into GPU packets |

Globals: data file `0x1CA8A10`, control file `0x1CA927C` (`GTE_CTRL_MATRICES`), float R mirror
`0x1CA9234`–`0x1CA9254`, `GTE_FLAG` `0x1CA92F8`.

## Open questions

- **RTPS and RTPT** are identified from their complete input/output signature — the SZ/SXY FIFO
  pushes, the perspective divide and the DQA/DQB depth cue are unambiguous — rather than from a
  line-by-line reading of their float math. If a subtle rounding detail ever matters, read them in
  full first.
- **`GTE_H_Zoom`'s old name** (`World_CameraZoom`) suggests the world-map code references it as a
  zoom value. The rename is correct — it is the GTE's projection distance H — but the world-map
  module deserves a check before reasoning about zoom behaviour there.
- **ctrl16–23** (colour matrix, FC) and data registers dr6, dr15, dr20–23 (the RGB FIFO) are
  untouched by the code studied so far, and so are unnamed.
