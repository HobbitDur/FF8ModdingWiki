---
layout: default
title: Tomb of the Unknown King
parent: Field
permalink: /technical-reference/field/tomb-of-the-unknown-king/
author: HobbitDur
---

1. TOC
{:toc}

# Tomb of the Unknown King

The tomb is ten fields, `gnroad1` to `gnview1`. Its maze is not built from one field per corridor: five corridor backgrounds are reused for every place in the maze, and one variable, **var486**, says where the party is and which way the camera looks. Each exit script reads var486, writes the next value and jumps to the field that draws it. Progress through the tomb is kept in **var491**, the two one-time scenes in **var485**.

## Fields
| Field ID | Field   | Role                                                           | var486                           |
| -------- | ------- | -------------------------------------------------------------- | -------------------------------- |
| 783      | gnroad1 | Straight corridor ending in a wall, a room door or the way out | 0, 6, 30, 40, 62, 73, 74, 75     |
| 784      | gnroad2 | Crossroad with four exits                                      | 48 values (12 places, 4 facings) |
| 785      | gnroad3 | Bend that turns right                                          | 7, 15, 22, 27, 41, 46, 55, 63    |
| 786      | gnroad4 | Bend that turns left                                           | 5, 14, 21, 29, 39, 49, 54, 65    |
| 787      | gnroad5 | Approach to the central building, with the bridge              | 16, 32, 38, 52, 76               |
| 788      | gnroom1 | Room 1: Sacred                                                 | sets 73                          |
| 789      | gnroom2 | Room 2: water lever                                            | sets 74                          |
| 790      | gnroom3 | Room 3: gearwheel                                              | sets 75                          |
| 791      | gnroom4 | Room 4: Sacred and Minotaur, the sealed arc                    | sets 76                          |
| 792      | gnview1 | Outside the tomb: students, save point, world map exit         | sets 0                           |

Field IDs are lines of `maplist` (see [Map jumps]({{ site.baseurl }}/technical-reference/field/field-opcodes/029-mapjump/)).

## How var486 drives the maze

Every corridor field has up to four line entities, `mapjump_FW`, `mapjump_LW`, `mapjump_RW` and `mapjump_BW` (forward, left, right, back as seen on screen). Their `touchOn` script is one long chain:

| Step | Instructions                                      |
| ---- | ------------------------------------------------- |
| 1    | `PSHM_B 486`, `PSHN_L N`, `CAL EQ`, `JPF next`     |
| 2    | `PSHN_L M`, `POPM_B 486`                          |
| 3    | push field, X, Y, Z, `MAPJUMP3` (facing, triangle) |
| 4    | `JMP end`, then the next value of N               |

`gnroad3` and `gnroad4` write the new value in each branch and share one `MAPJUMP3` at the end. The next field reads var486 again in its `Director` and object scripts to pick what it shows: the stone slab in `gnroad1`, the bridge and building views in `gnroad5`, the sword in `gnroad2`.

The camera always turns to face the way the party walked. Walking back out of a crossroad loads the next corridor looking the other way, so each place needs one var486 value per facing it can be seen from: four at a crossroad, one per field at a bend (`gnroad3` from one side, `gnroad4` from the other), two in a dead-end corridor.

The rooms and the outside set var486 themselves when they load (`Director` script): `gnview1` 0, `gnroom1` to `gnroom4` 73 to 76. Their exits are .inf gateways, not scripts: rooms 1 to 3 and `gnview1` lead to `gnroad1`, room 4 to `gnroad5`. From 73, 74 and 75, forward leads back into the maze and back re-enters the room. From 76, back leads to 72, the crossroad north of the centre, facing north, whichever side the party came from.

## Map positions

The dungeon map is a background layer of every corridor field (shown by the `map` entity). The "you are here" mark is a single animated tile of the `mark` entity; each `mark::onN` script moves it by `(dx, dy)` pixels with a background-move opcode, and `mapdisplay::default` picks the script from var486. Those offsets give the real place of every value. North is the top of the map; the entrance is at the top.

![Tomb map with the mark numbers]({{site.baseurl}}/assets/tomb_maze_map.png)

Green: crossroads (`gnroad2`). Blue: bends (`gnroad3`/`gnroad4`). Orange: dead-end corridors (`gnroad1`). Red: approaches to the centre (`gnroad5`). Violet: rooms.

