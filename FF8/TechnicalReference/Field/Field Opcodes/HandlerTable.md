---
layout: default
title: Opcode handler table (PC)
parent: Field Opcodes
grand_parent: Field
permalink: /technical-reference/field/field-opcodes/handler-table/
---

1. TOC
{:toc}

# Field script opcode handler table (FF8_EN.exe)

This page maps every field script opcode to its handler function in the PC executable, extracted from the dispatch table used by the script VM (see [Field module runtime](/technical-reference/field/field-module-runtime/) for the VM itself). The table at `FIELD_SCRIPT_OPCODE_TABLE` (0xB8DE94) has exactly **376 entries (opcodes 0x000-0x177)**; every entry points to a unique handler.

## Handler calling convention

Handlers receive the entity script context and the instruction's 24-bit parameter, and return a flag byte to the VM:

| Return bit | Meaning |
|-----------|---------|
| 1 | Yield — stop executing this entity until next frame |
| 2 | Advance the instruction pointer |
| 4 | Keep the "ready" bit of the current priority (used by RET/GJMP: value 4 = jump performed, IP already set) |

Common return values: 2 = done+continue, 1 = wait (retry same instruction next frame), 3 = done+yield, 4 = jump performed, 5 = wait without consuming.

Inside the entity context: the argument stack (dwords, stack index at +388), the eight **I registers** at +320 (script locals; I[0] doubles as the result register filled by ISTOUCH/ASK/RND/GETINFO...), current IP at +374 (in instruction words), per-priority saved IPs at +356 and the priority/ready bytes at +372/373.

## Corrections to the historical opcode list

The executable's own symbol names revealed several discrepancies with the historical opcode list; **the wiki opcode pages have been renumbered and renamed accordingly**:

* **Opcodes 0x16A-0x177 were shifted**: the historical list placed HASITEM at 0x170 up to SHOWTUTORIAL at 0x183, but on PC the same opcodes are **0x16A (HASITEM) through 0x177 (SHOWTUTORIAL)** — six lower. Opcodes 0x178-0x183 do not exist on PC (the table ends at 0x177).
* Spelling fixes from the exe symbols: `MAPJUMP0` (digit zero, not O), `SALARYON/SALARYOFF/SALARYDISPON/SALARYDISPOFF` (not SARALY*), `KEYSIGNCHANGE` (not KEYSIGHNCHANGE). Opcode 0x073 is `SCSROLL` in the original symbols — likely Square's own typo for CSCROLL; the wiki keeps CSCROLL.
* Tools that follow the old numbering still display the shifted values; when comparing with such tools, subtract 6 from opcode numbers at or above their 0x170.

## Formerly-unknown opcodes identified

| Opcode | Old name | Actual behavior (PC) |
|--------|----------|----------------------|
| 0x004 | — | **GJMP**: push return IP, jump to a script entry point (global jump) |
| 0x167 | UNKNOWN2 | Head pose: rotate head joint down (pitch 207), arg 0/1/2 = straight/right/left, 30 frames |
| 0x168 | UNKNOWN3 | Head pose: same, upward (pitch −207) |
| 0x169 | UNKNOWN4 | Sets the "move without walkmesh clipping" entity flag (+576) from the stack |
| 0x16F | UNKNOWN10 | **PC stub** — writes the result of a return-0 stub (PSX music status) |
| 0x170 | UNKNOWN11 | Turn to face a party character (by savemap party-entity map) at given speed |
| 0x171 | UNKNOWN12 | Sync-wait until the 0x170 turn completes |
| 0x172 | UNKNOWN13 | Pops one arg, returns the sound-effect attribute check (SdEffectAttrCheck) in I[0] |
| 0x174 | UNKNOWN15 | Sets the jump-duration divisor (LINKED_TO_LADDER global, default 28) used by JUMP/JUMP3 |
| 0x176 | UNKNOWN17 | **PC stub** — pops one arg, calls a null function |

