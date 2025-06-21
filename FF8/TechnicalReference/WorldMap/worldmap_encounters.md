---
layout: default
title: World Map Encounters
parent: WorldMap
permalink: /technical-reference/worldmap/world-map-encounters/
---

### W.I.P.

The World Map is divided in _Regions_, and each _Region_ is made up of different _Ground IDs_.  
For each _Ground ID_, 8 different encounter slots are available, and are ordered by rarity: the first 4 are common encounters, the following 2 are medium rarity, and the last 2 are rare encounters.  
These 8 slots each contain an [EncounterID](../../battle/encounter-codes/), these IDs are used to load the correct encounter from [scene.out](../../battle/battle-structure-sceneout/).  
The following is a list of all the possible encounters in FF8's World Map.

1. TOC
{:toc}

# Balamb

## Balamb Region (Region ID 0)

### Grasslands (Ground ID 6)
{: .no_toc }

| Encounter ID | Description | Rarity |
|--------------|-------------|--------|
| 514          | Bite Bug    | Common |
| 514          | Bite Bug    | Common |
| 514          | Bite Bug    | Common |
| 512          | 2 Bite Bug  | Common |
| 512          | 2 Bite Bug  | Medium |
| 520          | Glacial Eye | Medium |
| 513          | 3 Bite Bug  | Rare   |
| 513          | 3 Bite Bug  | Rare   |

### Forest (Ground ID 4)
{: .no_toc }

| Encounter ID | Description                 | Rarity |
|--------------|-----------------------------|--------|
| 515          | Caterchipillar              | Common |
| 515          | Caterchipillar              | Common |
| 515          | Caterchipillar              | Common |
| 515          | Caterchipillar              | Common |
| 516          | Caterchipillar + 2 Bite Bug | Medium |
| 516          | Caterchipillar + 2 Bite Bug | Medium |
| 521          | T-Rexaur                    | Rare   |
| 521          | T-Rexaur                    | Rare   |

### Beach (Ground ID 10)
{: .no_toc }

| Encounter ID | Description      | Rarity |
|--------------|------------------|--------|
| 517          | 2 Fastitocalon-F | Common |
| 517          | 2 Fastitocalon-F | Common |
| 517          | 2 Fastitocalon-F | Common |
| 517          | 2 Fastitocalon-F | Common |
| 517          | 2 Fastitocalon-F | Medium |
| 517          | 2 Fastitocalon-F | Medium |
| 517          | 2 Fastitocalon-F | Rare   |
| 517          | 2 Fastitocalon-F | Rare   |

### Next to Mountains (Ground ID 24)
{: .no_toc }

| Encounter ID | Description   | Rarity |
|--------------|---------------|--------|
| 518          | Glacial Eye   | Common |
| 518          | Glacial Eye   | Common |
| 518          | Glacial Eye   | Common |
| 518          | Glacial Eye   | Common |
| 518          | Glacial Eye   | Medium |
| 519          | 2 Glacial Eye | Medium |
| 519          | 2 Glacial Eye | Rare   |
| 519          | 2 Glacial Eye | Rare   |

# Galbadia

## Dollet Region (Region ID 1)

### Forest (Ground Type 0)
{: .no_toc }

| Encounter ID | Description                    | Rarity |
|--------------|--------------------------------|--------|
| 542          | 3 Funguar                      | Common |
| 542          | 3 Funguar                      | Common |
| 542          | 3 Funguar                      | Common |
| 542          | 3 Funguar                      | Common |
| 549          | Wendigo + Anacondaur + Funguar | Medium |
| 549          | Wendigo + Anacondaur + Funguar | Medium |
| 549          | Wendigo + Anacondaur + Funguar | Rare   |
| 549          | Wendigo + Anacondaur + Funguar | Rare   |

### Grasslands (Ground Type 6)
{: .no_toc }

| Encounter ID | Description | Rarity |
|--------------|-------------|--------|
| 539          | Geezard     | Common |
| 539          | Geezard     | Common |
| 539          | Geezard     | Common |
| 540          | 2 Geezard   | Common |
| 540          | 2 Geezard   | Medium |
| 540          | 2 Geezard   | Medium |
| 541          | 3 Geezard   | Rare   |
| 541          | 3 Geezard   | Rare   |