| Mark | Offset   | Kind                   | Field   | Facing N | Facing E | Facing S | Facing W |
| ---- | -------- | ---------------------- | ------- | -------- | -------- | -------- | -------- |
| 1    | -3, -41  | Dead-end corridor      | gnroad1 | 6        |          | 0        |          |
| 4    | -19, -31 | Bend (turns left)      | gnroad4 |          | 22       | 5        |          |
| 3    | -3, -31  | Junction               | gnroad2 | 18       | 9        | 1        | 3        |
| 2    | 16, -31  | Bend (turns right)     | gnroad3 |          |          | 7        | 14       |
| 9    | -34, -15 | Bend (turns left)      | gnroad4 |          | 41       | 21       |          |
| 8    | -19, -15 | Junction               | gnroad2 | 37       | 25       | 8        | 17       |
| 7    | -4, -15  | Junction               | gnroad2 | 72       | 23       | 4        | 13       |
| 6    | 16, -15  | Junction               | gnroad2 | 33       | 19       | 2        | 11       |
| 5    | 31, -15  | Bend (turns right)     | gnroad3 |          |          | 15       | 29       |
| 28   | -2, -8   | Approach to the centre | gnroad5 |          |          | 16, 76   |          |
| 15   | -41, 1   | Dead-end corridor      | gnroad1 |          | 73       |          | 40       |
| 14   | -34, 1   | Junction               | gnroad2 | 58       | 43       | 24       | 36       |
| 13   | -19, 1   | Junction               | gnroad2 | 56       | 42       | 20       | 71       |
| 27   | -14, 1   | Approach to the centre | gnroad5 |          | 38       |          |          |
| 25   | 9, 1     | Approach to the centre | gnroad5 |          |          |          | 32       |
| 12   | 16, 1    | Junction               | gnroad2 | 48       | 69       | 12       | 28       |
| 11   | 31, 1    | Junction               | gnroad2 | 45       | 34       | 10       | 26       |
| 10   | 38, 1    | Dead-end corridor      | gnroad1 |          | 30       |          | 75       |
| 26   | -2, 11   | Approach to the centre | gnroad5 | 52       |          |          |          |
| 20   | -34, 20  | Bend (turns left)      | gnroad4 | 55       | 39       |          |          |
| 19   | -19, 20  | Junction               | gnroad2 | 66       | 59       | 35       | 51       |
| 18   | -4, 20   | Junction               | gnroad2 | 64       | 57       | 70       | 47       |
| 17   | 16, 20   | Junction               | gnroad2 | 61       | 53       | 31       | 44       |
| 16   | 31, 20   | Bend (turns right)     | gnroad3 | 49       |          |          | 27       |
| 23   | -19, 36  | Bend (turns left)      | gnroad4 | 63       | 54       |          |          |
| 22   | -3, 37   | Junction               | gnroad2 | 68       | 67       | 50       | 60       |
| 21   | 16, 37   | Bend (turns right)     | gnroad3 | 65       |          |          | 46       |
| 24   | -4, 46   | Dead-end corridor      | gnroad1 | 74       |          | 62       |          |

The rooms have their own marks, used by their `mapdisplay` scripts:

| Mark | Offset | Place                 | Field   | var486     |
| ---- | ------ | --------------------- | ------- | ---------- |
| 29   | -50, 1 | Room 1 (Sacred)       | gnroom1 | 73 on load |
| 30   | -4, 56 | Room 2 (water lever)  | gnroom2 | 74 on load |
| 31   | 48, -1 | Room 3 (gearwheel)    | gnroom3 | 75 on load |
| 32   | -2, 1  | Room 4 (the Brothers) | gnroom4 | 76 on load |

## Every value of var486

Facing is the camera direction. Each exit gives the value written and the field loaded.

