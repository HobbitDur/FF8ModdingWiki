---
layout: default
parent: Menu
title: magsort.bin file format
permalink: /technical-reference/menu/magsort/
author: hobbitdur
---

This file contains how each magic need to be ordered.
There is 7 entry, each entry containing 64 Ids corresponding to the [MagicID]({{site.baseurl}}/technical-reference/list/magic-list/#magic).
In practice, there is only 50 bytes used as there is only 50 magic that can appear in the menu. There is then 14 zeros.
An exception for the last one: there is only 63 bytes, not 64. But the game seems to work without it.
Here the 7 entries possible:

- Manual: All values are at 0 as there is no sorting
- Attack-Restore-Indirect
- Attack-Indirect-Restore
- Restore-Attack-Indirect
- Restore-Indirect-Attack
- Indirect-Attack-Restore
- Indirect-Restore-Attack

# Category legend

The category (Attack/Restore/Indirect) are defined only by the sorting, but here in vanilla the association done common in all preset:

| Category     | Spell IDs | Description                                                                                                                                                                                                                 |
|--------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Attack**   | 01-14     | Fire, Fira, Firaga, Blizzard, Blizzara, Blizzaga, Thunder, Thundara, Thundaga, Water, Aero, Bio, Demi, Holy, Flare, Meteor, Quake, Tornado, Ultima, Apocalypse                                                              |
| **Restore**  | 15-1B     | Cure, Cura, Curaga, Life, Full Life, Regen, Esuna                                                                                                                                                                           |
| **Indirect** | 1C-32     | Sleep, Silence, Break, Death, Drain, Pain, Berserk, Float, Zombie, Meltdown, Scan, Full-cure, Wall, Rapture, Percent, Catastrophe, Dispel, Protect, Shell, Reflect, Aura, Double, Triple, Haste, Slow, Stop, Blind, Confuse |

# Preset

Here all vanilla preset:

## Preset 0: "Manual" (No sort)

All zeros - keeps original inventory order (no reordering)

---

## Preset 1: "Attack-Restore-Indirect"

| Order | ID | Spell      |
|-------|----|------------|
| 1     | 01 | Fire       |
| 2     | 02 | Fira       |
| 3     | 03 | Firaga     |
| 4     | 04 | Blizzard   |
| 5     | 05 | Blizzara   |
| 6     | 06 | Blizzaga   |
| 7     | 07 | Thunder    |
| 8     | 08 | Thundara   |
| 9     | 09 | Thundaga   |
| 10    | 0A | Water      |
| 11    | 0B | Aero       |
| 12    | 0C | Bio        |
| 13    | 0D | Demi       |
| 14    | 11 | Holy       |
| 15    | 12 | Flare      |
| 16    | 0E | Meteor     |
| 17    | 0F | Quake      |
| 18    | 10 | Tornado    |
| 19    | 13 | Ultima     |
| 20    | 14 | Apocalypse |
| 21    | 15 | Cure       |
| 22    | 16 | Cura       |
| 23    | 17 | Curaga     |
| 24    | 18 | Life       |
| 25    | 19 | Full Life  |
| 26    | 1A | Regen      |
| 27    | 1B | Esuna      |
| 28    | 32 | Dispel     |
| 29    | 28 | Protect    |
| 30    | 26 | Shell      |
| 31    | 29 | Reflect    |
| 32    | 27 | Double     |
| 33    | 2E | Triple     |
| 34    | 2A | Haste      |
| 35    | 30 | Slow       |
| 36    | 2B | Stop       |
| 37    | 21 | Blind      |
| 38    | 22 | Confuse    |
| 39    | 1C | Sleep      |
| 40    | 1D | Silence    |
| 41    | 1E | Break      |
| 42    | 1F | Death      |
| 43    | 2F | Drain      |
| 44    | 2C | Pain       |
| 45    | 23 | Berserk    |
| 46    | 24 | Float      |
| 47    | 25 | Zombie     |
| 48    | 31 | Meltdown   |
| 49    | 2D | Scan       |
| 50    | 20 | Full-cure  |

---

## Preset 2: "Attack-Indirect-Restore"

| Order | ID | Spell      |
|-------|----|------------|
| 1     | 01 | Fire       |
| 2     | 02 | Fira       |
| 3     | 03 | Firaga     |
| 4     | 04 | Blizzard   |
| 5     | 05 | Blizzara   |
| 6     | 06 | Blizzaga   |
| 7     | 07 | Thunder    |
| 8     | 08 | Thundara   |
| 9     | 09 | Thundaga   |
| 10    | 0A | Water      |
| 11    | 0B | Aero       |
| 12    | 0C | Bio        |
| 13    | 0D | Demi       |
| 14    | 11 | Holy       |
| 15    | 12 | Flare      |
| 16    | 0E | Meteor     |
| 17    | 0F | Quake      |
| 18    | 10 | Tornado    |
| 19    | 13 | Ultima     |
| 20    | 14 | Apocalypse |
| 21    | 32 | Dispel     |
| 22    | 28 | Protect    |
| 23    | 26 | Shell      |
| 24    | 29 | Reflect    |
| 25    | 27 | Double     |
| 26    | 2E | Triple     |
| 27    | 2A | Haste      |
| 28    | 30 | Slow       |
| 29    | 2B | Stop       |
| 30    | 21 | Blind      |
| 31    | 22 | Confuse    |
| 32    | 1C | Sleep      |
| 33    | 1D | Silence    |
| 34    | 1E | Break      |
| 35    | 1F | Death      |
| 36    | 2F | Drain      |
| 37    | 2C | Pain       |
| 38    | 23 | Berserk    |
| 39    | 24 | Float      |
| 40    | 25 | Zombie     |
| 41    | 31 | Meltdown   |
| 42    | 2D | Scan       |
| 43    | 20 | Full-cure  |
| 44    | 15 | Cure       |
| 45    | 16 | Cura       |
| 46    | 17 | Curaga     |
| 47    | 18 | Life       |
| 48    | 19 | Full Life  |
| 49    | 1A | Regen      |
| 50    | 1B | Esuna      |

---

## Preset 3: "Restore-Attack-Indirect"

| Order | ID | Spell      |
|-------|----|------------|
| 1     | 15 | Cure       |
| 2     | 16 | Cura       |
| 3     | 17 | Curaga     |
| 4     | 18 | Life       |
| 5     | 19 | Full Life  |
| 6     | 1A | Regen      |
| 7     | 1B | Esuna      |
| 8     | 01 | Fire       |
| 9     | 02 | Fira       |
| 10    | 03 | Firaga     |
| 11    | 04 | Blizzard   |
| 12    | 05 | Blizzara   |
| 13    | 06 | Blizzaga   |
| 14    | 07 | Thunder    |
| 15    | 08 | Thundara   |
| 16    | 09 | Thundaga   |
| 17    | 0A | Water      |
| 18    | 0B | Aero       |
| 19    | 0C | Bio        |
| 20    | 0D | Demi       |
| 21    | 11 | Holy       |
| 22    | 12 | Flare      |
| 23    | 0E | Meteor     |
| 24    | 0F | Quake      |
| 25    | 10 | Tornado    |
| 26    | 13 | Ultima     |
| 27    | 14 | Apocalypse |
| 28    | 32 | Dispel     |
| 29    | 28 | Protect    |
| 30    | 26 | Shell      |
| 31    | 29 | Reflect    |
| 32    | 27 | Double     |
| 33    | 2E | Triple     |
| 34    | 2A | Haste      |
| 35    | 30 | Slow       |
| 36    | 2B | Stop       |
| 37    | 21 | Blind      |
| 38    | 22 | Confuse    |
| 39    | 1C | Sleep      |
| 40    | 1D | Silence    |
| 41    | 1E | Break      |
| 42    | 1F | Death      |
| 43    | 2F | Drain      |
| 44    | 2C | Pain       |
| 45    | 23 | Berserk    |
| 46    | 24 | Float      |
| 47    | 25 | Zombie     |
| 48    | 31 | Meltdown   |
| 49    | 2D | Scan       |
| 50    | 20 | Full-cure  |

---

## Preset 4: "Restore-Indirect-Attack"

| Order | ID | Spell      |
|-------|----|------------|
| 1     | 15 | Cure       |
| 2     | 16 | Cura       |
| 3     | 17 | Curaga     |
| 4     | 18 | Life       |
| 5     | 19 | Full Life  |
| 6     | 1A | Regen      |
| 7     | 1B | Esuna      |
| 8     | 32 | Dispel     |
| 9     | 28 | Protect    |
| 10    | 26 | Shell      |
| 11    | 29 | Reflect    |
| 12    | 27 | Double     |
| 13    | 2E | Triple     |
| 14    | 2A | Haste      |
| 15    | 30 | Slow       |
| 16    | 2B | Stop       |
| 17    | 21 | Blind      |
| 18    | 22 | Confuse    |
| 19    | 1C | Sleep      |
| 20    | 1D | Silence    |
| 21    | 1E | Break      |
| 22    | 1F | Death      |
| 23    | 2F | Drain      |
| 24    | 2C | Pain       |
| 25    | 23 | Berserk    |
| 26    | 24 | Float      |
| 27    | 25 | Zombie     |
| 28    | 31 | Meltdown   |
| 29    | 2D | Scan       |
| 30    | 20 | Full-cure  |
| 31    | 01 | Fire       |
| 32    | 02 | Fira       |
| 33    | 03 | Firaga     |
| 34    | 04 | Blizzard   |
| 35    | 05 | Blizzara   |
| 36    | 06 | Blizzaga   |
| 37    | 07 | Thunder    |
| 38    | 08 | Thundara   |
| 39    | 09 | Thundaga   |
| 40    | 0A | Water      |
| 41    | 0B | Aero       |
| 42    | 0C | Bio        |
| 43    | 0D | Demi       |
| 44    | 11 | Holy       |
| 45    | 12 | Flare      |
| 46    | 0E | Meteor     |
| 47    | 0F | Quake      |
| 48    | 10 | Tornado    |
| 49    | 13 | Ultima     |
| 50    | 14 | Apocalypse |

---

## Preset 5: "Indirect-Attack-Restore"

| Order | ID | Spell      |
|-------|----|------------|
| 1     | 32 | Dispel     |
| 2     | 28 | Protect    |
| 3     | 26 | Shell      |
| 4     | 29 | Reflect    |
| 5     | 27 | Double     |
| 6     | 2E | Triple     |
| 7     | 2A | Haste      |
| 8     | 30 | Slow       |
| 9     | 2B | Stop       |
| 10    | 21 | Blind      |
| 11    | 22 | Confuse    |
| 12    | 1C | Sleep      |
| 13    | 1D | Silence    |
| 14    | 1E | Break      |
| 15    | 1F | Death      |
| 16    | 2F | Drain      |
| 17    | 2C | Pain       |
| 18    | 23 | Berserk    |
| 19    | 24 | Float      |
| 20    | 25 | Zombie     |
| 21    | 31 | Meltdown   |
| 22    | 2D | Scan       |
| 23    | 20 | Full-cure  |
| 24    | 01 | Fire       |
| 25    | 02 | Fira       |
| 26    | 03 | Firaga     |
| 27    | 04 | Blizzard   |
| 28    | 05 | Blizzara   |
| 29    | 06 | Blizzaga   |
| 30    | 07 | Thunder    |
| 31    | 08 | Thundara   |
| 32    | 09 | Thundaga   |
| 33    | 0A | Water      |
| 34    | 0B | Aero       |
| 35    | 0C | Bio        |
| 36    | 0D | Demi       |
| 37    | 11 | Holy       |
| 38    | 12 | Flare      |
| 39    | 0E | Meteor     |
| 40    | 0F | Quake      |
| 41    | 10 | Tornado    |
| 42    | 13 | Ultima     |
| 43    | 14 | Apocalypse |
| 44    | 15 | Cure       |
| 45    | 16 | Cura       |
| 46    | 17 | Curaga     |
| 47    | 18 | Life       |
| 48    | 19 | Full Life  |
| 49    | 1A | Regen      |
| 50    | 1B | Esuna      |

---

## Preset 6: "Indirect-Restore-Attack" (Incomplete - likely unused)

| Order | ID | Spell      |
|-------|----|------------|
| 1     | 32 | Dispel     |
| 2     | 28 | Protect    |
| 3     | 26 | Shell      |
| 4     | 29 | Reflect    |
| 5     | 27 | Double     |
| 6     | 2E | Triple     |
| 7     | 2A | Haste      |
| 8     | 30 | Slow       |
| 9     | 2B | Stop       |
| 10    | 21 | Blind      |
| 11    | 22 | Confuse    |
| 12    | 1C | Sleep      |
| 13    | 1D | Silence    |
| 14    | 1E | Break      |
| 15    | 1F | Death      |
| 16    | 2F | Drain      |
| 17    | 2C | Pain       |
| 18    | 23 | Berserk    |
| 19    | 24 | Float      |
| 20    | 25 | Zombie     |
| 21    | 31 | Meltdown   |
| 22    | 2D | Scan       |
| 23    | 20 | Full-cure  |
| 24    | 15 | Cure       |
| 25    | 16 | Cura       |
| 26    | 17 | Curaga     |
| 27    | 18 | Life       |
| 28    | 19 | Full Life  |
| 29    | 1A | Regen      |
| 30    | 1B | Esuna      |
| 31    | 01 | Fire       |
| 32    | 02 | Fira       |
| 33    | 03 | Firaga     |
| 34    | 04 | Blizzard   |
| 35    | 05 | Blizzara   |
| 36    | 06 | Blizzaga   |
| 37    | 07 | Thunder    |
| 38    | 08 | Thundara   |
| 39    | 09 | Thundaga   |
| 40    | 0A | Water      |
| 41    | 0B | Aero       |
| 42    | 0C | Bio        |
| 43    | 0D | Demi       |
| 44    | 11 | Holy       |
| 45    | 12 | Flare      |
| 46    | 0E | Meteor     |
| 47    | 0F | Quake      |
| 48    | 10 | Tornado    |
| 49    | 13 | Ultima     |
| 50    | 14 | Apocalypse |****