### Beach (Ground Type 10)
{: .no_toc }

| Encounter ID | Description      | Rarity |
|--------------|------------------|--------|
| 543          | 3 Fastitocalon-F | Common |
| 543          | 3 Fastitocalon-F | Common |
| 543          | 3 Fastitocalon-F | Common |
| 543          | 3 Fastitocalon-F | Common |
| 543          | 3 Fastitocalon-F | Medium |
| 548          | 2 Adamantoise    | Medium |
| 548          | 2 Adamantoise    | Rare   |
| 548          | 2 Adamantoise    | Rare   |

### Top of Plateau (Ground ID 14)
{: .no_toc }

| Encounter ID | Description            | Rarity |
|--------------|------------------------|--------|
| 544          | Anacondaur             | Common |
| 544          | Anacondaur             | Common |
| 544          | Anacondaur             | Common |
| 544          | Anacondaur             | Common |
| 545          | Anacondaur + 2 Geezard | Medium |
| 545          | Anacondaur + 2 Geezard | Medium |
| 545          | Anacondaur + 2 Geezard | Rare   |
| 545          | Anacondaur + 2 Geezard | Rare   |

### Next to Plateau on Grass (Ground ID 15)
{: .no_toc }

| Encounter ID | Description            | Rarity |
|--------------|------------------------|--------|
| 546          | Geezard                | Common |
| 546          | Geezard                | Common |
| 546          | Geezard                | Common |
| 546          | Geezard                | Common |
| 547          | Anacondaur + 2 Geezard | Medium |
| 547          | Anacondaur + 2 Geezard | Medium |
| 547          | Anacondaur + 2 Geezard | Rare   |
| 547          | Anacondaur + 2 Geezard | Rare   |

## Timber Region (Region ID 2)

### Forest (Ground ID 0)
{: .no_toc }

| Encounter ID | Description            | Rarity |
|--------------|------------------------|--------|
| 528          | 2 Funguar + Cockatrice | Common |
| 528          | 2 Funguar + Cockatrice | Common |
| 528          | 2 Funguar + Cockatrice | Common |
| 529          | Wendigo                | Common |
| 529          | Wendigo                | Medium |
| 530          | Ochu                   | Medium |
| 527          | 2 Anacondaur           | Rare   |
| 527          | 2 Anacondaur           | Rare   |

### Grasslands (Ground ID 6)
{: .no_toc }

Shared with _Region ID 19_.  

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 522          | Thrustaevis           | Common |
| 522          | Thrustaevis           | Common |
| 535          | Funguar               | Common |
| 535          | Funguar               | Common |
| 523          | 2 Thrustaevis         | Medium |
| 524          | Thrustaevis + Geezard | Medium |
| 524          | Thrustaevis + Geezard | Rare   |
| 523          | 2 Thrustaevis         | Rare   |

### Badlands (Ground ID 7)
{: .no_toc }

| Encounter ID | Description | Rarity |
|------------- |-------------|--------|
| 525          | Geezard     | Common |
| 525          | Geezard     | Common |
| 525          | Geezard     | Common |
| 525          | Geezard     | Common |
| 525          | Geezard     | Medium |
| 526          | 2 Geezard   | Medium |
| 526          | 2 Geezard   | Rare   |
| 526          | 2 Geezard   | Rare   |

### Beach (Ground ID 10)
{: .no_toc }

Shared with _Region ID 19_.  

| Encounter ID | Description      | Rarity |
|--------------|------------------|--------|
| 531          | 2 Fastitocalon-F | Common |
| 531          | 2 Fastitocalon-F | Common |
| 531          | 2 Fastitocalon-F | Common |
| 531          | 2 Fastitocalon-F | Common |
| 531          | 2 Fastitocalon-F | Medium |
| 536          | 3 Fastitocalon-F | Medium |
| 536          | 3 Fastitocalon-F | Rare   |
| 536          | 3 Fastitocalon-F | Rare   |