| var486 | Field   | Mark | Facing | Forward                    | Left         | Right        | Back         |
| ------ | ------- | ---- | ------ | -------------------------- | ------------ | ------------ | ------------ |
| 0      | gnroad1 | 1    | south  | 1 (gnroad2)                |              |              | gnview1      |
| 1      | gnroad2 | 3    | south  | 4 (gnroad2)                | 7 (gnroad3)  | 5 (gnroad4)  | 6 (gnroad1)  |
| 2      | gnroad2 | 6    | south  | 12 (gnroad2)               | 15 (gnroad3) | 13 (gnroad2) | 14 (gnroad4) |
| 3      | gnroad2 | 3    | west   | 5 (gnroad4)                | 4 (gnroad2)  | 6 (gnroad1)  | 7 (gnroad3)  |
| 4      | gnroad2 | 7    | south  | 16 (gnroad5)               | 19 (gnroad2) | 17 (gnroad2) | 18 (gnroad2) |
| 5      | gnroad4 | 4    | south  | 8 (gnroad2)                |              |              | 9 (gnroad2)  |
| 6      | gnroad1 | 1    | north  | gnview1                    |              |              | 1 (gnroad2)  |
| 7      | gnroad3 | 2    | south  | 2 (gnroad2)                |              |              | 3 (gnroad2)  |
| 8      | gnroad2 | 8    | south  | 20 (gnroad2)               | 23 (gnroad2) | 21 (gnroad4) | 22 (gnroad3) |
| 9      | gnroad2 | 3    | east   | 7 (gnroad3)                | 6 (gnroad1)  | 4 (gnroad2)  | 5 (gnroad4)  |
| 10     | gnroad2 | 11   | south  | 27 (gnroad3)               | 30 (gnroad1) | 28 (gnroad2) | 29 (gnroad4) |
| 11     | gnroad2 | 6    | west   | 13 (gnroad2)               | 12 (gnroad2) | 14 (gnroad4) | 15 (gnroad3) |
| 12     | gnroad2 | 12   | south  | 31 (gnroad2)               | 34 (gnroad2) | 32 (gnroad5) | 33 (gnroad2) |
| 13     | gnroad2 | 7    | west   | 17 (gnroad2)               | 16 (gnroad5) | 18 (gnroad2) | 19 (gnroad2) |
| 14     | gnroad4 | 2    | west   | 3 (gnroad2)                |              |              | 2 (gnroad2)  |
| 15     | gnroad3 | 5    | south  | 10 (gnroad2)               |              |              | 11 (gnroad2) |
| 16     | gnroad5 | 28   | south  | gnroom4 if bridge down     |              |              | 72 (gnroad2) |
| 17     | gnroad2 | 8    | west   | 21 (gnroad4)               | 20 (gnroad2) | 22 (gnroad3) | 23 (gnroad2) |
| 18     | gnroad2 | 3    | north  | 6 (gnroad1)                | 5 (gnroad4)  | 7 (gnroad3)  | 4 (gnroad2)  |
| 19     | gnroad2 | 6    | east   | 15 (gnroad3)               | 14 (gnroad4) | 12 (gnroad2) | 13 (gnroad2) |
| 20     | gnroad2 | 13   | south  | 35 (gnroad2)               | 38 (gnroad5) | 36 (gnroad2) | 37 (gnroad2) |
| 21     | gnroad4 | 9    | south  | 24 (gnroad2)               |              |              | 25 (gnroad2) |
| 22     | gnroad3 | 4    | east   | 9 (gnroad2)                |              |              | 8 (gnroad2)  |
| 23     | gnroad2 | 7    | east   | 19 (gnroad2)               | 18 (gnroad2) | 16 (gnroad5) | 17 (gnroad2) |
| 24     | gnroad2 | 14   | south  | 39 (gnroad4)               | 42 (gnroad2) | 40 (gnroad1) | 41 (gnroad3) |
| 25     | gnroad2 | 8    | east   | 23 (gnroad2)               | 22 (gnroad3) | 20 (gnroad2) | 21 (gnroad4) |
| 26     | gnroad2 | 11   | west   | 28 (gnroad2)               | 27 (gnroad3) | 29 (gnroad4) | 30 (gnroad1) |
| 27     | gnroad3 | 16   | west   | 44 (gnroad2)               |              |              | 45 (gnroad2) |
| 28     | gnroad2 | 12   | west   | 32 (gnroad5)               | 31 (gnroad2) | 33 (gnroad2) | 34 (gnroad2) |
| 29     | gnroad4 | 5    | west   | 11 (gnroad2)               |              |              | 10 (gnroad2) |
| 30     | gnroad1 | 10   | east   | gnroom3 once slab sunk     |              |              | 26 (gnroad2) |
| 31     | gnroad2 | 17   | south  | 46 (gnroad3)               | 49 (gnroad4) | 47 (gnroad2) | 48 (gnroad2) |
| 32     | gnroad5 | 25   | west   | gnroom4 (never: no bridge) |              |              | 69 (gnroad2) |
| 33     | gnroad2 | 6    | north  | 14 (gnroad4)               | 13 (gnroad2) | 15 (gnroad3) | 12 (gnroad2) |
| 34     | gnroad2 | 11   | east   | 30 (gnroad1)               | 29 (gnroad4) | 27 (gnroad3) | 28 (gnroad2) |
| 35     | gnroad2 | 19   | south  | 54 (gnroad4)               | 57 (gnroad2) | 55 (gnroad3) | 56 (gnroad2) |
| 36     | gnroad2 | 14   | west   | 40 (gnroad1)               | 39 (gnroad4) | 41 (gnroad3) | 42 (gnroad2) |
| 37     | gnroad2 | 8    | north  | 22 (gnroad3)               | 21 (gnroad4) | 23 (gnroad2) | 20 (gnroad2) |
| 38     | gnroad5 | 27   | east   | gnroom4 (never: no bridge) |              |              | 71 (gnroad2) |
| 39     | gnroad4 | 20   | east   | 59 (gnroad2)               |              |              | 58 (gnroad2) |
| 40     | gnroad1 | 15   | west   | gnroom1                    |              |              | 43 (gnroad2) |
| 41     | gnroad3 | 9    | east   | 25 (gnroad2)               |              |              | 24 (gnroad2) |
| 42     | gnroad2 | 13   | east   | 38 (gnroad5)               | 37 (gnroad2) | 35 (gnroad2) | 36 (gnroad2) |
| 43     | gnroad2 | 14   | east   | 42 (gnroad2)               | 41 (gnroad3) | 39 (gnroad4) | 40 (gnroad1) |
| 44     | gnroad2 | 17   | west   | 47 (gnroad2)               | 46 (gnroad3) | 48 (gnroad2) | 49 (gnroad4) |
| 45     | gnroad2 | 11   | north  | 29 (gnroad4)               | 28 (gnroad2) | 30 (gnroad1) | 27 (gnroad3) |
| 46     | gnroad3 | 21   | west   | 60 (gnroad2)               |              |              | 61 (gnroad2) |
| 47     | gnroad2 | 18   | west   | 51 (gnroad2)               | 50 (gnroad2) | 52 (gnroad5) | 53 (gnroad2) |
| 48     | gnroad2 | 12   | north  | 33 (gnroad2)               | 32 (gnroad5) | 34 (gnroad2) | 31 (gnroad2) |
| 49     | gnroad4 | 16   | north  | 45 (gnroad2)               |              |              | 44 (gnroad2) |
| 50     | gnroad2 | 22   | south  | 62 (gnroad1)               | 65 (gnroad4) | 63 (gnroad3) | 64 (gnroad2) |
| 51     | gnroad2 | 19   | west   | 55 (gnroad3)               | 54 (gnroad4) | 56 (gnroad2) | 57 (gnroad2) |
| 52     | gnroad5 | 26   | north  | gnroom4 (never: no bridge) |              |              | 70 (gnroad2) |
| 53     | gnroad2 | 17   | east   | 49 (gnroad4)               | 48 (gnroad2) | 46 (gnroad3) | 47 (gnroad2) |
| 54     | gnroad4 | 23   | east   | 67 (gnroad2)               |              |              | 66 (gnroad2) |
| 55     | gnroad3 | 20   | north  | 58 (gnroad2)               |              |              | 59 (gnroad2) |
| 56     | gnroad2 | 13   | north  | 37 (gnroad2)               | 36 (gnroad2) | 38 (gnroad5) | 35 (gnroad2) |
| 57     | gnroad2 | 18   | east   | 53 (gnroad2)               | 52 (gnroad5) | 50 (gnroad2) | 51 (gnroad2) |
| 58     | gnroad2 | 14   | north  | 41 (gnroad3)               | 40 (gnroad1) | 42 (gnroad2) | 39 (gnroad4) |
| 59     | gnroad2 | 19   | east   | 57 (gnroad2)               | 56 (gnroad2) | 54 (gnroad4) | 55 (gnroad3) |
| 60     | gnroad2 | 22   | west   | 63 (gnroad3)               | 62 (gnroad1) | 64 (gnroad2) | 65 (gnroad4) |
| 61     | gnroad2 | 17   | north  | 48 (gnroad2)               | 47 (gnroad2) | 49 (gnroad4) | 46 (gnroad3) |
| 62     | gnroad1 | 24   | south  | gnroom2 once slab sunk     |              |              | 68 (gnroad2) |
| 63     | gnroad3 | 23   | north  | 66 (gnroad2)               |              |              | 67 (gnroad2) |
| 64     | gnroad2 | 18   | north  | 52 (gnroad5)               | 51 (gnroad2) | 53 (gnroad2) | 50 (gnroad2) |
| 65     | gnroad4 | 21   | north  | 61 (gnroad2)               |              |              | 60 (gnroad2) |
| 66     | gnroad2 | 19   | north  | 56 (gnroad2)               | 55 (gnroad3) | 57 (gnroad2) | 54 (gnroad4) |
| 67     | gnroad2 | 22   | east   | 65 (gnroad4)               | 64 (gnroad2) | 62 (gnroad1) | 63 (gnroad3) |
| 68     | gnroad2 | 22   | north  | 64 (gnroad2)               | 63 (gnroad3) | 65 (gnroad4) | 62 (gnroad1) |
| 69     | gnroad2 | 12   | east   | 34 (gnroad2)               | 33 (gnroad2) | 31 (gnroad2) | 32 (gnroad5) |
| 70     | gnroad2 | 18   | south  | 50 (gnroad2)               | 53 (gnroad2) | 51 (gnroad2) | 52 (gnroad5) |
| 71     | gnroad2 | 13   | west   | 36 (gnroad2)               | 35 (gnroad2) | 37 (gnroad2) | 38 (gnroad5) |
| 72     | gnroad2 | 7    | north  | 18 (gnroad2)               | 17 (gnroad2) | 19 (gnroad2) | 16 (gnroad5) |
| 73     | gnroad1 | 15   | east   | 43 (gnroad2)               |              |              | gnroom1      |
| 74     | gnroad1 | 24   | north  | 68 (gnroad2)               |              |              | gnroom2      |
| 75     | gnroad1 | 10   | west   | 26 (gnroad2)               |              |              | gnroom3      |
| 76     | gnroad5 | 28   | south  | gnroom4                    |              |              | 72 (gnroad2) |

