---
layout: default
parent: Menu
title: Weapon upgrade (mwepon.bin)
permalink: /technical-reference/menu/mwepon/
---

### mwepon.bin

Junk Shop weapon-upgrade recipes - 12 bytes per weapon upgrade. The retail file holds 33
entries (396 bytes). Entry names are stored separately in `mwepon.msg`.

| Type   | Size | Value                              |
|--------|------|------------------------------------|
| UInt16 | 2    | Offset of the name inside mwepon.msg |
| UInt8  | 1    | Unused                             |
| UInt8  | 1    | Price                              |
| UInt8  | 1    | Item 1 id                          |
| UInt8  | 1    | Item 1 quantity                    |
| UInt8  | 1    | Item 2 id                          |
| UInt8  | 1    | Item 2 quantity                    |
| UInt8  | 1    | Item 3 id                          |
| UInt8  | 1    | Item 3 quantity                    |
| UInt8  | 1    | Item 4 id                          |
| UInt8  | 1    | Item 4 quantity                    |

Upgrade Price = Price \* 10

Buying an upgrade charges Price \* 10 gils and removes each Item quantity from the
inventory. An [Item]({{site.baseurl}}/technical-reference/list/item) id of 0 (Nothing) marks
an empty recipe slot and is ignored.

The 2-byte name offset and the 3rd byte (unused padding, always 0 in the retail file) do not
affect gameplay; an editor keeps them as-is so the recipe stays byte-perfect.

The game reads each field as a byte from `mweaponbinbuffer + 12 * weapon_id`. Affordability
uses `gil >= 10 * price`, and both the "can afford" scan and the purchase loop iterate the four
item/quantity pairs starting at byte 4.

| Function                            | Address    |
|-------------------------------------|------------|
| JunkShop_UpgradeMenuHandler         | 0x4EA890   |
| JunkShop_BuildAvailableUpgradeList  | 0x4EA770   |
