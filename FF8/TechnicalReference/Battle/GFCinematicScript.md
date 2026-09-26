---
title: GF cinematic script and mag files
layout: default
parent: Battle
permalink: /technical-reference/battle/gf-cinematic-script/
nav_order: 7
---

# GF cinematic script and mag files

The seven summons of the [GF cinematic engine](GFCinematicEngine.md) (Ifrit, Leviathan, Bahamut,
Cerberus, Alexander, the Brothers, Eden) keep their whole choreography as byte code in their mag
files. This page is the file-format and instruction-set reference; the engine that runs it is on
the engine page. The FF8UltimateEditor tool **Laguna** (and `cli.py laguna`) disassembles, simulates
and patches these scripts with the tables below.

1. TOC
{:toc}

## Files

| GF | Effect id | Files | Streamed parts (`battle/`) |
|----|-----------|-------|----------------------------|
| Ifrit | 201 | `magic/MAG200_B.00`, `.01` | `mag200_b.02`-`.12` |
| Leviathan | 6 | `magic/MAG005_B.00`, `.01` | `mag005_b.02`-`.17` |
| Bahamut | 202 | `magic/MAG201_B.00`, `.01` | `mag201_b.02`-`.39` |
| Cerberus | 203 | `magic/MAG202_B.00`, `.01` | `mag202_b.02`-`.12` |
| Alexander | 204 | `magic/MAG203_B.00`, `.01` | `mag203_b.02`-`.15` |
| Brothers | 205 | `magic/MAG204_B.00`, `.01` | `mag204_b.02`-`.11` |
| Eden | 206 | `magic/MAG205_B.00`, `.01` | `mag205_b.02`-`.56` |

The engine keeps up to 64 **file slots**. Slot 0 is the `.00` and slot 1 the `.01`, both loaded
when the summon starts; slot *k* (2 and up) is `battle/magNNN_b.0k`, loaded during the summon by
script opcode `0x006` (battle file id = a per-GF base + *k*). The `.00` holds the script, the sound
effects, the voice bank and some resources; the `.01` holds most textures and meshes and, at its
header offset `0x1C`, a zero-filled area that the engine uses as RAM for the bone array and the
bump allocator. Streamed parts are either packed files with the same header or raw VRAM page dumps.

### Header

Every packed file starts with twelve `u32` offsets:

| Offset | Content |
|--------|---------|
| `0x00` | 0 |
| `0x04` | Script: root program (`.00` only). The script region runs to the sound-effect table |
| `0x08` | CLUT table (= end of the texture table) |
| `0x0C` | Object table: `u32 count`, then `u32 offset[count]` relative to the table start, 0 = not in this file |
| `0x10` | Sound-effect table (`.00` only), one FF8 sound block per entry |
| `0x14` | Texture table, always `0x30` |
| `0x18` | Music-stream table |
| `0x1C` | End of the tables. In the `.01`: start of the engine RAM area |
| `0x20` | Stage camera animation (unused: 0 in all seven GFs) |
| `0x24` | Voice bank (`.00` only) |
| `0x28`, `0x2C` | 0 |

