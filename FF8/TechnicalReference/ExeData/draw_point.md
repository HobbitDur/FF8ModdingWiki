---
layout: default
title: Draw point
parent: ExeData
author: HobbitDur, Maki
permalink: /technical-reference/exedata/draw-point/
---

1. TOC 
{:toc}

# Draw point definition

The draw point is stored in two places, lets call them *_DrawPointData_* and *_DrawPointStatus_*.
_DrawPointData_ is an array of 256 bytes. Each byte contains the data at start for each draw point: the magic, the refill option and the high yield.
_DrawPointStatus_ is an array of 2 bits size (so 2 bits per draw point) that stored the current state in memory of the draw point.

## Draw point data

Those data are setup at the start of the game.
Here a table to explain what each part of the byte does:

| bit | Name       | Flag | Description                                                                                        |
|-----|------------|------|----------------------------------------------------------------------------------------------------|
| 0-5 | MagicID    | 0x3F | Can be any magic from the [magic list]({{site.baseurl}}/technical-reference/list/magic-list#magic) |
| 6   | Refill     | 0x40 | True (1) if the draw point will refill                                                             |
| 7   | High yield | 0x80 | True (1) if the draw point will draw more than 10 magic.                                           |

Each value corresponds to a 'Draw ID' that is referenced in the field script. For example, the field script for a draw point
is quite basic and will just read 'drawpoint(15)' for instance.

## Draw point status

For each draw point, 2 bits are defined giving the following possibilities:

| State ID | 	Description                              |
|----------|-------------------------------------------|
| 0        | 	Fully stocked                            |
| 1        | 	Partially stocked                        |
| 2        | 	Empty but can refill (white swirl)       |
| 3        | 	Empty and will never refill (blue swirl) |

## Draw point Visibility

Visiblity seems to be set from Field in group's Init.
0 for hidden, 1 for visible.

## Code start

In the code, the values start at:

- For DrawPointData:
    - OG (2013): 0x0B92328
    - Remaster:
- For DrawPointStatus (to be confirmed):
    - OG (2013): 0x1CFEA2C
    - Remaster:

## Draw Points refill process

This part need to be improved

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

# List default draw point

| ID  | Address  | Hex Value | Integer Value | High Yield | Refill | Magic     | Location (Maki name)                                                     | Field/World | Field ref (Myst) | Location (Myst name)                         |
|-----|----------|-----------|---------------|------------|--------|-----------|--------------------------------------------------------------------------|-------------|------------------|----------------------------------------------|
| 001 | 0xB92328 | 0x55      | 85            | 0          | 1      | Cure      | Balamb Garden courtyard                                                  | Field       | 65               | B-Garden - Front Gate                        |
| 002 | 0xB92329 | 0x44      | 68            | 0          | 1      | Blizzard  | Balamb Garden training center                                            | Field       | 78               | B-Garden - Training Center                   |
| 003 | 0xB9232A | 0x99      | 153           | 1          | 0      | Full-Life | Balamb Garden MD level                                                   | Field       | 68               | B-Garden - MD Level                          |
| 004 | 0xB9232B | 0x9B      | 155           | 1          | 0      | Esuna     | Balamb Garden library next to the book shelf                             | Field       | 64               | B-Garden - Library                           |
| 005 | 0xB9232C | 0x0D      | 13            | 0          | 0      | Demi      | Balamb Garden cafeteria (only during Garden Riot)                        | Field       | 67               | B-Garden - Cafeteria                         |
| 006 | 0xB9232D | 0xCC      | 204           | 1          | 1      | Bio       | Balamb Garden B2 floor                                                   | Field       | 81               | B-Garden - Master Room                       |
| 007 | 0xB9232E | 0xC7      | 199           | 1          | 1      | Thunder   | Balamb outside junk shop                                                 | Field       | 85               | Balamb - Town Square                         |
| 008 | 0xB9232F | 0xD5      | 213           | 1          | 1      | Cure      | Balamb harbor                                                            | Field       | 87               | Balamb Harbor                                |
| 009 | 0xB92330 | 0xC1      | 193           | 1          | 1      | Fire      | Fire Cavern                                                              | Field       | 92               | Fire Cavern                                  |
| 010 | 0xB92331 | 0xE9      | 233           | 1          | 1      | Silence   | Dollet town square                                                       | Field       | 93               | Dollet - Town Square                         |
| 011 | 0xB92500 | 0xE6      | 230           | 1          | 1      | Blind     | Dollet Communications Tower                                              | Field       | 99               | Dollet - Comm Tower                          |
| 012 | 0xB92501 | 0x72      | 114           | 0          | 1      | Scan      | Timber Pub Aurora back alley                                             | Field       | 101              | Timber - City Square                         |
| 013 | 0xB92502 | 0x55      | 85            | 0          | 1      | Cure      | Timber outside the pub                                                   | Field       | 101/182          | Timber - City Square/Centra- Excavation Site |
| 014 | 0xB92503 | 0x06      | 6             | 0          | 0      | Blizzaga  | Timber Maniacs Building left room                                        | Field       | 109              | Timber - Editorial Department                |
| 015 | 0xB92504 | 0xE3      | 227           | 1          | 1      | Haste     | Galbadia Garden lobby                                                    | Field       | 113              | G-Garden - Hall                              |
| 016 | 0xB92505 | 0xD8      | 216           | 1          | 1      | Life      | Galbadia Garden changing rooms                                           | Field       | 117              | G-Garden - Clubroom                          |
| 017 | 0xB92506 | 0xDE      | 222           | 1          | 1      | Shell     | Galbadia Garden courtyard                                                | Field       | 122              | G-Garden - Athletic Track                    |
| 018 | 0xB92507 | 0xDD      | 221           | 1          | 1      | Protect   | Galbadia Garden ice rink                                                 | Field       | 125              | G-Garden - Gymnasium                         |
| 019 | 0xB92508 | 0x21      | 33            | 0          | 0      | Double    | Galbadia Garden auditorium                                               | Field       | 121              | G-Garden - Auditorium                        |
| 020 | 0xB92509 | 0xA0      | 160           | 1          | 0      | Aura      | Outside Galbadia Garden during Garden war                                | Field       | 124              | G-Garden - Back Entrance                     |
| 021 | 0xB9250A | 0x55      | 85            | 0          | 1      | Cure      | Timber forests in a Laguna dream                                         | Field       | 110              | Timber Forest                                |
| 022 | 0xB9250B | 0x4A      | 74            | 0          | 1      | Water     | Timber forests in a Laguna dream                                         | Field       | 110              | Timber Forest                                |
| 023 | 0xB9250C | 0x48      | 72            | 0          | 1      | Thundara  | Deling City park                                                         | Field       | 129              | Deling City - City Square                    |
| 024 | 0xB9250D | 0x70      | 112           | 0          | 1      | Zombie    | Deling City Sewers                                                       | Field       | 134              | Deling City - Sewer                          |
| 025 | 0xB9250E | 0x5B      | 91            | 0          | 1      | Esuna     | Deling City Sewers                                                       | Field       | 134              | Deling City - Sewer                          |
| 026 | 0xB9250F | 0x4C      | 76            | 0          | 1      | Bio       | Deling City Sewers                                                       | Field       | 134              | Deling City - Sewer                          |
| 027 | 0xB92510 | 0xC2      | 194           | 1          | 1      | Fira      |                                                                          | Field       | -1               | Unused                                       |
| 028 | 0xB92511 | 0xEE      | 238           | 1          | 1      | Berserk   | D-District Prison Floor 9 - right cell                                   | Field       | 135              | Galbadia - D-District Prison                 |
| 029 | 0xB92512 | 0x09      | 9             | 0          | 0      | Thundaga  | D-District Prison Floor 11 - right cell                                  | Field       | 135              | Galbadia - D-District Prison                 |
| 030 | 0xB92513 | 0x4B      | 75            | 0          | 1      | Aero      | Outside D-District Prison                                                | Field       | 136              | Desert                                       |
| 031 | 0xB92514 | 0xC5      | 197           | 1          | 1      | Blizzara  | Missile Base - control room                                              | Field       | 137              | Galbadia - Missile Base                      |
| 032 | 0xB92515 | 0xE6      | 230           | 1          | 1      | Blind     | Missile Base room with G-Soldiers who ask to deliver a message           | Field       | 137              | Galbadia - Missile Base                      |
| 033 | 0xB92516 | 0x59      | 89            | 0          | 1      | Full-Life | Missile Base - silo room                                                 | Field       | 137              | Galbadia - Missile Base                      |
| 034 | 0xB92517 | 0xEC      | 236           | 1          | 1      | Drain     | Winhill road south from town square                                      | Field       | 138              | Winhill - Village                            |
| 035 | 0xB92518 | 0xDC      | 220           | 1          | 1      | Dispel    | Winhill town square                                                      | Field       | 138              | Winhill - Village                            |
| 036 | 0xB92519 | 0x17      | 23            | 0          | 0      | Curaga    | Winhill Laguna's room in the dream                                       | Field       | 140              | Winhill - Vacant House                       |
| 037 | 0xB9251A | 0x1F      | 31            | 0          | 0      | Reflect   | Winhill east road                                                        | Field       | 138              | Winhill - Village                            |
| 038 | 0xB9251B | 0xDD      | 221           | 1          | 1      | Protect   | Tomb of the Unknown King - outside                                       | Field       | 145              | Tomb of the Unknown King                     |
| 039 | 0xB9251C | 0xEF      | 239           | 1          | 1      | Float     | Tomb of the Unknown King - north room                                    | Field       | 145              | Tomb of the Unknown King                     |
| 040 | 0xB9251D | 0x56      | 86            | 0          | 1      | Cura      | Tomb of the Unknown King - east room                                     | Field       | 145              | Tomb of the Unknown King                     |
| 041 | 0xB9251E | 0xE3      | 227           | 1          | 1      | Haste     | Fishermans Horizon abandoned train station                               | Field       | 154              | FH - Station Yard                            |
| 042 | 0xB9251F | 0xDE      | 222           | 1          | 1      | Shell     | Fishermans Horizon junk shop                                             | Field       | 147              | FH - Residential Area                        |
| 043 | 0xB92520 | 0xDA      | 218           | 1          | 1      | Regen     | Fishermans Horizon overlooking the sun panel                             | Field       | 146              | Fishermans Horizon                           |
| 044 | 0xB92521 | 0x19      | 25            | 0          | 0      | Full-Life | Fishermans Horizon Master Fisherman's fishing spot                       | Field       | 150              | FH - Factory                                 |
| 045 | 0xB92522 | 0x93      | 147           | 1          | 0      | Ultima    | Fishermans Horizon mayor's house                                         | Field       | 149              | FH - Mayor's Residence                       |
| 046 | 0xB92523 | 0xC9      | 201           | 1          | 1      | Thundaga  | Great Salt Lake past the dinosaur skeleton                               | Field       | 157              | FH - Great Salt Lake                         |
| 047 | 0xB92524 | 0x10      | 16            | 0          | 0      | Meteor    | Great Salt Lake dinosaur skeleton                                        | Field       | 157              | FH - Great Salt Lake                         |
| 048 | 0xB92525 | 0x57      | 87            | 0          | 1      | Curaga    | Esthar city streets near city entrance                                   | Field       | 159              | Esthar - City                                |
| 049 | 0xB92526 | 0x44      | 68            | 0          | 1      | Blizzard  | Esthar outside palace                                                    | Field       | 159              | Esthar - City                                |
| 050 | 0xB92527 | 0xD1      | 209           | 1          | 1      | Quake     | Esthar outside Odine's Lab                                               | Field       | 160              | Esthar - Odine's Laboratory                  |
| 051 | 0xB92528 | 0x52      | 82            | 0          | 1      | Tornado   | Esthar shopping mall                                                     | Field       | 159              | Esthar - City                                |
| 052 | 0xB92529 | 0xE1      | 225           | 1          | 1      | Double    | Esthar Odine's Lab in a Laguna dream                                     | Field       | 167              | Dr. Odine's Laboratory- Lobby                |
| 053 | 0xB9252A | 0x2D      | 45            | 0          | 0      | Pain      |                                                                          | Field       | -1               | Unused                                       |
| 054 | 0xB9252B | 0x0F      | 15            | 0          | 0      | Flare     | Esthar Odine's Lab in a Laguna dream                                     | Field       | 167              | Dr. Odine's Laboratory- Lobby                |
| 055 | 0xB9252C | 0x65      | 101           | 0          | 1      | Stop      | Sorceress Memorial                                                       | Field       | 173              | Esthar Sorceress Memorial                    |
| 056 | 0xB9252D | 0x65      | 101           | 0          | 1      | Stop      |                                                                          | Field       | -1               | Unused                                       |
| 057 | 0xB9252E | 0xD8      | 216           | 1          | 1      | Life      | Tears' Point entrance                                                    | Field       | 177              | Tears' Point                                 |
| 058 | 0xB9252F | 0x1F      | 31            | 0          | 0      | Reflect   | Tears' Point middle                                                      | Field       | 177              | Tears' Point                                 |
| 059 | 0xB92530 | 0xEB      | 235           | 1          | 1      | Death     | Lunatic Pandora Laboratory in a Laguna dream                             | Field       | 178              | Lunatic Pandora Laboratory                   |
| 060 | 0xB92531 | 0x0E      | 14            | 0          | 0      | Holy      | Lunatic Pandora near Elevator #1                                         | Field       | 182              | Centra - Excavation Site                     |
| 061 | 0xB92532 | 0x69      | 105           | 0          | 1      | Silence   | Lunatic Pandora                                                          | Field       | 182              | Centra - Excavation Site                     |
| 062 | 0xB92533 | 0x13      | 19            | 0          | 0      | Ultima    | Lunatic Pandora                                                          | Field       | 182              | Centra - Excavation Site                     |
| 063 | 0xB92534 | 0x67      | 103           | 0          | 1      | Confuse   |                                                                          | Field       | 182              | Centra - Excavation Site                     |
| 064 | 0xB92535 | 0x6A      | 106           | 0          | 1      | Break     | Lunatic Pandora on the way to fight Adel                                 | Field       | 181              | Lunatic Pandora                              |
| 065 | 0xB92536 | 0xD0      | 208           | 1          | 1      | Meteor    | Lunatic Pandora entrance                                                 | Field       | 181              | Lunatic Pandora                              |
| 066 | 0xB92537 | 0x57      | 87            | 0          | 1      | Curaga    | Lunatic Pandora elevator room                                            | Field       | 181              | Lunatic Pandora                              |
| 067 | 0xB92538 | 0x64      | 100           | 0          | 1      | Slow      |                                                                          | Field       | -1               | Unused                                       |
| 068 | 0xB92539 | 0x57      | 87            | 0          | 1      | Curaga    | Edea's Orphanage                                                         | Field       | 185              | Edea's House- Bedroom                        |
| 069 | 0xB9253A | 0x0F      | 15            | 0          | 0      | Flare     |                                                                          | Field       | -1               | Unused                                       |
| 070 | 0xB9253B | 0x8E      | 142           | 1          | 0      | Holy      |                                                                          | Field       | -1               | Unused                                       |
| 071 | 0xB9253C | 0x68      | 104           | 0          | 1      | Sleep     | Centra Excavation Site                                                   | Field       | 182              | Centra- Excavation Site                      |
| 072 | 0xB9253D | 0xE7      | 231           | 1          | 1      | Confuse   | Centra Excavation Site                                                   | Field       | 182              | Centra- Excavation Site                      |
| 073 | 0xB9253E | 0x4B      | 75            | 0          | 1      | Aero      | Centra Ruins right ladder after the lift                                 | Field       | 189              | Centra Ruins                                 |
| 074 | 0xB9253F | 0x2C      | 44            | 0          | 0      | Drain     | Centra Ruins platform after the first staircase                          | Field       | 189              | Centra Ruins                                 |
| 075 | 0xB92540 | 0x2D      | 45            | 0          | 0      | Pain      | Centra Ruins next to the dome                                            | Field       | 189              | Centra Ruins                                 |
| 076 | 0xB92541 | 0xC9      | 201           | 1          | 1      | Thundaga  | Trabia Garden in front of the statue                                     | Field       | 190              | Trabia Garden- Front Gate                    |
| 077 | 0xB92542 | 0x30      | 48            | 0          | 0      | Zombie    | Trabia Garden cemetery                                                   | Field       | 191              | T-Garden - Cemetery                          |
| 078 | 0xB92543 | 0x20      | 32            | 0          | 0      | Aura      | Trabia Garden stage                                                      | Field       | 193              | T-Garden - Festival Stage                    |
| 079 | 0xB92544 | 0xD3      | 211           | 1          | 1      | Ultima    | Shumi Village - above ground                                             | Field       | 197              | Shumi Village - Desert Village               |
| 080 | 0xB92545 | 0x46      | 70            | 0          | 1      | Blizzaga  | Shumi Village - outside elder's house                                    | Field       | 199              | Shumi Village - Village                      |
| 081 | 0xB92546 | 0x43      | 67            | 0          | 1      | Firaga    | Shumi Village workshop                                                   | Field       | 201              | Shumi Village - Residence                    |
| 082 | 0xB92547 | 0xD2      | 210           | 1          | 1      | Tornado   |                                                                          | Field       | -1               | Unused                                       |
| 083 | 0xB92548 | 0xCE      | 206           | 1          | 1      | Holy      | White SeeD Ship                                                          | Field       | 207              | White SeeD Ship- Cabin                       |
| 084 | 0xB92549 | 0x56      | 86            | 0          | 1      | Cura      | Ragnarok room with a red Propagator                                      | Field       | 210              | Ragnarok - Aisle                             |
| 085 | 0xB9254A | 0x58      | 88            | 0          | 1      | Life      | Ragnarok hangar upstairs                                                 | Field       | 210              | Ragnarok - Aisle                             |
| 086 | 0xB9254B | 0x19      | 25            | 0          | 0      | Full-Life | Ragnarok room with save point                                            | Field       | 211              | Ragnarok - Hangar                            |
| 087 | 0xB9254C | 0x5C      | 92            | 0          | 1      | Dispel    | Deep Sea Research Center second level                                    | Field       | 217              | Deep Sea Research Center- Lv                 |
| 088 | 0xB9254D | 0x5B      | 91            | 0          | 1      | Esuna     | Deep Sea Research Center secret room                                     | Field       | 217              | Deep Sea Research Center- Lv                 |
| 089 | 0xB9254E | 0xA2      | 162           | 1          | 0      | Triple    | Deep Sea Research Center third screen on the way to Ultima Weapon's lair | Field       | 218              | Deep Sea Deposit                             |
| 090 | 0xB9254F | 0x13      | 19            | 0          | 0      | Ultima    | Deep Sea Research Center fifth screen on the way to Ultima Weapon's lair | Field       | 218              | Deep Sea Deposit                             |
| 091 | 0xB92550 | 0xF1      | 241           | 1          | 1      | Meltdown  | Lunar Base room before the escape pods                                   | Field       | 221              | Lunar Base - Pod                             |
| 092 | 0xB92551 | 0x10      | 16            | 0          | 0      | Meteor    | Lunar Base Ellone's room                                                 | Field       | 225              | Lunar Base - Residential Zone                |
| 093 | 0xB92552 | 0xE3      | 227           | 1          | 1      | Haste     |                                                                          | Field       | -1               | Unused                                       |
| 094 | 0xB92553 | 0xE4      | 228           | 1          | 1      | Slow      |                                                                          | Field       | -1               | Unused                                       |
| 095 | 0xB92554 | 0xD7      | 215           | 1          | 1      | Curaga    |                                                                          | Field       | -1               | Unused                                       |
| 096 | 0xB92555 | 0xD8      | 216           | 1          | 1      | Life      |                                                                          | Field       | -1               | Unused                                       |
| 097 | 0xB92556 | 0xE5      | 229           | 1          | 1      | Stop      |                                                                          | Field       | -1               | Unused                                       |
| 098 | 0xB92557 | 0xDA      | 218           | 1          | 1      | Regen     |                                                                          | Field       | -1               | Unused                                       |
| 099 | 0xB92558 | 0xE1      | 225           | 1          | 1      | Double    |                                                                          | Field       | -1               | Unused                                       |
| 100 | 0xB92559 | 0x22      | 34            | 0          | 0      | Triple    |                                                                          | Field       | 228              | Wilderness                                   |
| 101 | 0xB9255A | 0x0F      | 15            | 0          | 0      | Flare     | Ultimecia Castle outside                                                 | Field       | 248              | Ultimecia Castle                             |
| 102 | 0xB9255B | 0x57      | 87            | 0          | 1      | Curaga    | Ultimecia Castle storage room                                            | Field       | 237              | Ultimecia Castle - Storage Room              |
| 103 | 0xB9255C | 0x56      | 86            | 0          | 1      | Cura      | Ultimecia Castle passageway                                              | Field       | 233              | Ultimecia Castle - Passageway                |
| 104 | 0xB9255D | 0x72      | 114           | 0          | 1      | Scan      |                                                                          | Field       | -1               | Unused                                       |
| 105 | 0xB9255E | 0x5B      | 91            | 0          | 1      | Esuna     |                                                                          | Field       | -1               | Unused                                       |
| 106 | 0xB9255F | 0x64      | 100           | 0          | 1      | Slow      | Ultimecia Castle courtyard                                               | Field       | 243              | Ultimecia Castle - Courtyard                 |
| 107 | 0xB92560 | 0x5C      | 92            | 0          | 1      | Dispel    | Ultimecia Castle chapel                                                  | Field       | 244              | Ultimecia Castle - Chapel                    |
| 108 | 0xB92561 | 0x65      | 101           | 0          | 1      | Stop      | Ultimecia Castle clock tower                                             | Field       | 245              | Ultimecia Castle - Clock Tower               |
| 109 | 0xB92562 | 0x58      | 88            | 0          | 1      | Life      |                                                                          | Field       | 246              | Ultimecia Castle - Master Room               |
| 110 | 0xB92563 | 0x0F      | 15            | 0          | 0      | Flare     |                                                                          | Field       | -1               | Unused                                       |
| 111 | 0xB92564 | 0x20      | 32            | 0          | 0      | Aura      | Ultimecia Castle wine cellar                                             | Field       | 232              | Ultimecia Castle - Wine Cellar               |
| 112 | 0xB92565 | 0x0E      | 14            | 0          | 0      | Holy      | Ultimecia Castle treasure room                                           | Field       | 236              | Ultimecia Castle - Treasure Rm               |
| 113 | 0xB92566 | 0x10      | 16            | 0          | 0      | Meteor    |                                                                          | Field       | 231              | Ultimecia Castle - Terrace                   |
| 114 | 0xB92567 | 0x31      | 49            | 0          | 0      | Meltdown  | Ultimecia Castle art gallery                                             | Field       | 238              | Ultimecia Castle - Art Gallery               |
| 115 | 0xB92568 | 0x13      | 19            | 0          | 0      | Ultima    | Ultimecia Castle armory                                                  | Field       | 240              | Ultimecia Castle - Armory                    |
| 116 | 0xB92569 | 0x19      | 25            | 0          | 0      | Full-Life | Ultimecia Castle prison                                                  | Field       | 241              | Ultimecia Castle - Prison Cell               |
| 117 | 0xB9256A | 0x22      | 34            | 0          | 0      | Triple    |                                                                          | Field       | 245              | Ultimecia Castle - Clock Tower               |
| 118 | 0xB9256B | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 119 | 0xB9256C | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 120 | 0xB9256D | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 121 | 0xB9256E | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 122 | 0xB9256F | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 123 | 0xB92570 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 124 | 0xB92571 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 125 | 0xB92572 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 126 | 0xB92573 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 127 | 0xB92574 | 0x81      | 129           | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 128 | 0xB92575 | 0x55      | 85            | 1          | 0      | Fire      |                                                                          | Field       | -1               | Unused                                       |
| 129 | 0xB92576 | 0x5B      | 91            | 0          | 1      | Cure      |                                                                          | World       | 1                | Balamb - Alcauld Plains                      |
| 130 | 0xB92577 | 0x47      | 71            | 0          | 1      | Esuna     |                                                                          | World       | 1                | Balamb - Alcauld Plains                      |
| 131 | 0xB92578 | 0x42      | 66            | 0          | 1      | Thunder   |                                                                          | World       | 6                | Timber - Mandy Beach                         |
| 132 | 0xB92579 | 0x48      | 72            | 0          | 1      | Fira      |                                                                          | World       | 8                | Timber - Lanker Plains                       |
| 133 | 0xB9257A | 0x45      | 69            | 0          | 1      | Thundara  |                                                                          | World       | 17               | Timber - Shenand Hill                        |
| 134 | 0xB9257B | 0x44      | 68            | 0          | 1      | Blizzara  |                                                                          | World       | 15               | Galbadia - Monterosa Plateau                 |
| 135 | 0xB9257C | 0x41      | 65            | 0          | 1      | Blizzard  |                                                                          | World       | 10               | Timber - Yaulny Canyon                       |
| 136 | 0xB9257D | 0x55      | 85            | 0          | 1      | Fire      |                                                                          | World       | -1               | Unused                                       |
| 137 | 0xB9257E | 0x4A      | 74            | 0          | 1      | Cure      |                                                                          | World       | 11               | Dollet - Hasberry Plains                     |
| 138 | 0xB9257F | 0x56      | 86            | 0          | 1      | Water     |                                                                          | World       | 14               | Dollet - Malgo Peninsula                     |
| 139 | 0xB92580 | 0x5B      | 91            | 0          | 1      | Cura      |                                                                          | World       | 11               | Dollet - Hasberry Plains                     |
| 140 | 0xB92581 | 0x72      | 114           | 0          | 1      | Esuna     |                                                                          | World       | 20               | Great Plains of Galbadia                     |
| 141 | 0xB92582 | 0x5E      | 94            | 0          | 1      | Scan      |                                                                          | World       | 21               | Galbadia - Wilburn Hill                      |
| 142 | 0xB92583 | 0x63      | 99            | 0          | 1      | Shell     |                                                                          | World       | 15               | Galbadia - Monterosa Plateau                 |
| 143 | 0xB92584 | 0x4B      | 75            | 0          | 1      | Haste     |                                                                          | World       | 23               | Galbadia - Dingo Desert                      |
| 144 | 0xB92585 | 0x4C      | 76            | 0          | 1      | Aero      |                                                                          | World       | 15               | Galbadia - Monterosa Plateau                 |
| 145 | 0xB92586 | 0x58      | 88            | 0          | 1      | Bio       |                                                                          | World       | 15               | Galbadia - Monterosa Plateau                 |
| 146 | 0xB92587 | 0x4D      | 77            | 0          | 1      | Life      |                                                                          | World       | 24               | Winhill - Winhill Bluffs                     |
| 147 | 0xB92588 | 0x5D      | 93            | 0          | 1      | Demi      |                                                                          | World       | 62               | Centra - Centra Crater                       |
| 148 | 0xB92589 | 0x4E      | 78            | 0          | 1      | Protect   |                                                                          | World       | 61               | Centra - Nectar Peninsula                    |
| 149 | 0xB9258A | 0x49      | 73            | 0          | 1      | Holy      |                                                                          | World       | 57               | Centra - Cape of Good Hope                   |
| 150 | 0xB9258B | 0x65      | 101           | 0          | 1      | Thundaga  |                                                                          | World       | 55               | Centra - Almaj Mountains                     |
| 151 | 0xB9258C | 0x43      | 67            | 0          | 1      | Stop      |                                                                          | World       | 53               | Esthar - Shalmal Peninsula                   |
| 152 | 0xB9258D | 0x5A      | 90            | 0          | 1      | Firaga    |                                                                          | World       | 50               | Esthar - Kashkabald Desert                   |
| 153 | 0xB9258E | 0x46      | 70            | 0          | 1      | Regen     |                                                                          | World       | 26               | Trabia - Winter Island                       |
| 154 | 0xB9258F | 0x67      | 103           | 0          | 1      | Blizzaga  |                                                                          | World       | 26               | Trabia - Winter Island                       |
| 155 | 0xB92590 | 0x4F      | 79            | 0          | 1      | Confuse   |                                                                          | World       | 30               | Trabia - Hawkwind Plains                     |
| 156 | 0xB92591 | 0x5C      | 92            | 0          | 1      | Flare     |                                                                          | World       | 32               | Trabia - Bika Snowfield                      |
| 157 | 0xB92592 | 0x64      | 100           | 0          | 1      | Dispel    |                                                                          | World       | 32               | Trabia - Bika Snowfield                      |
| 158 | 0xB92593 | 0x51      | 81            | 0          | 1      | Slow      |                                                                          | World       | 32               | Trabia - Bika Snowfield                      |
| 159 | 0xB92594 | 0x57      | 87            | 0          | 1      | Quake     |                                                                          | World       | 37               | Trabia - Vienne Mountains                    |
| 160 | 0xB92595 | 0x52      | 82            | 0          | 1      | Curaga    |                                                                          | World       | 46               | Esthar - West Coast                          |
| 161 | 0xB92596 | 0x19      | 25            | 0          | 1      | Tornado   |                                                                          | World       | 39               | Esthar - Nortes Mountains                    |
| 162 | 0xB92597 | 0x5F      | 95            | 0          | 0      | Full-Life |                                                                          | World       | 39               | Esthar - Nortes Mountains                    |
| 163 | 0xB92598 | 0x20      | 32            | 0          | 1      | Reflect   |                                                                          | World       | 25               | Winhill - Humphrey Archipelago               |
| 164 | 0xB92599 | 0x11      | 17            | 0          | 0      | Aura      |                                                                          | World       | 13               | Dollet - Long Horn Island                    |
| 165 | 0xB9259A | 0x61      | 97            | 0          | 0      | Quake     |                                                                          | World       | 12               | Dollet - Holy Glory Cape                     |
| 166 | 0xB9259B | 0x6A      | 106           | 0          | 1      | Double    |                                                                          | World       | -1               | Unused                                       |
| 167 | 0xB9259C | 0x10      | 16            | 0          | 1      | Break     |                                                                          | World       | 17               | Timber- Shenand Hill                         |
| 168 | 0xB9259D | 0x13      | 19            | 0          | 0      | Meteor    |                                                                          | World       | 41               | Esthar - Grandidi Forest                     |
| 169 | 0xB9259E | 0x22      | 34            | 0          | 0      | Ultima    |                                                                          | World       | 41               | Esthar - Grandidi Forest                     |
| 170 | 0xB9259F | 0x67      | 103           | 0          | 0      | Triple    |                                                                          | World       | 41               | Esthar - Grandidi Forest                     |
| 171 | 0xB925A0 | 0x66      | 102           | 0          | 1      | Confuse   |                                                                          | World       | 42               | Esthar - Millefeuille Archipelago            |
| 172 | 0xB925A1 | 0xD1      | 209           | 0          | 1      | Blind     |                                                                          | World       | 41               | Esthar - Grandidi Forest                     |
| 173 | 0xB925A2 | 0x68      | 104           | 1          | 1      | Quake     |                                                                          | World       | 26               | Trabia - Winter Island                       |
| 174 | 0xB925A3 | 0x69      | 105           | 0          | 1      | Sleep     |                                                                          | World       | 26               | Trabia - Winter Island                       |
| 175 | 0xB925A4 | 0xCF      | 207           | 0          | 1      | Silence   |                                                                          | World       | 26               | Trabia - Winter Island                       |
| 176 | 0xB925A5 | 0x6B      | 107           | 1          | 1      | Flare     |                                                                          | World       | 32               | Trabia - Bika Snowfield                      |
| 177 | 0xB925A6 | 0x6C      | 108           | 0          | 1      | Death     |                                                                          | World       | 31               | Trabia - Albatross Archipelago               |
| 178 | 0xB925A7 | 0xED      | 237           | 0          | 1      | Drain     |                                                                          | World       | 12               | Dollet - Holy Glory Cape                     |
| 179 | 0xB925A8 | 0x6E      | 110           | 1          | 1      | Pain      |                                                                          | World       | 11               | Dollet - Hasberry Plains                     |
| 180 | 0xB925A9 | 0x6F      | 111           | 0          | 1      | Berserk   |                                                                          | World       | 15               | Galbadia - Monterosa Plateau                 |
| 181 | 0xB925AA | 0x70      | 112           | 0          | 1      | Float     |                                                                          | World       | 21               | Galbadia - Wilburn Hill                      |
| 182 | 0xB925AB | 0x71      | 113           | 0          | 1      | Zombie    |                                                                          | World       | 22               | Galbadia - Rem Archipelago                   |
| 183 | 0xB925AC | 0x93      | 147           | 0          | 1      | Meltdown  |                                                                          | World       | 15               | Galbadia - Monterosa Plateau                 |
| 184 | 0xB925AD | 0xD2      | 210           | 1          | 0      | Ultima    |                                                                          | World       | 16               | Galbadia - Lallapalooza Canyon               |
| 185 | 0xB925AE | 0xD1      | 209           | 1          | 1      | Tornado   |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 186 | 0xB925AF | 0xD0      | 208           | 1          | 1      | Quake     |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 187 | 0xB925B0 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 188 | 0xB925B1 | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 189 | 0xB925B2 | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 190 | 0xB925B3 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 191 | 0xB925B4 | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 192 | 0xB925B5 | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 193 | 0xB925B6 | 0xD2      | 210           | 1          | 1      | Full-Life |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 194 | 0xB925B7 | 0xD1      | 209           | 1          | 1      | Tornado   |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 195 | 0xB925B8 | 0xD0      | 208           | 1          | 1      | Quake     |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 196 | 0xB925B9 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 197 | 0xB925BA | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 198 | 0xB925BB | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 199 | 0xB925BC | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 200 | 0xB925BD | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 201 | 0xB925BE | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 202 | 0xB925BF | 0xD2      | 210           | 1          | 1      | Full-Life |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 203 | 0xB925C0 | 0xD1      | 209           | 1          | 1      | Tornado   |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 204 | 0xB925C1 | 0xD0      | 208           | 1          | 1      | Quake     |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 205 | 0xB925C2 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 206 | 0xB925C3 | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 207 | 0xB925C4 | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 208 | 0xB925C5 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 209 | 0xB925C6 | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 210 | 0xB925C7 | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 211 | 0xB925C8 | 0xD3      | 211           | 1          | 1      | Full-Life |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 212 | 0xB925C9 | 0xD0      | 208           | 1          | 1      | Ultima    |                                                                          | World       | 51               | Island Closest to Heaven                     |
| 213 | 0xB925CA | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 214 | 0xB925CB | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 215 | 0xB925CC | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          | World       | 19               | Island Closest to Hell                       |
| 216 | 0xB925CD | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 217 | 0xB925CE | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 218 | 0xB925CF | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 219 | 0xB925D0 | 0xD0      | 208           | 1          | 1      | Full-Life |                                                                          | World       | 19               | Island Closest to Hell                       |
| 220 | 0xB925D1 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 221 | 0xB925D2 | 0xE2      | 226           | 1          | 1      | Holy      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 222 | 0xB925D3 | 0xE0      | 224           | 1          | 1      | Triple    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 223 | 0xB925D4 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 224 | 0xB925D5 | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 225 | 0xB925D6 | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 226 | 0xB925D7 | 0xD0      | 208           | 1          | 1      | Full-Life |                                                                          | World       | 19               | Island Closest to Hell                       |
| 227 | 0xB925D8 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 228 | 0xB925D9 | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 229 | 0xB925DA | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          | World       | 19               | Island Closest to Hell                       |
| 230 | 0xB925DB | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 231 | 0xB925DC | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 232 | 0xB925DD | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 233 | 0xB925DE | 0xD0      | 208           | 1          | 1      | Full-Life |                                                                          | World       | 19               | Island Closest to Hell                       |
| 234 | 0xB925DF | 0xE2      | 226           | 1          | 1      | Meteor    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 235 | 0xB925E0 | 0xCF      | 207           | 1          | 1      | Triple    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 236 | 0xB925E1 | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          | World       | 19               | Island Closest to Hell                       |
| 237 | 0xB925E2 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 238 | 0xB925E3 | 0xE2      | 226           | 1          | 1      | Ultima    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 239 | 0xB925E4 | 0xD9      | 217           | 1          | 1      | Triple    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 240 | 0xB925E5 | 0xD0      | 208           | 1          | 1      | Full-Life |                                                                          | World       | 19               | Island Closest to Hell                       |
| 241 | 0xB925E6 | 0xCE      | 206           | 1          | 1      | Meteor    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 242 | 0xB925E7 | 0xCF      | 207           | 1          | 1      | Holy      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 243 | 0xB925E8 | 0xE0      | 224           | 1          | 1      | Flare     |                                                                          | World       | 19               | Island Closest to Hell                       |
| 244 | 0xB925E9 | 0xD3      | 211           | 1          | 1      | Aura      |                                                                          | World       | 19               | Island Closest to Hell                       |
| 245 | 0xB925EA | 0x44      | 68            | 1          | 1      | Ultima    |                                                                          | World       | 19               | Island Closest to Hell                       |
| 246 | 0xB925EB | 0x55      | 85            | 0          | 1      | Blizzard  |                                                                          | World       | 1                | Balamb - Alcauld Plains                      |
| 247 | 0xB925EC | 0xDC      | 220           | 0          | 1      | Cure      |                                                                          | World       | 1                | Balamb - Alcauld Plains                      |
| 248 | 0xB925ED | 0xE7      | 231           | 1          | 1      | Dispel    |                                                                          | World       | 15               | Galbadia - Monterosa Plateau                 |
| 249 | 0xB925EE | 0x10      | 16            | 1          | 1      | Confuse   |                                                                          | World       | 20               | Great Plains of Galbadia                     |
| 250 | 0xB925EF | 0x21      | 33            | 0          | 0      | Meteor    |                                                                          | World       | 43               | Great Plains of Esthar                       |
| 251 | 0xB925F0 | 0x20      | 32            | 0          | 0      | Double    |                                                                          | World       | 43               | Great Plains of Esthar                       |
| 252 | 0xB925F1 | 0x0E      | 14            | 0          | 0      | Aura      |                                                                          | World       | 43               | Great Plains of Esthar                       |
| 253 | 0xB925F2 | 0x0F      | 15            | 0          | 0      | Holy      |                                                                          | World       | 43               | Great Plains of Esthar                       |
| 254 | 0xB925F3 | 0x13      | 19            | 0          | 0      | Flare     |                                                                          | World       | 47               | Esthar - Sollet Mountains                    |
| 255 | 0xB925F4 | 0xF2      | 242           | 0          | 0      | Ultima    |                                                                          | World       | 48               | Esthar - Abadan Plains                       |
| 256 | 0xB925F5 | 0x00      | 0             | 1          | 1      | Scan      |                                                                          | World       | -1               | Unused                                       |