`gnroad1`'s `mapjump_BW` also holds a copy of `gnroad5`'s table (16, 32, 38, 52). `gnroad1` never runs with those values.

## Progress gates

| Step | Field and script                | What happens                                                                                                                                                                                                                                      |
| ---- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | `gnview1` `G_student2::default` | First visit: two Garden students run past ("F-Float!"), var485 \|= 0xD5 (bits 1, 4, 16, 64, 128). The students exist only while `var485 & 469` is 0.                                                                                              |
| 2    | `gnroom1` `battleline::touchOn` | The statue speaks, `BATTLE` 189 (Sacred), then var491 \|= 2.                                                                                                                                                                                      |
| 3    | `gnroad1` `Director`, `seigyo`  | With var491 & 2 clear, states 30 and 62 show an inscribed stone slab and lock walkmesh triangles 79, 82 and 85: rooms 2 and 3 are closed. Once set, the slab is sunk.                                                                             |
| 4    | `gnroom2` `WaterRun::talk`      | A party member pulls the lever: var491 \|= 4. Water flows, and ripples show in `gnroad5`.                                                                                                                                                         |
| 5    | `gnroom3` `gearwheel::talk`     | var491 \|= 8.                                                                                                                                                                                                                                     |
| 6    | `gnroad5` `Director`, `hasi`    | Triangles 37 and 39 (the bridge) are locked on load. They unlock only with var491 & 4 and & 8, and only if var486 is 16 (north approach) or var84 is 791 (back from room 4). The bridge picture: raised, half down with only & 8, down with both. |
| 7    | `gnroom4` `battleline::touchOn` | `BATTLE` 190 (Sacred and Minotaur), var491 \|= 16, var485 \|= 2 (brothers gone, triangles 99, 112, 115, 131 unlocked), `MENUNAME` 7 (Brothers), `GETCARD` 87 (Minotaur).                                                                          |
| 8    | `gnroom4` `ArcTop::open`        | The sealed one speaks: var491 \|= 32. No script reads bits 16 and 32.                                                                                                                                                                             |

