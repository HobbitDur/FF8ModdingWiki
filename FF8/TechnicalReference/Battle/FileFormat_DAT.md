---
title: Monster files (c0mxxx.dat)
layout: default
parent: Battle
author: Mirex, JWP, random_npc, myst6re, HobbitDur
permalink: /technical-reference/battle/monster-files-c0mxxxdat/
---

1. TOC
   {:toc}

## Header

DAT file is divided into 11 sections (except for c0m127.dat, which contains only 2 sections : 7th and 8th).

| Offset              | Length                | Description                                            |
|---------------------|-----------------------|--------------------------------------------------------|
| 0                   | 4 bytes               | Number of sections (always =11, except for c0m127.dat) |
| 4                   | nbSections \* 4 bytes | Section Positions                                      |
| 4 + nbSections \* 4 | 4 bytes               | File size                                              |

## Section 1: Skeleton

More info on [OpenVIII](https://github.com/MaKiPL/OpenVIII/blob/4ac151daad7cd1475eb0694dd0715bc35d7a4b39/FF8/debug_battleDat.cs)

| Offset | Length                      | Description     |
|--------|-----------------------------|-----------------|
| 0      | 1 byte                      | Number of bones |
| 1      | 1 byte                      | Extra data      |
| 2      | 6 bytes                     | Unknown         |
| 8      | s16f (divide by 4096f)      | scaleX          |
| 10     | s16f (divide by 4096f)      | scale -Z        |
| 12     | s16f (divide by 4096f)      | scale Y         |
| 14     | 2 bytes                     | Unknown         |
| 16     | Number of bones \* 48 bytes | Bones           |

When "Extra data" is 1, it adds 3 axes transformations to be read from the bone struct. In vanilla, this extra data flag is always at 0.

### Bone struct

| Offset | Length                 | Description              |
|--------|------------------------|--------------------------|
| 0      | 2 bytes                | Parent id                |
| 2      | s16f (divide by 4096f) | Bone size (?)            |
| 4      | s16f (divide by 4096f) | RotX, multiplied by 360f |
| 6      | s16f (divide by 4096f) | RotY, multiplied by 360f |
| 8      | s16f (divide by 4096f) | RotZ, multiplied by 360f |
| 10     | s16f (divide by 4096f) | someX                    |
| 12     | s16f (divide by 4096f) | someY                    |
| 14     | s16f (divide by 4096f) | someZ                    |
| 16     | 32 bytes               | Unknown (often empty)    |

SomeX, someY and someZ are read only if the "Extra data" flag is set.
If the entity is slowed, the RotX, RotY and RotZ are divided by 2.
The 3 rotation are added to the animation, so it's a fix bone change applied to all animation.

## Section 2: Model geometry

### Header (data sub table)

| Offset             | Length               | Description             |
|--------------------|----------------------|-------------------------|
| 0                  | 4 bytes              | Number of objects       |
| 4                  | nbObjects \* 4 bytes | Object Positions        |
| 4 + nbObjects \* 4 | Varies               | Object Data (see below) |
| Varies             | 4 bytes              | Total count of vertices |

### Object Data

| Offset | Length                     | Description               |
|--------|----------------------------|---------------------------|
| 0      | 2 bytes                    | Number of Vertices Data   |
| 2      | Varies \* NbVerticesData   | Vertices Data (see below) |
| Varies | 4 - (absolutePosition % 4) | Padding (0x00)            |
| Varies | 2 bytes                    | Num triangles             |
| Varies | 2 bytes                    | Num quads                 |
| Varies | 8 bytes                    | Always empty              |
| Varies | numTriangles \* 16 bytes   | Triangles                 |
| Varies | numQuads \* 20 bytes       | Quads                     |

#### Vertice Data

| Offset | Length                | Description                       |
|--------|-----------------------|-----------------------------------|
| 0      | 2 bytes               | Bone id                           |
| 2      | 2 bytes               | Number of vertices                |
| 4      | nbVertices \* 6 bytes | Vertices (nbVertices \* 3 shorts) |

#### Useful structures

```
struct vertice {  
     sint16    x, y, z;  
};
```

(sizeof = 6)

```
struct triangle {  
     uint16    vertex_indexes[3]; // vertex_indexes[0] &= 0xFFF, other bits are unknown  
     uint8 texCoords1[2];  
     uint8 texCoords2[2];  
     uint16    textureID_related;  
     uint8 texCoords3[2];  
     uint16    u; // textureID_related2  
};
```

(sizeof = 16)

```
struct quad {  
     uint16    vertex_indexes[4]; // vertex_indexes[0] &= 0xFFF, other bits are unknown  
     uint8 texCoords1[2];  
     uint16    textureID_related;  
     uint8 texCoords2[2];  
     uint16    u; // textureID_related2  
     uint8 texCoords3[2];  
     uint8 texCoords4[2];  
};
```

(sizeof = 20)

## Section 3: Model animation

More info on [OpenVIII](https://github.com/MaKiPL/OpenVIII/blob/4ac151daad7cd1475eb0694dd0715bc35d7a4b39/FF8/debug_battleDat.cs)

### Header (data sub table)

| Offset      | Length                  | Description          |
|-------------|-------------------------|----------------------|
| 0           | 4 bytes                 | Number of animations |
| 4           | nbAnimations \* 4 bytes | Animations Pointers  |
| AnimPointer | Varies                  | Animation            |

### Animation

| Offset | Length | Description      |
|--------|--------|------------------|
| 0      | 1 byte | Number of frames |
| 1      | Varies | Animation frame  |

### Animation frame

Each frame is one vector location and BonesCount*RotationVectorData. Vector location is used to manipulate the model in world space, where all the animation is
rotating each bone.
The frames work accumulatively, so in order to get the final rotation at in example frame 5, you have to add all rotations from frames 0,1,2,3 and 4.

| Offset | Length                          | Description                                                              |
|--------|---------------------------------|--------------------------------------------------------------------------|
| 0      | LocationVectorData              | LocationVectorData                                                       |
| Varies | 1 BIT                           | Mode bit (1 if there is additional data in RotationVectorData, bUnk1...) |
| Varies | RotationVectorData * bonesCount | Rotation Vector data per bone                                            |

### Location vector data

| Offset | Length       | Description |
|--------|--------------|-------------|
| 0      | PositionType | Location X  |
| Varies | PositionType | Location Y  |
| Varies | PositionType | Location Z  |

### Rotation vector data

| Offset | Length                      | Description |
|--------|-----------------------------|-------------|
| 0      | RotationType                | Rotation X  |
| Varies | RotationType                | Rotation Y  |
| Varies | RotationType                | Rotation Z  |
| Varies | 1 BIT                       | bUnk1       |
| Varies | 0 if bUnk1==0, else 16 BITs | Unk1 data   |
| Varies | 1 BIT                       | bUnk2       |
| Varies | 0 if bUnk2==0, else 16 BITs | Unk2 data   |
| Varies | 1 BIT                       | bUnk3       |
| Varies | 0 if bUnk3==0, else 16 BITs | Unk3 data   |

We don't know what the Unk1, Unk2 and Unk3 do. Enemies works without them, but as it's important to keep up with the current bit position, we need to read it
anyway

### Position type

Position is BIT length. First we read the count of bits to read by reading first 2 bits.

| Offset | Length           | Description      |
|--------|------------------|------------------|
| 0      | 2 BITs           | PositionTypeBits |
| 0+0b11 | PositionTypeBits | Vector axis      |

#### PositionTypeBits

| PositionTypeBits value | Bits to read for one vector axis |
|------------------------|----------------------------------|
| 0b00                   | 3                                |
| 0b01                   | 6                                |
| 0b10                   | 9                                |
| 0b11                   | 16                               |

### Rotation type

Rotation is also BIT length. First read first bit to see, if there's rotation data. If no, continue. If yes, then read the rotation data similar to Position
Type

| Offset  | Length           | Description                           |
|---------|------------------|---------------------------------------|
| 0       | 1 BIT            | IsRotationTypeAvailable               |
| 0+0b1   | 2 BIT            | RotationTypeBits                      |
| 0+0b100 | RotationTypeBits | Rotation vector axis (pitch/yaw/roll) |

#### RotationTypeBits

| PositionTypeBits value | Bits to read for one vector axis |
|------------------------|----------------------------------|
| 0b00                   | 3                                |
| 0b01                   | 6                                |
| 0b10                   | 8                                |
| 0b11                   | 12                               |

## Section 4: Dynamic texture data

Optional section, often empty.
It contains info on dynamic texture (like blink-eyes)

It starts with a list of offset followed by data.
The offset list start with a 0 offset which must be ignored. Each offset is 2 bytes.
The number of offset need to be deduced: so read each 2 bytes till you read a bit that is inferior to the previous.
The offset value start at the beginning of the section.

Each data pointed by the offset look like this:

```
struct DynamicTextureData
{
  BYTE textureNum;                      ///< Which texture page/slot to use
  BYTE vram_x_offset;
  BYTE vram_y_offset;
  BYTE sprite_width_in_vram_coord;      ///< Width of region to copy, in X you need to multiply by 2 to get the pixel value
  BYTE sprite_height_in_vram_coord;     ///< Height of region to copy
  BYTE number_destination;
  WORD unk2;
  BYTE source_uv_u;                     ///< X offset of source sprite in VRAM (x2 to get pixel for X)
  BYTE source_uv_v;                     ///< Y offset of source sprite in VRAM
  UV_VRAM dest_uv[6]; ///< Actually pairs of bytes: {dest_u, dest_v} for each frame
};
struct UV_VRAM
{
  BYTE u;                               ///< X in VRAM (x2 to get pixel)
  BYTE v;                               ///< Y in VRAM
};

```

The number of `dest_uv` depends of the `number_of_destination`.

Important point is that all UV and sprite width/height is expressed in VRAM value, which mean you need to multiply the X value by 2 to get the pixel value (Y is
already in pixel).

TODO: Add the monster list that have an animated texture section.

## Section 5: Animation sequences

### Header

| Offset | Length                 | Description         |
|--------|------------------------|---------------------|
| 0      | 2 bytes                | Number of sequences |
| 2      | nbSequences \* 2 bytes | Sequences Positions |

Contain sequence of animation. They define specific movement/action when using an ability/or just being.
Some old info can be found here: [Qhimm message](https://forums.qhimm.com/index.php?topic=19362.0)

Now how it works. The sequence animation is composed of opcode, followed by parameters (often 1, sometimes 2 or 0). Each op code define an action to do.

### Execution model

The sequences are executed by a small byte-code VM (`computeAnimationSequence` at `0x50DB40` in FF8_EN.exe). The VM itself only implements the arithmetic
opcodes (`C0`-`E5`) and the conditional jumps (`E6`-`F3`); everything below `0xC0` is delegated to a callback. The same VM is reused with different callbacks
for:

- **Entity sequences** (this section 5): callbacks `AnimSeq_DispatchActionOpcode` (opcodes &lt; 0xC0), `AnimSeq_ReadSpecialVar_C3` (C3-family special reads) and
  `AnimSeq_WriteSpecialVar_E5` (E5 special writes).
- **Camera sequences** (section 6): same VM with camera-specific callbacks (see section 6).

The per-frame driver (`AnimSeq_UpdateEntityPerFrame` at `0x504290`) runs every battle frame:

1. If a *background sequence id* was set (opcode `9A`), that sequence is executed first, every frame.
2. The main sequence resumes at the byte offset saved from the previous frame (`currentSequenceCurrentByte`).
3. The interpreter runs until an opcode *pauses* it: queuing an animation (opcode &lt; 0x80), `A1` (yield), `A9` (terminate), `AC`, or `B9` (frame wait). The
   current byte offset is then saved and execution resumes there the next frame.

All `int16` parameters are **little-endian**.

### Opcode between C0 and E3: set a "current_value"

Those opcode are meant to store and modify a local values (that is then used by later opcodes).  
To analyze it, it is done on two part. First defining how to use the param, then knowing how to modify the local variable (store in what is called the _stack_)

#### How to interpret the params

Do OpCode & 3:

- case 0: 2 param int16 value (C0, C4, D0,...)
- case 1: 1 param sign value (C1, C5, C9, D1, D5, D9, DD,...)
- case 2: 1 param unsigned value (C2, C6, D2, DA,...)
- case 3: 1 param, two cases: (C3, C7, CB, CF, D3...)
    - Param < 0x80: special handle to set param value (cf dedicated chapter).
    - Param >= 0x80: Read from stack value stored at param (from E5 opcode)

#### How to modify the local var

Do opcode & FC:

- case 0xC0u: (C0, C1, C2, C3)
  current_value_computed = param;
- case 0xC4u:// C4, C5, C6, C7
  current_value_computed += param;
- case 0xC8u:
  current_value_computed -= param;
- case 0xCCu:
  current_value_computed *= param;
- case 0xD0u:
  current_value_computed /= param;
- case 0xD4u:
  current_value_computed &= param;
- case 0xD8u:
  current_value_computed |= param;
- case 0xDCu:
  current_value_computed ^= param;
- case 0xE0u:
  current_value_computed %= param;

#### Case 3 param < 0x80:

On each case a specific code is done, often it just read a value in memory that as a specific purpose.
Full list (from `AnimSeq_ReadSpecialVar_C3` at `0x5044B0`):

| Param              | Value read                                                                                                                  |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------|
| 0x00-0x07          | Local variable `e5_data_saved[param]` of the entity (written by E5 0x00-0x07)                                               |
| 0x08               | Battle state flags (`some_flag`)                                                                                            |
| 0x09               | Current frame of the active animation                                                                                       |
| 0x0A               | Total frames of the active animation                                                                                        |
| 0x0B               | Base sequence id (`basedAnimSeq`)                                                                                           |
| 0x0C               | Random value [0..32767]                                                                                                     |
| 0x0D               | Position Z                                                                                                                  |
| 0x0E               | Position X                                                                                                                  |
| 0x0F               | Position Y                                                                                                                  |
| 0x10               | Speed depending of distance to target. On itself, speed_factor = 1000. On a target, speed_factor = 5000\*distance/4096      |
| 0x11               | Speed from 0x10 adjusted: Speed_0x10 - (2000\*(attacker_speed_factor + target_speed_factor)/4096). Set to 1000 if on itself |
| 0x12               | Stored sine (set via E5 0x12)                                                                                               |
| 0x13               | Stored cosine (set via E5 0x13)                                                                                             |
| 0x14-0x16          | Weapon anim data words at +28/+30/+32 (writable via E5 0x14-0x16), 0 if no weapon                                           |
| 0x17               | Y rotation & 0xFFF                                                                                                          |
| 0x18               | Slot id of the current target                                                                                               |
| 0x19               | Hit flag 2 of the current target (`hitType2 & 2`)                                                                           |
| 0x1A               | Angle between the target and the attacker & 0xFFF                                                                           |
| 0x1B               | Own slot id                                                                                                                 |
| 0x1C               | 2048 if monster; else 0 if (rotY & 0xFFF) <= 2048, else 4096                                                                |
| 0x1F               | Animation status flags (`anim_status`)                                                                                      |
| 0x22               | Back attack / preemptive strike info                                                                                        |
| 0x23               | Camera flag (shared with camera sequences)                                                                                  |
| 0x24               | Model size scale                                                                                                            |
| 0x25 / 0x26 / 0x27 | Z / Y / X scale                                                                                                             |
| 0x28               | 1 if GF summon data loaded, else 0                                                                                          |
| 0x29               | Unknown byte                                                                                                                |
| 0x2A               | Animation speed factor                                                                                                      |
| 0x2C               | Original sceneout position X                                                                                                |
| 0x2E               | 1 if another entity is alive and free (not dead/stopped/petrified), else 0                                                  |
| 0x33               | Combat scene ID                                                                                                             |
| 0x35               | Y offset of target's effect-spawn point 0xF1 above its base Y                                                               |
| 0x36               | Y offset of target's effect-spawn point 0xF0 above its base Y                                                               |
| 0x37               | Invisibility flag                                                                                                           |
| > 0x77             | `current_value = *(E5_7F_save + 2 * (0x7F - param))`; so at 0x7F it's E5_7F_save[0]                                         |

Unlisted values return 0.

### E5 case:

two cases:
Param < 0x80: special handle to save (and use) the current_value
Param >= 0x80: Write to stack current_value at param

#### Param < 0x80

Full list (from `AnimSeq_WriteSpecialVar_E5` at `0x5048E0`):

| Param              | Effect                                                                                                                   |
|--------------------|--------------------------------------------------------------------------------------------------------------------------|
| 0x00-0x07          | Write local variable `e5_data_saved[param]` (readable via C3 0x00-0x07)                                                  |
| 0x08               | Write battle state flags (`some_flag`)                                                                                   |
| 0x0B               | Set base sequence id (`basedAnimSeq`)                                                                                    |
| 0x0D               | Set position Z                                                                                                           |
| 0x0E               | Set position X                                                                                                           |
| 0x0F               | Set position Y                                                                                                           |
| 0x12               | Compute and store sin(current_value) (readable via C3 0x12)                                                              |
| 0x13               | Compute and store cos(current_value) (readable via C3 0x13)                                                              |
| 0x14-0x16          | Write weapon anim data words at +28/+30/+32 (no-op if no weapon)                                                         |
| 0x17               | Rotate the entity (Y rotation, 0-4096)                                                                                   |
| 0x1D               | Move hit particle position (written into skeleton header)                                                                |
| 0x1E               | Move selection cursor position (written into skeleton header)                                                            |
| 0x20               | Hide/show a model part: value > 0 hides section-2 object (value-1), value < 0 shows object (-1-value). See opcodes 81/A6 |
| 0x21               | Same as 0x30 (target forwards/backwards rotation)                                                                        |
| 0x24               | Set model scale (4096 is 1x scale)                                                                                       |
| 0x25 / 0x26 / 0x27 | Set Z / Y / X scale                                                                                                      |
| 0x2A               | Set animation speed factor                                                                                               |
| 0x2B               | Set the entity's camera var (readable from camera sequences via camera-C3 0x15)                                          |
| 0x2C               | Set X position (also updates original sceneout X)                                                                        |
| 0x2D               | Set target's Y scale (makes target flat)                                                                                 |
| 0x2F               | Set a global linked to battle stage 137 (Edea's room)                                                                    |
| 0x30               | Set target's rotation (forwards/backwards) (gets reset when target comes back from an attack)                            |
| 0x31               | Set target's rotation (left/right) (gets reset when target comes back from an attack)                                    |
| 0x32               | Set target's rotation (lean to a side) (gets reset when target comes back from an attack)                                |
| 0x34               | Set target's Y position                                                                                                  |
| > 0x77             | `*(E5_7F_save + 2 * (127 - param)) = current_value` (so 0x7F writes E5_7F_save[0])                                       |

### 0xE4: set to zero (BUGGED)

`E4` sets `current_value = 0` but **never advances the instruction pointer**: the interpreter re-reads the same byte forever and the game hangs. Confirmed in
FF8_EN.exe (`xor esi, esi` then jump back to the opcode fetch). Do not use it; use `C1 00` instead.

### 0xE6 to 0xF3: jumps

Those are conditional jumps (if). They check `current_value` and either continue the flow or jump. The jump target is **relative to the address of the jump
opcode itself**: `new_position = opcode_position + offset` (the offset is signed, so backward jumps are possible — offset 0 would hang).

Byte-offset versions (1 signed byte param, opcode size 2):

- E6: Unconditional jump
- E7: jump if current_value > 0
- E8: jump if current_value >= 0
- E9: jump if current_value == 0
- EA: jump if current_value != 0
- EB: jump if current_value <= 0
- EC: jump if current_value < 0

int16 versions (2 bytes little-endian offset, opcode size 3), same conditions:

- ED: Unconditional jump
- EE: current_value > 0
- EF: current_value >= 0
- F0: current_value == 0
- F1: current_value != 0
- F2: current_value <= 0
- F3: current_value < 0

When the condition is not met, execution continues after the parameter (opcode + 2 bytes for E6-EC, opcode + 3 bytes for ED-F3).

### Opcode < 0x80

This queues the animation by the ID defined in section 3 and pauses the sequence until the animation finishes.
Does *(BATTLE_STATE_CONTROLER + 44) |= 0xAu; and end local sequence

## 0x80 <= Opcode < C0

Full opcode list (decoded from `AnimSeq_DispatchActionOpcode` at `0x504BB0` in FF8_EN.exe). Opcodes not listed (87-8F, B3) are no-ops with no parameter.

| Opcode             | Params | Description                                                                                                                                                                                                                                                                                                                                          |
|--------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 80 XX              | 1      | Step **dynamic texture animation** XX (section 4). If `number_destination` > 0: advances the frame counter (data byte 6 = speed in 1/8th frame units, byte 7 = counter) and blits the next dest UV. If `number_destination` == 0: scrolls the texture region in VRAM by byte 6 pixels (UV scroll, e.g. conveyor/water)                               |
| 81 XX              | 1      | Restore hidden model part XX: clears bit XX of the hidden-parts bitmask (set via E5 0x20) and runs a 15-frame re-attach effect                                                                                                                                                                                                                       |
| 82                 | 0      | Set combat flag 0x40 (unknown purpose)                                                                                                                                                                                                                                                                                                               |
| 83 XX              | 1      | Load battle stage camera/geometry (XX = load command bitmask)                                                                                                                                                                                                                                                                                        |
| 84 XX              | 1      | Start a sine-wave vertex animation task (model wobble), XX = wave parameter                                                                                                                                                                                                                                                                          |
| 85                 | 0      | Hide the yellow triangle of chara selection (clears the flag)                                                                                                                                                                                                                                                                                        |
| 86                 | 0      | Show the yellow triangle of chara selection (sets the flag)                                                                                                                                                                                                                                                                                          |
| 90 XX              | 1      | **Multi-part monster link**: XX < 3 unlinks the whole chain; 3 <= XX < 0x10 links self to monster slot XX; XX >= 0x10 links self to the loaded monster whose com_id == XX (used by Ultimecia final form, etc.)                                                                                                                                       |
| 91 XX YY           | 2      | Print monster battle text XX with param YY (urgent text channel)                                                                                                                                                                                                                                                                                     |
| 92 XX              | 1      | **Setup targeting context**: XX < 7 → target = slot XX (attacker unchanged); XX >= 7 → attacker = self, keep current target mask. Recomputes C3 0x10/0x11 speed factors, C3 0x18 target slot, C3 0x1A angle, and rotates the attacker toward the target                                                                                              |
| 93 XX YY           | 2      | Trigger sequence YY on another entity: XX < 0x10 = slot id; XX >= 0x10 = every loaded entity (except self) with com_id == XX                                                                                                                                                                                                                         |
| 94                 | 0      | Toggle the shadow                                                                                                                                                                                                                                                                                                                                    |
| 95                 | 0      | Reset current position to original position (X and Z)                                                                                                                                                                                                                                                                                                |
| 96 X1 X2 X3        | 3      | **Camera shake** (earthquake): offset interpolated from X1 to X2 over X3 frames, sign alternating every frame                                                                                                                                                                                                                                        |
| 97                 | var    | Play actor sound effect: same encoding as B8 but plays through the actor SE path (`linkedToSoundAnimSeq(addr, 0x80)`)                                                                                                                                                                                                                                |
| 98                 | var    | Same as 97, second variant (`linkedToSoundAnimSeq(addr, 0x81)`)                                                                                                                                                                                                                                                                                      |
| 99 XX YY..FF       | var    | Queue **walk/step effect + sound** timeline on bone XX. Each following byte: bits 0-5 = frames to wait, bit 6 = skip effect, bit 7 = skip sound. List ends with FF                                                                                                                                                                                   |
| 9A XX              | 1      | Set **background sequence id** XX: that sequence is executed every frame *before* the main one (cleared by writing 0; skipped while combat flag 0x08 is set)                                                                                                                                                                                         |
| 9B XX YY           | 2      | Start texture animation XX with destination index computed through the C3 special-value reader from YY                                                                                                                                                                                                                                               |
| 9C                 | 0      | Turn back (combat_flags  = TURN_BACK)                                                                                                                                                                                                                                                                                                                |
| 9D                 | 0      | Mark self as dead/removed in the battle bookkeeping data (flag 0x40, status bit 0, setMaskEnable)                                                                                                                                                                                                                                                    |
| 9E XX YY           | 2      | Move self smoothly toward entity slot XX, YY = speed/step parameter                                                                                                                                                                                                                                                                                  |
| 9F XX..FF          | var    | **Blink timeline**: each byte = frame delay before toggling texture animation 0 on/off; ends with FF. The task auto-ends when the sequence changes                                                                                                                                                                                                   |
| A0 XX              | 1      | Play animation XX *without* waiting; skipped if XX is already the current animation (unless in preparation phase)                                                                                                                                                                                                                                    |
| A1                 | 0      | **Yield**: pause the sequence for this frame, resume here next frame                                                                                                                                                                                                                                                                                 |
| A2                 | 0      | End of sequence: reset base rotation and jump to the next queued/auto sequence                                                                                                                                                                                                                                                                       |
| A3                 | 0      | Set current sequence as base sequence; jump to the pending next sequence if it exists, else set the continue flag                                                                                                                                                                                                                                    |
| A4                 | 0      | Set the preparation flag (0x4)                                                                                                                                                                                                                                                                                                                       |
| A5 XX              | 1      | Trigger magic/limit effect (loads from magic.fs etc.). XX forced to 01 when battle flag 0x40000000 is set: <br>- 00: character/boss magic effect<br>- 01: GF summon<br>- 02: normal limit break<br>- 03: finisher limit break<br>- 04: enemy magic effect<br>- 05: like 04 (placeholder, unused)                                                     |
| A6 X1 + 4×int16    | 9      | **Detach model part**: detaches section-2 object X1 from the skeleton and makes it fly off with initial velocity (vx, vy, vz); velocity decays 1/8 per frame, gravity +100/frame on Y. 4th int16 stored in the task (unknown use). The object is hidden via the hidden-parts bitmask (see E5 0x20 / opcode 81)                                       |
| A7 XX              | 1      | Jump to sequence XX                                                                                                                                                                                                                                                                                                                                  |
| A8 XX              | 1      | Fade / visibility: <br>- 01: slowly disappear (re-appears suddenly at the end)<br>- 02 or 0C: re-appear<br>- 03: disappear and stay invisible<br>- 06: leave combat by disappearing (no XP gained)                                                                                                                                                   |
| A9                 | 0      | End sequence and terminate transforms (`TerminateSequenceAndUpdateTransforms`)                                                                                                                                                                                                                                                                       |
| AA                 | 0      | Apply the pending **action result** (damage numbers, status, hit animation) to **all targets** at once                                                                                                                                                                                                                                               |
| AB X1 X2 ... A1    | var    | **Renzokuken init**: reads two bytes, then scans the following opcodes until A1, summing the frame counts of each animation opcode into stage buckets (split at each A0). Used to build the R1-trigger timing                                                                                                                                        |
| AC XX              | 1      | Restore the base model (undo model swap: comFileData = comFileDataBis, also for the weapon), reset rotation, queue sequence XX \| 0x1000 (auto-pick if XX = 0) and end the sequence                                                                                                                                                                  |
| AD X1 X2X3 X4      | 4      | Same task as AE with the midpoint bone forced to FF: AE(X1, FF, X2X3, X4)                                                                                                                                                                                                                                                                            |
| AE X1 X2 X3X4 X5   | 5      | **Drag the target**: per-frame task that pulls the target's position toward attacker bone X1 (X1 = FF: target's own base position; bit 7 of X1 selects the target reference point). X2 = second bone to average with (midpoint) unless FF. X3X4 = int16 bone interpolation factor. X5 = duration in frames. The target's shadow is hidden until done |
| AF XX              | 1      | Trigger sequence XX on the current target                                                                                                                                                                                                                                                                                                            |
| B0 XX FF ..        | var    | Spawn **hit particle effect on the attacker** (see flag table below)                                                                                                                                                                                                                                                                                 |
| B1 XX YY..FF       | var    | Same as 99 but for the SFX variant (walk sound type 2)                                                                                                                                                                                                                                                                                               |
| B2                 | 0      | Apply the action result to the current target, then **advance to the next target** (multi-target attacks)                                                                                                                                                                                                                                            |
| B4 XX FF ..        | var    | Apply target hit reaction (snap-back if flagged) + spawn **hit particle effect on the target**. Same encoding as B0; the visual is skipped when the attack missed                                                                                                                                                                                    |
| B5 / B6 X1 X2 (X3) | var    | Play local (monster .dat section 9 AKAO) sound X1. X2 = flag byte (see B8). X1 >= 7 unexpected                                                                                                                                                                                                                                                       |
| B7                 | 0      | Apply the action result (damage/status/hit animation) to the current target                                                                                                                                                                                                                                                                          |
| B8 X1 X2 (X3)      | var    | Play sound X1 from the general audio list. X2 flag byte:<br>- & 0x4: volume = 128<br>- else & 0x1: volume from target's position on screen, else from attacker's position<br>- & 0x2: one more param X3 = channel mask<br>When the attack missed, plays the miss sound instead                                                                       |
| B9 XX              | 1      | **Wait XX - 1 frames** before executing the next opcode (pauses the interpreter)                                                                                                                                                                                                                                                                     |
| BA                 | 0      | Advance the current animation by one frame (manual tick)                                                                                                                                                                                                                                                                                             |
| BB                 | 0      | Print the pending battle text (ability/attack name), if one is flagged                                                                                                                                                                                                                                                                               |
| BC XX              | 1      | Nop (parameter ignored)                                                                                                                                                                                                                                                                                                                              |
| BD XX YY           | 2      | Start texture animation XX with destination index YY                                                                                                                                                                                                                                                                                                 |
| BE XX              | 1      | Stop texture animation 0; XX != 0 sets the GF-hidden status flag (model hidden during GF summon), XX == 0 clears it                                                                                                                                                                                                                                  |
| BF XX              | 1      | If the attack connected (hit animation set, no snap-back reaction pending, target not defending/invincible): trigger hit sequence XX on the target; else skip                                                                                                                                                                                        |

### B0/B4 flag byte

The second byte of B0/B4 defines the parameter count and the effect placement:

| Bit                    | Meaning                                                                                                                                                                                                                  |
|------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x01                   | One more byte (effect param 1)                                                                                                                                                                                           |
| 0x02                   | One more byte (effect param 2; bit 7 of it is forced from the camera angle)                                                                                                                                              |
| 0x04                   | One more byte (effect param 3)                                                                                                                                                                                           |
| 0x08                   | Spawn the effect at a specific bone → one more byte (bone id). **Warning**: the game consumes this byte only when the attack hits; on a miss (B4) it would be executed as the next opcode. Vanilla data avoids this case |
| 0x10                   | Spawn the effect at a random bone (no extra byte)                                                                                                                                                                        |
| 0x20                   | Flip the effect direction (used with 0x08/0x10)                                                                                                                                                                          |
| 0x40                   | Custom position → three more int16 LE (x, y, z)                                                                                                                                                                          |
| none of 0x08/0x10/0x40 | Spawn the default effect on the entity                                                                                                                                                                                   |

### Example

Normal attack sequence of the Bite Bug, fully annotated:

**Walk toward the target:**

- `C3 11`: current_value = adjusted speed factor (distance-scaled)
- `C5 64`: current_value += 100
- `E5 FF`: stack[0xFF] = current_value
- `C1 00`: current_value = 0
- `CB FF`: current_value -= stack[0xFF] (negate: total distance to cover)
- `E5 02`: local var e5[2] = current_value
- `BB`: print the attack name
- `08`: play animation 08 and wait (attack stance)
- `A0 09`: play animation 09 without waiting (fly forward)
- `C3 0A`: current_value = total frames of the current animation
- `E5 7F`: E5_7F_save[0] = current_value (loop counter = frame count)
- **loop start:**
- `C3 02` `C9 00` `E5 FF`: stack[0xFF] = e5[2]
- `C3 FF` `CF 09` `E5 FE`: stack[0xFE] = e5[2] * current_frame
- `C3 FE` `D3 0A` `E5 FD`: stack[0xFD] = e5[2] * current_frame / total_frames (linear interpolation)
- `C1 00` `C7 FD`: current_value = stack[0xFD]
- `E5 0F`: write the position offset → the model slides toward the target
- `A1`: yield (resume next frame)
- `C3 7F` `C5 FF` `E5 7F`: decrement the loop counter
- `E7 E1`: if counter > 0, jump back 0x100-0xE1 = 31 bytes (loop start)

**Bite three times:**

- `A0 0A`: play animation 0A without waiting (bite)
- `B9 06`: wait 5 frames
- `97 02 01`: play actor sound 02, volume from the target's position
- `BF 04`: if the attack connected, trigger hit sequence 04 on the target
- `B4 1A 00`: apply hit reaction + spawn hit effect 0x1A on the target (default placement)
- `B9 04`: wait 3 frames
- `97 02 01` `BF 04` `B4 1A 00`: second bite
- `B9 04` `97 02 01` `B4 1A 00`: third bite
- `AA`: apply the action result (damage/status) to all targets
- `C3 08` `DA 80` `E5 08`: state flags |= 0x80
- `C3 08` `D9 08` `E5 08`: state flags |= 0x08
- `A1`: yield

**Walk back:**

- `A0 0B`: play animation 0B without waiting (fly back)
- `C3 0A` `E5 7F`: loop counter = total frames
- `C1 00` `CB 02` `E5 FF`: stack[0xFF] = -e5[2] (reverse direction)
- `C3 FF` `CF 09` `E5 FE` `C3 FE` `D3 0A` `E5 FD`: interpolate as before
- `C3 02` `C7 FD` `E5 0F`: position = e5[2] + interpolated value (slides back home)
- `A1`: yield
- `C3 7F` `C5 FF` `E5 7F` `E7 E1`: decrement and loop
- `0C`: play animation 0C and wait (landing)
- `A2`: end of sequence (jump to the next queued/idle sequence)

## Section 6: Camera sequence

The camera sequences reuse the **same byte-code VM** as section 5 (arithmetic `C0`-`E5` and jumps `E6`-`F3` behave identically), with camera-specific
callbacks (`CameraSeq_DispatchActionOpcode` at `0x509810`, driver `BS_UpdateCameraSequence` at `0x509610`).

Camera opcodes < 0xC0:

| Opcode | Params | Description                                                                         |
|--------|--------|-------------------------------------------------------------------------------------|
| 00 XX  | 1      | Play camera animation XX from the current camera animation collection               |
| 01     | 0      | Yield (pause for this frame, resume next frame)                                     |
| 02     | 0      | End the camera sequence and clear the camera pointer                                |
| 03     | 0      | Unknown camera operation + clear flag bit 15                                        |
| 04 XX  | 1      | Start a camera oscillation (wobble) task with param XX                              |
| 05 XX  | 1      | Play camera animation whose id is read through the camera special-value reader (XX) |
| 06     | 0      | Set camera flag bit 15                                                              |
| 07     | 0      | Clear camera flag bit 15                                                            |
| 08     | 0      | Reset the wobble factor (4096) and the camera flag                                  |
| 09 XX  | 1      | Nop (parameter skipped)                                                             |
| other  | -      | Reset wobble factor and end the sequence                                            |

Camera C3-family special reads (`CameraSeq_ReadSpecialVar_C3` at `0x509640`):

| Param     | Value read                                                       |
|-----------|------------------------------------------------------------------|
| 0x00-0x07 | Camera animation local variables                                 |
| 0x10      | Camera flag variable                                             |
| 0x11      | Random value                                                     |
| 0x13      | Count of party members in a specific animation state             |
| 0x15      | Target entity's camera var (set by entity sequences via E5 0x2B) |
| 0x16      | Target's animation status (with dead-flag fixup)                 |
| 0x17      | Battle task value                                                |
| 0x18      | Attacker slot id                                                 |
| 0x19      | Target slot id                                                   |
| 0x1A      | Number of affected targets                                       |
| 0x1B      | Count of party members with animation status 0                   |
| 0x1C-0x22 | Random value modulo 2..8                                         |
| > 0x77    | Camera stack (same principle as the entity stack)                |

Camera E5 writes: params < 8 write the camera animation local variables, 0x10 writes the camera flag variable, > 0x77 writes the camera stack.

## Section 7: Informations & stats

| Offset | Length     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|--------|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | 24 bytes   | Monster name in [FF8 String]({{site.baseurl}}/technical-reference/Miscellaneous/FF8String)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 24     | 4 bytes    | HP values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 28     | 4 bytes    | Str values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 32     | 4 bytes    | Vit values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 36     | 4 bytes    | Mag values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 40     | 4 bytes    | Spr values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 44     | 4 bytes    | Spd values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 48     | 4 bytes    | Eva values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 52     | 16*4 bytes | [Abilities](#abilities), low level                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 116    | 16*4 bytes | [Abilities](#abilities), med level                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 180    | 16*4 bytes | [Abilities](#abilities), high level                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 244    | 1 byte     | Med level start                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| 245    | 1 byte     | High level start                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 246    | 1 byte     | Camera flag (activated when launching magic for ex) 0x8 => value=5, 0x4 => value=4, else value=3-flag_value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 247    | 1 byte     | [LSB] Zombie / Fly / zz1 / LvUp-Down Immunity / HP Hidden / Auto-Reflect / Auto-Shell / Auto-Protect [MSB]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 248    | 3 bytes    | [Card]({{site.baseurl}}/technical-reference/Lists/Card_list#card-info) (drop/mod/rare mod)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 251    | 3 bytes    | [Devour]({{site.baseurl}}/technical-reference/Lists/Devour_list#devour-effects) (low/med/high)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 254    | 1 byte     | [LSB] <span id="increase-surprise-rng">[IncreaseSurpriseRNG]({{site.baseurl}}/technical-reference/battle/surprise-attack)</span> / <span id="decrease-surprise-rng">[DecreaseSurpriseRNG]({{site.baseurl}}/technical-reference/battle/surprise-attack)</span>  / <span id="surprise-attack-immunity">[SurpriseAttackImmunity]({{site.baseurl}}/technical-reference/battle/surprise-attack)</span> / <span id="increase-change-escape">[IncreaseChanceEscape]({{site.baseurl}}/technical-reference/battle/escape)</span>  / <span id="decrease-change-escape">[DecreaseChanceEscape]({{site.baseurl}}/technical-reference/battle/escape)</span> / unused / Gravity Immunity / Always obtains card [MSB] |
| 255    | 1 byte     | Unknown (flags, 4 bits used)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 256    | 2 bytes    | Extra EXP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| 258    | 2 bytes    | EXP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 260    | 8 bytes    | [Draw](#draw-mug-drop) (low)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 268    | 8 bytes    | [Draw](#draw-mug-drop) (med)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 276    | 8 bytes    | [Draw](#draw-mug-drop) (high)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 284    | 8 bytes    | [Mug](#draw-mug-drop)(low)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 292    | 8 bytes    | [Mug](#draw-mug-drop)(med)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| 300    | 8 bytes    | [Mug](#draw-mug-drop)(high)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| 308    | 8 bytes    | [Drop](#draw-mug-drop) (low)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 316    | 8 bytes    | [Drop](#draw-mug-drop) (med)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| 324    | 8 bytes    | [Drop](#draw-mug-drop) (high)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| 332    | 1 byte     | [Mug rate](#rate-value)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 333    | 1 byte     | [Drop rate](#rate-value)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| 334    | 1 byte     | Padding (0x00)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| 335    | 1 byte     | APs                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| 336    | 16 bytes   | [Renzokuken data](#renzokuken-data)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                         
| 352    | 8 bytes    | [Elemental resistance](#elemental-resistance) (Fire, Ice, Thunder, Earth, Poison, Wind, Water, Holy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| 360    | 20 bytes   | [Status resistance](#Status-resistance) (Death, Poison, Petrify, Darkness, Silence, Berserk, Zombie, Sleep,<br> Haste, Slow, Stop, Regen, Reflect, Doom, Slow Petrify, Float, Drain, Confuse , Expulsion, VIT0(but unused by the game))                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

### Abilities

Abilities are composed of:

| Length | Description                                                                             |
|--------|-----------------------------------------------------------------------------------------|
| 1 byte | [AbilityTypeID]({{site.baseurl}}/technical-reference/list/ability-list/#abilities-type) |
| 1 byte | [AnimationSequenceID](#animationsequenceid)                                             |
| 2 byte | [AbilityID]({{site.baseurl}}/technical-reference//list/ability-list/#monster_ability)   |

#### AnimationSequenceID

Refer to a sequence in the [Section 5](#section-5-animation-sequences)

### Renzokuken data

The data is 8*2 bytes, each 2 bytes corresponding to an ID on the [Special Action list]({{site.baseurl}}/technical-reference/list/special-action-list/)

### Draw Mug Drop

Each section is composed of 8 bytes corresponding to 4 id ([magic]({{site.baseurl}}/technical-reference/list/magic-list) for
draw, [Item]({{site.baseurl}}/technical-reference/list/item) for mug & drop) and 4 quantity.
Quantity is not used for draw (always 0 but no impact on game when changing it)

| Length | Description |
|--------|-------------|
| 1 byte | ID 1        |
| 1 byte | Quantity 1  |
| 1 byte | ID 2        |
| 1 byte | Quantity 2  |
| 1 byte | ID 3        |
| 1 byte | Quantity 3  |
| 1 byte | ID 4        |
| 1 byte | Quantity 4  |

### Elemental resistance

The % def value follow the formula:
value% = 900 - value_hex * 10

and to revert back:
value_hex = floor((900 - value%) / 10))

### Status resistance

The % def value follow the formula:
value% = value_hex - 100

and to revert back:
value_hex = value% + 100

### Rate value

The % def value follow the formula:
value% = value_hex * 100 / 255

and to revert back:
value_hex = value% * 255 / 100

## Section 8: Battle scripts/AI

| Offset | Length  | Description                |
|--------|---------|----------------------------|
| 0      | 4 bytes | Number of sub-sections     |
| 4      | 4 bytes | Offset to AI sub-section   |
| 8      | 4 bytes | Offset to text offsets     |
| 12     | 4 bytes | Offset to text sub-section |

### AI

| Offset | Length  | Description                              |
|--------|---------|------------------------------------------|
| 0      | 4 bytes | Offset to init code                      |
| 4      | 4 bytes | Offset to code executed at ennemy's turn |
| 8      | 4 bytes | Offset to counterattack code             |
| 12     | 4 bytes | Offset to death code                     |
| 16     | 4 bytes | Offset to "before dying or taking a hit" |

The runtime interpreter and section dispatch are documented in [Enemy AI VM Runtime](../enemy-ai-vm-runtime/). The per-opcode authoring reference
is [Battle Scripts](../battle-scripts/).

### Texts

Text offsets is a list of text positions (2 bytes each) in the text sub-section.

## Section 9: Sounds

Contains AKAO sequences (can be empty).

| Offset           | Length             | Description      |
|------------------|--------------------|------------------|
| 0                | 2 bytes            | Number of AKAOs  |
| 2                | nbAKAOs \* 2 bytes | AKAOs Positions  |
| 2 + nbAKAOs \* 2 | 2 bytes            | End of section 9 |
| 4 + nbAKAOs \* 2 | Varies \* nbAKAOs  | AKAOs            |

## Section 10: Sounds/Unknown

Contains AKAO sequence + unknown data (can be empty).

## Section 11: Textures

Contains some [TIMs]({{site.baseurl}}/technical-reference/psx/tim-file-format).

| Offset          | Length            | Description    |
|-----------------|-------------------|----------------|
| 0               | 4 bytes           | Number of TIMs |
| 4               | nbTIMs \* 4 bytes | TIMs Positions |
| 4 + nbTIMs \* 4 | 4 bytes           | End of file    |
| 8 + nbTIMs \* 4 | Varies \* nbTIMs  | TIMs           |

## Some info on other dat info

This section will grow to be independent, for the moment I write my findings.

File in dXcYYY.dat are files for battle characters. the X is the ID of the character (0 for squall), and YYY to differentiate the different battle (Two texture
diff for seed exam)
There is 7 section, the 3 first section are the same than monsters.

File in dXwYYY.dat are files for weapon battle characters. the X is the ID of the character (0 for squall), and YYY the ID of the weapon (0 for gunblade)
There is 8 section, the 3 first section are the same than monsters.

