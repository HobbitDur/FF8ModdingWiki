---
layout: default
title: Draw point
parent: ExeData
author: HobbitDur
permalink: /technical-reference/exedata/draw-point/
---

1. TOC
   {:toc}

# Field Draw Notes

## General info

All information for a Draw Point is stored in a single byte; the spell ID, whether the draw point refreshes,
and whether you get a low or high yield from the draw point.

Start with the spell ID, and then modify it if necessary:
Add 64 to Decimal ID for 2nd Bit - Refill Behavior (Added = Yes, Not Added = No)
Add 128 to Decimal ID for 1st Bit - Draw Yield (Added = High, Not Added = Low)
Add 192 to Decimal ID for Refill + High Yield to both be applied.

Each value corresponds to a 'Draw ID' that is referenced in the field script. For example, the field script for a draw point
is quite basic and will just read 'drawpoint(15)' for instance.

## Default values

Address Starts:
0x00B92328

Default Values
.data:00B92328 byte_B92328 db 55h, 44h, 99h, 9Bh, 0Dh, 0CCh, 0C7h, 0D5h, 0C1h, 0E9h  
.data:00B92500 db 0E6h, 72h, 55h, 6, 0E3h, 0D8h, 0DEh, 0DDh, 21h, 0A0h  
.data:00B92500 db 55h, 4Ah, 48h, 70h, 5Bh, 4Ch, 0C2h, 0EEh, 9, 4Bh, 0C5h  
.data:00B92500 db 0E6h, 59h, 0ECh, 0DCh, 17h, 1Fh, 0DDh, 0EFh, 56h, 0E3h  
.data:00B92500 db 0DEh, 0DAh, 19h, 93h, 0C9h, 10h, 57h, 44h, 0D1h, 52h  
.data:00B92500 db 0E1h, 2Dh, 0Fh, 65h, 65h, 0D8h, 1Fh, 0EBh, 0Eh, 69h  
.data:00B92500 db 13h, 67h, 6Ah, 0D0h, 57h, 64h, 57h, 0Fh, 8Eh, 68h, 0E7h  
.data:00B92500 db 4Bh, 2Ch, 2Dh, 0C9h, 30h, 20h, 0D3h, 46h, 43h, 0D2h  
.data:00B92500 db 0CEh, 56h, 58h, 19h, 5Ch, 5Bh, 0A2h, 13h, 0F1h, 10h  
.data:00B92500 db 0E3h, 0E4h, 0D7h, 0D8h, 0E5h, 0DAh, 0E1h, 22h, 0Fh  
.data:00B92500 db 57h, 56h, 72h, 5Bh, 64h, 5Ch, 65h, 58h, 0Fh, 20h, 0Eh  
.data:00B92500 db 10h, 31h, 13h, 19h, 22h, 81h, 81h, 81h, 81h, 81h, 81h  
.data:00B92500 db 81h, 81h, 81h, 81h, 81h, 55h, 5Bh, 47h, 42h, 48h, 45h  
.data:00B92500 db 44h, 41h, 55h, 4Ah, 56h, 5Bh, 72h, 5Eh, 63h, 4Bh, 4Ch  
.data:00B92500 db 58h, 4Dh, 5Dh, 4Eh, 49h, 65h, 43h, 5Ah, 46h, 67h, 4Fh  
.data:00B92500 db 5Ch, 64h, 51h, 57h, 52h, 19h, 5Fh, 20h, 11h, 61h, 6Ah  
.data:00B92500 db 10h, 13h, 22h, 67h, 66h, 0D1h, 68h, 69h, 0CFh, 6Bh  
.data:00B92500 db 6Ch, 0EDh, 6Eh, 6Fh, 70h, 71h, 93h, 0D2h, 0D1h, 0D0h  
.data:00B92500 db 0CEh, 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D2h, 0D1h, 0D0h  
.data:00B92500 db 0CEh, 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D2h, 0D1h, 0D0h  
.data:00B92500 db 0CEh, 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D3h, 0D0h, 0CEh  
.data:00B92500 db 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D0h, 0CEh, 0E2h, 0E0h  
.data:00B92500 db 0D3h, 0E2h, 0D9h, 0D0h, 0CEh, 0CFh, 0E0h, 0D3h, 0E2h  
.data:00B92500 db 0D9h, 0D0h, 0E2h, 0CFh, 0E0h, 0D3h, 0E2h, 0D9h, 0D0h  
.data:00B92500 db 0CEh, 0CFh, 0E0h, 0D3h, 44h, 55h, 0DCh, 0E7h, 10h, 21h  
.data:00B92500 db 20h, 0Eh, 0Fh, 13h, 0F2h