Other undocumented-but-named opcode families now visible in the table: the full scroll set (`DSCROLL/LSCROLL/CSCROLL` + `A`/`P` targeting and `2`/`3` layer variants), background shading (`BGSHADE`, `RBGSHADELOOP`, `BGSHADESTOP`, `BGSHADEOFF`), footstep sound control, eye textures (`OPENEYES`/`CLOSEEYES`/`BLINKEYES`), animation state save/restore (`PUSHANIME`/`POPANIME`), party management (`CHANGEPARTY`, `REFRESHPARTY`, `SETPARTY2`, `SWAP`, `ISMEMBER`), and misc (`RESETGF`, `ADDGIL`, `ADDPASTGIL` for Laguna's gil, `GETCARD/HOWMANYCARD/WHERECARD`, `PREMAPJUMP` which appends a synthetic gateway to the loaded .inf, `SETCAMERA/SETDCAMERA`, `POLYCOLOR/POLYCOLORALL`, `SHAKE`, `MENUTIPS`, `BROKEN` timers, `ENDING`).

## Full table

Notes column: `undocumented` = no wiki page exists for this opcode yet; `wiki:X` = the wiki page names it X (intentional, see corrections above).

| Opcode | Name | Handler | Notes |
|--------|------|---------|-------|
| 0x000 | NOP | 0x51C160 |  |
| 0x001 | CAL | 0x51C4B0 |  |
| 0x002 | JMP | 0x51C4D0 |  |
| 0x003 | JPF | 0x51C4F0 |  |
| 0x004 | GJMP | 0x51C530 |  |
| 0x005 | LBL | 0x51C570 |  |
| 0x006 | RET | 0x51C5C0 |  |
| 0x007 | PSHN_L | 0x51C990 |  |
| 0x008 | PSHI_L | 0x51CAB0 |  |
| 0x009 | POPI_L | 0x51CC70 |  |
| 0x00A | PSHM_B | 0x51CAF0 |  |
| 0x00B | POPM_B | 0x51CCA0 |  |
| 0x00C | PSHM_W | 0x51CB30 |  |
| 0x00D | POPM_W | 0x51CCD0 |  |
| 0x00E | PSHM_L | 0x51CB70 |  |
| 0x00F | POPM_L | 0x51CD00 |  |
| 0x010 | PSHSM_B | 0x51CBB0 |  |
| 0x011 | PSHSM_W | 0x51CBF0 |  |
| 0x012 | PSHSM_L | 0x51CC30 |  |
| 0x013 | PSHAC | 0x51CD30 |  |
| 0x014 | REQ | 0x51CD60 |  |
| 0x015 | REQSW | 0x51CED0 |  |
| 0x016 | REQEW | 0x51D060 |  |
| 0x017 | PREQ | 0x51D1F0 |  |
| 0x018 | PREQSW | 0x51D360 |  |
| 0x019 | PREQEW | 0x51D530 |  |
| 0x01A | UNUSE | 0x51DD80 |  |
| 0x01B | DEBUG | 0x51D700 |  |
| 0x01C | HALT | 0x51D710 |  |
| 0x01D | SET | 0x51D720 |  |
| 0x01E | SET3 | 0x51D780 |  |
| 0x01F | IDLOCK | 0x51D7F0 |  |
| 0x020 | IDUNLOCK | 0x51D830 |  |
| 0x021 | EFFECTPLAY2 | 0x51FF00 |  |
| 0x022 | FOOTSTEP | 0x520460 |  |
| 0x023 | JUMP | 0x5256A0 |  |
| 0x024 | JUMP3 | 0x525740 |  |
| 0x025 | LADDERUP | 0x525900 |  |
| 0x026 | LADDERDOWN | 0x525A30 |  |
| 0x027 | LADDERUP2 | 0x525B60 |  |
| 0x028 | LADDERDOWN2 | 0x525CA0 |  |
| 0x029 | MAPJUMP | 0x521A20 |  |
| 0x02A | MAPJUMP3 | 0x521AC0 |  |
| 0x02B | SETMODEL | 0x51D8F0 |  |
| 0x02C | BASEANIME | 0x51D9B0 |  |
| 0x02D | ANIME | 0x526570 |  |
| 0x02E | ANIMEKEEP | 0x526620 |  |
| 0x02F | CANIME | 0x5266D0 |  |
| 0x030 | CANIMEKEEP | 0x526810 |  |
| 0x031 | RANIME | 0x526890 |  |
| 0x032 | RANIMEKEEP | 0x526910 |  |
| 0x033 | RCANIME | 0x526990 |  |
| 0x034 | RCANIMEKEEP | 0x5269E0 |  |
| 0x035 | RANIMELOOP | 0x526A30 |  |
| 0x036 | RCANIMELOOP | 0x526AB0 |  |
| 0x037 | LADDERANIME | 0x51DA00 |  |
| 0x038 | DISCJUMP | 0x521B70 |  |
| 0x039 | SETLINE | 0x51DC30 |  |
| 0x03A | LINEON | 0x51DCE0 |  |
| 0x03B | LINEOFF | 0x51DD00 |  |
| 0x03C | WAIT | 0x51D870 |  |
| 0x03D | MSPEED | 0x5233E0 |  |
| 0x03E | MOVE | 0x523410 |  |
| 0x03F | MOVEA | 0x523640 |  |
| 0x040 | PMOVEA | 0x523880 |  |
| 0x041 | CMOVE | 0x523AD0 |  |
| 0x042 | FMOVE | 0x523C20 |  |
| 0x043 | PJUMPA | 0x525800 |  |
| 0x044 | ANIMESYNC | 0x5264D0 |  |
| 0x045 | ANIMESTOP | 0x5264F0 |  |
| 0x046 | MESW | 0x528E40 |  |
| 0x047 | MES | 0x528F20 |  |
| 0x048 | MESSYNC | 0x529900 |  |
| 0x049 | MESVAR | 0x528D40 |  |
| 0x04A | ASK | 0x529520 |  |
| 0x04B | WINSIZE | 0x529A20 |  |
| 0x04C | WINCLOSE | 0x529B60 |  |
| 0x04D | UCON | 0x51DDA0 |  |
| 0x04E | UCOFF | 0x51DE90 |  |
| 0x04F | MOVIE | 0x51F390 |  |
| 0x050 | MOVIESYNC | 0x51F4F0 |  |
| 0x051 | SETPC | 0x51E0E0 |  |
| 0x052 | DIR | 0x526E60 |  |
| 0x053 | DIRP | 0x526E90 |  |
| 0x054 | DIRA | 0x526F30 |  |
| 0x055 | PDIRA | 0x526F70 |  |
| 0x056 | SPUREADY | 0x51F520 |  |
| 0x057 | TALKON | 0x51EBB0 |  |
| 0x058 | TALKOFF | 0x51EBD0 |  |
| 0x059 | PUSHON | 0x51EBF0 |  |
| 0x05A | PUSHOFF | 0x51EC10 |  |
| 0x05B | ISTOUCH | 0x51ED80 |  |
| 0x05C | MAPJUMP0 | 0x521C30 |  |
| 0x05D | MAPJUMPON | 0x521CB0 |  |
| 0x05E | MAPJUMPOFF | 0x521CC0 |  |
| 0x05F | SETMESSPEED | 0x528E10 |  |
| 0x060 | SHOW | 0x51EAD0 |  |
| 0x061 | HIDE | 0x51EB40 |  |
| 0x062 | TALKRADIUS | 0x51EDD0 |  |
| 0x063 | PUSHRADIUS | 0x51EE00 |  |
| 0x064 | AMESW | 0x529020 |  |
| 0x065 | AMES | 0x5291E0 |  |
| 0x066 | GETINFO | 0x51EE30 |  |
| 0x067 | THROUGHON | 0x51ED40 |  |
| 0x068 | THROUGHOFF | 0x51ED60 |  |
| 0x069 | BATTLE | 0x523270 |  |
| 0x06A | BATTLERESULT | 0x5232E0 |  |
| 0x06B | BATTLEON | 0x523300 |  |
| 0x06C | BATTLEOFF | 0x523330 |  |
| 0x06D | KEYSCAN | 0x51DA50 |  |
| 0x06E | KEYON | 0x51DAA0 |  |
| 0x06F | AASK | 0x5296C0 |  |
| 0x070 | PGETINFO | 0x51EEB0 |  |
| 0x071 | DSCROLL | 0x520C40 |  |
| 0x072 | LSCROLL | 0x520C90 |  |
| 0x073 | SCSROLL | 0x520CF0 | wiki:CSCROLL |
| 0x074 | DSCROLLA | 0x520D50 |  |
| 0x075 | LSCROLLA | 0x520D90 | undocumented |
| 0x076 | CSCROLLA | 0x520DF0 | undocumented |
| 0x077 | SCROLLSYNC | 0x520F50 |  |
| 0x078 | RMOVE | 0x524030 | undocumented |
| 0x079 | RMOVEA | 0x5241A0 | undocumented |
| 0x07A | RPMOVEA | 0x524310 | undocumented |
| 0x07B | RCMOVE | 0x524490 | undocumented |
| 0x07C | RFMOVE | 0x524550 | undocumented |
| 0x07D | MOVESYNC | 0x524600 |  |
| 0x07E | CLEAR | 0x51D8B0 |  |
| 0x07F | DSCROLLP | 0x520E50 | undocumented |
| 0x080 | LSCROLLP | 0x520E90 | undocumented |
| 0x081 | CSCROLLP | 0x520EF0 | undocumented |
| 0x082 | LTURNR | 0x527250 | undocumented |
| 0x083 | LTURNL | 0x527320 | undocumented |
| 0x084 | CTURNR | 0x5273F0 |  |
| 0x085 | CTURNL | 0x5274C0 |  |
| 0x086 | ADDPARTY | 0x51E160 |  |
| 0x087 | SUBPARTY | 0x51E270 |  |
| 0x088 | CHANGEPARTY | 0x51E350 | undocumented |
| 0x089 | REFRESHPARTY | 0x51E5D0 | undocumented |
| 0x08A | SETPARTY | 0x51E400 |  |
| 0x08B | ISPARTY | 0x51E5E0 |  |
| 0x08C | ADDMEMBER | 0x51E670 |  |
| 0x08D | SUBMEMBER | 0x51E710 |  |
| 0x08E | ISMEMBER | 0x51E7D0 | undocumented |
| 0x08F | LTURN | 0x527590 | undocumented |
| 0x090 | CTURN | 0x527690 |  |
| 0x091 | PLTURN | 0x527790 | undocumented |
| 0x092 | PCTURN | 0x5278A0 |  |
| 0x093 | JOIN | 0x524BA0 |  |
| 0x094 | MESFORCUS | 0x5299F0 | undocumented |
| 0x095 | BGANIME | 0x520570 |  |
| 0x096 | RBGANIME | 0x520640 | undocumented |
| 0x097 | RGBANIMELOOP | 0x5206E0 | undocumented |
| 0x098 | BGANIMESYNC | 0x520780 | undocumented |
| 0x099 | BGDRAW | 0x5207A0 | undocumented |
| 0x09A | BGOFF | 0x520800 | undocumented |
| 0x09B | BGANIMESPEED | 0x520850 | undocumented |
| 0x09C | SETTIMER | 0x5216E0 |  |
| 0x09D | DISPTIMER | 0x521730 |  |
| 0x09E | SHADETIMER | 0x5217F0 | undocumented |
| 0x09F | SETGETA | 0x526C30 |  |
| 0x0A0 | SETROOTTRANS | 0x526C80 | undocumented |
| 0x0A1 | SETVIBRATE | 0x51F620 |  |
| 0x0A2 | STOPVIBRATE | 0x51F670 | undocumented |
| 0x0A3 | MOVIEREADY | 0x51F2C0 |  |
| 0x0A4 | GETTIMER | 0x521710 | undocumented |
| 0x0A5 | FADEIN | 0x5283B0 | undocumented |
| 0x0A6 | FADEOUT | 0x528490 | undocumented |
| 0x0A7 | FADESYNC | 0x528CA0 | undocumented |
| 0x0A8 | SHAKE | 0x520BA0 | undocumented |
| 0x0A9 | SHAKEOFF | 0x520C20 | undocumented |
| 0x0AA | FADEBLACK | 0x528D10 |  |
| 0x0AB | FOLLOWOFF | 0x51EC30 | undocumented |
| 0x0AC | FOLLOWON | 0x51ECF0 | undocumented |
| 0x0AD | GAMEOVER | 0x523370 |  |
| 0x0AE | ENDING | 0x523380 | undocumented |
| 0x0AF | SHADELEVEL | 0x526E30 |  |
| 0x0B0 | SHADEFORM | 0x526D30 | undocumented |
| 0x0B1 | FMOVEA | 0x523D70 | undocumented |
| 0x0B2 | FMOVEP | 0x523ED0 | undocumented |
| 0x0B3 | SHADESET | 0x526CD0 | undocumented |
| 0x0B4 | MUSICCHANGE | 0x51F7F0 |  |
| 0x0B5 | MUSICLOAD | 0x51F730 |  |
| 0x0B6 | FADENONE | 0x528CE0 | undocumented |
| 0x0B7 | POLYCOLOR | 0x526B00 | undocumented |
| 0x0B8 | POLYCOLORALL | 0x526B80 | undocumented |
| 0x0B9 | KILLTIMER | 0x5217B0 | undocumented |
| 0x0BA | CROSSMUSIC | 0x51FA50 | undocumented |
| 0x0BB | DUALMUSIC | 0x51FB00 | undocumented |
| 0x0BC | EFFECTPLAY | 0x51FEA0 |  |
| 0x0BD | EFFECTLOAD | 0x51FDE0 |  |
| 0x0BE | LOADSYNC | 0x51F680 | undocumented |
| 0x0BF | MUSICSTOP | 0x51FBD0 |  |
| 0x0C0 | MUSICVOL | 0x51FC70 |  |
| 0x0C1 | MUSICVOLTRANS | 0x51FCD0 |  |
| 0x0C2 | MUSICVOLFADE | 0x51FD40 | undocumented |
| 0x0C3 | ALLSEVOL | 0x51FFA0 |  |
| 0x0C4 | ALLSEVOLTRANS | 0x51FFD0 |  |
| 0x0C5 | ALLSEPOS | 0x520010 |  |
| 0x0C6 | ALLSEPOSTRANS | 0x520040 |  |
| 0x0C7 | SEVOL | 0x520080 |  |
| 0x0C8 | SEVOLTRANS | 0x5200C0 |  |
| 0x0C9 | SEPOS | 0x520110 |  |
| 0x0CA | SEPOSTRANS | 0x520150 |  |
| 0x0CB | SETBATTLEMUSIC | 0x51F700 |  |
| 0x0CC | BATTLEMODE | 0x523230 |  |
| 0x0CD | SESTOP | 0x5201A0 |  |
| 0x0CE | BGANIMEFLAG | 0x520880 | undocumented |
| 0x0CF | INITSOUND | 0x51F690 | undocumented |
| 0x0D0 | BGSHADE | 0x5208B0 | undocumented |
| 0x0D1 | BGSHADESTOP | 0x520AD0 | undocumented |
| 0x0D2 | RBGSHADELOOP | 0x5209A0 | undocumented |
| 0x0D3 | DSCROLL2 | 0x520FA0 | undocumented |
| 0x0D4 | LSCROLL2 | 0x521010 | undocumented |
| 0x0D5 | CSCROLL2 | 0x521090 | undocumented |
| 0x0D6 | DSCROLLA2 | 0x521110 | undocumented |
| 0x0D7 | LSCROLLA2 | 0x521170 | undocumented |
| 0x0D8 | CSCROLLA2 | 0x5211F0 | undocumented |
| 0x0D9 | DSCROLLP2 | 0x521270 | undocumented |
| 0x0DA | LSCROLLP2 | 0x5212D0 | undocumented |
| 0x0DB | CSCROLLP2 | 0x521350 | undocumented |
| 0x0DC | SCROLLSYNC2 | 0x520F60 | undocumented |
| 0x0DD | SCROLLMODE2 | 0x5213D0 | undocumented |
| 0x0DE | MENUENABLE | 0x521D00 | undocumented |
| 0x0DF | MENUDISABLE | 0x521CF0 | undocumented |
| 0x0E0 | FOOTSTEPON | 0x5204E0 | undocumented |
| 0x0E1 | FOOTSTEPOFF | 0x520500 | undocumented |
| 0x0E2 | FOOSTEPOFFALL | 0x520520 | undocumented |
| 0x0E3 | FOOTSTEPCUT | 0x520550 | undocumented |
| 0x0E4 | PREMAPJUMP | 0x521960 | undocumented |
| 0x0E5 | USE | 0x51DD60 |  |
| 0x0E6 | SPLIT | 0x525090 |  |
| 0x0E7 | ANIMESPEED | 0x5264A0 |  |
| 0x0E8 | RND | 0x51D8D0 |  |
| 0x0E9 | DCOLADD | 0x528570 | undocumented |
| 0x0EA | DCOLSUB | 0x528670 | undocumented |
| 0x0EB | TCOLADD | 0x528770 | undocumented |
| 0x0EC | TCOLSUB | 0x5288A0 | undocumented |
| 0x0ED | FCOLADD | 0x5289D0 | undocumented |
| 0x0EE | FCOLSUB | 0x528B20 |  |
| 0x0EF | COLSYNC | 0x528C70 | undocumented |
| 0x0F0 | DOFFSET | 0x525DE0 | undocumented |
| 0x0F1 | LOFFSETS | 0x525E70 | undocumented |
| 0x0F2 | COFFSETS | 0x525F30 | undocumented |
| 0x0F3 | LOFFSET | 0x525FF0 | undocumented |
| 0x0F4 | COFFSET | 0x5260A0 | undocumented |
| 0x0F5 | OFFSETSYNC | 0x526150 | undocumented |
| 0x0F6 | RUNENABLE | 0x526180 |  |
| 0x0F7 | RUNDISABLE | 0x526170 |  |
| 0x0F8 | MAPFADEOFF | 0x521CD0 | undocumented |
| 0x0F9 | MAPFADEON | 0x521CE0 | undocumented |
| 0x0FA | INITTRACE | 0x526190 | undocumented |
| 0x0FB | SETDRESS | 0x51D910 | undocumented |
| 0x0FC | GETDRESS | 0x51D960 | undocumented |
| 0x0FD | FACEDIR | 0x527B90 | undocumented |
| 0x0FE | FACEDIRA | 0x527C30 |  |
| 0x0FF | FACEDIRP | 0x527D30 |  |
| 0x100 | FACEDIRLIMIT | 0x528300 |  |
| 0x101 | FACEDIROFF | 0x527E40 |  |
| 0x102 | SALARYOFF | 0x51DB90 |  |
| 0x103 | SALARYON | 0x51DBC0 |  |
| 0x104 | SALARYDISPOFF | 0x51DBF0 |  |
| 0x105 | SALARYDISPON | 0x51DC10 |  |
| 0x106 | MESMODE | 0x528D80 |  |
| 0x107 | FACEDIRINIT | 0x528350 |  |
| 0x108 | FACEDIRI | 0x527AF0 | undocumented |
| 0x109 | JUNCTION | 0x51EFB0 |  |
| 0x10A | SETCAMERA | 0x5218E0 | undocumented |
| 0x10B | BATTLECUT | 0x523350 |  |
| 0x10C | FOOSTEPCOPY | 0x520490 | undocumented |
| 0x10D | WORLDMAPJUMP | 0x521820 |  |
| 0x10E | RFACEDIRI | 0x527F10 | undocumented |
| 0x10F | RFACEDIR | 0x527FA0 | undocumented |
| 0x110 | RFACEDIRA | 0x528030 | undocumented |
| 0x111 | RFACEDIRP | 0x528130 | undocumented |
| 0x112 | RFACEDIROFF | 0x528240 | undocumented |
| 0x113 | RFACEDIRSYNC | 0x527AD0 | undocumented |
| 0x114 | COPYINFO | 0x51F0C0 | undocumented |
| 0x115 | PCOPYINFO | 0x51F140 | undocumented |
| 0x116 | RAMESW | 0x529380 |  |
| 0x117 | BGSHADEOFF | 0x520B00 | undocumented |
| 0x118 | AXIS | 0x5261C0 | undocumented |
| 0x119 | AXISSYNC | 0x5261A0 | undocumented |
| 0x11A | MENUNORMAL | 0x521D10 |  |
| 0x11B | MENUPHS | 0x521D40 |  |
| 0x11C | BGCLEAR | 0x5216B0 | undocumented |
| 0x11D | GETPARTY | 0x51E640 |  |
| 0x11E | MENUSHOP | 0x521D60 |  |
| 0x11F | DISC | 0x523390 |  |
| 0x120 | DSCROLL3 | 0x5214C0 | undocumented |
| 0x121 | LSCROLL3 | 0x521530 | undocumented |
| 0x122 | CSCROLL3 | 0x5215F0 | undocumented |
| 0x123 | MACCEL | 0x524840 | undocumented |
| 0x124 | MLIMIT | 0x524810 | undocumented |
| 0x125 | ADDITEM | 0x522380 |  |
| 0x126 | SETWITCH | 0x523180 |  |
| 0x127 | SETODIN | 0x5231C0 |  |
| 0x128 | RESETGF | 0x51EA10 | undocumented |
| 0x129 | MENUNAME | 0x521DA0 |  |
| 0x12A | REST | 0x5220A0 | undocumented |
| 0x12B | MOVECANCEL | 0x524620 | undocumented |
| 0x12C | PMOVECANCEL | 0x5246F0 | undocumented |
| 0x12D | ACTORMODE | 0x51F1F0 |  |
| 0x12E | MENUSAVE | 0x522190 |  |
| 0x12F | SAVEENABLE | 0x5221B0 |  |
| 0x130 | PHSENABLE | 0x522280 |  |
| 0x131 | HOLD | 0x51EA50 |  |
| 0x132 | MOVIECUT | 0x51F600 |  |
| 0x133 | SETPLACE | 0x523200 |  |
| 0x134 | SETDCAMERA | 0x521930 | undocumented |
| 0x135 | CHOICEMUSIC | 0x51F9A0 | undocumented |
| 0x136 | GETCARD | 0x5224D0 | undocumented |
| 0x137 | DRAWPOINT | 0x522770 |  |
| 0x138 | PHSPOWER | 0x522230 |  |
| 0x139 | KEY | 0x51E0B0 | undocumented |
| 0x13A | CARDGAME | 0x5225A0 |  |
| 0x13B | SETBAR | 0x529BF0 | undocumented |
| 0x13C | DISPBAR | 0x529C40 | undocumented |
| 0x13D | KILLBAR | 0x529E70 | undocumented |
| 0x13E | SCROLLRAIO2 | 0x521460 | undocumented |
| 0x13F | WHOAMI | 0x51EF70 |  |
| 0x140 | MUSICSTATUS | 0x51FC20 | undocumented |
| 0x141 | MUSICREPLAY | 0x51F880 | undocumented |
| 0x142 | DOORLINEOFF | 0x51DD40 | undocumented |
| 0x143 | DOORLINEON | 0x51DD20 | undocumented |
| 0x144 | MUSICSKIP | 0x51F900 | undocumented |
| 0x145 | DYING | 0x5220B0 |  |
| 0x146 | SETHP | 0x522110 | undocumented |
| 0x147 | GETHP | 0x522150 | undocumented |
| 0x148 | MOVEFLUSH | 0x5247E0 |  |
| 0x149 | MUSICVOLSYNC | 0x51FDC0 | undocumented |
| 0x14A | PUSHANIME | 0x526390 | undocumented |
| 0x14B | POPANIME | 0x5263F0 | undocumented |
| 0x14C | KEYSCAN2 | 0x51DAF0 | undocumented |
| 0x14D | KEYON2 | 0x51DB40 | undocumented |
| 0x14E | PARTICLEON | 0x5230E0 | undocumented |
| 0x14F | PARTICLEOFF | 0x523110 | undocumented |
| 0x150 | KEYSIGNCHANGE | 0x51FBA0 |  |
| 0x151 | ADDGIL | 0x5223C0 | undocumented |
| 0x152 | ADDPASTGIL | 0x522420 | undocumented |
| 0x153 | ADDSEEDLEVEL | 0x522480 |  |
| 0x154 | PARTICLESET | 0x523140 | undocumented |
| 0x155 | SETDRAWPOINT | 0x523030 |  |
| 0x156 | MENUTIPS | 0x522070 | undocumented |
| 0x157 | LASTIN | 0x51E910 |  |
| 0x158 | LASTOUT | 0x51E990 |  |
| 0x159 | SEALEDOFF | 0x51E9C0 |  |
| 0x15A | MENUTUTO | 0x522010 | undocumented |
| 0x15B | OPENEYES | 0x526240 | undocumented |
| 0x15C | CLOSEEYES | 0x526280 | undocumented |
| 0x15D | BLINKEYES | 0x5262C0 | undocumented |
| 0x15E | SETCARD | 0x522500 |  |
| 0x15F | HOWMANYCARD | 0x522540 | undocumented |
| 0x160 | WHERECARD | 0x522570 | undocumented |
| 0x161 | ADDMAGIC | 0x5222D0 |  |
| 0x162 | SWAP | 0x51E8A0 | undocumented |
| 0x163 | SETPARTY2 | 0x51E860 | undocumented |
| 0x164 | SPUSYNC | 0x51F5B0 |  |
| 0x165 | BROKEN | 0x529D40 | undocumented |
| 0x166 | DISABLE_ANGELO | 0x529EB0 |  |
| 0x167 | UNKNOWN2 | 0x529EF0 |  |
| 0x168 | UNKNOWN3 | 0x529F70 |  |
| 0x169 | UNKNOWN4 | 0x526210 |  |
| 0x16A | HAS_ITEM | 0x522350 |  |
| 0x16B | CLOCKWISETURN | 0x526FD0 |  |
| 0x16C | COUNTERCLOCKWISETURN | 0x527070 |  |
| 0x16D | CLOCKWISETURN2 | 0x527110 |  |
| 0x16E | COUNTERCLOCKWISETURN2 | 0x5271B0 |  |
| 0x16F | UNKNOWN10 | 0x51FC40 |  |
| 0x170 | UNKNOWN11 | 0x5279B0 |  |
| 0x171 | UNKNOWN12 | 0x527AB0 |  |
| 0x172 | UNKNOWN13 | 0x520200 |  |
| 0x173 | PRESERVESOUNDCHANNEL | 0x520230 |  |
| 0x174 | UNKNOWN15 | 0x5258D0 |  |
| 0x175 | SETDRAWPOINTID | 0x5230A0 |  |
| 0x176 | UNKNOWN17 | 0x5219F0 |  |
| 0x177 | SHOWTUTORIAL | 0x522030 |  |

Addresses are for FF8_EN.exe (2000 PC release) as mapped in IDA (image base 0x400000). Handler names are the original Square symbol names preserved in the executable's community IDB.
