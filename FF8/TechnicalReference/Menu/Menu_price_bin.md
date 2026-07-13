---
layout: default
parent: Menu
title: Price (price.bin)
permalink: /technical-reference/menu/price/
---

### price.bin

Shop prices - 4 bytes per [Item]({{site.baseurl}}/technical-reference/list/item)

| Type   | Size | Value           |
|--------|------|-----------------|
| UInt16 | 2    | Base Price      |
| UInt8  | 1    | Sell Multiplier |
| UInt8  | 1    | Unused          |

Buy Price = Base Price \* 10

Sell Price = Base Price \* Sell Multiplier / 2

The game reads the Sell Multiplier as a single byte (`mov al, [entry+2]`); the 4th byte of each
entry is unused padding (always 0 in the retail file).
