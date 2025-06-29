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
| 0      | 2 bytes                     | Number of bones |
| 2      | 6 bytes                     | Unknown         |
| 8      | s16f (divide by 4096f)      | scaleX          |
| 10     | s16f (divide by 4096f)      | scale -Z        |
| 12     | s16f (divide by 4096f)      | scale Y         |
| 14     | 2 bytes                     | Unknown         |
| 16     | Number of bones \* 48 bytes | Bones           |

### Bone struct

| Offset | Length                 | Description                 |
|--------|------------------------|-----------------------------|
| 0      | 2 bytes                | Parent id                   |
| 2      | s16f (divide by 4096f) | Bone size (?)               |
| 4      | s16f (divide by 4096f) | unknown, multiplied by 360f |
| 6      | s16f (divide by 4096f) | unknown, multiplied by 360f |
| 8      | s16f (divide by 4096f) | unknown, multiplied by 360f |
| 10     | s16f (divide by 4096f) | unknown                     |
| 12     | s16f (divide by 4096f) | unknown                     |
| 14     | s16f (divide by 4096f) | unknown                     |
| 16     | 28 bytes               | Unknown (often empty)       |

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

Each frame is one vector location and BonesCount*RotationVectorData. Vector location is used to manipulate the model in world space, where all the animation is rotating each bone.
The frames work accumulatively, so in order to get the final rotation at in example frame 5, you have to add all rotations from frames 0,1,2,3 and 4.

| Offset | Length                          | Description                               |
|--------|---------------------------------|-------------------------------------------|
| 0      | LocationVectorData              | LocationVectorData                        |
| Varies | 1 BIT                           | Mode bit (contains additional info check) |
| Varies | RotationVectorData * bonesCount | Rotation Vector data per bone             |

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

We don't know what the Unk1, Unk2 and Unk3 do. Enemies works without them, but as it's important to keep up with the current bit position, we need to read it anyway

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

Rotation is also BIT length. First read first bit to see, if there's rotation data. If no, continue. If yes, then read the rotation data similar to Position Type

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

## Section 4: Texture animation data

Optional section, often empty.
It contains info on animated texture (like blink-eyes)
It starts with a list of offset followed by data that look like this:

```
struct texAnim
{
	uint8 textureNum;
	uint8 originalUCoord; //All UV coords here are for the upper left corner
	uint8 originalVCoord;
	uint8 regionUSize;
	uint8 regionVSize;
	uint8 copiedRegionCount; //1 less than the actual number
	uint8 unknown1;
	uint8 unknown2;
	//Insert remaining UV coords here
};
```