Resource tables are **global-index** tables shared by the files of a GF: resource *i* has a non-zero
entry only in the file that holds it. Which file slot holds each texture, CLUT, object and music
entry, and the VRAM rectangle of each texture and CLUT, come from a per-GF descriptor block in the
executable (see [Addresses](#addresses)). Textures and CLUTs reach VRAM only through script
opcodes (`0x027`, `0x029`, `0x04B`...).

### Objects

The opcode that uses an object id decides what it is; the data itself is recognisable:

- **Mesh**: a `0x30`-byte header (`+0x00` flags: bit 0 has a primitive list, bit 1 has vertices,
  bit 2 has normals; `+0x08` primitive list offset; `+0x14`/`+0x18` vertex offset/count;
  `+0x1C`/`+0x20` normal offset/count), 8-byte vertices (`s16 x, y, z, pad`) and a primitive list
  of `{u16 type, u16 count}` groups ending at a count of `0xFFFF`. Vertex fields in a primitive
  are **byte offsets** into the vertex array (index x 8). A mesh with flag bit 0 clear is a
  vertex-only morph target.

  | Type | Size | Primitive | Vertex fields | Other fields |
  |------|------|-----------|---------------|--------------|
  | 2 | 20 | lit Gouraud triangle | +14, +16, +18 | colours +0/+4/+8, normal +12 |
  | 6 | 12 | flat triangle | +4, +6, +8 | colour +0 |
  | 7 | 20 | Gouraud triangle | +12, +14, +16 | colours +0/+4/+8 |
  | 8 | 20 | flat textured triangle | +10, +12, +14 | colour +0, uv +4/+6/+8, clut +16, tpage +18 |
  | 9 | 28 | Gouraud textured triangle | +18, +20, +22 | colours +0/+4/+8, uv +12/+14/+16, clut +24, tpage +26 |
  | 12 | 28 | lit Gouraud quad | +20, +22, +24, +26 | colours +0..+12, normal +16 |
  | 16 | 12 | flat quad | +4, +6, +8, +10 | colour +0 |
  | 17 | 24 | Gouraud quad | +16, +18, +20, +22 | colours +0..+12 |
  | 18 | 24 | flat textured quad | +12, +14, +16, +18 | colour +0, uv +4..+10, clut +20, tpage +22 |
  | 19 | 36 | Gouraud textured quad | +24, +26, +28, +30 | colours +0..+12, uv +16..+22, clut +32, tpage +34 |

  Quads use the PlayStation vertex order (triangles 0-1-2 and 1-3-2). The other type numbers
  (0-19) have a record size in the engine but no renderer in any of the seven GFs.
- **Embedded battle model** (the creature): seven `u32` `{size, skeleton, geometry, animation, 0,
  0, size - 4}`, the three offsets pointing at standard battle `.dat` sections 1, 2 and 3. Opcode
  `0x03F` instantiates it and draw handler 3 renders it.
- **Sprite frame list**: 8-byte entries `{s32 frame offset from the object table, s16 duration,
  s8 code}` (code 0 = next entry, 1 = end, 2 = loop to the start); a frame is `u32 quadCount` and
  20-byte quads.

Particle pools are not in the files: opcode `0x058` allocates them at run time.

## Script format

A script is a stream of little-endian 16-bit words. The first word of an instruction is the
**opcode word**:

| Bits | Meaning |
|------|---------|
| 0-8 | Opcode (`0x000`-`0x146`) |
| 9-15 | Modifier, meaning depends on the opcode: wait length (`0x009`), component mask (generic writes), sub-operation (`0x005`, `0x039`...), flags |

Operands follow as 16-bit words. The **length is variable** (2 to 10 bytes, more for the inline data
blocks of `0x01A`, `0x043`, `0x044`, `0x04E`) and is decided by the opcode, sometimes by its modifier
bits or by an operand. Each handler advances the cursor itself; an instruction that does not
advance the cursor re-executes on the next tick (the "wait until" opcodes use this on purpose).

Every code reference - jump, call, loop, spawn, start of another channel, particle script, inline
data block - is a signed 16-bit **byte offset relative to the opcode word** of the instruction
(`0x059` with bit 12 set is relative to its first operand word instead). The scripts of all bones
therefore form one position-independent block from the root program to the sound-effect table, and
nothing outside it points into it: an edit that keeps every instruction's length needs no
relocation.

### Execution

A channel runs instructions back to back until one requests a wait; the wait is counted in units
of the wait speed of the bone (128 = one battle tick at the default speed), so `Wait n` (`0x009` with
modifier *n*) resumes the channel *n* ticks later. A bone has three channels; `0x026`/`0x08B`
start the other two, `0x032` and its variants create a new bone running a program, `0x000` ends a
channel (and kills the bone on channel 0). `0x003`/`0x004` are a two-level call stack per channel,
`0x01E`/`0x01F` a loop counter per bone and `0x0A7`/`0x0A8` loop counters shared by the scene.
Bones synchronise through a shared 16-bit flag word (`0x005`: set, clear, jump if any/none, wait
while any/until any) and a per-bone flag word (`0x10C`, `0x10D`). `0x001` ends the summon.

Replayed without the game (random opcodes seeded, battle-dependent branches not taken), the scripts
end after 322 ticks for Ifrit (324 measured in game), 578 for Leviathan, 604 for Bahamut, 279 for
Cerberus, 553 for Alexander, 460 for the Brothers and 1253 for Eden (15 ticks per second).

### Generic writes

Opcodes `0x00A`-`0x017` write the motion values of the current bone. Modifier bits 15..10 select
the components RotX, RotY, RotZ, PosX, PosY, PosZ (in that order); there is one operand per selected
component, except the "all" forms (`0x00D`-`0x00F`, `0x016`) which take one value for every selected
component and `0x017` which takes a base and a spread per component. The value `0x7654` leaves a
component unchanged.

| Opcode | Mode | Field |
|--------|------|-------|
| `0x00A` / `0x00D` / `0x010` | set / set all / add | accumulator (value << 16: whole units) |
| `0x00B` / `0x00E` | set / set all | velocity (value << 8) |
| `0x011` | set | velocity (value << 16: whole units per tick) |
| `0x00C` / `0x00F` | set / set all | acceleration (value >> 4) |
| `0x012` / `0x013` / `0x014` / `0x015` | add random 0..value | accumulator / velocity << 8 / acceleration (<< 4) / velocity << 16 |
| `0x016` / `0x017` | add random (all) / base +- random spread | accumulator |

Every tick the integrator adds acceleration to velocity and velocity to the accumulator; the
integer part of the accumulator is the output angle and position of the bone.

## Opcode reference

Lengths are Python expressions of `op` (the opcode word) and `w` (the following words, signed). The
table lists the implemented opcodes; the names are those of the IDA database.

| Op | Name | Length (bytes) | Operands | Meaning |
|----|------|----------------|----------|---------|
| `0x000` | EndChannel | `2` | - | If channel!=0: StreamCursor=0 (channel pointer stored as 0 = channel unused), wait 0x8000. If channel 0: KILL BONE: clear the 3 chanStreamPtr + chanWait, free its node-matrix slot (B651E0/B65270; key table 0x2797204 entry = bone id cleared), --sceneHeader+0x18 (live bone count), rt->boneCursor-- (order list shifted), wait=chanWaitSpeed. |
| `0x001` | LoopSequenceOrFinish | `4` | restartTarget | If ctx+0xD0 (loop count) < ctx+0xD1 (loop max): ++count, GF_Ifrit_InitBones(), cursor = opcode+param0, boneCursor=0 (whole summon restarts). Else: bone order list filled with 0xFF, SequenceState+8=0, all channels cleared, wait=-1, sceneHeader+0x18=0, sceneHeader+0x1A=4 (sequence finished). |
| `0x002` | Jump | `4` | target | StreamCursor += param0 (byte offset relative to the opcode word). |
| `0x003` | Call | `4` | target | Per-channel return stack: bone[+0x24 + 8*chan + 4*depth] = &param1 (= opcode+4), depth byte bone+0x44+chan ++ (2 levels per channel); cursor = opcode + param0. |
| `0x004` | Return | `2` | - | --depth byte bone+0x44+chan; cursor = saved return address from bone+0x24+8*chan+4*depth. |
| `0x005` | FlagOp | `4 + (2 if (op >> 12) in (2, 3) else 0)` | mask, target (sub-op 2/3 only) | Operates on the shared 16-bit sequence flag word *(rt+0x10)+2 (inter-bone synchronisation flags). Sub-ops 4/5 yield wait=chanWaitSpeed and leave the cursor on the instruction. Modifier: op>>12 = sub-op: 0 (and 6..15) flags\|=mask; 1 flags&=~mask; 2 if (flags&mask)!=0 jump opcode+param1 else fall through; 3 if (flags&mask)==0 jump; 4 wait (retry same instr next tick) while (flags&mask)!=0; 5 wait until (flags&mask)!=0. Bits 9..11 unused. |
| `0x006` | LoadFile | `4 if (op & 0x8000) == 0 else 2` | source (only when bit15 clear) | Starts an async battle-file load (pre_LoadBattleFile, callback B2BB40) of file ctx->frameLimit+ctx[0xA2]+slot into dest, records Magic_b_00[ctx[0xA2]+slot]=dest, ctx+0xB4=dest, sets busy flag byte_2798219. If a load is already busy: wait chanWaitSpeed and retry the same instruction. Modifier: bit15 clear: slot=op>>9 (0..63); param0 = source: lo byte 0xFF -> dest ctx+0xB8; lo<0x80 -> dest=Magic_b_00[lo] (+ sub-table offset via dword_1874894/dword_18748B0 indexed by hi byte unless hi==0xFF); lo&0x80 -> dest=Magic_b_00[lo&0x7F]+(hi<<12). bit15 set: slot=(op>>9)&0x3F, dest=ctx+0xB8; if slot&0x20 the file id = (slot&0x1F)+363 and Magic_b_00 is not updated. |
| `0x007` | SetFreezeOthers | `2` | - | Freeze/unfreeze other bones; marks current bone 0x80 in the bone order list (keeps running). Modifier: bit15 -> rt->boneSkipFlag=0xFF; bit14 -> boneSkipFlag=0 |
| `0x008` | WaitLoadDone | `2` | - | If a file load is busy (byte_2798219) or not completed (byte_2798218==0): wait chanWaitSpeed and retry; else advance. |
| `0x009` | Wait | `2` | - | vmWaitRequest = (op>>9)<<7 (128 = one tick at the default chanWaitSpeed). Modifier: op>>9 = tick count |
| `0x00A` | SetAccum | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x00: mode 0 Set, field desc 0): target accum (accumRotXYZ +0x50..0x58, accumPosXYZ +0x5C..0x64), encoding s32 16.16, value<<16; postAction 1: run BoneHandlerTable[bone->handlerId] then outAngle=HIWORD(accumRot) (B2C440). Operands: one s16 per set mask bit, 0x7654 = leave component unchanged. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x00B` | SetVel | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x01: mode 0 Set, field desc 1): target vel (velRotXYZ +0x68..0x70, velPosXYZ +0x74..0x7C), encoding s32, value<<8; no post action. Operands: one s16 per set mask bit, 0x7654 = leave component unchanged. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x00C` | SetAccel | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x02: mode 0 Set, field desc 2): target accel (accelRotXYZ +0x80..0x84, accelPosXYZ +0x86..0x8A), encoding s16, set: value>>4 / add+random: value<<4; postAction 2: recompute bone->flags (bit0 if any accelRot!=0, bit3 if any accelPos!=0) = integrator enable (B2D460). Operands: one s16 per set mask bit, 0x7654 = leave component unchanged. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x00D` | SetAllAccum | `4` | value/range (applied to all masked components) | Generic write (attrib 0x10: mode 1 SetAll, field desc 0): target accum (accumRotXYZ +0x50..0x58, accumPosXYZ +0x5C..0x64), encoding s32 16.16, value<<16; postAction 1: run BoneHandlerTable[bone->handlerId] then outAngle=HIWORD(accumRot) (B2C440). Operands: one s16 written to every masked component. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x00E` | SetAllVel | `4` | value/range (applied to all masked components) | Generic write (attrib 0x11: mode 1 SetAll, field desc 1): target vel (velRotXYZ +0x68..0x70, velPosXYZ +0x74..0x7C), encoding s32, value<<8; no post action. Operands: one s16 written to every masked component. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x00F` | SetAllAccel | `4` | value/range (applied to all masked components) | Generic write (attrib 0x12: mode 1 SetAll, field desc 2): target accel (accelRotXYZ +0x80..0x84, accelPosXYZ +0x86..0x8A), encoding s16, set: value>>4 / add+random: value<<4; postAction 2: recompute bone->flags (bit0 if any accelRot!=0, bit3 if any accelPos!=0) = integrator enable (B2D460). Operands: one s16 written to every masked component. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x010` | AddAccum | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x20: mode 2 Add, field desc 0): target accum (accumRotXYZ +0x50..0x58, accumPosXYZ +0x5C..0x64), encoding s32 16.16, value<<16; postAction 1: run BoneHandlerTable[bone->handlerId] then outAngle=HIWORD(accumRot) (B2C440). Operands: one s16 per set mask bit added, 0x7654 = skip. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x011` | SetVelInt | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x03: mode 0 Set, field desc 3): target vel (velRotXYZ +0x68..0x70, velPosXYZ +0x74..0x7C), encoding s32, value<<16; no post action. Operands: one s16 per set mask bit, 0x7654 = leave component unchanged. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x012` | AddRandomAccum | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x30: mode 3 AddRandom, field desc 0): target accum (accumRotXYZ +0x50..0x58, accumPosXYZ +0x5C..0x64), encoding s32 16.16, value<<16; postAction 1: run BoneHandlerTable[bone->handlerId] then outAngle=HIWORD(accumRot) (B2C440). Operands: one s16 range per set bit, adds rand(range) (0 = skip, word still consumed). Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x013` | AddRandomVel | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x31: mode 3 AddRandom, field desc 1): target vel (velRotXYZ +0x68..0x70, velPosXYZ +0x74..0x7C), encoding s32, value<<8; no post action. Operands: one s16 range per set bit, adds rand(range) (0 = skip, word still consumed). Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x014` | AddRandomAccel | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x32: mode 3 AddRandom, field desc 2): target accel (accelRotXYZ +0x80..0x84, accelPosXYZ +0x86..0x8A), encoding s16, set: value>>4 / add+random: value<<4; postAction 2: recompute bone->flags (bit0 if any accelRot!=0, bit3 if any accelPos!=0) = integrator enable (B2D460). Operands: one s16 range per set bit, adds rand(range) (0 = skip, word still consumed). Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x015` | AddRandomVelInt | `2 + 2*popcount((op >> 10) & 0x3F)` | one value per set mask bit, bit15 first | Generic write (attrib 0x33: mode 3 AddRandom, field desc 3): target vel (velRotXYZ +0x68..0x70, velPosXYZ +0x74..0x7C), encoding s32, value<<16; no post action. Operands: one s16 range per set bit, adds rand(range) (0 = skip, word still consumed). Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x016` | AddRandomAllAccum | `4` | value/range (applied to all masked components) | Generic write (attrib 0x40: mode 4 AddRandomAll, field desc 0): target accum (accumRotXYZ +0x50..0x58, accumPosXYZ +0x5C..0x64), encoding s32 16.16, value<<16; postAction 1: run BoneHandlerTable[bone->handlerId] then outAngle=HIWORD(accumRot) (B2C440). Operands: one range; ONE rand(range) added to every masked component. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x017` | AddRandomPairAccum | `2 + 4*popcount((op >> 10) & 0x3F)` | (base,range) pair per set mask bit | Generic write (attrib 0x50: mode 5 AddRandomPair, field desc 0): target accum (accumRotXYZ +0x50..0x58, accumPosXYZ +0x5C..0x64), encoding s32 16.16, value<<16; postAction 1: run BoneHandlerTable[bone->handlerId] then outAngle=HIWORD(accumRot) (B2C440). Operands: two s16 (a,b) per set bit: adds ((b<0 ? -a : a) + rand(b)); a first rand(a) call is made and discarded. Modifier: Component mask = bits 15..10, walked from bit 15: 15=RotX 14=RotY 13=RotZ 12=PosX 11=PosY 10=PosZ (6 components, not 3). Bit 9 ignored. |
| `0x01A` | SetBoneHandler | `4 + 2*(w[0] & 0xF)` | hi byte = boneHandlerId, lo nibble = N extra words, N handler parameter words | bone->handlerId(+0x18) = param0>>8; bone+0xA0 = pointer to param1 (inline handler parameter block of N words, read later by the bone handler). |
| `0x01B` | Nop4 | `4` | ignored | No effect, skips one operand word. |
| `0x01C` | PokeBoneField | `6` | boneOffset, value | *(bone + param0) = param1 (byte or word). Raw field poke on the current bone. Modifier: op>>9 == 1 -> write s16, otherwise write u8 |
| `0x01D` | WaitBoneGoneThenEnd | `4` | boneRef | Resolve bone ref param0 (GfCinematic_GetRotationVector @0xB65370 = find bone by id in the order list; 0xFFF0+ = relative refs via self/parent ids at +0x14/+0x16, bit14 = id relative to bone[0x1B]). While it exists: wait 128 (1 tick) and retry. When not found (returns bones[0]): executes op 0x00 (end channel / kill bone). |
| `0x01E` | SetLoopCounter | `4` | count | bone byte[+0x20 + (op>>14)] = param0 (loop counter for op 0x1F). Modifier: op>>14 = counter index (0..3) |
| `0x01F` | LoopDecJump | `4` | target | --bone[+0x20+(op>>14)]; if nonzero cursor = opcode+param0 (backward loop) else fall through. Modifier: op>>14 = counter index |
| `0x020` | SetFadeLayers | `2` | - | RGB = clamp(outPosX/Y/Z,0..255) packed (B66A90); intensity = clamp(16*outAngleX,0..4096); writes intensity+colour into the 4 entries of stru_1D9898C (global colour/fade layers, 44 bytes each; op 0x6D toggles their bit1). |
| `0x021` | SetDataPointer | `8` | offset, size | Sets engine work-buffer pointers inside the magic texture buffer. Modifier: bit15: base = Magic_b_01+*(Magic_b_01+0x1C) else MAGIC_TEXTURE_BUFFER_PTR. sub=(op>>12)&7: 1 -> ctx+0xB8 = base+offset; 2 -> ctx+0x212 = base+offset, half=(size<<8)/2 stored, ctx+0x216 = ptr + half*pingPong (double buffer); other -> ctx+0x74 and ctx+0x70 = base+offset (bump arena base/cursor). |
| `0x022` | ApplyActionResult | `2` | - | Applies the GF action result (ctx+0xCC -> action: target array +8, count +16): all targets (ApplyActionResultToTargets) or only the target whose TargetSlotId == bone+0x1B (ApplyActionResultToTarget). Modifier: (op & 0xF000)==0x8000 -> all targets |
| `0x023` | SetBlendMode | `2` | - | <=3: bone+0xCC \|= 0x02000000 (semi-trans), bone+0x92 bits5-6 = abr; >3: clear semi-trans bit, bits5-6 = 1. Modifier: op>>9 = abr 0..3 (semi-transparent); >3 = opaque |
| `0x024` | SetOptionBits | `2` | - | Sets the bone's draw option byte +0xDE (OT bias / blending variants). Modifier: v=op>>9: if (v&3)!=0 bone+0xDE = v else bone+0xDE \|= v |
| `0x025` | SetSpriteOriented | `4` | spriteRef | Same as op 0x36 (sprite setup, draw handler 5) then orientation byte bone+0x1E = 9. |
| `0x026` | StartChannel | `6` | channel (0 = first free of 1..2), program | bone->chanStreamPtr[ch] = opcode + param1, chanWait[ch]=0, return-stack depth[ch]=0 (B2D8A0). Starts a parallel script on the SAME bone. If param0==0 and channels 1,2 are busy the scan reaches index 3 (overflows into chanWait); if that is nonzero too the instruction is skipped. |
| `0x027` | UploadAltTexAndImage | `4` | textureId | If a file load is busy: wait+retry. Else upload alternative texture param0 (isGF_Ifrit_AltTextureLoader @B2E700: Magic_ReadAlternativeTexture + GF_AlternativeTexture_UNK), then rewinds 4 and uploads image param0 from the loaded-file table (B2E750, as op 0x28). Each step waits chanWaitSpeed and retries the whole instruction if the VRAM queue is full. |
| `0x028` | UploadImage | `4` | imageId | Thunk to B2E750: if load busy wait; else B66560(param0) resolves image data (ctx+0xA8 index -> Magic_b_00 file) + RECT (ctx+0x9C table) and queues the VRAM upload; queue full -> wait+retry, success -> advance 4. |
| `0x029` | VramUpload | `4 if (op & 0x8000) else (8 if (op & 0x4000) else (10 if (op & 0x2000) else 4))` | rectIndex / textureId / inline RECT x, (bit14) file index / (bit13) RECT y, (bit14) 4KB page / (bit13) RECT w, (bit13) RECT h | Queues Battle_QueueVramUpload_Type0_RectData. Waits+retries while a file load is busy. Modifier: bit15: rect=ctx+0x98 table[param0] (8-byte RECTs), data=ctx+0xB4 (last loaded file) len 4; else bit14: rect=table[param0], data=Magic_b_00[param1&0x7F]+(param2<<12) len 8; else bit13: inline RECT {x,y,w,h}=param0..3, data=ctx+0xB4 len 10; else: alt-texture upload of param0 (as op 0x27 first half) len 4. |
| `0x02A` | StopChannels | `2` | - | bone->chanStreamPtr[ch]=0 (kills parallel channel scripts on the current bone). Modifier: op>>14 = channel (1..3); 0 = channels 1 and 2 |
| `0x02B` | PlaySE | `4` | attr | BdPlaySE(ctx+0xC4 table[op>>9], attr=param0, pos=0x80 centre). Modifier: op>>9 = sound index in the table at ctx+0xC4 |
| `0x02C` | StopSoundChannels | `2` | - | sub_46B450(0, mask): stops the masked sound channels. Modifier: (op>>9)&0xF = channel mask (bit n -> sound channel n+1) |
| `0x02D` | SetCameraFlag | `2` | - | BYTE1(CAMERA_FLAG_RELATED) \|= 0x80. |
| `0x02E` | SetBoneIdShort | `2` | - | bone id (+0x12) = the NEXT stream word (param0), but the cursor only advances 2, so that word is then executed as an opcode. |
| `0x02F` | StopMotion | `2` | - | Zero velRot/velPos/accelRot/accelPos (+0x68..+0x8B), recompute integrator flags (B2D460). |
| `0x030` | PlaySummonStream | `2` | - | BdPlaySummonStream(0x80, 1, op>>9). Modifier: op>>9 = stream argument |
| `0x031` | TransSummonStream | `2` | - | If file load busy wait+retry; else BdTransSummonStream(B25DB0(slot), &ctx+0xA3 ready flag). Pair with 0x34. Modifier: (op>>9)&0xF = stream slot; bit15 -> byte_1D96DC4=0 |
| `0x032` | SpawnBone | `4` | program | If the bone order list has room (list[sceneHeader+0x38 - 1]==0xFF): take the first free bone slot (chanStreamPtr[0]==0), append it to the order list, its chan0 = opcode+param0, ++sceneHeader+0x18, init (B65160), copy accumRot/accumPos, handlerId, renderListOffset, +0x1B target slot and +0xB0..0xB7 from the current bone; new+0x14 = parent id, new+0x16 = parent+0x14, new id = sceneHeader[0]++; run its bone handler; workspace+0xFC = new bone. Else skip. |
| `0x033` | SetBoneId | `4` | id | bone id (+0x12) = param0 (key for node matrices and bone refs). |
| `0x034` | WaitStreamReady | `2` | - | If ctx+0xA3 (summon-stream ready flag set by 0x31) == 0: wait chanWaitSpeed and retry; else advance. |
| `0x035` | NullNoAdvance | `2` | - | nullsub: does not advance the cursor nor set a wait -> infinite loop if executed. Unused. |
| `0x036` | SetSprite | `4` | spriteRef (bit15: hi7=group, lo8=frame) | B66270: semi-trans bits in +0xCC, frame-script pointers +0xD0/+0xD4/+0xD8 and descriptor +0xE4 from the sprite table (param0 bit15 selects group/frame form), sets draw handler 5 (B65320 also appends the bone to the draw order list); orientation +0x1E = 1. |
| `0x037` | ResetAccum | `2` | - | Zero accumRot/accumPos (+0x50..+0x67), run the bone handler, outAngle = HIWORD(accumRot). |
| `0x038` | SetTargetModelColor | `2` | - | RGB = clamp(base colour bytes at CURRENT_BS_MODEL_PALETTE + src - 128) packed, stored at (*(sceneHeader+0x60+4*bone[0x1B]))+0x28: tints the battle model of the target slot. Modifier: (op & 0xFE00) != 0 -> source outAngleXYZ, else outPosXYZ |
| `0x039` | CameraAndSound | `4` | lookAtBoneRef / voice (lo=slot, hi=sound-1) | Camera / sound opcode (existing name kept). Modifier: op>>12 sub-op (see IDA comment) |
| `0x03A` | NullNoAdvance | `2` | - | nullsub: no advance, no wait (hang if executed). Unused. |
| `0x03B` | SequenceFlags | `4` | bits (bit15 = clear) | param0>=0: SequenceState+8 \|= param0; else SequenceState+8 &= ~(param0&0x7FFF). |
| `0x03C` | SetMeshScaled | `4` | meshId | B2F380: clear semi-trans, +0xBC=0, mesh ptr +0xD8 = B657E0(meshId), draw handler 1 registered; then drawHandlerId=2 (mesh with outAngle*16 XYZ scale). |
| `0x03D` | SetMeshTexParam | `8` | drawHandler, meshRes, texParam | colour(+0xCC)=0x808080 keeping bit25; meshPtr(+0xD8)=MagResource(w1); +0xB8=16*w2; +0xBC=0; SetDrawHandler(w0 & 0xFF) (also adds the bone to the draw order list). |
| `0x03E` | SetInlineDescriptor3 | `8` | data0, data1, data2 | bone+0xBC = pointer to the 3 inline words following the opcode (&w0); data read by the draw handler. |
| `0x03F` | CreateEmbeddedModel | `4` | modelRes | Allocates (bump arena, 0x80 bytes) an embedded battle-model instance from mag resource w0 (skeleton/anim/geometry, BattleAnimHeader+Cmd, pre_Battle_ReadAnimation), stores it at bone+0xBC and selects draw handler 3 (the creature). |
| `0x040` | ColourFromBoneOutPos | `4` | srcBone | bone colour(+0xCC) RGB = clamp(0..255) of srcBone outPos X/Y/Z, top byte kept. |
| `0x041` | EmbeddedModelFlags | `6 if (op >> 12) == 1 else 4` | bits_or_data0, data1 (sub-op 1 only) | Flag/override operations on the embedded model instance at bone+0xBC (created by 0x3F). Modifier: op>>12 sub-op: 0 = clear bits w0 in instance word +2; 1 = set flag 0x400 in instance word +2 and instance+0x7C = &w0 (2 inline words); 8 = set bits w0; any other sub-op does NOT advance the cursor (hang, never used). |
| `0x042` | EntityAnimSeq *(Bahamut, Brothers only)* | `4` | seqIndex_or_target | Entity = SceneHeader entity ptr [bone+0x1B] (bone's battle-entity slot, SceneHeader+0x60+4*slot). Sub 0: QueueChainTransformation(entity, p0) = start that entity's section-5 AnimSeq p0 (multi-part chain aware; bit 0x1000 forces). Sub 2: if entity.anim_cmd.current_frame (+0x72) == total_frames (+0x73) jump rel p0. Modifier: op>>9 = sub-op: 0 = start anim seq; 2 = test anim finished. Any other value returns without advancing the cursor (would hang; unused). |
| `0x043` | SetDrawHandlerInlineData | `6 + 2*w[1]` | drawHandler, wordCount, data[wordCount] | SetDrawHandler(w0); bone+0xB8 = pointer to the inline block of w1 words; bone+0xBC=0; cursor skips the block. |
| `0x044` | SetDrawHandlerInlineDataReset | `6 + 2*w[1]` | drawHandler, wordCount, data[wordCount] | As 0x43 and also clears bone+0xC0 and bone+0xC4 (handler frame/timer state). |
| `0x045` | EntityFlagBits | `4` | bits | Sets/clears bits in the first u16 (entity_flags/status_flags) of the FF8BattleEntitySlotData of bone->slotId (sceneHeader+0x60 table). Modifier: op>>12: 0 = set bits w0; 1 = clear bits only if (sceneHeader+0x4E[slot] & w0)==0; 8 = clear bits; others = no-op. |
| `0x046` | JumpIfTargetResult | `4` | target | Conditional jump to opcode address + w0 on the action-result state of the bone's target slot; else falls through (4 bytes). Modifier: op>>9 condition on the target record (ctx+0xCC list, 24-byte entries, entry[0]==bone slot): 1 = jump if entry[3]&4; 2 = jump if entry[2]&8; 3 = jump if entry[3]&2; 4 = jump if BATTLE_SLOT_DATA[slot].status_2 & 0x2000; other (0,5..127) = jump if !(entry[3]&4). |
| `0x047` | CameraShakeFromOutPos | `2` | - | BATTLE_CAMERA_SHAKE_OFFSET_X/Y/Z = current bone outPos X/Y/Z. |
| `0x048` | OverrideEntityTransform | `2` | - | Drives the battle entity of bone->slotId from the bone outputs. Modifier: (op>>9)&0xF: 0 = entity based_position(+0x1C..+0x20) = outPos, and if bit15 also entity+0x24 = outPosY; 1 = entity based_rotation(+0x0C..+0x10) = outAngle; others = flag only. Always entity status_flags \|= 0x10. |
| `0x049` | JumpIfEntitySize | `6` | value, target | Compares entity+0x26 (s16; IDB name animation_speed_factor, used as size/radius by 0x60/0x75) with w0, jumps to opcode address + w1. Modifier: op & 0xFE00 != 0: fall through if entity+0x26 >= w0 else jump; == 0: fall through if entity+0x26 <= w0 else jump. |
| `0x04A` | SetMeshDrawHandler | `4` | meshRes | colour &= 0x2FFFFFF; +0xBC=0; meshPtr(+0xD8)=MagResource(w0); SetDrawHandler(op>>9). Modifier: op>>9 = draw handler id |
| `0x04B` | TintPaletteUpload | `10 if (op >> 12) == 1 else (8 if (op >> 12) == 2 else 6)` | clutRes (lo=res id, hi=dest bank), firstColour, colourCount (sub-op 1/2), rgbSrcBone (sub-op 1) | Copies CLUT resource (w0&0xFF) from colour w1, adds a 5-bit RGB delta (outAngle X/Y/Z, <32) to each 15-bit colour into bank 0x279822C+512*(w0>>8), uploads it as alternate texture palette. Modifier: op>>12: 0 = 256 colours, delta from own outAngle; 1 = w2 colours, delta from bone w3 outAngle; 2 = w2 colours, own outAngle. |
| `0x04C` | SetBoneHandler | `4` | boneHandler | boneHandlerId(+0x18) = w0; runs BoneHandlerTable[w0] immediately. |
| `0x04D` | SetupScreenTint | `2` | - | boneHandlerId=0, renderListOffset=0, SetDrawHandler(4) (full-screen tint). |
| `0x04E` | SetDescriptorInlineData | `6 + 2*w[1]` | slot, wordCount, data[wordCount] | *(u32*)(bone+0xB8+4*w0) = pointer to inline block of w1 words; cursor skips the block. |
| `0x04F` | Nop4F | `8` | unused0, unused1, unused2 | No-op, skips 3 words. |
| `0x050` | FreeArenaBlock | `2` | - | Arena top (ctx+0x74) -= bone+0xC4 bytes (4-aligned): releases the bone's pool. |
| `0x051` | SetOptionBitsAndC0 | `4` | valueC0 | bone+0xDE \|= op>>9; bone+0xC0 (u16) = w0. Modifier: op>>9 ORed into option bits +0xDE |
| `0x052` | SetTexture | `4` | texRes | w0 == -1: clear tpage(+0x92), uv(+0x9A), clut(+0x9E); else set them from texture resource w0 (tpage keeps bits 0x60). |
| `0x053` | MusicVolume | `4` | volume | Sets music volume w0 (low byte), no transition. Modifier: bit15: 1 = Music_SetVolumeTrans(channel 0); 0 = sub_47E3C0 (credits/intro channel, skipped if ENCOUTER_BATTLE_FLAG&2) |
| `0x054` | SetMesh | `4` | meshRes | colour &= 0x2FFFFFF; +0xBC=0; meshPtr(+0xD8)=MagResource(w0); SetDrawHandler(1). |
| `0x055` | JumpIfSummonState | `4` | target | Conditional jump to opcode address + w0 on summon-wide state. Modifier: op>>9: 1 = jump if ctx+0xD0 != ctx+0xD1; 2 = jump if (rec.byte1 & 3)==1; 3 = jump if rec.byte1 & 2; other = jump if ctx+0xD0 != 0 (rec = *(ctx+0xC0)). |
| `0x056` | SetClippedMesh | `6` | meshRes, clipMode | As 0x54, then draw handler 9 (Y-plane clipped mesh) and +0xC2 = w1. |
| `0x057` | Nop57 | `2` | - | No-op. |
| `0x058` | CreateParticlePool | `4` | count | Allocates 80*w0+16 bytes (arena) as particle pool at +0xB8, clears it, SetDrawHandler(6). |
| `0x059` | EmitParticle | `6 if op & 0x1000 else 4` | poolBone (bit12 only), particleScript | Takes next ring slot of the pool, starts its particle mini-script at (bit12: address of w0 + w1; else opcode address + w0); particle pos = current bone outPos<<8, tpage/uv/colour from pool bone. Modifier: bit12 = emit into the pool of bone w0 (else own pool). |
| `0x05A` | SetBoneHandlerParam | `6` | boneHandler, paramB0 | boneHandlerId=w0, bone+0xB0=w1, runs the handler. |
| `0x05B` | AttachToModelJoint | `8 if op & 0x800 else 4` | modelBone, joint(lo)/nodeOfs(hi), scaleX16 | Attaches the bone to a joint of an embedded or battle model (BattleModel_BuildBoneMatricesFromPose + sub_B66B80). Modifier: bit10 = use the battle entity of bone->slotId (w0 ignored); bit11 = explicit joint w1 & scale 16*w2 (else joint = own outAngleX, scale 4096, matrix scaled by modelBone outAngle*16); op>>12: 0 = accumPos = joint pos + run bone handler; 1 = own node = Cam x joint matrix; 2 = write joint matrix to bone+0x20+(w1>>8) (if nonzero) or own node. |
| `0x05C` | SnapToBoneVertex *(Leviathan, Brothers, Eden only)* | `8 if (op & 0x8000) else 6` | targetBone, vertexIndex, matrixParam (only when bit15 set) | Sets the CURRENT bone's accumPos (<<16) to the position of vertex vertexIndex of another bone's model, then calls the current bone's BoneHandlerTable[handlerId]. bit15 clear: vertex = lerp(modelA.v, modelB.v, weightBone.outPos/256 per axis) from morph descriptor *(target+0xBC) = {weightBone, modelA, modelB}, scaled by target.outAngle (16*x/4096), + parent(target).outPos. bit15 set: matrix from parent(target).outAngle + matrixParam (sub_B65590), scaled by target.outAngle, transform target.outPos and vertex of target's model (*(target+0xD8)). Modifier: bit15 (curOpcode < 0) selects mode: clear = morph-lerp vertex path (3 words); set = model-vertex transform path (4 words). Other bits ignored. |
| `0x05D` | SpawnPerTarget | `4` | program | For each target (count sceneHeader+0x41, slots at sceneHeader+0x48+i) spawns a clone bone via op 0x32's routine (0xB2D610) running program at opcode address + w0, and sets the clone's slotId(+0x1B). |
| `0x05E` | PosFromSlotHome | `2` | - | accumPos = s16 xyz at sceneHeader+0x84+8*slot <<16; runs bone handler, refreshes outAngle. |
| `0x05F` | PosFromEntityOffset | `8` | dx, dy, dz | accumPos = entity based_position + w (component skipped if w == 0x7654); boneHandlerId=1, runs handler 1. |
| `0x060` | PosFromEntityJoint | `8 if op & 0x8000 else 4` | joint, radiusMul, angle | accumPos = world position of joint w0 of the slot entity (+ orbit offset); runs bone handler. Modifier: bit15 = orbit: X += w1*(entity+0x26)*sin(16*w2)>>..., Z += ...cos. |
| `0x061` | CopyAccumFromBone | `6` | mask, srcBone | For mask bits 0..5 (rotXYZ,posXYZ) copies srcBone accumRot/accumPos; refreshes outAngle, runs bone handler. Modifier: shared with 0x62: only op word == 0x0061 exactly copies accumulators; any other word copies velocities |
| `0x062` | CopyVelFromBone | `6` | mask, srcBone | Same as 0x61 with velRot/velPos. Modifier: see 0x61 |
| `0x063` | PosFromBoneViaParent | `6` | srcBone, rotOrder | Transforms srcBone outPos by its parent bone's (parentNodeId as bone ref) rotation (order w1: 0,1,2,3) + outPos; result to own accumPos; runs bone handler. |
| `0x064` | SetBoneSlot | `4 if (op & 0x9000) == 0x1000 else 2` | slot (bit12 only) | Sets bone->slotId(+0x1B), the battle slot used by every entity opcode. Modifier: bit15 = slot of *(ctx+0xC0) (caster/primary); else bit12 = slot w0; else sceneHeader+0x48 (first target). |
| `0x065` | NodeCamRotFromPos | `4` | unused | Node = Cam x Rot(outPos as angles), translation = camera translation. |
| `0x066` | NodeCamTranslate | `4` | unused | Node = camera rotation, translation = Cam x outPos, projection = ctx+2. |
| `0x067` | NodeCamRotTranslate | `4` | unused | Node = Cam x Rot(outAngle), translation = Cam x outPos. Modifier: op>>12 = rotation order (0 default,1,2,3=ZYX) |
| `0x068` | SetParentNode | `4` | parentNodeId | parentNodeId(+0x9C) = w0 (param0, wiki says param1: wrong). |
| `0x069` | NodeChildOfParent | `6` | unused, parentBone | Node = Rot(outAngle) x Cam x parent node (w1), translation = outPos. |
| `0x06A` | NodeCamRotLocalPos | `4` | unused | Node = Cam x Rot(outAngle), translation = raw outPos, projection = ctx+2. Modifier: op>>12 = rotation order |
| `0x06B` | SetFlagCA | `2` | - | bone+0xCA \|= 0x8000 (sprite frame-set mode flag, see sprite setup sub_B66270). |
| `0x06C` | ClearFlagCA | `2` | - | bone+0xCA &= ~0x8000. |
| `0x06D` | PartyRecordFlag | `2` | - | Sets/clears bit1 of byte +5 in 4 records of 44 bytes at 0x1D9898C. Modifier: bit15: 1 = clear bit1, 0 = set bit1 |
| `0x06E` | PosFromTargetsJointAvg | `4` | joint | accumPos components = average position of joint w0 over all targets; runs bone handler. Modifier: op bits 12/13/14 = write X/Y/Z |
| `0x06F` | Nop6F | `6` | unused0, unused1 | No-op. |
| `0x070` | Unused70 | `2` | - | nullsub, does not advance (would hang); never valid. Modifier: n/a |
| `0x071` | DrawEntityInCinematic | `2` | - | entity_flags \|= 0x20 on the slot entity and renders its battle model into the cinematic render list (sub_5088A0); bit15 undoes the flag. Modifier: bit15: 1 = clear entity_flags 0x20; 0 = set it and draw the entity now |
| `0x072` | RotFromEntity | `2` | - | accumRot = slot entity based_rotation(+0x0C) <<16; refreshes outAngle. |
| `0x073` | SetSpriteOrient2 | `6` | spriteRes, paramB8 | Sprite setup (sub_B2DA00: sprite res w0, draw handler 5, orientation 1), then orientation(+0x1E)=2 and bone+0xB8 = w1 (s16). |
| `0x074` | DrawFlagBits | `4` | bits | drawFlags(+0x4C) \|= w0; with bit15 code does flags &= ~w0 then flags \|= ~w0 => flags = ~w0. Modifier: bit15: 1 = 'clear' (buggy), 0 = set |
| `0x075` | AccumFromEntitySize | `4` | mul | Selected accumulators = (entitySize * w0) << 8; runs bone handler, refreshes outAngle. Modifier: bits15..10 = mask rotX,rotY,rotZ,posX,posY,posZ; bit9 = size = max(entity+0x26, joint0 height extents) |
| `0x076` | AccumAddRandom | `4` | rangeBone | Per masked component accum += rand(range)<<16, range = rangeBone outAngle (rot) / outPos (pos); runs bone handler. Modifier: bits15..10 = mask rotX,rotY,rotZ,posX,posY,posZ |
| `0x077` | Nop77 | `6` | unused0, unused1 | No-op. |
| `0x078` | SetTexPage | `4` | page | bone+0x9A (tpage/uv base) = sceneHdr[+0x1C] + (page & 0xF) + 4*(page & 0x1F0) (X page bits 0-3, Y page bits 4-8 moved to the PSX tpage layout). |
| `0x079` | CompareFieldJump | `6` | value, target | bit15=0: if field < value fall through (+6) else jump; bit15=1: if field > value fall through else jump. Jump = cursor += target (relative to the opcode word). Used to loop until an accumulator crosses a value. Modifier: bits 12-14 = field index f: tested value = hi16 of dword at bone+0x50+4*f (0-2 accumRot XYZ, 3-5 accumPos XYZ, 6-7 velRot X/Y); bit 15 = comparison direction |
| `0x07A` | NodeFromParentAndMatrix | `6` | parentBone, matrixOffset | Node builder: own node slot (sub_B65480, keyed by bone id) = ComposeAffineTransform(parentNode, M) where parentNode = node of parentBone (camera node 0 if parentBone==0) and M = 3x3 matrix at curBone+matrixOffset (or the own node's current matrix if 0). Modifier: bit 15: node projection value (matrix +0x12) = word ctx+0x02, else 0 |
| `0x07B` | WaitThenReloadA8defTim | `2` | - | If byte_2798218 (a8def.tim loader-idle flag) != 0: queue a load_aA8defTim task (sub_508630(dword ctx+0xB8, &flag); clears the flag) and continue (+2). Else vmWaitRequest = bone->chanWaitSpeed without advancing: the same instruction re-executes next tick (wait-until). |
| `0x07C` | RandomOffsetXZ | `10` | radiusZBase, radiusZRand, radiusXBase, radiusXRand | a=rand(4096); accumPosZ += 16*(radiusZBase+rand(radiusZRand))*cos(a); accumPosX += 16*(radiusXBase+rand(radiusXRand))*sin(a) (random point on an ellipse in the XZ plane). Consumes rand(). |
| `0x07D` | SetBoneCount | `4` | count | If count > sceneHdr[+0x38] (bones in use): clears chanStreamPtr[0] of bones [old..count) and sets sceneHdr[+0x38]=count (grow only). |
| `0x081` | SetSpriteAnimOriented | `4` | frameScript | Same as op 0x80 (sub_B2DA00 -> sub_B66270(frameScript): sprite frame script at bone+0xD0.., colour code 0x2C, draw handler 5; frameScript bit15 = bank (p>>8)&0x7F + index p&0xFF), then bone+0x1E (orientation) = op>>12. Modifier: bits 12-15 = sprite orientation type written to bone+0x1E |
| `0x082` | VelocityTowardBone | `6` | targetBone, frames | velPos XYZ = (target.accumPos - cur.accumPos)/frames (linear move onto another bone's position in N ticks). |
| `0x083` | ColorFromOutAngle | `2` | - | bone+0xCC colour RGB (low 24 bits) = clamp(outAngle X/Y/Z, 0, 255); top byte (GPU code / semi-trans) kept. |
| `0x084` | CopyMatrix | `8` | srcBone, srcOffset, dstOffset | Copies a 32-byte matrix (3x3 + proj + translation) from srcBone+srcOffset (srcBone's node slot if 0) to curBone+dstOffset (cur's node slot if 0) via sub_B656A0. |
| `0x087` | VelocityScaleAccum | `6` | scale256, frames | For each masked component: vel = ((accum>>16)*(scale256-256)<<8)/frames, so after `frames` ticks accum = accum*scale256/256 (scale toward/away from the origin). Modifier: bits 15..10 = component mask (bit15 velRotX .. bit10 velPosZ) |
| `0x089` | StepEmbeddedModelAnim | `2` | - | sub_B269B0(bone+0xBC model block): SetupParentXformScaled, clear bit1 of block+2, GF_201Ifrit_StepEmbeddedModelAnim (advance creature keyframes), set bit1 again. |
| `0x08A` | BattleScreenFx | `6 if (op >> 12) not in (1, 2, 3) else (4 if (op >> 12) in (1, 2) else 2)` | value, value2 | sub-op 1: sub_501F30(value) (retarget the existing battle fx task dword_1D96EBC: +0xE=value); 2: sub_501E40(value) (create that fx task if none, param=value); 3: sub_4A8480(0) (battle state: set bit 2 at +943, clear 0x100 at +942), no operand; other: byte +0xB = value+1 and byte +9 = value2 of the struct pointed by ctx+0xC0 (action/command context). Modifier: bits 12-15 = sub-op |
| `0x08B` | StartChannel | `6` | channel, target | Starts a script on the SAME bone: channel = channel (1-3) or, if 0, first free of chanStreamPtr[1..3] (none free -> no-op). chanStreamPtr[ch] = (opcodeAddr + target) & 0x7FFFFFFF (positive = runs in the Pos phase); chanWait[ch]=0 and per-channel byte bone+0x44+ch = 0 (sub_B2D8A0). Current stream continues. |
| `0x08D` | ModelFlagsSetClear | `4` | bits | Object entry = dword sceneHdr[0x60 + 4*byte bone+0x1B]; its dword +0x7C \|= bits (or &= ~bits). Modifier: bit 15: 0 = OR bits, 1 = AND NOT bits |
| `0x08E` | RemoveFromDrawList | `2` | - | Removes the current bone id from g_GfCinematic_DrawOrderList (MAG_006_sub_B65270). |
| `0x090` | Nop10 | `10` | unused0, unused1, unused2, unused3 | No-op that just skips 10 bytes (stub in the Ifrit copy; probably a real opcode in another GF of the family). |
| `0x091` | AccumFromBoneOutputs | `6` | mask, srcBone | For mask bits 0..5 (LOW bit first: rotX,rotY,rotZ,posX,posY,posZ): cur.accum[i] = src.out[i]<<16 (outAngle XYZ / outPos XYZ); then recompute outAngle (B2C440) and run BoneHandlerTable[handlerId] (snap to another bone's pose). |
| `0x092` | SetField92And9A | `6` | value92, value9A | bone+0x92 (word after outAngleZ) = value92, bone+0x9A (tpage/uv base) = value9A. |
| `0x093` | BuildLightMatrices *(Ifrit, Leviathan only)* | `10` | lightSlot, lightBoneA, lightBoneB, lightBoneC | Builds a light set in BoneMatrixTable[slot]: +0 light-direction matrix = M(cols = 16*outPos of bones A/B/C, zero when -1) * Rot(16*lowbyte(cur.outPos)); +0x20 light-colour matrix (16*outAngle of A/B/C); +0x40 back colour = 16*cur.outAngle. Used when drawing bones with matrixSlotId != 0. |
| `0x095` | Nop4 | `4` | unused0 | No-op that just skips 4 bytes (stub in the Ifrit copy; probably a real opcode in another GF of the family). |
| `0x096` | CaptureScreenToVram *(Cerberus, Eden only)* | `6` | vramX, vramY | workspace.altTexParamA = vramX, workspace+0xF4 = vramY, then inserts into the render list a MoveImage of the current display buffer (5 strips of 64 px = 320 wide) to VRAM (vramX, vramY): screen grab for later distortion effects. Cerberus sub 0xB0EB60 (renamed GF_203Cerberus_QueueScreenCaptureMoveImage) = Eden GF_206Eden_Draw26_QueueScreenCaptureMoveImage 0xAEA2F0. |
| `0x09B` | ClearOptionBits | `2` | - | bone+0xDE (option bits: OT bias/blending) &= ~((op>>9)&0x7F). Modifier: bits 9-15 = bits to clear in bone+0xDE |
| `0x09C` | SpawnBoneChained | `4` | target | Same as op 0x32 (sub_B2D610): if the bone order list has room, take the first bone with chanStreamPtr[0]==0, append it to the bone order list and draw list, its chanStreamPtr[0] = opcodeAddr+target, clone accumPos/accumRot, handlerId, renderListOffset, +0x1B, +0xB0..0xB7, owner (+0x14/+0x16 = cur +0x12/+0x14), id = sceneHdr[0]++; run its bone handler; ws->parentMatrixPtr = new bone. 0x9C then overwrites new+0x14/+0x16 with id/+0x14 of the PREVIOUS bone in the array (chain). |
| `0x09D` | RecenterModelOffsetBone *(Brothers only)* | `10` | modelId, scaleX, scaleY, scaleZ | Computes the bounding-box centre c of model modelId's vertices (count at model+0x18, verts at model+*(model+0x14), 8-byte stride); cur.accumPos += (c*scale/256)<<16 per axis; calls the current bone handler; then subtracts c from every vertex (mesh re-centred IN PLACE, so later calls see c ~ 0). |
| `0x09E` | JumpIfCtxFlag15Clear | `4` | target | If (ctx->flags & 0x8000)==0 jump cursor += target, else continue (+4). |
| `0x09F` | JumpIfCtxFlag15Set | `4` | target | If (ctx->flags & 0x8000)!=0 jump cursor += target, else continue (+4). Decoded from raw bytes (no IDA function there). |
| `0x0A0` | JumpIfCtxFlag13Clear | `4` | target | If (ctx->flags & 0x2000)==0 jump cursor += target, else continue (+4). |
| `0x0A1` | RandomJump | `6` | threshold, target | r=\|rand(256)\|; if r <= threshold jump cursor += target, else continue (+6). Probability (threshold+1)/256. |
| `0x0A2` | Nop4 | `4` | unused0 | No-op that just skips 4 bytes (stub in the Ifrit copy; probably a real opcode in another GF of the family). |
| `0x0A4` | SetBoneHandler | `6` | handlerId, refBone | bone->boneHandlerId (+0x18) = handlerId, word bone+0xB0 = refBone; if handlerId==3, converts current outPos to polar around refBone: accumPosZ = angle<<16, accumPosX = XZ distance<<16, accumPosY = (cur.outPosY-ref.outPosY)<<16; then runs the bone handler. |
| `0x0A5` | Nop4 | `4` | unused0 | No-op that just skips 4 bytes (stub in the Ifrit copy; probably a real opcode in another GF of the family). |
| `0x0A6` | Nop4 | `4` | unused0 | No-op that just skips 4 bytes (stub in the Ifrit copy; probably a real opcode in another GF of the family). |
| `0x0A7` | SetCounter | `6` | counterIdx, value | byte sceneHdr[0x14 + counterIdx] = value (loop counter for op 0xA8). |
| `0x0A8` | DecCounterJumpNZ | `6` | counterIdx, target | if (--byte sceneHdr[0x14+counterIdx]) != 0 jump cursor += target, else continue (+6) (DJNZ loop). |
| `0x0AA` | SetLightSlot | `4` | slot | bone->lightSlot (+0xE1, matrixSlotId) = slot (-1 = 0 = unlit). |
| `0x0AC` | AccelerateToTarget | `(4 + 2*popcount((op >> 10) & 0x3F)) if (op & 0x200) else 6` | frames, targetBone, targets | For each masked component, accel = (target - accum - frames*vel) / (frames*(frames+1)) (fixed point) so the bone reaches target after `frames` ticks; target = targetBone.accum or immediate<<16. Then recomputes bone->flags (bit0 rot accel / bit3 pos accel). Modifier: bits 15..10 = component mask (accel rotX,rotY,rotZ,posX,posY,posZ); bit 9 = immediate targets instead of a target bone |
| `0x0AE` | NextTargetOrJump | `4` | doneTarget | Target iterator: if byte ctx+0xD0 (index) < byte ctx+0xD1 (count): ++index, load that target entry (ctx+0xCC = entries+20*index; sceneHdr +0x44/+0x48/+0x4E.. entity lists; bone+0x1B = first entity) and continue (+4); else jump cursor += doneTarget. |
| `0x0B0` | RandomWait | `4` | maxTicks | vmWaitRequest = rand(maxTicks)*chanWaitSpeed; if that is 0, execution continues without yielding. |
| `0x0B1` | SetSeqStateByte6 | `4` | value | byte g_GfCinematic_SequenceStatePtr+6 = value. |
| `0x0B2` | SetCtxByteA2 | `4` | value | byte ctx+0xA2 = value. |
| `0x0B6` | QueueVramBlit *(Eden only)* | `4` | blockOffset | QueueBlitCommand(&block.rect, block.x2, block.y2): queues a type-3 VRAM rect copy command in g_command_bffer. Modifier: unused (scripts encode 0x80B6) |
| `0x0B7` | SdStreamingVolume *(Eden only)* | `6` | a, b | SdStreamingVolumeTranslation(a, b): PSX streamed-audio volume change. On PC it is a stub that only prints a warning, so this is effectively a no-op. Modifier: op>>12 = sub-op; only 1 is implemented (script word 0x10B7). |
| `0x0B8` | Nop8 | `8` | unused0, unused1, unused2 | No-op that just skips 8 bytes (stub in the Ifrit copy; probably a real opcode in another GF of the family). |
| `0x0B9` | NegateField | `4` | fieldIdx | If fieldIdx > 0: dword at bone+0x50+4*fieldIdx = -itself (1-2 accumRot Y/Z -> recompute outAngle; 3-5 accumPos -> run bone handler; >=6 vel/acc, no recompute). fieldIdx 0 (accumRotX) is a no-op (>0 test). |
| `0x0BA` | NegateFieldNeg | `4` | fieldIdx | If fieldIdx < 0: dword at bone+0x50+4*fieldIdx (before accumRot: -1 = +0x4C drawFlags ...) = -itself, then recompute outAngle. Else no-op. |
| `0x0BC` | SetSpriteFrameSpeed | `4` | speed | bone+0xCA (sprite frame speed) = speed. |
| `0x0C0` | VelPosTowardSpawner | `4` | frames | Target = bone whose id is cur+0x14 (the spawner/parent bone id, set by the spawn ops 0x32/0x135); velPos XYZ = (target.accumPos - cur.accumPos) / frames (16.16), i.e. 'move onto the spawner in N frames' (follow with a wait). |
| `0x0C1` | Nop | `2` | - | No-op (skips the opcode word only). |
| `0x0C3` | PauseResumeSounds | `2` | - | bit15 clear -> sub_46B3A0(2),(3) (runs sub_46A740 on all 32 DirectSound instances = pause/stop); bit15 set -> sub_46B3E0(2),(3) (sub_46A7E0 on all 32 = resume). Modifier: bit15: 0 = pause, 1 = resume |
| `0x0C4` | NodeLocalNoCamera | `4` | unused | Node builder: this bone's node slot (sub_B65480 find-or-alloc) = rotation matrix from outAngle (order op>>12), translation = raw outPos (NOT multiplied by node 0/camera), projection word (+0x12) = *(u16*)(ctx+2). Modifier: bits12-15 (op>>12) = Euler rotation order passed to sub_B65590 |
| `0x0C5` | JumpIfBattleStage *(Brothers only)* | `6` | stageId, target | If COMBAT_SCENE_ID (current battle stage) == stageId, jump to opcode_addr + target; otherwise fall through. |
| `0x0C6` | SetFogColorAndNear | `2` | - | Depth cue/fog: GTE far colour RFC/GFC/BFC = outAngleX/Y/Z*16 (someCameraWork_45DD60); fog near = outPosX (sub_56CCC0 stores dword_209AB64 and recomputes GTE_DQA/DQB via sub_56CC50(near, far, outPosY)). |
| `0x0C7` | InitSpriteAnimH22 | `4` | spriteAnimId | Runs op 0x36's handler sub_B2DA00: sub_B66270(id) sets up the sprite frame script (bit15 set: table (id>>8)&0x7F entry id&0xFF; else table id), colour code bits, draw handler 5 + draw-list add, bone+0x1E = 1; then overrides drawHandlerId = 22. |
| `0x0CB` | NodeLookAt | `6` | eyeBone, targetBone | Node builder: look-at matrix from eyeBone.outPos toward targetBone.outPos (sub_B66E50), translation = outPos of the chosen bone, composed with node 0 (camera); projection word = 0. Modifier: bit12: translation from targetBone (1) or eyeBone (0) |
| `0x0CC` | SetBoneHandler7 | `4` | value | bone+0xB0 = value; boneHandlerId = 7; runs BoneHandler 7 immediately (handler 7: outPos = bone[*(u16*)(bone+0xA0)].outPos + hi(accumPos), i.e. position relative to another bone). |
| `0x0CD` | SetRenderListOffset | `4` | otBucket | bone->renderListOffset (+0x48) = param0 (OT depth bucket of this bone's packets). |
| `0x0CE` | SetBoneId | `4` | id | bone->id (+0x12) = param0 + bone+0x1B (per-bone battle-slot / id base byte). Changes the key used by node slots and bone lookups by id. |
| `0x0CF` | RetargetToMultiPartRoot *(Brothers, Eden only)* | `2` | - | Entity = SceneHeader entity[bone+0x1B]. If it is part of a multi-part chain (entity+0x8C): sub 0 saves the bone slot at hdr+372 and sets hdr+378 = 1; sub 1 first backs up the target count (hdr+65) to hdr+378 and the target list hdr+72.. to hdr+372... Both then retarget bone.entitySlot and hdr target[0] (+72) to the chain root (compare_com_127_501FF0 = lowest slot in the chain) and set the target count to 1. Not multi-part: hdr+378 = 0. Modifier: op>>12 = sub-op 0 or 1; any other value returns without advancing (unused). |
| `0x0D0` | RemoveFromDrawList | `2` | - | Removes the current bone from g_GfCinematic_DrawOrderList (MAG_006_sub_B65270); bone stops being drawn. |
| `0x0D1` | JumpIfModelSlot0FileId *(Brothers only)* | `6` | fileId, target | If battle model slot 0 (stru_1D9898C[0].battle_file_id) == fileId, jump to opcode_addr + target; otherwise fall through. |
| `0x0D2` | NegateMotionComponent | `4` | index | Negates dword #index of the block at bone+0x50 (0-2 accumRot XYZ, 3-5 accumPos, 6-8 velRot, 9-11 velPos), then runs the bone handler and outAngle = hi(accumRot) (sub_B2C440). Bounce / mirror. |
| `0x0D3` | ColorFromBoneOutPos | `4` | srcBone | colour (+0xCC, low 24 bits) = clamp(src.outPos XYZ * src.outAngleX / 256, 0..255) as R,G,B; top byte (code/semi-trans) kept. Animated colour through a helper bone. |
| `0x0D4` | SetColor | `4 if op & 0x8000 else 8` | r_or_grey, g (only if bit15 clear), b (only if bit15 clear) | colour (+0xCC) low 24 bits = R \| G<<8 \| B<<16, top byte kept. Modifier: bit15: 1 = grey, one word (R=G=B=param0); 0 = three words R,G,B |
| `0x0D5` | NorgBossTargetFixup *(Brothers only)* | `4` | target | Active only when COMBAT_SCENE_ID == COMBAT_SCENE_NORG_BOSS_MASTERS_ROOM. Sub 0: if the first target (hdr+72) != slot 3, set flag byte 0x2796D30 = 1 and force the target list (hdr+65 = 4, hdr+75 = 3, copy a position to hdr+156, hdr+84/+108); otherwise flag = 0. Sub 1: if flag && bone.entitySlot == 3, jump to opcode_addr + target. Modifier: op>>12 = sub-op 0 or 1. Outside the Norg room every value skips 4; inside it, other values hang. |
| `0x0D7` | Nop2 | `4` | unused | No-op skipping one operand word (stub of a feature of another GF copy). |
| `0x0DA` | RenderEntityToVram *(Brothers only)* | `2 if (op & 0x1000) else 10` | x, y, w, h | bit12 set: bone.scalePacked (colour) = (scalePacked & 0x2000000) \| 0x808000 \| ((2*byte(dword_1D98A4C) - 160)/3 + 127). bit12 clear: if the RenderCtx[1] flag word == 0, stores the rect in workspace+0xD0.., allocates a 23532-byte scratch buffer (sub_B656E0) and calls sub_B65F30, which renders battle model slot 1 (stru_1D9898C[1]) off-screen at the current bone's outPos/outAngle into VRAM rect (x, y, w, h). The cursor always advances 10. Modifier: bit12 selects the mode. |
| `0x0DF` | SetupDrawHandler29 | `10` | a, b, c, d | bone+0xB8 = 2*a, +0xBC = 2*b, +0xC0 = 0x279822C + 2*c (pointer into a global table), +0xC4 = d; drawHandlerId = 29 (0x1D) and bone added to the draw list (sub_B65320). |
| `0x0E7` | WaitUntilFieldGreater | `6` | fieldByteOffset, value | If *(s16*)(bone+0x8C+off) > value: continue (cursor += 6); else vmWaitRequest = chanWaitSpeed and cursor stays (re-test next tick). off 0/2/4 = outAngle XYZ, 8/10/12 = outPos XYZ. |
| `0x0EB` | AddToDrawList | `2` | - | Adds the current bone to g_GfCinematic_DrawOrderList if absent (sub_B652E0), drawHandlerId unchanged. |
| `0x0F1` | Nop2 | `4` | unused | No-op skipping one operand word. |
| `0x0F2` | BakeOutPosToAccum | `2` | - | accumPos XYZ = outPos XYZ << 16 and boneHandlerId = 0: freezes the current (possibly derived) position into the accumulators and returns to the plain handler. |
| `0x0FB` | WaitUntilFieldLess | `6` | fieldByteOffset, value | If *(s16*)(bone+0x8C+off) < value: continue (cursor += 6); else yield chanWaitSpeed and re-test next tick. |
| `0x0FD` | JumpIfFieldInRange | `10` | fieldByteOffset, min, max, target | If min <= *(s16*)(bone+0x8C+off) <= max: cursor += target (relative to the opcode word); else fall through (cursor += 10). |
| `0x104` | BuildBillboardSlot | `4` | slot | Aux/billboard matrix slot (32-byte table at 0x2798B68 + 32*slot): rotation = CamMatrixAlt x Rot(outAngle), translation = CamMatrixAlt * outPos; projection word = 0. |
| `0x105` | NodeFromBillboardSlot | `6` | slot, unused | Node builder: this bone's node = slot[slot] (0x2798B68 table) x Rot(outAngle, order op>>12), translation = slot * outPos; projection word = 0. Modifier: bits12-15 = Euler rotation order for sub_B65590 |
| `0x106` | WaitUntilFieldLessThanBone | `6` | fieldByteOffset, otherBone | If cur.field(off) < other.field(off): continue (cursor += 6); else yield chanWaitSpeed and re-test next tick. |
| `0x10C` | BoneFlagOps | `6 if ((op >> 12) & 0xF) in (2, 3) else 4` | mask, target (sub 2/3 only) | Same as op 0x05 but on the per-bone flag word bone+0x4A. Sub 2/3: taken jump = cursor += target (relative to opcode word), else cursor += 6. Sub 4/5: while the condition holds, yield chanWaitSpeed and re-test (length 4 once passed). Modifier: op>>12 = sub-op: 0 (and 6..15) set bits; 1 clear bits; 2 jump if (flags&mask)!=0; 3 jump if ==0; 4 wait while (flags&mask)!=0; 5 wait while ==0 |
| `0x10D` | WaitOtherBoneFlags | `6` | otherBone, mask | Tests another bone's +0x4A flag word against mask&0x3FFF; continues (cursor += 6) when satisfied, else yield chanWaitSpeed and re-test next tick. Cross-bone synchronisation. Modifier: bit12: 1 = wait until (other.flags4A & mask)==0; 0 = wait until !=0 |
| `0x110` | PlaceAtMidpoint | `6` | boneA, boneB | cur.boneHandlerId = A.boneHandlerId; cur.accumPos = midpoint of A.accumPos and B.accumPos; runs the bone handler. |
| `0x116` | NodeCamPosLocalRot | `4` | unused | Node builder: translation = node 0 (camera) * outPos, rotation = Rot(outAngle) alone (NOT multiplied by the camera); projection word = 0. Screen-aligned object at a world position. |
| `0x117` | SetRotRelativeToRoot | `8` | angleX, angleY, angleZ | accumRot XYZ = (angle - g_GfCinematic_RootAngleXYZ) << 16, then outAngle = hi(accumRot) (sub_B2C440). Absolute angle compensated by the root orientation. |
| `0x11B` | SetFogColorAndFar | `2` | - | Same as 0xC6 but sets fog FAR = outPosX (dword_C78BF0 via sub_56CCA0): GTE far colour = outAngle*16, DQA/DQB recomputed with outPosY. |
| `0x120` | SetCtx74FromCtx70 | `4` | offset64k | ctx+0x74 = ctx+0x70 + (param0 << 16). ctx+0x70/+0x74 are the pointers set by op 0x21 (sub-op 0/3+: base in the magic buffer + u32); this rewinds/sets the second pointer (bump arena top per the wiki) to base + N*64KB. |
| `0x127` | Nop4 | `6` | unused, unused | No-op skipping two operand words. |
| `0x135` | SpawnBoneWithId | `6` | program, newBoneId | Same as op 0x32 (sub_B2D610): if the bone order list has room, take the first free bone (chanStreamPtr[0]==0), append it to the bone order list, chanStreamPtr[0] = opcode word address + program, copy accumPos/accumRot/handlerId/renderListOffset/+0x1B/+0xB0..B7 from the current bone, +0x14 = current id, +0x16 = current +0x14, id = hdr[0]++, run its bone handler; then this op overwrites the new bone's id (+0x12) with newBoneId. |
| `0x13D` | BattleEntityVisibility | `4` | mode | Hide/restore battle entities (bit 2 of the 156-byte entity records at 0x1D96FC0; restore keeps entities flagged hidden in sceneHdr+78): mode 0 restore caster's side, 1 hide caster's side, 2 restore opposite side, 3 hide opposite side, 4 restore all 7, 5 hide all 7. Caster side from bones[0]+0x1B (<3 = party). |
| `0x140` | WaitScaledBySlot | `4` | frames | vmWaitRequest = (frames * u8 sceneHdr[204 + bone+0x1B]) << 7: wait scaled by a per-battle-slot factor. |

The other table entries (`0x094`, `0x09A`, `0x0A3`, `0x0AB`, `0x0AD`, `0x0AF`, `0x0B3`, `0x0B4`, `0x0B5`, `0x0BB`, `0x0BD`, `0x0BE`, `0x0CA`, `0x0DB`, `0x0E2`, `0x0ED`, `0x0F0`, `0x0F4`, `0x0F9`, `0x109`, `0x10B`, `0x112`, `0x113`, `0x11A`, `0x12E`, `0x134`, `0x136`, `0x144`, `0x145`, `0x146`) are empty handlers in every GF: they never advance the
cursor, so a script using one hangs.

## Addresses

| Op | Name | Handler (Ifrit module unless noted) |
|----|------|---------|
| `0x000` | EndChannel | `0xB2FEB0` |
| `0x001` | LoopSequenceOrFinish | `0xB2FB20` |
| `0x002` | Jump | `0xB2AE30` |
| `0x003` | Call | `0xB2AE50` |
| `0x004` | Return | `0xB2AEB0` |
| `0x005` | FlagOp | `0xB2C030` |
| `0x006` | LoadFile | `0xB2BA10` |
| `0x007` | SetFreezeOthers | `0xB2BC10` |
| `0x008` | WaitLoadDone | `0xB2BBD0` |
| `0x009` | Wait | `0xB2FE80` |
| `0x00A` | SetAccum | `0xB2C480` |
| `0x00B` | SetVel | `0xB2C480` |
| `0x00C` | SetAccel | `0xB2C480` |
| `0x00D` | SetAllAccum | `0xB2C480` |
| `0x00E` | SetAllVel | `0xB2C480` |
| `0x00F` | SetAllAccel | `0xB2C480` |
| `0x010` | AddAccum | `0xB2C480` |
| `0x011` | SetVelInt | `0xB2C480` |
| `0x012` | AddRandomAccum | `0xB2C480` |
| `0x013` | AddRandomVel | `0xB2C480` |
| `0x014` | AddRandomAccel | `0xB2C480` |
| `0x015` | AddRandomVelInt | `0xB2C480` |
| `0x016` | AddRandomAllAccum | `0xB2C480` |
| `0x017` | AddRandomPairAccum | `0xB2C480` |
| `0x01A` | SetBoneHandler | `0xB2D070` |
| `0x01B` | Nop4 | `0xB2BE10` |
| `0x01C` | PokeBoneField | `0xB2BDC0` |
| `0x01D` | WaitBoneGoneThenEnd | `0xB2FF70` |
| `0x01E` | SetLoopCounter | `0xB2AF00` |
| `0x01F` | LoopDecJump | `0xB2AF80` |
| `0x020` | SetFadeLayers | `0xB2E2F0` |
| `0x021` | SetDataPointer | `0xB2B450` |
| `0x022` | ApplyActionResult | `0xB2B530` |
| `0x023` | SetBlendMode | `0xB2DFA0` |
| `0x024` | SetOptionBits | `0xB2DAF0` |
| `0x025` | SetSpriteOriented | `0xB2DAA0` |
| `0x026` | StartChannel | `0xB2D4C0` |
| `0x027` | UploadAltTexAndImage | `0xB2E540` |
| `0x028` | UploadImage | `0xB2E530` |
| `0x029` | VramUpload | `0xB2E440` |
| `0x02A` | StopChannels | `0xB2D590` |
| `0x02B` | PlaySE | `0xB25BB0` |
| `0x02C` | StopSoundChannels | `0xB25CD0` |
| `0x02D` | SetCameraFlag | `0xB2BC60` |
| `0x02E` | SetBoneIdShort | `0xB2D5E0` |
| `0x02F` | StopMotion | `0xB2C8D0` |
| `0x030` | PlaySummonStream | `0xB25CA0` |
| `0x031` | TransSummonStream | `0xB25C00` |
| `0x032` | SpawnBone | `0xB2D610` |
| `0x033` | SetBoneId | `0xB2B020` |
| `0x034` | WaitStreamReady | `0xB25C70` |
| `0x035` | NullNoAdvance | `0xB2E6C0` |
| `0x036` | SetSprite | `0xB2DA00` |
| `0x037` | ResetAccum | `0xB2C400` |
| `0x038` | SetTargetModelColor | `0xB2E230` |
| `0x039` | CameraAndSound | `0xB2B750` |
| `0x03A` | NullNoAdvance | `0xB2FFB0` |
| `0x03B` | SequenceFlags | `0xB2B980` |
| `0x03C` | SetMeshScaled | `0xB2F3E0` |
| `0x03D` | SetMeshTexParam | `0xB2F430` |
| `0x03E` | SetInlineDescriptor3 | `0xB2F530` |
| `0x03F` | CreateEmbeddedModel | `0xB26820` |
| `0x040` | ColourFromBoneOutPos | `0xB2DD30` |
| `0x041` | EmbeddedModelFlags | `0xB26900` |
| `0x042` | EntityAnimSeq | `Bahamut 0xB24BB0, Brothers 0xAFEF60` |
| `0x043` | SetDrawHandlerInlineData | `0xB2B220` |
| `0x044` | SetDrawHandlerInlineDataReset | `0xB2B1B0` |
| `0x045` | EntityFlagBits | `0xB2BC80` |
| `0x046` | JumpIfTargetResult | `0xB2B290` |
| `0x047` | CameraShakeFromOutPos | `0xB2B9D0` |
| `0x048` | OverrideEntityTransform | `0xB2C9E0` |
| `0x049` | JumpIfEntitySize | `0xB2BD10` |
| `0x04A` | SetMeshDrawHandler | `0xB2F4C0` |
| `0x04B` | TintPaletteUpload | `0xB2E080` |
| `0x04C` | SetBoneHandler | `0xB2C3D0` |
| `0x04D` | SetupScreenTint | `0xB26DF0` |
| `0x04E` | SetDescriptorInlineData | `0xB2B950` |
| `0x04F` | Nop4F | `0xB2E580` |
| `0x050` | FreeArenaBlock | `0xB300E0` |
| `0x051` | SetOptionBitsAndC0 | `0xB2DB40` |
| `0x052` | SetTexture | `0xB2E5C0` |
| `0x053` | MusicVolume | `0xB25D10` |
| `0x054` | SetMesh | `0xB2F380` |
| `0x055` | JumpIfSummonState | `0xB2B380` |
| `0x056` | SetClippedMesh | `0xB2F3F0` |
| `0x057` | Nop57 | `0xB2AE20` |
| `0x058` | CreateParticlePool | `0xB29D70` |
| `0x059` | EmitParticle | `0xB29DE0` |
| `0x05A` | SetBoneHandlerParam | `0xB2D8D0` |
| `0x05B` | AttachToModelJoint | `0xB2F090` |
| `0x05C` | SnapToBoneVertex | `Leviathan 0xB64090, Brothers 0xAFEBF0, Eden 0xAF3660` |
| `0x05D` | SpawnPerTarget | `0xB2D7F0` |
| `0x05E` | PosFromSlotHome | `0xB2C870` |
| `0x05F` | PosFromEntityOffset | `0xB2C780` |
| `0x060` | PosFromEntityJoint | `0xB2CE00` |
| `0x061` | CopyAccumFromBone | `0xB2CCC0` |
| `0x062` | CopyVelFromBone | `0xB2CCC0` |
| `0x063` | PosFromBoneViaParent | `0xB2EF70` |
| `0x064` | SetBoneSlot | `0xB2B0E0` |
| `0x065` | NodeCamRotFromPos | `0xB2E7D0` |
| `0x066` | NodeCamTranslate | `0xB2E830` |
| `0x067` | NodeCamRotTranslate | `0xB2E950` |
| `0x068` | SetParentNode | `0xB2ECB0` |
| `0x069` | NodeChildOfParent | `0xB2E9E0` |
| `0x06A` | NodeCamRotLocalPos | `0xB2E8C0` |
| `0x06B` | SetFlagCA | `0xB2DB90` |
| `0x06C` | ClearFlagCA | `0xB2DBB0` |
| `0x06D` | PartyRecordFlag | `0xB2BD70` |
| `0x06E` | PosFromTargetsJointAvg | `0xB2CF70` |
| `0x06F` | Nop6F | `0xB2E590` |
| `0x070` | Unused70 | `0xB26810` |
| `0x071` | DrawEntityInCinematic | `0xB2DCC0` |
| `0x072` | RotFromEntity | `0xB2C820` |
| `0x073` | SetSpriteOrient2 | `0xB2DA40` |
| `0x074` | DrawFlagBits | `0xB2C360` |
| `0x075` | AccumFromEntitySize | `0xB2D0B0` |
| `0x076` | AccumAddRandom | `0xB2D170` |
| `0x077` | Nop77 | `0xB2BE20` |
| `0x078` | SetTexPage | `0xB2E040` |
| `0x079` | CompareFieldJump | `0xB2BE30` |
| `0x07A` | NodeFromParentAndMatrix | `0xB2EB90` |
| `0x07B` | WaitThenReloadA8defTim | `0xB2BB80` |
| `0x07C` | RandomOffsetXZ | `0xB2D210` |
| `0x07D` | SetBoneCount | `0xB2BE90` |
| `0x081` | SetSpriteAnimOriented | `0xB2DA80` |
| `0x082` | VelocityTowardBone | `0xB2C900` |
| `0x083` | ColorFromOutAngle | `0xB2DF10` |
| `0x084` | CopyMatrix | `0xB2EC40` |
| `0x087` | VelocityScaleAccum | `0xB2D2B0` |
| `0x089` | StepEmbeddedModelAnim | `0xB26980` |
| `0x08A` | BattleScreenFx | `0xB2BEF0` |
| `0x08B` | StartChannel | `0xB2D520` |
| `0x08D` | ModelFlagsSetClear | `0xB2BFA0` |
| `0x08E` | RemoveFromDrawList | `0xB2DBD0` |
| `0x090` | Nop10 | `0xB2E5A0` |
| `0x091` | AccumFromBoneOutputs | `0xB2CD50` |
| `0x092` | SetField92And9A | `0xB2E670` |
| `0x093` | BuildLightMatrices | `Ifrit 0xB2F590, Leviathan 0xB64420` |
| `0x095` | Nop4 | `0xB2EB80` |
| `0x096` | CaptureScreenToVram | `Cerberus 0xB16F60, Eden 0xAF2760` |
| `0x09B` | ClearOptionBits | `0xB2DAB0` |
| `0x09C` | SpawnBoneChained | `0xB2D860` |
| `0x09D` | RecenterModelOffsetBone | `Brothers 0xAFEFF0` |
| `0x09E` | JumpIfCtxFlag15Clear | `0xB2FFC0` |
| `0x09F` | JumpIfCtxFlag15Set | `0xB2FFF0` |
| `0x0A0` | JumpIfCtxFlag13Clear | `0xB30030` |
| `0x0A1` | RandomJump | `0xB2B080` |
| `0x0A2` | Nop4 | `0xB30020` |
| `0x0A4` | SetBoneHandler | `0xB2D920` |
| `0x0A5` | Nop4 | `0xB2AF30` |
| `0x0A6` | Nop4 | `0xB2AF40` |
| `0x0A7` | SetCounter | `0xB2AF50` |
| `0x0A8` | DecCounterJumpNZ | `0xB2AFD0` |
| `0x0AA` | SetLightSlot | `0xB2F7D0` |
| `0x0AC` | AccelerateToTarget | `0xB2D340` |
| `0x0AE` | NextTargetOrJump | `0xB2FBE0` |
| `0x0B0` | RandomWait | `0xB30060` |
| `0x0B1` | SetSeqStateByte6 | `0xB2B150` |
| `0x0B2` | SetCtxByteA2 | `0xB2BB50` |
| `0x0B6` | QueueVramBlit | `Eden 0xAF27C0` |
| `0x0B7` | SdStreamingVolume | `Eden 0xAE3350` |
| `0x0B8` | Nop8 | `0xB26BF0` |
| `0x0B9` | NegateField | `0xB2CA80` |
| `0x0BA` | NegateFieldNeg | `0xB2CAD0` |
| `0x0BC` | SetSpriteFrameSpeed | `0xB2DC60` |
| `0x0C0` | VelPosTowardSpawner | `0xB2C970` |
| `0x0C1` | Nop | `0xB2C3B0` |
| `0x0C3` | PauseResumeSounds | `0xB25D60` |
| `0x0C4` | NodeLocalNoCamera | `0xB2EA70` |
| `0x0C5` | JumpIfBattleStage | `Brothers 0xAFB240` |
| `0x0C6` | SetFogColorAndNear | `0xB2F820` |
| `0x0C7` | InitSpriteAnimH22 | `0xB2DA30` |
| `0x0CB` | NodeLookAt | `0xB2ECE0` |
| `0x0CC` | SetBoneHandler7 | `0xB2CB70` |
| `0x0CD` | SetRenderListOffset | `0xB2B170` |
| `0x0CE` | SetBoneId | `0xB2B050` |
| `0x0CF` | RetargetToMultiPartRoot | `Brothers 0xAFCBE0, Eden 0xAF1830` |
| `0x0D0` | RemoveFromDrawList | `0xB2DC00` |
| `0x0D1` | JumpIfModelSlot0FileId | `Brothers 0xAFB270` |
| `0x0D2` | NegateMotionComponent | `0xB2CB20` |
| `0x0D3` | ColorFromBoneOutPos | `0xB2DE30` |
| `0x0D4` | SetColor | `0xB2DDD0` |
| `0x0D5` | NorgBossTargetFixup | `Brothers 0xAFB630` |
| `0x0D7` | Nop2 | `0xB2C240` |
| `0x0DA` | RenderEntityToVram | `Brothers 0xAFDB00` |
| `0x0DF` | SetupDrawHandler29 | `0xB2E3A0` |
| `0x0E7` | WaitUntilFieldGreater | `0xB2C250` |
| `0x0EB` | AddToDrawList | `0xB2DC30` |
| `0x0F1` | Nop2 | `0xB2F8C0` |
| `0x0F2` | BakeOutPosToAccum | `0xB2CBD0` |
| `0x0FB` | WaitUntilFieldLess | `0xB2C290` |
| `0x0FD` | JumpIfFieldInRange | `0xB2C320` |
| `0x104` | BuildBillboardSlot | `0xB2EDB0` |
| `0x105` | NodeFromBillboardSlot | `0xB2EE40` |
| `0x106` | WaitUntilFieldLessThanBone | `0xB2C2D0` |
| `0x10C` | BoneFlagOps | `0xB2C100` |
| `0x10D` | WaitOtherBoneFlags | `0xB2C1D0` |
| `0x110` | PlaceAtMidpoint | `0xB2CC20` |
| `0x116` | NodeCamPosLocalRot | `0xB2EB10` |
| `0x117` | SetRotRelativeToRoot | `0xB2EF00` |
| `0x11B` | SetFogColorAndFar | `0xB2F870` |
| `0x120` | SetCtx74FromCtx70 | `0xB2B420` |
| `0x127` | Nop4 | `0xB2E430` |
| `0x135` | SpawnBoneWithId | `0xB2D7C0` |
| `0x13D` | BattleEntityVisibility | `0xB2B5D0` |
| `0x140` | WaitScaledBySlot | `0xB300A0` |
| `0x1874F10` | Ifrit VmOpcodeTable | 0x147 entries; the table of every GF = its DrawHandlerTable + `0x1A4` |
| `0x1874ED6` / `0x1874EF0` | Ifrit VmOpcodeAttribTable / VmFieldDescTable | generic writes |
| `0x1874894` | GF_201Ifrit_MagDescriptor | per-GF resource descriptor (VRAM rectangles, file slots) |
| `0x2798A68` | g_GfCinematic_MagFileSlot | 64 file slot base pointers |