### Top of Plateau (Ground ID 14)
{: .no_toc }

Shared with _Region ID 19_.  

| Encounter ID | Description   | Rarity |
|--------------|---------------|--------|
| 537          | Wendigo       | Common |
| 537          | Wendigo       | Common |
| 537          | Wendigo       | Common |
| 537          | Wendigo       | Common |
| 532          | 2 Thrustaevis | Medium |
| 532          | 2 Thrustaevis | Medium |
| 532          | 2 Thrustaevis | Rare   |
| 532          | 2 Thrustaevis | Rare   |

### Next to Plateau on Grass (Ground ID 15)
{: .no_toc }

Shared with _Region ID 19_.  

| Encounter ID | Description | Rarity |
|--------------|-------------|--------|
| 533          | Geezard     | Common |
| 533          | Geezard     | Common |
| 533          | Geezard     | Common |
| 533          | Geezard     | Common |
| 533          | Geezard     | Medium |
| 538          | 3 Geezard   | Medium |
| 538          | 3 Geezard   | Rare   |
| 538          | 3 Geezard   | Rare   |

### Next to Plateau on Badlands (Ground ID 16)
{: .no_toc }

Shared with _Region ID 19_

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 534          | Thrustaevis + Geezard | Common |
| 534          | Thrustaevis + Geezard | Common |
| 534          | Thrustaevis + Geezard | Common |
| 534          | Thrustaevis + Geezard | Common |
| 534          | Thrustaevis + Geezard | Medium |
| 534          | Thrustaevis + Geezard | Medium |
| 534          | Thrustaevis + Geezard | Rare   |
| 534          | Thrustaevis + Geezard | Rare   |

## Small 1 chunk area roughly around Galbadia Garden (Region ID 3)

### Forest (Ground ID 0)
{: .no_toc }

| Encounter ID | Description | Rarity |
|--------------|-------------|--------|
| 553          | Grendel     | Common |
| 553          | Grendel     | Common |
| 553          | Grendel     | Common |
| 553          | Grendel     | Common |
| 553          | Grendel     | Medium |
| 553          | Grendel     | Medium |
| 553          | Grendel     | Rare   |
| 553          | Grendel     | Rare   |

### Grasslands (Ground ID 6)
{: .no_toc }

| Encounter ID | Description | Rarity |
|--------------|-------------|--------|
| 550          | Blood Soul  | Common |
| 550          | Blood Soul  | Common |
| 550          | Blood Soul  | Common |
| 550          | Blood Soul  | Common |
| 550          | Blood Soul  | Medium |
| 550          | Blood Soul  | Medium |
| 550          | Blood Soul  | Rare   |
| 550          | Blood Soul  | Rare   |

### Badlands (Ground ID 7)
{: .no_toc }

Shared with _Region ID 19_

| Encounter ID | Description             | Rarity |
|--------------|-------------------------|--------|
| 551          | Belhelmel + Blood Soul  | Common |
| 551          | Belhelmel + Blood Soul  | Common |
| 551          | Belhelmel + Blood Soul  | Common |
| 552          | Belhelmel + Geezard     | Common |
| 552          | Belhelmel + Geezard     | Medium |
| 552          | Belhelmel + Geezard     | Medium |
| 556          | Thrustaevis + 2 Geezard | Rare   |
| 556          | Thrustaevis + 2 Geezard | Rare   |

### Top of Plateau (Ground ID 14)
{: .no_toc }

| Encounter ID | Description | Rarity |
|--------------|-------------|--------|
| 554          | Thrustaevis | Common |
| 554          | Thrustaevis | Common |
| 554          | Thrustaevis | Common |
| 554          | Thrustaevis | Common |
| 554          | Thrustaevis | Medium |
| 554          | Thrustaevis | Medium |
| 554          | Thrustaevis | Rare   |
| 554          | Thrustaevis | Rare   |

### Next to Plateau on Badlands (Ground ID 16)
{: .no_toc }