Refer to this message for more info: [Qhimm message](https://forums.qhimm.com/index.php?topic=11137.msg165149#msg165149)

## Section 5: Animation sequences

### Header

| Offset | Length                 | Description         |
|--------|------------------------|---------------------|
| 0      | 2 bytes                | Number of sequences |
| 2      | nbSequences \* 2 bytes | Sequences Positions |

Contain sequence of animation. They define specific movement/action when using an ability/or just being.
Some old info can be found here: [Qhimm message](https://forums.qhimm.com/index.php?topic=19362.0)

Now how it works. The sequence animation is composed of opcode, followed by parameters (often 1, sometimes 2 or 0). Each op code define an action to do.


### Opcode between C0 and E3: set a "current_value"
Those opcode are meant to store and modify a local values (that is then used by later opcodes).  
To analyze it, it is done on two part. First defining how to use the param, then knowing how to modify the local variable (store in what is called the _stack_)

#### How to interpret the params
Do OpCode & 3:
- case 0: 2 param int16 value (C0, C4, D0,...)
- case 1: 1 param sign value (C1, C5, C9, D1, D9 ...)
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
Param values known:
- Param < 0x07: current_value = *(BATTLE_STATE_CONTROLER + 2 * param + 20); BATTLE_STATE_CONTROLER is at 0x1D98200
- 0x08: LOWORD(return_value) = *(BATTLE_STATE_CONTROLER + 44);
- 0x09:  LOWORD(return_value) = *(SHARED_ANIMATION_DATA + 6);(High byte of C3_12_SINE)
- 0x0A: LOWORD(return_value) = *(SHARED_ANIMATION_DATA + 7); (High byte of C3_13_09_COSINE)
- 0x10: Speed depending of distance to target
- 0x11: Some other computed speed depending of distance and slot id data
- 0x33: Combat scene ID
- Param > 0x77: current_value = *(E5_7F_save + 2 * (0x7F - param)); so at 0x7F it's E5_7F_save

### E5 case:
two cases:
    Param < 0x80: special handle to save (and use) the current_value
    Param >= 0x80: Write to stack current_value at param
    
#### Param < 0x80 
- Param < 0x08: *(BATTLE_STATE_CONTROLER + 2 * sequence_command_param_1 + 20) = current_value_computed; BATTLE_STATE_CONTROLER is at 0x1D98200
- 0x08: *(BATTLE_STATE_CONTROLER + 44) = current_value_computed;
- 0x0F: *(BATTLE_STATE_CONTROLER + 40) = current_value_computed;
- 0x17: rotate the sequence (0-4096)
- 0x1D: move hit particle position ?
- 0x1E: move selection cursor position ?
- 0x21: same as 0x31
- 0x24: set enemy model scale (4096 is 1x scale)
- 0x25: set enemy's Z scale
- 0x26: set enemy's Y scale
- 0x27: set enemy's X scale
- 0x2C: set enemy's X position
- 0x2D: set target's Y scale? (seems to make target flat)
- 0x30: set target's rotation (forwards/backwards) (gets reset when target comes back from an attack)
- 0x31: set target's rotation (left/right) (gets reset when target comes back from an attack)
- 0x32: set target's rotation (lean to a side) (gets reset when target comes back from an attack)
- 0x34: set target's Y position
- Param > 0x77: *(dword_1D9820C + 2 * (127 - sequence_command_param_1)) = current_value_computed; (so 0x7F save at 0x1D9820C)

### 0xE6 < opcode < 0xF3
Those are conditional jump (if)
Those value check the current_value and decide to either continue the flow or jump the number of hex value define by the param
E7: current_value > 0:

    
### Opcode < 0x80
This queue the animation by the ID defined in section 3
Does *(BATTLE_STATE_CONTROLER + 44) |= 0xAu; and end local sequence

## 0x80 < Opcode < C0
Each one of those opcode are special:
- 85: Hide the yellow triangle of chara selection
- 86: Show the yellow triangle of chara selection
- 94: Toogle the shadow
- 95: Reset current position to original position (X and Z)
- 97: *param_address_anim_seq = linkedToSoundAnimSeq(*param_address_anim_seq, 128);
- A0 XX: Queue animation XX and  *(BATTLE_STATE_CONTROLER + 44) |= 2u;
- A1: End local sequence
- A2: Seems to be the end of seq animation, but didn't confirm on the code
- A8: Makes the enemy fade away or fade in, based on the following byte.
  - param is 0x01: Slowly dissapear (but re-appear suddenly at the end)
  - param 0x02 or 0x0C: re-appear (Make the animation of re-appearing, so dissapear suddenly to re-appear slowly)
  - param is 0x03: Make it Invisible (by dissapearing and saying invisible)
  - param is 0x06: Leave the combat by dissapearing (no xp gained)
- AA: Dunno
- B7: Dunno
- B9 XX : Set BATTLE_STATE_CONTROLER + 1 to XX - 1
- BB: Handle text
- B4: Seems to jump to other anim sequence
- BF: No idea

### Example
If we use the normal attack animation of bite bug, here for each opcode/param what it does:
- C3 11: Set current_value to some speed (between 1000 and 5000)
- C5 64: Add 0x64 to current_value
- E5 FF: Store current_value to stack 0xFF
- C1 00: Set current_value to 0x00
- CB FF: Substract to current_value value stored at 0xFF (so did actually put a minus in front of current_value)
- E5 02: Store current_value to BATTLE_STATE_CONTROLER + 2 * param + 20, 
- BB: Handle text
- 08: Queue animation 08
- A0 09: Queue animation 09
- C3 0A: Set current_value to some angle
- E5 7F: Save current_value to 0x1D9820C
- C3 02: Set current_value to *(0x1D98218); (linked to E5_02_CASE)
- C9 00: Substract 0 to current_value
- E5 FF:  Store current_value to stack 0xFF
- C3 FF: Read value from stack 0xFF
- CF 09: Multiply the current_value by an angle
- E5 FE: Store current_value to stack 0xFE
- C3 FE: Set current_value to stack 0xFE
- D3 0A: Divide current_value by an angle
- E5 FD: Store current_value to stack 0xFD
- C1 00: Set current_value to 0
- C7 FD: Add to current_value value at stack FD
- E5 0F: Set BATTLE_STATE_CONTROLER + 40 to current_value
- A1: End local sequence
- C3 7F: Set current_value to value stored at E5_7F_save
- C5 FF: Add -1 to current_value
- E5 7F: Save current_value to 0x1D9820C
- E7 E1: Save current_value to stack 0xE1
- A0 0A: Queue animation 0A
- B9 06: Set BATTLE_STATE_CONTROLER + 1 to 05
- 97: Linked to sound, seems no param but I could be wrong
- 02: Queue anim 02 
- 01: Queue anim 01
- BF 04: No idea
- B4: Jump to some other anim seq ?
- 1A: Queue animation 1A
- 00: Queue animation 00
- B9 04: Set BATTLE_STATE_CONTROLER + 1 to 03
- 97 02 01: Cf upper
- BF: Some sound effect ?
- 04: Queue animation 04
- B4 1A 00: Cf upper
- B9 04: Set BATTLE_STATE_CONTROLER + 1 to 03
- 97 02 01: cf upper
- B4 1A 00 : cf upper
- AA: Dunno
- C3 08: Set current_value to BATTLE_STATE_CONTROLER + 44
- DA 80: Current_value OR 0x80
- E5 08 : set BATTLE_STATE_CONTROLER + 44 to current_value
- C3 08: Set current_value to BATTLE_STATE_CONTROLER + 44
- D9 08: current_value OR 0x08
- E5 08: set BATTLE_STATE_CONTROLER + 44 to current_value
- A1: End local sequence
- A0 0B: Queue animation 0B
- C3 0A: Set current value to some angle
- E5 7F: Save current_value to 0x1D9820C
- C1 00: Set current_value to 0
- CB 02: Decrease current_value by the value at *(BATTLE_STATE_CONTROLER + 24);
- E5 FF: Store current_value at stack 0xFF
- C3 FF: Set current_value from stack 0xFF
- CF 09: Multiply current_value by some angle
- E5 FE: Write current_value to stack 0xFE
- C3 FE: set current_value from stack 0xFE
- D3 0A: Divide current_value by an angle
- E5 FD: Write current_value to stack 0xFD
- C3 02: Set current_value to value at *(BATTLE_STATE_CONTROLER + 24);
- C7 FD:  Add to current_value value at stack FD
- E5 0F: Set BATTLE_STATE_CONTROLER + 40 to current_value
- A1: End local sequence
- C3 7F: Set current_value to value stored at E5_7F_save
- C5 FF: Add -1 to current_value
- E5 7F: Save current_value to 0x1D9820C
- E7 E1: If current_value > 0: continue, either jump E1 forward
- 0C: Play animation 0C
- A2: Dunno

## Section 6: Camera sequence

Not analysed, but defined camera work.

## Section 7: Informations & stats

| Offset | Length     | Description                                                                                                                                                                                                                            |
|--------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0      | 24 bytes   | Monster name in [FF8 String]({{site.baseurl}}/FF8/Technical Reference/Miscellaneous/FF8String)                                                                                                                                         |
| 24     | 4 bytes    | HP values                                                                                                                                                                                                                              |
| 28     | 4 bytes    | Str values                                                                                                                                                                                                                             |
| 32     | 4 bytes    | Vit values                                                                                                                                                                                                                             |
| 36     | 4 bytes    | Mag values                                                                                                                                                                                                                             |
| 40     | 4 bytes    | Spr values                                                                                                                                                                                                                             |
| 44     | 4 bytes    | Spd values                                                                                                                                                                                                                             |
| 48     | 4 bytes    | Eva values                                                                                                                                                                                                                             |
| 52     | 16*4 bytes | [Abilities](#abilities), low level                                                                                                                                                                                                     |
| 116    | 16*4 bytes | [Abilities](#abilities), med level                                                                                                                                                                                                     |
| 180    | 16*4 bytes | [Abilities](#abilities), high level                                                                                                                                                                                                    |
| 244    | 1 byte     | Med level start                                                                                                                                                                                                                        |
| 245    | 1 byte     | High level start                                                                                                                                                                                                                       |
| 246    | 1 byte     | Unknown (flags, 3 bits used)                                                                                                                                                                                                           |
| 247    | 1 byte     | [LSB] Zombie / Fly / zz1 / LvUp-Down Immunity / HP Hidden / Auto-Reflect / Auto-Shell / Auto-Protect [MSB]                                                                                                                             |
| 248    | 3 bytes    | [Card]({{site.baseurl}}/FF8/Technical Reference/Lists/Card_list#card-info) (drop/mod/rare mod)                                                                                                                                         |
| 251    | 3 bytes    | [Devour]({{site.baseurl}}/FF8/Technical Reference/Lists/Devour_list#devour-effects) (low/med/high)                                                                                                                                     |
| 254    | 1 byte     | [LSB] zz1 / zz2 / unused / unused / unused / unused / Gravity Immunity / Always obtains card [MSB]                                                                                                                                     |
| 255    | 1 byte     | Unknown (flags, 4 bits used)                                                                                                                                                                                                           |
| 256    | 2 bytes    | Extra EXP                                                                                                                                                                                                                              |
| 258    | 2 bytes    | EXP                                                                                                                                                                                                                                    |
| 260    | 8 bytes    | [Draw](#draw-mug-drop) (low)                                                                                                                                                                                                           |
| 268    | 8 bytes    | [Draw](#draw-mug-drop) (med)                                                                                                                                                                                                           |
| 276    | 8 bytes    | [Draw](#draw-mug-drop) (high)                                                                                                                                                                                                          |
| 284    | 8 bytes    | [Mug](#draw-mug-drop)(low)                                                                                                                                                                                                             |
| 292    | 8 bytes    | [Mug](#draw-mug-drop)(med)                                                                                                                                                                                                             |
| 300    | 8 bytes    | [Mug](#draw-mug-drop)(high)                                                                                                                                                                                                            |
| 308    | 8 bytes    | [Drop](#draw-mug-drop) (low)                                                                                                                                                                                                           |
| 316    | 8 bytes    | [Drop](#draw-mug-drop) (med)                                                                                                                                                                                                           |
| 324    | 8 bytes    | [Drop](#draw-mug-drop) (high)                                                                                                                                                                                                          |
| 332    | 1 byte     | [Mug rate](#rate-value)                                                                                                                                                                                                                |
| 333    | 1 byte     | [Drop rate](#rate-value)                                                                                                                                                                                                               |
| 334    | 1 byte     | Padding (0x00)                                                                                                                                                                                                                         |
| 335    | 1 byte     | APs                                                                                                                                                                                                                                    |
| 336    | 16 bytes   | [Renzokuken data](#renzokuken-data)                                                                                                                                                                                                    |                                                                         
| 352    | 8 bytes    | [Elemental resistance](#elemental-resistance) (Fire, Ice, Thunder, Earth, Poison, Wind, Water, Holy)                                                                                                                                   |
| 360    | 20 bytes   | [Status resistance](#mental-resistance) (Death, Poison, Petrify, Darkness, Silence, Berserk, Zombie, Sleep,<br> Haste, Slow, Stop, Regen, Reflect, Doom, Slow Petrify, Float, Drain, Confuse , Expulsion, VIT0(but unused by the game)) |

### Abilities

Abilities are composed of:

| Length | Description                                                                                 |
|--------|---------------------------------------------------------------------------------------------|
| 1 byte | [AbilityTypeID]({{site.baseurl}}/FF8/Technical Reference/Lists/Ability_list#abilities-type) |
| 1 byte | [AnimationSequenceID](#animationsequenceid)                                                 |
| 2 byte | [AbilityID]({{site.baseurl}}/FF8/Technical Reference/Lists/Ability_list#abilities)          |

#### AnimationSequenceID

Refer to a sequence in the [Section 5](#section-5-animation-sequences)

### Renzokuken data

The data is 8*2 bytes, each 2 bytes corresponding to an ID on the [Special Action list]({{site.baseurl}}/FF8/Technical Reference/Lists/Specialaction_list)

### Draw Mug Drop

Each section is composed of 8 bytes corresponding to 4 id ([magic]({{site.baseurl}}/FF8/Technical Reference/Lists/Magic_list) for
draw, [Item]({{site.baseurl}}/FF8/Technical Reference/Lists/Item_list) for mug & drop) and 4 quantity.
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

Contains some [TIMs]({{site.baseurl}}/FF8/Technical Reference/PSX/TIM_Format).

| Offset          | Length            | Description    |
|-----------------|-------------------|----------------|
| 0               | 4 bytes           | Number of TIMs |
| 4               | nbTIMs \* 4 bytes | TIMs Positions |
| 4 + nbTIMs \* 4 | 4 bytes           | End of file    |
| 8 + nbTIMs \* 4 | Varies \* nbTIMs  | TIMs           |