From the east, south and west approaches (32, 52, 38) the building shows its side or back and the bridge never comes down.

## Variables

| Var        | Size | Use in the tomb                                                                                                                   |
| ---------- | ---- | --------------------------------------------------------------------------------------------------------------------------------- |
| 486        | byte | Place and camera facing, 0 to 76 (tables above).                                                                                  |
| 491        | byte | Progress: +2 Sacred driven off, +4 water channel open, +8 gearwheel turned, +16 Sacred and Minotaur beaten, +32 sealed one freed. |
| 485        | byte | +1, +4, +16, +64, +128 students scene played (set together); +2 brothers gone from room 4.                                        |
| 730        | byte | +32 has the tomb map: the map key works and offers Escape. +64 has the location displayer: the map shows the mark.                |
| 84         | word | Last field. Arrival placement and sounds: 787 in `gnroad2`, 788 to 790 in `gnroad1`, 791 in `gnroad5` (also unlocks the bridge).  |
| 88         | byte | Move-Find. The save points of rooms 1 and 3 show only with it (room 1 also needs var491 & 2).                                     |
| 261        | byte | Save point state, as everywhere.                                                                                                  |
| 728        | byte | Student ID number on the sword (`MESVAR`), shown in `gnroad2` at mark 3 in states 1 and 18.                                       |
| 1024, 1025 | byte | Temporary: statue volume ramp in `gnroom1`, Move-Find copies for the save points.                                                 |