| Encounter ID | Description              | Rarity |
|--------------|--------------------------|--------|
| 555          | Thrustaevis + Blood Soul | Common |
| 555          | Thrustaevis + Blood Soul | Common |
| 555          | Thrustaevis + Blood Soul | Common |
| 555          | Thrustaevis + Blood Soul | Common |
| 555          | Thrustaevis + Blood Soul | Medium |
| 555          | Thrustaevis + Blood Soul | Medium |
| 555          | Thrustaevis + Blood Soul | Rare   |
| 555          | Thrustaevis + Blood Soul | Rare   |

## Deling City Area (Region ID 4)

### Grasslands (Ground ID 6)
{: .no_toc }

| Encounter ID | Description   | Rarity |
|--------------|---------------|--------|
| 557          | Geezard       | Common |
| 557          | Geezard       | Common |
| 557          | Geezard       | Common |
| 558          | Thrustaevis   | Common |
| 558          | Thrustaevis   | Medium |
| 558          | Thrustaevis   | Medium |
| 559          | 2 Thrustaevis | Rare   |
| 559          | 2 Thrustaevis | Rare   |

### Badlands (Ground ID 7)
{: .no_toc }

| Encounter ID | Description                    | Rarity |
|--------------|--------------------------------|--------|
| 560          | Wendigo                        | Common |
| 560          | Wendigo                        | Common |
| 580          | Geezard                        | Common |
| 580          | Geezard                        | Common |
| 561          | 2 Wendigo                      | Medium |
| 561          | 2 Wendigo                      | Medium |
| 552          | Wendigo + Geezard + Blood Soul | Rare   |
| 553          | Belhelmel                      | Rare   |

### Desert (Ground ID 8)
{: .no_toc }

Shared with _Region ID 19_.  
Unused in _Region ID 3_.  

| Encounter ID | Description                     | Rarity |
|--------------|---------------------------------|--------|
| 568          | 3 Fastitocalon-F                | Common |
| 568          | 3 Fastitocalon-F                | Common |
| 581          | 1 Fastitocalon                  | Common |
| 569          | 2 Fastitocalon-F + Fastitocalon | Common |
| 570          | Abyss Worm                      | Medium |
| 571          | 2 Fastitocalon-F                | Medium |
| 571          | 2 Fastitocalon-F                | Rare   |
| 572          | Chimera                         | Rare   |

### Beach (Ground ID 10)
{: .no_toc }

| Encounter ID | Description                   | Rarity |
|--------------|-------------------------------|--------|
| 564          | 2 Fastitocalon-F              | Common |
| 564          | 2 Fastitocalon-F              | Common |
| 564          | 2 Fastitocalon-F              | Common |
| 564          | 2 Fastitocalon-F              | Common |
| 564          | 2 Fastitocalon-F              | Medium |
| 578          | Fastitocalon-F + Fastitocalon | Medium |
| 578          | Fastitocalon-F + Fastitocalon | Rare   |
| 578          | Fastitocalon-F + Fastitocalon | Rare   |

### Top of Plateau (Ground ID 14)
{: .no_toc }

| Encounter ID | Description               | Rarity |
|------------- |---------------------------|--------|
| 565          | 2 Geezard                 | Common |
| 565          | 2 Geezard                 | Common |
| 565          | 2 Geezard                 | Common |
| 565          | 2 Geezard                 | Common |
| 566          | Thrustaevis + Geezard     | Medium |
| 566          | Thrustaevis + Geezard     | Medium |
| 567          | 2 Thrustaevis + Belhelmel | Rare   |
| 567          | 2 Thrustaevis + Belhelmel | Rare   |

### Next to Plateau on Grass (Ground ID 15)
{: .no_toc }

| Encounter ID | Description         | Rarity |
|--------------|---------------------|--------|
| 573          | 3 Geezard           | Common |
| 573          | 3 Geezard           | Common |
| 573          | 3 Geezard           | Common |
| 573          | 3 Geezard           | Common |
| 574          | 2 Funguar           | Medium |
| 574          | 2 Funguar           | Medium |
| 579          | Funguar + 2 Geezard | Rare   |
| 579          | Funguar + 2 Geezard | Rare   |

