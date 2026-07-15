---
layout: default
parent: Menu
title: Shop (shop.bin)
permalink: /technical-reference/menu/shop-shopbin/
---

# Shop.bin doc

The file shop.bin is composed of 20 shops, each shop having 16 items. Each item as 2 values: The item itself, and the rarity. When "rare" is checked, the item will be shown in shop
only if the player as the ability "[Familiar](https://finalfantasy.fandom.com/wiki/Familiar_(Final_Fantasy_VIII))" of tonberry.
The shop list is sorted, meaning that there is no offset, and the X<sub>eme</sub> shop is hardlink to a specific shop.

## How the field opens a shop (shop ID remap)

A field script opens a shop with the **`MENUSHOP`** opcode (handler `SCRIPT_MENUSHOP`), which pops one byte — the **shop ID** — off the script stack and requests hosted menu 23 (Shop). The shop program (`Menu_Prog11_ShopMenu_Init`) does **not** use that ID directly: it passes it through a remap table, **`SHOP_ID_REMAP_TABLE`** (52 bytes), before selecting the shop:

| Field shop ID | Remapped value | Result |
|---------------|----------------|--------|
| 0 – 20 | 0 – 20 (identity) | Item shop — shop.bin record N |
| 21 – 31 | 0 | Falls back to item shop 0 (effectively invalid) |
| **32 – 42** | **21** | **Junk Shop** (weapon remodel) |
| 43 – 51 | 0 | Falls back to item shop 0 |

The value **21 is a reserved sentinel**, not a real item shop: when `SHOP_ID_REMAP_TABLE[id] == 21` the program branches to the Junk Shop (`Menu_Prog12_JunkShop_Init`, weapon-upgrade menu built from mwepon.bin), never touching shop.bin. This is why **shop ID 32 appears to have "no shop"** — it is not an item shop at all, it is the first of the 11 junk-shop IDs (32–42). All eleven behave identically: the junk-shop code ignores which ID was used, so 32–42 all open the same weapon-remodel menu.

Consequently shop.bin only needs records **0–20** (the 21 item shops); IDs in 21–31 and 43+ are unused and fall back to shop 0.

## Reference

- [Items description](#items-description)
- [Shop description](#shop-description)
- [Shop.bin description](#shopbin-description)
- [Items list](#items)
- [Shop name list](#shop-name)

## Items description

[Top of page](#shopbin-doc)

| Data size | Description                                         |
|-----------|-----------------------------------------------------|
| 1 byte    | [Item ID](#items)                                   |
| 1 byte    | Rarity _<br/><br/> 0x00 - Rare <br/> 0xFF - Common_ |

## Shop description

[Top of page](#shopbin-doc)

| Data size | Description                                  |
|-----------|----------------------------------------------|
| 2 bytes   | [Items Description](#items-description) n°1  |
| 2 bytes   | [Items Description](#items-description) n°2  |
| 2 bytes   | [Items Description](#items-description) n°3  |
| 2 bytes   | [Items Description](#items-description) n°4  |
| 2 bytes   | [Items Description](#items-description) n°5  |
| 2 bytes   | [Items Description](#items-description) n°6  |
| 2 bytes   | [Items Description](#items-description) n°7  |
| 2 bytes   | [Items Description](#items-description) n°8  |
| 2 bytes   | [Items Description](#items-description) n°9  |
| 2 bytes   | [Items Description](#items-description) n°10 |
| 2 bytes   | [Items Description](#items-description) n°11 |
| 2 bytes   | [Items Description](#items-description) n°12 |
| 2 bytes   | [Items Description](#items-description) n°13 |
| 2 bytes   | [Items Description](#items-description) n°14 |
| 2 bytes   | [Items Description](#items-description) n°15 |
| 2 bytes   | [Items Description](#items-description) n°16 |

## Shop.bin description

[Top of page](#shopbin-doc)

| Data size | Description                                |
|-----------|--------------------------------------------|
| 32 bytes  | [Shop Description](#shop-description) n°1  |
| 32 bytes  | [Shop Description](#shop-description) n°2  |
| 32 bytes  | [Shop Description](#shop-description) n°3  |
| 32 bytes  | [Shop Description](#shop-description) n°4  |
| 32 bytes  | [Shop Description](#shop-description) n°5  |
| 32 bytes  | [Shop Description](#shop-description) n°6  |
| 32 bytes  | [Shop Description](#shop-description) n°7  |
| 32 bytes  | [Shop Description](#shop-description) n°8  |
| 32 bytes  | [Shop Description](#shop-description) n°9  |
| 32 bytes  | [Shop Description](#shop-description) n°10 |
| 32 bytes  | [Shop Description](#shop-description) n°11 |
| 32 bytes  | [Shop Description](#shop-description) n°12 |
| 32 bytes  | [Shop Description](#shop-description) n°13 |
| 32 bytes  | [Shop Description](#shop-description) n°14 |
| 32 bytes  | [Shop Description](#shop-description) n°15 |
| 32 bytes  | [Shop Description](#shop-description) n°16 |
| 32 bytes  | [Shop Description](#shop-description) n°17 |
| 32 bytes  | [Shop Description](#shop-description) n°18 |
| 32 bytes  | [Shop Description](#shop-description) n°19 |
| 32 bytes  | [Shop Description](#shop-description) n°20 |

## Items

[Item list](({{site.baseurl}}/technical-reference/list/item))

## Shop name

[Top of page](#shopbin-doc)

| Shop ID | Name                                        |
|---------|---------------------------------------------|
| 0x00    | Timber Pet Shop                             |
| 0x01    | Balamb Shop                                 |
| 0x02    | Dollet Shop                                 |
| 0x03    | Timber Shop                                 |
| 0x04    | Deling City Shop                            |
| 0x05    | Winhill Shop                                |
| 0x06    | FH Shop                                     |
| 0x07    | Trabia Shop - UNUSED!                       |
| 0x08    | Esthar Shop (Cloud's Shop)                  |
| 0x09    | Balamb Shop (Laguna's World) - UNUSED!      |
| 0x0A    | Dollet Shop (Laguna's World) - UNUSED!      |
| 0x0B    | Timber Shop (Laguna's World) - UNUSED!      |
| 0x0C    | Deling City Shop (Laguna's World) - UNUSED! |
| 0x0D    | Winhill Shop (Laguna's World)               |
| 0x0E    | FH Shop (Laguna's World) - UNUSED!          |
| 0x0F    | Trabia Shop (Laguna's World) - UNUSED!      |
| 0x10    | Man from Garden                             |
| 0x11    | Esthar Pet Shop (Cheryl's store)            |
| 0x12    | Esthar Book Store (Karen's shop)            |
| 0x13    | Esthar Shop!!! (Johnny's shop)              |

## Function addresses

| Function | Address | Description |
|---|---|---|
| `SCRIPT_MENUSHOP` | 0x521D60 | `MENUSHOP` field-script opcode handler |
| `Menu_Prog11_ShopMenu_Init` | 0x4EDA40 | Shop menu program init |
| `SHOP_ID_REMAP_TABLE` | 0xB88918 | 52-byte field shop ID → shop.bin record remap table (global variable/data, not a function) |