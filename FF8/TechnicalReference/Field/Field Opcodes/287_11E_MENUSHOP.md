---
layout: default
parent: Field Opcodes
title: 11E_MENUSHOP
nav_order: 287
permalink: /technical-reference/field/field-opcodes/11e-menushop/
---

-   Opcode: **0x11E**
-   Short name: **MENUSHOP**
-   Long name: Open menu shop

#### Argument

none

#### Stack

  
*ShopID*

**MENUSHOP**

#### Description

Opens a shop. The handler (`SCRIPT_MENUSHOP`, 0x521D60) pops one byte — the **shop ID** — off the script stack, stores it as the menu sub-parameter, and requests hosted menu **23** (Shop) by setting the next module to the menu module.

The shop program (`Menu_Prog11_ShopMenu_Init`, 0x4EDA40) does **not** use the popped ID directly. It first passes it through a remap table, `SHOP_ID_REMAP_TABLE` (0xB88918, 52 bytes):

| Shop ID | Remaps to | Result |
|---------|-----------|--------|
| 0 – 20 | 0 – 20 (identity) | Item shop — [shop.bin]({{ site.baseurl }}/technical-reference/menu/shop-shopbin/) record N |
| 21 – 31 | 0 | Falls back to item shop 0 (unused) |
| **32 – 42** | **21** | **Junk Shop** (weapon remodel, `Menu_Prog12_JunkShop_Init`) |
| 43 – 51 | 0 | Falls back to item shop 0 (unused) |

The remapped value **21 is a reserved sentinel** for the Junk Shop, never a real item-shop record: when `SHOP_ID_REMAP_TABLE[id] == 21` the program opens the weapon-upgrade menu (built from `mwepon.bin`) instead of a shop.bin shop. So a shop ID of **32** is the first of the eleven Junk-Shop IDs (32–42), all of which open the same weapon-remodel menu — the junk-shop code ignores which ID was used. Item shops therefore only occupy IDs 0–20.

See [Shop (shop.bin)]({{ site.baseurl }}/technical-reference/menu/shop-shopbin/) for the shop-data format and the full remap table.