### Next to Plateau on Badlands (Ground ID 16)
{: .no_toc }

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 575          | Thrustaevis           | Common |
| 575          | Thrustaevis           | Common |
| 575          | Thrustaevis           | Common |
| 576          | Thrustaevis + Geezard | Common |
| 576          | Thrustaevis + Geezard | Medium |
| 576          | Thrustaevis + Geezard | Medium |
| 577          | 2 Thrustaevis         | Rare   |
| 577          | 2 Thrustaevis         | Rare   |

## Winhil Region (Region ID 6)

### Grasslands (Ground ID 6)
{: .no_toc }

| Encounter ID | Description    | Rarity |
|--------------|----------------|--------|
| 582          | Blood Soul     | Common |
| 582          | Blood Soul     | Common |
| 582          | Blood Soul     | Common |
| 583          | Lefty + Righty | Common |
| 583          | Lefty + Righty | Medium |
| 584          | Vysage         | Medium |
| 584          | Vysage         | Rare   |
| 584          | Vysage         | Rare   |

### Badlands (Ground ID 7)
{: .no_toc }

| Encounter ID | Description             | Rarity |
|--------------|-------------------------|--------|
| 585          | Cockatrice + Blood Soul | Common |
| 585          | Cockatrice + Blood Soul | Common |
| 585          | Cockatrice + Blood Soul | Common |
| 585          | Cockatrice + Blood Soul | Common |
| 585          | Cockatrice + Blood Soul | Medium |
| 585          | Cockatrice + Blood Soul | Medium |
| 585          | Cockatrice + Blood Soul | Rare   |
| 585          | Cockatrice + Blood Soul | Rare   |

### Beach (Ground ID 10)
{: .no_toc }

| Encounter ID | Description                     | Rarity |
|--------------|---------------------------------|--------|
| 586          | Fastitocalon-F                  | Common |
| 586          | Fastitocalon-F                  | Common |
| 586          | Fastitocalon-F                  | Common |
| 586          | Fastitocalon-F                  | Common |
| 586          | Fastitocalon-F                  | Medium |
| 587          | Lefty + Fastitocalon-F + Righty | Medium |
| 587          | Lefty + Fastitocalon-F + Righty | Rare   |
| 587          | Lefty + Fastitocalon-F + Righty | Rare   |

### Top of Plateau (Ground ID 14)
{: .no_toc }

| Encounter ID | Description | Rarity |
|--------------|-------------|--------|
| 588          | 2 Grendel   | Common |
| 588          | 2 Grendel   | Common |
| 588          | 2 Grendel   | Common |
| 588          | 2 Grendel   | Common |
| 589          | Grendel     | Medium |
| 589          | Grendel     | Medium |
| 589          | Grendel     | Rare   |
| 589          | Grendel     | Rare   |

### Next to Plateau on Grass (Ground ID 15)
{: .no_toc }

| Encounter ID | Description         | Rarity |
|--------------|---------------------|--------|
| 590          | Lefty               | Common |
| 590          | Lefty               | Common |
| 590          | Lefty               | Common |
| 590          | Lefty               | Common |
| 591          | Righty + Blood Soul | Medium |
| 591          | Righty + Blood Soul | Medium |
| 591          | Righty + Blood Soul | Rare   |
| 591          | Righty + Blood Soul | Rare   |

### Next to Plateau on Badlands (Ground ID 16)
{: .no_toc }

| Encounter ID | Description             | Rarity |
|--------------|-------------------------|--------|
| 592          | Vysage + Lefty + Righty | Common |
| 592          | Vysage + Lefty + Righty | Common |
| 592          | Vysage + Lefty + Righty | Common |
| 592          | Vysage + Lefty + Righty | Common |
| 592          | Vysage + Lefty + Righty | Medium |
| 592          | Vysage + Lefty + Righty | Medium |
| 592          | Vysage + Lefty + Righty | Rare   |
| 592          | Vysage + Lefty + Righty | Rare   |

## Central and North-West Galbadia (Region ID 19)