## Map key and escape

Every field except `gnview1` runs `mapdisplay::default` in a loop. With var730 & 32 it waits for the map key (`KEYSCAN` 256), shows the `map` layer and, with var730 & 64, the mark for the current var486. A second key opens "Escape from the dungeon?": yes runs `ADDSEEDLEVEL` -100 (one SeeD rank) and `MAPJUMP3` to `gnview1`.

## Inscriptions

The slab in front of rooms 3 and 2 (states 30 and 62) holds a dead student's directions, read by `Squall::read`:

| State | Text                                                                  | Result when each word is one exit                                          |
| ----- | --------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| 30    | Back, forward, right, left, right, forward.                           | 30, 26, 28, 33, 13, 18, 6: the entrance corridor facing out.               |
| 62    | Back, forward, left twice, forward twice, right twice, forward twice. | 62, 68, 64, 51, 54, 67, 65: stops at a bend, where there is no right exit. |

## Draw points

| Field     | Draw point | Magic   |
| --------- | ---------- | ------- |
| `gnview1` | 38         | Protect |
| `gnroom2` | 39         | Float   |
| `gnroom3` | 40         | Cura    |

See [Draw points]({{ site.baseurl }}/technical-reference/exedata/draw-point/) for the table.

## Script reference

| Field         | Script                                         | Role                             |
| ------------- | ---------------------------------------------- | -------------------------------- |
| all corridors | `mapjump_FW/LW/RW/BW::touchOn`                 | Exit tables on var486            |
| all corridors | `mapdisplay::default`                          | Map key, mark, escape            |
| all corridors | `mark::on1` to `mark::on32`                    | Mark offsets                     |
| `gnroad1`     | `seigyo::up/down/no`, `stone`                  | Slab raised, sunk, hidden        |
| `gnroad1`     | `talkline`, `Squall::read`                     | Reading the slab                 |
| `gnroad2`     | `sword::talk`                                  | Student ID (var728)              |
| `gnroad5`     | `hasi`, `tatemono`, `hamon`                    | Bridge, building view, ripples   |
| `gnroom1`     | `battleline::touchOn`, `YoungerSeclet::appear` | Statue and battle 189            |
| `gnroom2`     | `WaterRun::talk`, `seigyo::start`              | Lever and water                  |
| `gnroom3`     | `gearwheel::talk`                              | Gearwheel                        |
| `gnroom4`     | `battleline::touchOn`, `ArcTop::open`          | Battle 190, Brothers, sealed one |
| `gnview1`     | `G_student2::default`, `worldmap::touchOn`     | Students scene, world map exit   |