## Explanation

255 Draw Points, that the Field Script can reference. Each value is a spell ID, whether the draw point refills,
and whether the draw point gives a low or high yield.

Example:
You want to edit Draw ID 15

- 15 -1 = 14 (want to start counting from 0 instead of 1)
- 792500 + 14 = 79250E (location of Draw ID 15)

If you want to set it to give Cure, which is MagicID #15 in the bin,
then you input the following value:

- 0x15 (Cure, no refill)
- 0x55 (Cure, refills)

Represented in binary, it'd look like this:

- 0x15 = 00010101 (Cure, no refill)
- 0x55 = 01010101 (Cure, refills)

The 01 at the start of 0x55 is two bits that set a bool for refill.
Keep an eye out for that when setting the value (I think I added this note for debugging or something)

Visiblity seems to be set from Field in group's Init.
0 for hidden, 1 for visible.

From the Wiki (some additional info on how it works, like refill):

| State ID | 	Description                           |
|----------|----------------------------------------|
| 0        | 	Fully stocked                         |
| 1        | 	Partially stocked                     |
| 2        | 	Empty but refills (white swirl)       |
| 3        | 	Empty and doesn't refill (blue swirl) |

Draw points start off at state 0 and move to state 2 or 3 when drawn from.
There are two flags for each draw point, one which defines if the draw point is rich, and one which defines if it refills.

## Draw Points

magic_id = byte & 0x3F
refill = (byte >> 6) & 1 (0x40)
extra_magic = byte >> 7 (0x80)

Walk-Restock Check:

- Every 10,240 steps it checks it
- Var 164 (savegame + 0xE14)

Each Draw is then given a random number 0 - 32,767

- ended with 1 (x86 TEST opcode) for a 50% chance
- that it'll be restocked.

Unknown16 in Field script binds Drawpoint to Variable

- Is usually the same as Draw ID.
- Stored at Field Vars 100-164 (Savegame + 0xDD4)

1st Bit determines the amount you can draw, calculated as:

- 6-15 if fully stocked with bit set
- 3-8 if partial, bit set/fully if bit not set
- 2-4 if partial, no bit set

World Map is: 2-5 with bit-set, 1-2 if not set  
So in practice, if its = 0 you get 3-8 or 2-4.  
if its = 1 you get 6-15 or 3-8

## List default draw point