### Grasslands (Ground ID 6)
{: .no_toc }

Shared with _Region ID 2_.  

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 522          | Thrustaevis           | Common |
| 522          | Thrustaevis           | Common |
| 535          | Funguar               | Common |
| 535          | Funguar               | Common |
| 523          | 2 Thrustaevis         | Medium |
| 524          | Thrustaevis + Geezard | Medium |
| 524          | Thrustaevis + Geezard | Rare   |
| 523          | 2 Thrustaevis         | Rare   |

### Badlands (Ground ID 7)
{: .no_toc }

Shared with _Region ID 3_.  

| Encounter ID | Description             | Rarity |
|--------------|-------------------------|--------|
| 551          | Belhelmel + Blood Soul  | Common |
| 551          | Belhelmel + Blood Soul  | Common |
| 551          | Belhelmel + Blood Soul  | Common |
| 552          | Belhelmel + Geezard     | Common |
| 552          | Belhelmel + Geezard     | Medium |
| 552          | Belhelmel + Geezard     | Medium |
| 556          | Thrustaevis + 2 Geezard | Rare   |
| 556          | Thrustaevis + 2 Geezard | Rare   |


### Desert (Ground ID 8)
{: .no_toc }

Shared with _Region ID 3_.  

| Encounter ID | Description                     | Rarity |
|--------------|---------------------------------|--------|
| 568          | 3 Fastitocalon-F                | Common |
| 568          | 3 Fastitocalon-F                | Common |
| 581          | 1 Fastitocalon                  | Common |
| 569          | 2 Fastitocalon-F + Fastitocalon | Common |
| 570          | Abyss Worm                      | Medium |
| 571          | 2 Fastitocalon-F                | Medium |
| 571          | 2 Fastitocalon-F                | Rare   |
| 572          | Chimera                         | Rare   |

### Beach (Ground ID 10)
{: .no_toc }

Shared with _Region ID 2_.  

| Encounter ID | Description           | Rarity |
|------------- |-----------------------|--------|
| 531          | 2 Fastitocalon-F      | Common |
| 531          | 2 Fastitocalon-F      | Common |
| 531          | 2 Fastitocalon-F      | Common |
| 531          | 2 Fastitocalon-F      | Common |
| 531          | 2 Fastitocalon-F      | Medium |
| 536          | 3 Fastitocalon-F      | Medium |
| 536          | 3 Fastitocalon-F      | Rare   |
| 536          | 3 Fastitocalon-F      | Rare   |

### Top of Plateau (Ground ID 14)
{: .no_toc }

Shared with _Region ID 2_.  

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 537          | Wendigo               | Common |
| 537          | Wendigo               | Common |
| 537          | Wendigo               | Common |
| 537          | Wendigo               | Common |
| 532          | 2 Thrustaevis         | Medium |
| 532          | 2 Thrustaevis         | Medium |
| 532          | 2 Thrustaevis         | Rare   |
| 532          | 2 Thrustaevis         | Rare   |


### Next to Plateau on Grass (Ground ID 15)
{: .no_toc }

Shared with _Region ID 2_.  

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 533          | Geezard               | Common |
| 533          | Geezard               | Common |
| 533          | Geezard               | Common |
| 533          | Geezard               | Common |
| 533          | Geezard               | Medium |
| 538          | 3 Geezard             | Medium |
| 538          | 3 Geezard             | Rare   |
| 538          | 3 Geezard             | Rare   |

### Next to Plateau on Badlands (Ground ID 16)
{: .no_toc }

Shared with _Region ID 2_.  

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 534          | Thrustaevis + Geezard | Common |
| 534          | Thrustaevis + Geezard | Common |
| 534          | Thrustaevis + Geezard | Common |
| 534          | Thrustaevis + Geezard | Common |
| 534          | Thrustaevis + Geezard | Medium |
| 534          | Thrustaevis + Geezard | Medium |
| 534          | Thrustaevis + Geezard | Rare   |
| 534          | Thrustaevis + Geezard | Rare   |

# Trabia

## Trabia Region (Region ID 8)

