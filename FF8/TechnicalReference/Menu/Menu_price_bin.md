---
layout: default
parent: Menu
title: Price (price.bin)
permalink: /technical-reference/menu/price-pricebin/
---

### price.bin

Shop prices - 4 bytes per [Item]({{site.baseurl}}/FF8/TechnicalReference/Lists/item_list)

| Type   | Size | Value           |
|--------|------|-----------------|
| UInt16 | 2    | Base Price      |
| UInt16 | 2    | Sell Multiplier |

Buy Price = Base Price \* 10

Sell Price = Base Price \* Sell Multiplier / 2