| ID  | Address  | Hex Value | Integer Value | High Yield | Refill | Magic     | Location                                                                 |
|-----|----------|-----------|---------------|------------|--------|-----------|--------------------------------------------------------------------------|
| 001 | 0xB92328 | 0x55      | 85            | 0          | 1      | Cure      | Balamb Garden courtyard                                                  |
| 002 | 0xB92329 | 0x44      | 68            | 0          | 1      | Blizzard  | Balamb Garden training center                                            |
| 003 | 0xB9232A | 0x99      | 153           | 1          | 0      | Full-Life | Balamb Garden MD level                                                   |
| 004 | 0xB9232B | 0x9B      | 155           | 1          | 0      | Esuna     | Balamb Garden library next to the book shelf                             |
| 005 | 0xB9232C | 0x0D      | 13            | 0          | 0      | Demi      | Balamb Garden cafeteria (only during Garden Riot)                        |
| 006 | 0xB9232D | 0xCC      | 204           | 1          | 1      | Bio       | Balamb Garden B2 floor                                                   |
| 007 | 0xB9232E | 0xC7      | 199           | 1          | 1      | Thunder   | Balamb outside junk shop                                                 |
| 008 | 0xB9232F | 0xD5      | 213           | 1          | 1      | Cure      | Balamb harbor                                                            |
| 009 | 0xB92330 | 0xC1      | 193           | 1          | 1      | Fire      | Fire Cavern                                                              |
| 010 | 0xB92331 | 0xE9      | 233           | 1          | 1      | Silence   | Dollet town square                                                       |
| 011 | 0xB92500 | 0xE6      | 230           | 1          | 1      | Blind     | Dollet Communications Tower                                              |
| 012 | 0xB92501 | 0x72      | 114           | 0          | 1      | Scan      | Timber Pub Aurora back alley                                             |
| 013 | 0xB92502 | 0x55      | 85            | 0          | 1      | Cure      | Timber outside the pub                                                   |
| 014 | 0xB92503 | 0x06      | 6             | 0          | 0      | Blizzaga  | Timber Maniacs Building left room                                        |
| 015 | 0xB92504 | 0xE3      | 227           | 1          | 1      | Haste     | Galbadia Garden lobby                                                    |
| 016 | 0xB92505 | 0xD8      | 216           | 1          | 1      | Life      | Galbadia Garden changing rooms                                           |
| 017 | 0xB92506 | 0xDE      | 222           | 1          | 1      | Shell     | Galbadia Garden courtyard                                                |
| 018 | 0xB92507 | 0xDD      | 221           | 1          | 1      | Protect   | Galbadia Garden ice rink                                                 |
| 019 | 0xB92508 | 0x21      | 33            | 0          | 0      | Double    | Galbadia Garden auditorium                                               |
| 020 | 0xB92509 | 0xA0      | 160           | 1          | 0      | Aura      | Outside Galbadia Garden during Garden war                                |
| 021 | 0xB9250A | 0x55      | 85            | 0          | 1      | Cure      | Timber forests in a Laguna dream                                         |
| 022 | 0xB9250B | 0x4A      | 74            | 0          | 1      | Water     | Timber forests in a Laguna dream                                         |
| 023 | 0xB9250C | 0x48      | 72            | 0          | 1      | Thundara  | Deling City park                                                         |
| 024 | 0xB9250D | 0x70      | 112           | 0          | 1      | Zombie    | Deling City Sewers                                                       |
| 025 | 0xB9250E | 0x5B      | 91            | 0          | 1      | Esuna     | Deling City Sewers                                                       |
| 026 | 0xB9250F | 0x4C      | 76            | 0          | 1      | Bio       | Deling City Sewers                                                       |
| 027 | 0xB92510 | 0xC2      | 194           | 1          | 1      | Fira      |                                                                          |
| 028 | 0xB92511 | 0xEE      | 238           | 1          | 1      | Berserk   | D-District Prison Floor 9 - right cell                                   |
| 029 | 0xB92512 | 0x09      | 9             | 0          | 0      | Thundaga  | D-District Prison Floor 11 - right cell                                  |
| 030 | 0xB92513 | 0x4B      | 75            | 0          | 1      | Aero      | Outside D-District Prison                                                |
| 031 | 0xB92514 | 0xC5      | 197           | 1          | 1      | Blizzara  | Missile Base - control room                                              |
| 032 | 0xB92515 | 0xE6      | 230           | 1          | 1      | Blind     | Missile Base room with G-Soldiers who ask to deliver a message           |
| 033 | 0xB92516 | 0x59      | 89            | 0          | 1      | Full-Life | Missile Base - silo room                                                 |
| 034 | 0xB92517 | 0xEC      | 236           | 1          | 1      | Drain     | Winhill road south from town square                                      |
| 035 | 0xB92518 | 0xDC      | 220           | 1          | 1      | Dispel    | Winhill town square                                                      |
| 036 | 0xB92519 | 0x17      | 23            | 0          | 0      | Curaga    | Winhill Laguna's room in the dream                                       |
| 037 | 0xB9251A | 0x1F      | 31            | 0          | 0      | Reflect   | Winhill east road                                                        |
| 038 | 0xB9251B | 0xDD      | 221           | 1          | 1      | Protect   | Tomb of the Unknown King - outside                                       |
| 039 | 0xB9251C | 0xEF      | 239           | 1          | 1      | Float     | Tomb of the Unknown King - north room                                    |
| 040 | 0xB9251D | 0x56      | 86            | 0          | 1      | Cura      | Tomb of the Unknown King - east room                                     |
| 041 | 0xB9251E | 0xE3      | 227           | 1          | 1      | Haste     | Fishermans Horizon abandoned train station                               |
| 042 | 0xB9251F | 0xDE      | 222           | 1          | 1      | Shell     | Fishermans Horizon junk shop                                             |
| 043 | 0xB92520 | 0xDA      | 218           | 1          | 1      | Regen     | Fishermans Horizon overlooking the sun panel                             |
| 044 | 0xB92521 | 0x19      | 25            | 0          | 0      | Full-Life | Fishermans Horizon Master Fisherman's fishing spot                       |
| 045 | 0xB92522 | 0x93      | 147           | 1          | 0      | Ultima    | Fishermans Horizon mayor's house                                         |
| 046 | 0xB92523 | 0xC9      | 201           | 1          | 1      | Thundaga  | Great Salt Lake past the dinosaur skeleton                               |
| 047 | 0xB92524 | 0x10      | 16            | 0          | 0      | Meteor    | Great Salt Lake dinosaur skeleton                                        |
| 048 | 0xB92525 | 0x57      | 87            | 0          | 1      | Curaga    | Esthar city streets near city entrance                                   |
| 049 | 0xB92526 | 0x44      | 68            | 0          | 1      | Blizzard  | Esthar outside palace                                                    |
| 050 | 0xB92527 | 0xD1      | 209           | 1          | 1      | Quake     | Esthar outside Odine's Lab                                               |
| 051 | 0xB92528 | 0x52      | 82            | 0          | 1      | Tornado   | Esthar shopping mall                                                     |
| 052 | 0xB92529 | 0xE1      | 225           | 1          | 1      | Double    | Esthar Odine's Lab in a Laguna dream                                     |
| 053 | 0xB9252A | 0x2D      | 45            | 0          | 0      | Pain      |                                                                          |
| 054 | 0xB9252B | 0x0F      | 15            | 0          | 0      | Flare     | Esthar Odine's Lab in a Laguna dream                                     |
| 055 | 0xB9252C | 0x65      | 101           | 0          | 1      | Stop      | Sorceress Memorial                                                       |
| 056 | 0xB9252D | 0x65      | 101           | 0          | 1      | Stop      |                                                                          |
| 057 | 0xB9252E | 0xD8      | 216           | 1          | 1      | Life      | Tears' Point entrance                                                    |
| 058 | 0xB9252F | 0x1F      | 31            | 0          | 0      | Reflect   | Tears' Point middle                                                      |
| 059 | 0xB92530 | 0xEB      | 235           | 1          | 1      | Death     | Lunatic Pandora Laboratory in a Laguna dream                             |
| 060 | 0xB92531 | 0x0E      | 14            | 0          | 0      | Holy      | Lunatic Pandora near Elevator #1                                         |
| 061 | 0xB92532 | 0x69      | 105           | 0          | 1      | Silence   | Lunatic Pandora                                                          |
| 062 | 0xB92533 | 0x13      | 19            | 0          | 0      | Ultima    | Lunatic Pandora                                                          |
| 063 | 0xB92534 | 0x67      | 103           | 0          | 1      | Confuse   |                                                                          |
| 064 | 0xB92535 | 0x6A      | 106           | 0          | 1      | Break     | Lunatic Pandora on the way to fight Adel                                 |
| 065 | 0xB92536 | 0xD0      | 208           | 1          | 1      | Meteor    | Lunatic Pandora entrance                                                 |
| 066 | 0xB92537 | 0x57      | 87            | 0          | 1      | Curaga    | Lunatic Pandora elevator room                                            |
| 067 | 0xB92538 | 0x64      | 100           | 0          | 1      | Slow      |                                                                          |
| 068 | 0xB92539 | 0x57      | 87            | 0          | 1      | Curaga    | Edea's Orphanage                                                         |
| 069 | 0xB9253A | 0x0F      | 15            | 0          | 0      | Flare     |                                                                          |
| 070 | 0xB9253B | 0x8E      | 142           | 1          | 0      | Holy      |                                                                          |
| 071 | 0xB9253C | 0x68      | 104           | 0          | 1      | Sleep     | Centra Excavation Site                                                   |
| 072 | 0xB9253D | 0xE7      | 231           | 1          | 1      | Confuse   | Centra Excavation Site                                                   |
| 073 | 0xB9253E | 0x4B      | 75            | 0          | 1      | Aero      | Centra Ruins right ladder after the lift                                 |
| 074 | 0xB9253F | 0x2C      | 44            | 0          | 0      | Drain     | Centra Ruins platform after the first staircase                          |
| 075 | 0xB92540 | 0x2D      | 45            | 0          | 0      | Pain      | Centra Ruins next to the dome                                            |
| 076 | 0xB92541 | 0xC9      | 201           | 1          | 1      | Thundaga  | Trabia Garden in front of the statue                                     |
| 077 | 0xB92542 | 0x30      | 48            | 0          | 0      | Zombie    | Trabia Garden cemetery                                                   |
| 078 | 0xB92543 | 0x20      | 32            | 0          | 0      | Aura      | Trabia Garden stage                                                      |
| 079 | 0xB92544 | 0xD3      | 211           | 1          | 1      | Ultima    | Shumi Village - above ground                                             |
| 080 | 0xB92545 | 0x46      | 70            | 0          | 1      | Blizzaga  | Shumi Village - outside elder's house                                    |
| 081 | 0xB92546 | 0x43      | 67            | 0          | 1      | Firaga    | Shumi Village workshop                                                   |
| 082 | 0xB92547 | 0xD2      | 210           | 1          | 1      | Tornado   |                                                                          |
| 083 | 0xB92548 | 0xCE      | 206           | 1          | 1      | Holy      | White SeeD Ship                                                          |
| 084 | 0xB92549 | 0x56      | 86            | 0          | 1      | Cura      | Ragnarok room with a red Propagator                                      |
| 085 | 0xB9254A | 0x58      | 88            | 0          | 1      | Life      | Ragnarok hangar upstairs                                                 |
| 086 | 0xB9254B | 0x19      | 25            | 0          | 0      | Full-Life | Ragnarok room with save point                                            |
| 087 | 0xB9254C | 0x5C      | 92            | 0          | 1      | Dispel    | Deep Sea Research Center second level                                    |
| 088 | 0xB9254D | 0x5B      | 91            | 0          | 1      | Esuna     | Deep Sea Research Center secret room                                     |
| 089 | 0xB9254E | 0xA2      | 162           | 1          | 0      | Triple    | Deep Sea Research Center third screen on the way to Ultima Weapon's lair |
| 090 | 0xB9254F | 0x13      | 19            | 0          | 0      | Ultima    | Deep Sea Research Center fifth screen on the way to Ultima Weapon's lair |
| 091 | 0xB92550 | 0xF1      | 241           | 1          | 1      | Meltdown  | Lunar Base room before the escape pods                                   |
| 092 | 0xB92551 | 0x10      | 16            | 0          | 0      | Meteor    | Lunar Base Ellone's room                                                 |
| 093 | 0xB92552 | 0xE3      | 227           | 1          | 1      | Haste     |                                                                          |
| 094 | 0xB92553 | 0xE4      | 228           | 1          | 1      | Slow      |                                                                          |
| 095 | 0xB92554 | 0xD7      | 215           | 1          | 1      | Curaga    |                                                                          |
| 096 | 0xB92555 | 0xD8      | 216           | 1          | 1      | Life      |                                                                          |
| 097 | 0xB92556 | 0xE5      | 229           | 1          | 1      | Stop      |                                                                          |
| 098 | 0xB92557 | 0xDA      | 218           | 1          | 1      | Regen     |                                                                          |
| 099 | 0xB92558 | 0xE1      | 225           | 1          | 1      | Double    |                                                                          |
| 100 | 0xB92559 | 0x22      | 34            | 0          | 0      | Triple    |                                                                          |
| 101 | 0xB9255A | 0x0F      | 15            | 0          | 0      | Flare     | Ultimecia Castle outside                                                 |
| 102 | 0xB9255B | 0x57      | 87            | 0          | 1      | Curaga    | Ultimecia Castle storage room                                            |
| 103 | 0xB9255C | 0x56      | 86            | 0          | 1      | Cura      | Ultimecia Castle passageway                                              |
| 104 | 0xB9255D | 0x72      | 114           | 0          | 1      | Scan      |                                                                          |
| 105 | 0xB9255E | 0x5B      | 91            | 0          | 1      | Esuna     |                                                                          |
| 106 | 0xB9255F | 0x64      | 100           | 0          | 1      | Slow      | Ultimecia Castle courtyard                                               |
| 107 | 0xB92560 | 0x5C      | 92            | 0          | 1      | Dispel    | Ultimecia Castle chapel                                                  |
| 108 | 0xB92561 | 0x65      | 101           | 0          | 1      | Stop      | Ultimecia Castle clock tower                                             |
| 109 | 0xB92562 | 0x58      | 88            | 0          | 1      | Life      |                                                                          |
| 110 | 0xB92563 | 0x0F      | 15            | 0          | 0      | Flare     |                                                                          |
| 111 | 0xB92564 | 0x20      | 32            | 0          | 0      | Aura      | Ultimecia Castle wine cellar                                             |
| 112 | 0xB92565 | 0x0E      | 14            | 0          | 0      | Holy      | Ultimecia Castle treasure room                                           |
| 113 | 0xB92566 | 0x10      | 16            | 0          | 0      | Meteor    |                                                                          |
| 114 | 0xB92567 | 0x31      | 49            | 0          | 0      | Meltdown  | Ultimecia Castle art gallery                                             |
| 115 | 0xB92568 | 0x13      | 19            | 0          | 0      | Ultima    | Ultimecia Castle armory                                                  |
| 116 | 0xB92569 | 0x19      | 25            | 0          | 0      | Full-Life | Ultimecia Castle prison                                                  |
| 117 | 0xB9256A | 0x22      | 34            | 0          | 0      | Triple    |                                                                          |
| 118 | 0xB9256B | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 119 | 0xB9256C | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 120 | 0xB9256D | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 121 | 0xB9256E | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 122 | 0xB9256F | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 123 | 0xB92570 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 124 | 0xB92571 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 125 | 0xB92572 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 126 | 0xB92573 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 127 | 0xB92574 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          |
| 128 | 0xB92575 | 0x55      | 85            | 1          | 0      | Fire      |                                                                          |
| 129 | 0xB92576 | 0x5B      | 91            | 0          | 1      | Cure      |                                                                          |
| 130 | 0xB92577 | 0x47      | 71            | 0          | 1      | Esuna     |                                                                          |
| 131 | 0xB92578 | 0x42      | 66            | 0          | 1      | Thunder   |                                                                          |
| 132 | 0xB92579 | 0x48      | 72            | 0          | 1      | Fira      |                                                                          |
| 133 | 0xB9257A | 0x45      | 69            | 0          | 1      | Thundara  |                                                                          |
| 134 | 0xB9257B | 0x44      | 68            | 0          | 1      | Blizzara  |                                                                          |
| 135 | 0xB9257C | 0x41      | 65            | 0          | 1      | Blizzard  |                                                                          |
| 136 | 0xB9257D | 0x55      | 85            | 0          | 1      | Fire      |                                                                          |
| 137 | 0xB9257E | 0x4A      | 74            | 0          | 1      | Cure      |                                                                          |
| 138 | 0xB9257F | 0x56      | 86            | 0          | 1      | Water     |                                                                          |
| 139 | 0xB92580 | 0x5B      | 91            | 0          | 1      | Cura      |                                                                          |
| 140 | 0xB92581 | 0x72      | 114           | 0          | 1      | Esuna     |                                                                          |
| 141 | 0xB92582 | 0x5E      | 94            | 0          | 1      | Scan      |                                                                          |
| 142 | 0xB92583 | 0x63      | 99            | 0          | 1      | Shell     |                                                                          |
| 143 | 0xB92584 | 0x4B      | 75            | 0          | 1      | Haste     |                                                                          |
| 144 | 0xB92585 | 0x4C      | 76            | 0          | 1      | Aero      |                                                                          |
| 145 | 0xB92586 | 0x58      | 88            | 0          | 1      | Bio       |                                                                          |
| 146 | 0xB92587 | 0x4D      | 77            | 0          | 1      | Life      |                                                                          |
| 147 | 0xB92588 | 0x5D      | 93            | 0          | 1      | Demi      |                                                                          |
| 148 | 0xB92589 | 0x4E      | 78            | 0          | 1      | Protect   |                                                                          |
| 149 | 0xB9258A | 0x49      | 73            | 0          | 1      | Holy      |                                                                          |
| 150 | 0xB9258B | 0x65      | 101           | 0          | 1      | Thundaga  |                                                                          |
| 151 | 0xB9258C | 0x43      | 67            | 0          | 1      | Stop      |                                                                          |
| 152 | 0xB9258D | 0x5A      | 90            | 0          | 1      | Firaga    |                                                                          |
| 153 | 0xB9258E | 0x46      | 70            | 0          | 1      | Regen     |                                                                          |
| 154 | 0xB9258F | 0x67      | 103           | 0          | 1      | Blizzaga  |                                                                          |
| 155 | 0xB92590 | 0x4F      | 79            | 0          | 1      | Confuse   |                                                                          |
| 156 | 0xB92591 | 0x5C      | 92            | 0          | 1      | Flare     |                                                                          |
| 157 | 0xB92592 | 0x64      | 100           | 0          | 1      | Dispel    |                                                                          |
| 158 | 0xB92593 | 0x51      | 81            | 0          | 1      | Slow      |                                                                          |
| 159 | 0xB92594 | 0x57      | 87            | 0          | 1      | Quake     |                                                                          |
| 160 | 0xB92595 | 0x52      | 82            | 0          | 1      | Curaga    |                                                                          |
| 161 | 0xB92596 | 0x19      | 25            | 0          | 1      | Tornado   |                                                                          |
| 162 | 0xB92597 | 0x5F      | 95            | 0          | 0      | Full-Life |                                                                          |
| 163 | 0xB92598 | 0x20      | 32            | 0          | 1      | Reflect   |                                                                          |
| 164 | 0xB92599 | 0x11      | 17            | 0          | 0      | Aura      |                                                                          |
| 165 | 0xB9259A | 0x61      | 97            | 0          | 0      | Quake     |                                                                          |
| 166 | 0xB9259B | 0x6A      | 106           | 0          | 1      | Double    |                                                                          |
| 167 | 0xB9259C | 0x10      | 16            | 0          | 1      | Break     |                                                                          |
| 168 | 0xB9259D | 0x13      | 19            | 0          | 0      | Meteor    |                                                                          |
| 169 | 0xB9259E | 0x22      | 34            | 0          | 0      | Ultima    |                                                                          |
| 170 | 0xB9259F | 0x67      | 103           | 0          | 0      | Triple    |                                                                          |
| 171 | 0xB925A0 | 0x66      | 102           | 0          | 1      | Confuse   |                                                                          |
| 172 | 0xB925A1 | 0xD1      | 209           | 0          | 1      | Blind     |                                                                          |
| 173 | 0xB925A2 | 0x68      | 104           | 1          | 1      | Quake     |                                                                          |
| 174 | 0xB925A3 | 0x69      | 105           | 0          | 1      | Sleep     |                                                                          |
| 175 | 0xB925A4 | 0xCF      | 207           | 0          | 1      | Silence   |                                                                          |
| 176 | 0xB925A5 | 0x6B      | 107           | 1          | 1      | Flare     |                                                                          |
| 177 | 0xB925A6 | 0x6C      | 108           | 0          | 1      | Death     |                                                                          |
| 178 | 0xB925A7 | 0xED      | 237           | 0          | 1      | Drain     |                                                                          |
| 179 | 0xB925A8 | 0x6E      | 110           | 1          | 1      | Pain      |                                                                          |
| 180 | 0xB925A9 | 0x6F      | 111           | 0          | 1      | Berserk   |                                                                          |
| 181 | 0xB925AA | 0x70      | 112           | 0          | 1      | Float     |                                                                          |
| 182 | 0xB925AB | 0x71      | 113           | 0          | 1      | Zombie    |                                                                          |
| 183 | 0xB925AC | 0x93      | 147           | 0          | 1      | Meltdown  |                                                                          |
| 184 | 0xB925AD | 0xD2      | 210           | 1          | 0      | Ultima    |                                                                          |
| 185 | 0xB925AE | 0xD1      | 209           | 1          | 1      | Tornado   |                                                                          |
| 186 | 0xB925AF | 0xD0      | 208           | 1          | 1      | Quake     |                                                                          |
| 187 | 0xB925B0 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          |
| 188 | 0xB925B1 | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          |
| 189 | 0xB925B2 | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          |
| 190 | 0xB925B3 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          |
| 191 | 0xB925B4 | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          |
| 192 | 0xB925B5 | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          |
| 193 | 0xB925B6 | 0xD2      | 210           | 1          | 1      | Full-Life |                                                                          |
| 194 | 0xB925B7 | 0xD1      | 209           | 1          | 1      | Tornado   |                                                                          |
| 195 | 0xB925B8 | 0xD0      | 208           | 1          | 1      | Quake     |                                                                          |
| 196 | 0xB925B9 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          |
| 197 | 0xB925BA | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          |
| 198 | 0xB925BB | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          |
| 199 | 0xB925BC | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          |
| 200 | 0xB925BD | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          |
| 201 | 0xB925BE | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          |
| 202 | 0xB925BF | 0xD2      | 210           | 1          | 1      | Full-Life |                                                                          |
| 203 | 0xB925C0 | 0xD1      | 209           | 1          | 1      | Tornado   |                                                                          |
| 204 | 0xB925C1 | 0xD0      | 208           | 1          | 1      | Quake     |                                                                          |
| 205 | 0xB925C2 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          |
| 206 | 0xB925C3 | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          |
| 207 | 0xB925C4 | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          |
| 208 | 0xB925C5 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          |
| 209 | 0xB925C6 | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          |
| 210 | 0xB925C7 | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          |
| 211 | 0xB925C8 | 0xD3      | 211           | 1          | 1      | Full-Life |                                                                          |
| 212 | 0xB925C9 | 0xD0      | 208           | 1          | 1      | Ultima    |                                                                          |
| 213 | 0xB925CA | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          |
| 214 | 0xB925CB | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          |
| 215 | 0xB925CC | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          |
| 216 | 0xB925CD | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          |
| 217 | 0xB925CE | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          |
| 218 | 0xB925CF | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          |
| 219 | 0xB925D0 | 0xD0      | 208           | 1          | 1      | Full-Life |                                                                          |
| 220 | 0xB925D1 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          |
| 221 | 0xB925D2 | 0xE2      | 226           | 1          | 1      | Holy      |                                                                          |
| 222 | 0xB925D3 | 0xE0      | 224           | 1          | 1      | Triple    |                                                                          |
| 223 | 0xB925D4 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          |
| 224 | 0xB925D5 | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          |
| 225 | 0xB925D6 | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          |
| 226 | 0xB925D7 | 0xD0      | 208           | 1          | 1      | Full-Life |                                                                          |
| 227 | 0xB925D8 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          |
| 228 | 0xB925D9 | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          |
| 229 | 0xB925DA | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          |
| 230 | 0xB925DB | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          |
| 231 | 0xB925DC | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          |
| 232 | 0xB925DD | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          |
| 233 | 0xB925DE | 0xD0      | 208           | 1          | 1      | Full-Life |                                                                          |
| 234 | 0xB925DF | 0xE2      | 226           | 1          | 1      | Meteor    |                                                                          |
| 235 | 0xB925E0 | 0xCF      | 207           | 1          | 1      | Triple    |                                                                          |
| 236 | 0xB925E1 | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          |
| 237 | 0xB925E2 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          |
| 238 | 0xB925E3 | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          |
| 239 | 0xB925E4 | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          |
| 240 | 0xB925E5 | 0xD0      | 208           | 1          | 1      | Full-Life |                                                                          |
| 241 | 0xB925E6 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          |
| 242 | 0xB925E7 | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          |
| 243 | 0xB925E8 | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          |
| 244 | 0xB925E9 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          |
| 245 | 0xB925EA | 0x44      | 68            | 1          | 1      | Ultima    |                                                                          |
| 246 | 0xB925EB | 0x55      | 85            | 0          | 1      | Blizzard  |                                                                          |
| 247 | 0xB925EC | 0xDC      | 220           | 0          | 1      | Cure      |                                                                          |
| 248 | 0xB925ED | 0xE7      | 231           | 1          | 1      | Dispel    |                                                                          |
| 249 | 0xB925EE | 0x10      | 16            | 1          | 1      | Confuse   |                                                                          |
| 250 | 0xB925EF | 0x21      | 33            | 0          | 0      | Meteor    |                                                                          |
| 251 | 0xB925F0 | 0x20      | 32            | 0          | 0      | Double    |                                                                          |
| 252 | 0xB925F1 | 0x0E      | 14            | 0          | 0      | Aura      |                                                                          |
| 253 | 0xB925F2 | 0x0F      | 15            | 0          | 0      | Holy      |                                                                          |
| 254 | 0xB925F3 | 0x13      | 19            | 0          | 0      | Flare     |                                                                          |
| 255 | 0xB925F4 | 0xF2      | 242           | 0          | 0      | Ultima    |                                                                          |
| 256 | 0xB925F5 | 0x00      | 0             | 1          | 1      | Scan      |                                                                          |