### Frosted Forest (Ground ID 1)
{: .no_toc }

| Encounter ID | Description            | Rarity |
|--------------|------------------------|--------|
| 612          | 2 Bite Bug             | Common |
| 612          | 2 Bite Bug             | Common |
| 613          | Gayla + 2 Bite Bug     | Common |
| 613          | Gayla + 2 Bite Bug     | Common |
| 614          | Snow Lion + 2 Bite Bug | Medium |
| 614          | Snow Lion + 2 Bite Bug | Medium |
| 615          | Blue Dragon            | Rare   |
| 615          | Blue Dragon            | Rare   |

### Forest (Ground ID 5)
{: .no_toc }

| Encounter ID | Description         | Rarity |
|--------------|---------------------|--------|
| 629          | Gayla + Mesmerize   | Common |
| 630          | 2 Gayla + Mesmerize | Common |
| 629          | Gayla + Mesmerize   | Common |
| 629          | Gayla + Mesmerize   | Common |
| 630          | 2 Gayla + Mesmerize | Medium |
| 630          | 2 Gayla + Mesmerize | Medium |
| 632          | Ochu                | Rare   |    
| 631          | Blue Dragon         | Rare   |

### Frozen Grasslands (Ground ID 7)
{: .no_toc }

Shared with _Region ID 11_.

| Encounter ID | Description                  | Rarity |
|--------------|------------------------------|--------|
| 622          | Mesmerize                    | Common |
| 622          | Mesmerize                    | Common |
| 622          | Mesmerize                    | Common |
| 623          | 2 Mesmerize                  | Common |
| 623          | 2 Mesmerize                  | Medium |
| 623          | 2 Mesmerize                  | Medium |
| 624          | Bite Bug + Gayla + Mesmerize | Rare   |    
| 624          | Bite Bug + Gayla + Mesmerize | Rare   |

### Snowlands (Ground ID 9)
{: .no_toc }

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 610          | Bite Bug              | Common |
| 610          | Bite Bug              | Common |
| 608          | Gayla                 | Common |
| 608          | Gayla                 | Common |
| 608          | Gayla                 | Medium |
| 609          | 2 Gayla               | Medium |
| 609          | 2 Gayla               | Rare   |    
| 611          | Mesmerize + Snow Lion | Rare   |

### Beach (Ground ID 10)
{: .no_toc }

| Encounter ID | Description      | Rarity |
|--------------|------------------|--------|
| 616          | Fastitocalon-F   | Common |
| 616          | Fastitocalon-F   | Common |
| 616          | Fastitocalon-F   | Common |
| 617          | 2 Fastitocalon-F | Common |
| 617          | 2 Fastitocalon-F | Medium |
| 617          | 2 Fastitocalon-F | Medium |
| 618          | Fastitocalon     | Rare   |    
| 618          | Fastitocalon     | Rare   |

### Top of Plateau (Ground ID 14)
{: .no_toc }

| Encounter ID | Description              | Rarity |
|--------------|--------------------------|--------|
| 633          | Bite Bug                 | Common |
| 633          | Bite Bug                 | Common |
| 633          | Bite Bug                 | Common |
| 633          | Bite Bug                 | Common |
| 634          | Blue Dragon	           | Medium |
| 634          | Blue Dragon	           | Medium |
| 635          | Blue Dragon + 2 Bite Bug | Rare   |    
| 635          | Blue Dragon + 2 Bite Bug | Rare   |

### Next to Frozen Mountains on Frozen Grasslands (Ground ID 16)
{: .no_toc }

Shared with _Region ID 11_.

| Encounter ID | Description       | Rarity |
|--------------|-------------------|--------|
| 619          | Gayla             | Common |
| 619          | Gayla             | Common |
| 619          | Gayla             | Common |
| 621          | 3 Bite Bug        | Common |
| 621          | 3 Bite Bug        | Medium |
| 621          | 3 Bite Bug        | Medium |
| 604          | Mesmerize + Gayla | Rare   |    
| 604          | Mesmerize + Gayla | Rare   |

