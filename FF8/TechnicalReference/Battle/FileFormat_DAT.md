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

Contain sequence of animation. Not much known yet, all info are found here: [Qhimm message](https://forums.qhimm.com/index.php?topic=19362.0)

### Header

| Offset | Length                 | Description         |
|--------|------------------------|---------------------|
| 0      | 2 bytes                | Number of sequences |
| 2      | nbSequences \* 2 bytes | Sequences Positions |

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
| 360    | 20 bytes   | [Status resistance](#mental-resistance) (Death, Poison, Petrify, Darkness, Silence, Berserk, Zombie, Sleep,<br> Haste, Slow, Stop, Regen, Reflect, Doom, Slow Petrify, Float, Confuse, Drain, Expulsion, VIT0(but unused by the game)) |

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
