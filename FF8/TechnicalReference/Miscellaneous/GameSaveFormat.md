---
layout: default
parent: Miscellaneous
title: Game Save Format
permalink: /technical-reference/miscellaneous/game-save-format/
---

By myst6re.

## The save format

PC steam version: Offsets start from at 384 (0x0180). File is compressed with LZS.

| Offset | Size                | Data                                                                                |
|--------|---------------------|-------------------------------------------------------------------------------------|
| 0x0000 | 2 bytes             | Checksum                                                                            |
| 0x0002 | 2 bytes             | Always 0x08FF                                                                       |
| 0x0004 | 2 bytes             | **Preview:** Location ID                                                            |
| 0x0006 | 2 bytes             | **Preview:** 1st character's current HP                                             |
| 0x0008 | 2 bytes             | **Preview:** 1st character's max HP                                                 |
| 0x000A | 2 bytes             | **Preview:** save count                                                             |
| 0x000C | 4 bytes             | **Preview:** Amount of Gil                                                          |
| 0x0010 | 4 bytes             | **Preview:** Total number of seconds played                                         |
| 0x0014 | 1 byte              | **Preview:** 1st character's level                                                  |
| 0x0015 | 1 byte              | **Preview:** 1st character's portrait                                               |
| 0x0016 | 1 byte              | **Preview:** 2nd character's portrait                                               |
| 0x0017 | 1 byte              | **Preview:** 3rd character's portrait                                               |
| 0x0018 | 12 bytes            | **Preview:** Squall's name (0x00 terminated)                                        |
| 0x0024 | 12 bytes            | **Preview:** Rinoa's name (0x00 terminated)                                         |
| 0x0030 | 12 bytes            | **Preview:** Angelo's name (0x00 terminated)                                        |
| 0x003C | 12 bytes            | **Preview:** Boko's name (0x00 terminated)                                          |
| 0x0048 | 4 bytes             | **Preview:** Current Disk (0 based)                                                 |
| 0x004C | 4 bytes             | **Preview:** Current save (last saved game)                                         |
| 0x0050 | 68 bytes            | **Guardian Forces:** Quetzalcoatl                                                   |
| 0x00B4 | 68 bytes            | **Guardian Forces:** Shiva                                                          |
| 0x00D8 | 68 bytes            | **Guardian Forces:** Ifrit                                                          |
| 0x011C | 68 bytes            | **Guardian Forces:** Siren                                                          |
| 0x0160 | 68 bytes            | **Guardian Forces:** Brothers                                                       |
| 0x01A4 | 68 bytes            | **Guardian Forces:** Diablos                                                        |
| 0x01E8 | 68 bytes            | **Guardian Forces:** Carbuncle                                                      |
| 0x022C | 68 bytes            | **Guardian Forces:** Leviathan                                                      |
| 0x0270 | 68 bytes            | **Guardian Forces:** Pandemonia                                                     |
| 0x02B4 | 68 bytes            | **Guardian Forces:** Cerberus                                                       |
| 0x02F8 | 68 bytes            | **Guardian Forces:** Alexander                                                      |
| 0x033C | 68 bytes            | **Guardian Forces:** Doomtrain                                                      |
| 0x0380 | 68 bytes            | **Guardian Forces:** Bahamut                                                        |
| 0x03C4 | 68 bytes            | **Guardian Forces:** Cactuar                                                        |
| 0x0408 | 68 bytes            | **Guardian Forces:** Tonberry                                                       |
| 0x044C | 68 bytes            | **Guardian Forces:** Eden                                                           |
| 0x0490 | 152 bytes           | **Characters:** Squall                                                              |
| 0x0528 | 152 bytes           | **Characters:** Zell                                                                |
| 0x05C0 | 152 bytes           | **Characters:** Irvine                                                              |
| 0x0658 | 152 bytes           | **Characters:** Quistis                                                             |
| 0x06F0 | 152 bytes           | **Characters:** Rinoa                                                               |
| 0x0788 | 152 bytes           | **Characters:** Selphie                                                             |
| 0x0820 | 152 bytes           | **Characters:** Seifer                                                              |
| 0x08B8 | 152 bytes           | **Characters:** Edea                                                                |
| 0x0950 | 400 bytes           | Shops                                                                               |
| 0x0AE0 | 20 bytes            | Configuration                                                                       |
| 0x0AF4 | 4 bytes             | Party (0xFF terminated)                                                             |
| 0x0AF8 | 4 bytes             | Known weapons                                                                       |
| 0x0AFC | 12 bytes            | Griever name (FF8 text format)                                                      |
| 0x0B08 | 1 bytes             | Weapon ID Laguna                                                                    |
| 0x0B09 | 1 bytes             | Weapon ID Kiros                                                                     |
| 0x0B0A | 1 bytes             | Weapon ID Ward                                                                      |
| 0x0B0B | 1 bytes             | Unknown                                                                             |
| 0x0B0C | 4 bytes             | Amount of Gil                                                                       |
| 0x0B10 | 4 bytes             | Amount of Gil (Laguna)                                                              |
| 0x0B14 | 2 bytes             | **Limit Break** Quistis                                                             |
| 0x0B16 | 2 bytes             | **Limit Break** Zell                                                                |
| 0x0B18 | 1 byte              | **Limit Break** Irvine                                                              |
| 0x0B19 | 1 byte              | **Limit Break** Selphie                                                             |
| 0x0B1A | 1 byte              | **Limit Break** Angelo completed                                                    |
| 0x0B1B | 1 byte              | **Limit Break** Angelo known                                                        |
| 0x0B1C | 8 bytes             | **Limit Break** Angelo points                                                       |
| 0x0B24 | 32 bytes            | **Items** battle order                                                              |
| 0x0B44 | 396 bytes           | **Items** 198 items (Item ID and Quantity)                                          |
| 0x0CD0 | 4 bytes             | Game time                                                                           |
| 0x0CD4 | 4 bytes             | Countdown                                                                           |
| 0x0CD8 | 4 bytes             | Unknown                                                                             |
| 0x0CDC | 4 bytes             | **Battle:** victory count                                                           |
| 0x0CE0 | 2 bytes             | Unknown                                                                             |
| 0x0CE2 | 2 bytes             | **Battle:** battle escaped                                                          |
| 0x0CE4 | 4 bytes             | Unknown                                                                             |
| 0x0CE8 | 4 bytes             | **Battle:** Tonberry killed count                                                   |
| 0x0CEC | 4 bytes             | **Battle:** Tonberry Sr killed (yeah, this is a boolean)                            |
| 0x0CF0 | 4 bytes             | Unknown                                                                             |
| 0x0CF4 | 4 bytes             | **Battle:** First "Bug" battle (R1 tip)                                             |
| 0x0CF8 | 4 bytes             | **Battle:** First "Bomb" battle (Elemental tip)                                     |
| 0x0CFC | 4 bytes             | **Battle:** First "T-Rex" battle (Mental tip)                                       |
| 0x0D00 | 4 bytes             | **Battle:** First "Irvine" battle (Irvine's limit break tip)                        |
| 0x0D04 | 8 bytes             | **Battle:** Magic drawn once                                                        |
| 0x0D0C | 20 bytes            | **Battle:** Ennemy scanned once                                                     |
| 0x0D20 | 1 byte              | **Battle:** Renzokuken auto                                                         |
| 0x0D21 | 1 byte              | **Battle:** Renzokuken indicator                                                    |
| 0x0D22 | 1 byte              | **Battle:** dream/Odin/Phoenix/Gilgamesh/Angelo disabled/Angel Wing enabled/???/??? |
| 0x0D23 | 16 bytes            | Tutorial infos                                                                      |
| 0x0D33 | 1 byte              | SeeD test level                                                                     |
| 0x0D34 | 4 bytes             | Unknown                                                                             |
| 0x0D38 | 4 bytes             | Party (last byte always = 255)                                                      |
| 0x0D3C | 4 bytes             | Unknown                                                                             |
| 0x0D40 | 2 bytes             | Module (1= field, 2= worldmap, 3= battle)                                           |
| 0x0D42 | 2 bytes             | Current field                                                                       |
| 0x0D44 | 2 bytes             | Previous field                                                                      |
| 0x0D46 | 3\*2 bytes (signed) | Coord X (party1, party2, party3)                                                    |
| 0x0D4C | 3\*2 bytes (signed) | Coord Y (party1, party2, party3)                                                    |
| 0x0D52 | 3\*2 bytes          | Triangle ID (party1, party2, party3)                                                |
| 0x0D58 | 3\*1 bytes          | Direction (party1, party2, party3)                                                  |
| 0x0D5B | 1 byte              | *Padding*                                                                           |
| 0x0D5C | 4 bytes             | Unknown                                                                             |
| 0x0D60 | 256 + 1024 bytes    | [Field vars](variables/)                                                          |
| 0x1260 | 128 bytes           | Worldmap (TODO)                                                                     |
| 0x12E0 | 128 bytes           | Triple Triad (TODO)                                                                 |
| 0x1360 | 64 bytes            | Chocobo World (TODO)                                                                |

  

### Guardian Forces

The checksum calculation starts here.

There are 16 G-F: Quetzalcoatl, Shiva, Ifrit, Siren, Brothers, Diablos, Carbuncle, Leviathan, Pandemonia, Cerberus, Alexander, Doomtrain, Bahamut, Cactuar, Tonberry, Eden.  
For each G-F:

| Offset | Size     | Data                                                                       |
|--------|----------|----------------------------------------------------------------------------|
| 0x00   | 12 bytes | Name (0x00 terminated)                                                     |
| 0x0C   | 4 bytes  | Experience                                                                 |
| 0x10   | 1 byte   | Unknown                                                                    |
| 0x11   | 1 byte   | Exists                                                                     |
| 0x12   | 2 bytes  | HP                                                                         |
| 0x14   | 16 bytes | Complete abilities (1 bit = 1 ability completed, 9 bits unused)            |
| 0x24   | 24 bytes | APs (1 byte = 1 ability of the GF, 2 bytes unused)                         |
| 0x3C   | 2 bytes  | Number of kills                                                            |
| 0x3E   | 2 bytes  | Number of KOs                                                              |
| 0x41   | 1 byte   | Learning ability                                                           |
| 0x42   | 3 bytes  | Forgotten abilities (1 bit = 1 ability of the GF forgotten, 2 bits unused) |

### Characters

Squall, Zell, Irvine, Quistis, Rinoa, Selphie, Seifer, Edea. For each character:

| Offset | Size          | Data                                                                                                                            |
|--------|---------------|---------------------------------------------------------------------------------------------------------------------------------|
| 0x00   | 2 bytes       | Current HPs                                                                                                                     |
| 0x02   | 2 bytes       | Max HPs                                                                                                                         |
| 0x04   | 4 bytes       | Experience                                                                                                                      |
| 0x08   | 1 byte        | Model ID                                                                                                                        |
| 0x09   | 1 byte        | Weapon ID                                                                                                                       |
| 0x0A   | 1 byte        | STR                                                                                                                             |
| 0x0B   | 1 byte        | VIT                                                                                                                             |
| 0x0C   | 1 byte        | MAG                                                                                                                             |
| 0x0D   | 1 byte        | SPR                                                                                                                             |
| 0x0E   | 1 byte        | SPD                                                                                                                             |
| 0x0F   | 1 byte        | LCK                                                                                                                             |
| 0x10   | 2\*32 bytes   | Magics                                                                                                                          |
| 0x50   | 3 bytes       | Commands                                                                                                                        |
| 0x53   | 1 byte        | *Padding or unused command*                                                                                                     |
| 0x54   | 4 bytes       | Abilities                                                                                                                       |
| 0x58   | 2 bytes       | Junctionned GFs                                                                                                                 |
| 0x5A   | 1 byte        | Unknown                                                                                                                         |
| 0x5B   | 1 byte        | Alternative model (Normal, SeeD, Soldier...)                                                                                    |
| 0x5C   | 1 byte        | Junction HP                                                                                                                     |
| 0x5D   | 1 byte        | Junction STR                                                                                                                    |
| 0x5E   | 1 byte        | Junction VIT                                                                                                                    |
| 0x5F   | 1 byte        | Junction MAG                                                                                                                    |
| 0x60   | 1 byte        | Junction SPR                                                                                                                    |
| 0x61   | 1 byte        | Junction SPD                                                                                                                    |
| 0x62   | 1 byte        | Junction EVA                                                                                                                    |
| 0x63   | 1 byte        | Junction HIT                                                                                                                    |
| 0x64   | 1 byte        | Junction LCK                                                                                                                    |
| 0x65   | 1 byte        | Junction elemental attack                                                                                                       |
| 0x66   | 1 byte        | Junction mental attack                                                                                                          |
| 0x67   | 4 bytes       | Junction elemental defense                                                                                                      |
| 0x6B   | 4 bytes       | Junction mental defense                                                                                                         |
| 0x6F   | 1 byte        | Unknown (padding?)                                                                                                              |
| 0x70   | 16 \* 2 bytes | Compatibility with GFs                                                                                                          |
| 0x90   | 2 bytes       | Number of kills                                                                                                                 |
| 0x92   | 2 bytes       | Number of KOs                                                                                                                   |
| 0x94   | 1 byte        | Exists                                                                                                                          |
| 0x95   | 1 byte        | Unknown                                                                                                                         |
| 0x96   | 1 byte        | Mental Status  tr("Mort") << tr("Poison") << tr("Fossile") << tr("Darkness") << tr("Aphasie") << tr("Trouble") << tr("Zombie"); |
| 0x97   | 1 byte        | Unknown                                                                                                                         |

### Worldmap

| Offset | Size | Data                                                                                                                         |
|--------|------|------------------------------------------------------------------------------------------------------------------------------|
| 0x00   | 12   | `char_pos[6]` (Character position: x, z, y, ?, ?, rotation (0->4095))                                                        |
| 0x0C   | 12   | `uknown_pos1[6]` (Unknown position 1)                                                                                        |
| 0x18   | 12   | `ragnarok_pos[6]` (Ragnarok position)                                                                                        |
| 0x24   | 12   | `bgu_pos[6]` (Balamb Garden University position)                                                                             |
| 0x30   | 12   | `car_pos[6]` (Car position)                                                                                                  |
| 0x3C   | 12   | `uknown_pos2[6]` (Unknown position 2)                                                                                        |
| 0x48   | 12   | `uknown_pos3[6]` (Unknown position 3)                                                                                        |
| 0x54   | 12   | `uknown_pos4[6]` (Unknown position 4)                                                                                        |
| 0x60   | 2    | `steps_related` (Steps related)                                                                                              |
| 0x62   | 1    | `car_rent` (Car rent status)  0x00:forbidden ,0xFF:none,0x51:balamb1,0x52:balamb2,0x57:esthar                                |
| 0x63   | 7    | `u1[7]` (Unknown, `u1[6]` = deep sea?)                                                                                       |
| 0x6A   | 2    | `u2` (Always 0xFFFF?)                                                                                                        |
| 0x6C   | 2    | `u3` (`u3[1]` = deep sea?)                                                                                                   |
| 0x6E   | 1    | `disp_map_config` (0: none, 1: minisphere, 2: minimap)                                                                       |
| 0x6F   | 1    | `u4` (Unknown)                                                                                                               |
| 0x70   | 2    | `car_steps_related` (Car steps related)                                                                                      |
| 0x72   | 2    | `car_steps_related2` (Car steps related)                                                                                     |
| 0x74   | 1    | `vehicles_instructions_worldmap` Car,Unused,BGU,Chocobo,Hydre,???,???,Unused                                                 |
| 0x75   | 1    | `koyok_quest` (Koyok quest flags)04 : Mandy Beach,Winhill,Trabia,Kashkabald Desert,UFO? Battu,80 : Koyo K Battu/Soigné/Mangé |
| 0x76   | 8    | `obel_quest` (Obel quest flags)                                                                                              |
| 0x7E   | 2    | `u6[2]` (Unknown)                                                                                                            |

#### Obel quest flag

[0] => avoir fredonné twice|???|Unused|Unused|n ricochets|infini ricochets|Vu ryo|Vu ryo² ("100x + de ricochets que toi !")
[1] => Ryo a donné tablette|Unused|Indices ombre pour trouver l'idiot|Unused|Unused|Unused|Indice ombre pour Eldbeak|Eldbeak trouvé
[2] => Trésor île Minde|Trésor Plaine de Mordor|Unused|Unused|Unused|Unused|Unused|Unused
[3] => ???|Pierre Balamb|Pierre Ryo|Pierre Timber|Pierre Galbadia|Toutes les pierres|Indice Ombre pour Balamb|???
[4] => ??? (mordor var?)
[5] => ???|???|???|???|Block access Lunatic Pandora|???|Block access Lunatic Pandora|???
[6] => avoir parlé à l'ombre|Accepter de chercher l'idiot|Avoir vu l'idiot|...
[7] => ??? (temp var)




### Triple Triad

| Offset | Size | Data                                              |
|--------|------|---------------------------------------------------|
| 0x00   | 77   | `cards[77]` (Array of 77 cards)                   |
| 0x4D   | 33   | `card_locations[33]` (Array of 33 card locations) |
| 0x6E   | 5    | `cards_rare[5]` (Array of 5 rare cards)           |
| 0x73   | 1    | `u1` (Padding or unknown)                         |
| 0x74   | 2    | `tt_victory_count` (TT victory count)             |
| 0x76   | 2    | `tt_defeat_count` (TT defeat count)               |
| 0x78   | 2    | `tt_egality_count` (TT egality count)             |
| 0x7A   | 2    | `u2` (Unknown)                                    |
| 0x7C   | 4    | `u3` (Unknown)                                    |

### Chocobo World

| Offset | Size               | Data                                                                                                           |
|--------|--------------------|----------------------------------------------------------------------------------------------------------------|
| 0x00   | 1 byte (bit field) | Enabled / In world / MiniMog found / Demon King defeated / Koko kidnapped / Hurry! / Koko met / Event Wait off |
| 0x01   | 1 byte             | Level                                                                                                          |
| 0x02   | 1 byte             | Current HP                                                                                                     |
| 0x03   | 1 byte             | Max HP                                                                                                         |
| 0x04   | 2 bytes            | Weapon (4 bit = 1 weapon)                                                                                      |
| 0x06   | 1 byte             | Rank                                                                                                           |
| 0x07   | 1 byte             | Move                                                                                                           |
| 0x08   | 4 bytes            | Save count                                                                                                     |
| 0x0C   | 2 bytes            | id related                                                                                                     |
| 0x0E   | 6 bytes            | Unknown                                                                                                        |
| 0x14   | 1 byte             | Item Class A count                                                                                             |
| 0x15   | 1 byte             | Item Class B count                                                                                             |
| 0x16   | 1 byte             | Item Class C count                                                                                             |
| 0x17   | 1 byte             | Item Class D count                                                                                             |
| 0x18   | 16 bytes           | Unknown                                                                                                        |
| 0x28   | 4 bytes            | Associated save ID                                                                                             |
| 0x2C   | 1 byte             | Unknown                                                                                                        |
| 0x2D   | 1 byte             | Boko Attack (star count: 0 = ChocoFire, 1 = ChocoFlare, 2 = ChocoMeteor, 3 = ChocoBocle)                       |
| 0x2E   | 1 byte             | Unknown                                                                                                        |
| 0x2F   | 1 byte             | Home walking                                                                                                   |
| 0x30   | 16 bytes           | Unknown (unused?)                                                                                              |


### Configuration

| Offset | Size | Data                                                                                  |
|--------|------|---------------------------------------------------------------------------------------|
| 0x00   | 1    | `vts_combat` (VTS combat setting)                                                     |
| 0x01   | 1    | `vts_msg_combat` (VTS message combat setting)                                         |
| 0x02   | 1    | `vts_msg` (VTS message setting)                                                       |
| 0x03   | 1    | `analog_volume` (Analog volume setting)                                               |
| 0x04   | 1    | `divers` (Miscellaneous settings) joystick,vibration,manette,???,???,pointeur,son,ATB |
| 0x05   | 1    | `scan` (Scan setting)                                                                 |
| 0x06   | 1    | `camera` (Camera setting)                                                             |
| 0x07   | 1    | MAP SEAL                                                                              |
| 0x08   | 1    | `L2` (L2 button mapping)                                                              |
| 0x09   | 1    | `R2` (R2 button mapping)                                                              |
| 0x0A   | 1    | `L1` (L1 button mapping)                                                              |
| 0x0B   | 1    | `R1` (R1 button mapping)                                                              |
| 0x0C   | 1    | `TRIANGLE` (Triangle button mapping)                                                  |
| 0x0D   | 1    | `ROND` (Circle button mapping)                                                        |
| 0x0E   | 1    | `CROIX` (Cross button mapping)                                                        |
| 0x0F   | 1    | `CARRE` (Square button mapping)                                                       |
| 0x10   | 1    | `SELECT` (Select button mapping)                                                      |
| 0x11   | 1    | `u4` (Unknown)                                                                        |
| 0x12   | 1    | `u5` (Unknown)                                                                        |
| 0x13   | 1    | `START` (Start button mapping)                                                        |