### Next to Frozen Mountains on Snowlands (Ground ID 17)
{: .no_toc }

| Encounter ID | Description              | Rarity |
|--------------|--------------------------|--------|
| 633          | Bite Bug                 | Common |
| 633          | Bite Bug                 | Common |
| 633          | Bite Bug                 | Common |
| 633          | Bite Bug                 | Common |
| 634          | Blue Dragon	          | Medium |
| 634          | Blue Dragon	          | Medium |
| 635          | Blue Dragon + 2 Bite Bug | Rare   |    
| 635          | Blue Dragon + 2 Bite Bug | Rare   |

## Shumi Village Area (Region ID 9)

### Frozen Grasslands (Ground ID 7)
{: .no_toc }

| Encounter ID | Description           | Rarity |
|--------------|-----------------------|--------|
| 598          | Mesmerize             | Common |
| 598          | Mesmerize             | Common |
| 598          | Mesmerize             | Common |
| 596          | Forbidden             | Common |
| 596          | Forbidden             | Medium |
| 597          | Forbidden + Mesmerize | Medium |
| 597          | Forbidden + Mesmerize | Rare   |
| 599          | Ochu                  | Rare   |

### Snowlands (Ground ID 9)
{: .no_toc }

| Encounter ID | Description | Rarity |
|--------------|-------------|--------|
| 593          | Mesmerize   | Common |
| 593          | Mesmerize   | Common |
| 593          | Mesmerize   | Common |
| 594          | 2 Mesmerize | Common |
| 594          | 2 Mesmerize | Medium |
| 594          | 2 Mesmerize | Medium |
| 595          | Snow Lion   | Rare   |
| 595          | Snow Lion   | Rare   |

### Beach (Ground ID 10)
{: .no_toc }

| Encounter ID | Description                   | Rarity |
|--------------|-------------------------------|--------|
| 616          | Fastitocalon-F                | Common |
| 600          | Snow Lion                     | Common |
| 601          | 2 Fastitocalon-F              | Common |
| 602          | Fastitocalon + Fastitocalon-F | Medium |
| 602          | Fastitocalon + Fastitocalon-F | Medium |
| 603          | Adamantoise                   | Rare   |
| 603          | Adamantoise                   | Rare   |

### Next to Frozen Mountains on Snowlands (Ground ID 17)
{: .no_toc }

| Encounter ID | Description             | Rarity |
|--------------|-------------------------|--------|
| 604          | Mesmerize + Gayla       | Common |
| 604          | Mesmerize + Gayla       | Common |
| 605          | 2 Gayla                 | Common |
| 605          | 2 Gayla                 | Common |
| 606          | Snow Lion + 2 Mesmerize | Medium |
| 606          | Snow Lion + 2 Mesmerize | Medium |
| 607          | Blue Dragon             | Rare   |
| 607          | Blue Dragon             | Rare   |

## Winter Island (Region ID 17)

### Snowlands (Ground ID 9)
{: .no_toc }

| Encounter ID | Description       | Rarity |
|--------------|-------------------|--------|
| 694          | Snow Lion         | Common |
| 695          | Gayla + Mesmerize | Common |
| 695          | Gayla + Mesmerize | Common |
| 695          | Gayla + Mesmerize | Common |
| 696          | Gayla + Forbidden | Medium |
| 696          | Gayla + Forbidden | Medium |
| 696          | Gayla + Forbidden | Rare   |
| 694          | Snow Lion         | Rare   |

### Next to Frozen Mountains on Snowlands (Ground ID 17)
{: .no_toc }

| Encounter ID | Description | Rarity |
|--------------|------------ |--------|
| 697          | Forbidden   | Common |
| 697          | Forbidden   | Common |
| 697          | Forbidden   | Common |
| 697          | Forbidden   | Common |
| 698          | 2 Forbidden | Medium |
| 698          | 2 Forbidden | Medium |
| 698          | 2 Forbidden | Rare   |
| 698          | 2 Forbidden | Rare   |

# Inaccessible Encounters

### Roads
{: .no_toc }

### Railways
{: .no_toc }
