---
layout: default
parent: Menu
title: Mngrp Textbox Section
permalink: /technical-reference/menu/mngrp-textbox-section/
---

# TextBox

<img src="https://github.com/user-attachments/assets/6f73a84e-9cf3-4721-8d95-854a524f3270" width="300">

TextBox are mainly found in the menu, for example for the tutorial.
They can be composed of:

* An ID
* A title
* A parent TextBox ID (the one we used to get to the current TextBox)
* Often different [cursor location id]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8Char#cursor-location-id)
* Button info
* And sometimes a left box id and/or a right box id to be able to move with the left or right cross.

There is 5 section with string info in it, but before those 5 sections there is a "Seek map" section which indicate the different position of a String Entry.

## Seek Map

Before the several string sections (5), there is a section with a map of seek data.
The seek map is composed of 4 bytes containing the number of seek location, then for each of those seek location, 4 bytes info. So the total size of the seek
map is 4 + 4*(Number seek).

### Number seek

| Type   | Size | Value | Description               |
|--------|------|-------|---------------------------|
| UInt32 | 4    | Count | Number of seek locations. |

### Seek location info

| Type   | Size | Value           | Description                                        |
|--------|------|-----------------|----------------------------------------------------|
| UInt16 | 2    | Seek\_Location  | From beginning of section to start of String Entry |
| UInt16 | 2    | Section\_Number | 0-5                                                |

## String Entry

Then each string complex section is composed of the following data:

| Type                                                                               | Size                           | Value             | Description                                                                                                      |
|------------------------------------------------------------------------------------|--------------------------------|-------------------|------------------------------------------------------------------------------------------------------------------|
| UInt16                                                                             | 2                              | Parent TextBox ID | **0xFFFF** for the first TextBox                                                                                 |
| UInt16                                                                             | 2                              | Left TextBox ID   | **0xFFFF** if no TextBox linked                                                                                  |
| UInt16                                                                             | 2                              | Right TextBox ID  | **0xFFFF** if no TextBox linked                                                                                  |
| UInt16                                                                             | 2                              | Entry\_Length     | Exact length of the entry in bytes, from the start of the entry, terminators included.                          |
| [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String) | Depends                        | Title             | The title of the TextBox, no offset specified to know the end. <br/>The **0x00** determines the end of the title |
| [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String) | Entry\_Length - 8 - Title_size | TextBox content   | The text in the TextBox, ends with **0x00**                                                                     |

Entries start on a **4-byte boundary**: the next entry begins at `align4(entry_start + Entry_Length)`, so 0 to 3
padding bytes (0x00) can follow an entry.

## How the engine reads an entry

The in-game information browser locates an entry through the Seek Map, then:

* reads the three link IDs at +0/+2/+4 (Parent is followed with the Square button, the two others with the
  page-navigation buttons; **0xFFFF** disables the button),
* **ignores Entry_Length entirely**,
* copies the title from +8 up to its **0x00** terminator,
* takes the content as the string starting right after the title terminator.

So Entry_Length and the 4-byte alignment are storage conventions of the original files rather than something the
browser depends on, but tools should preserve them.

## Engine addresses (FF8 PC 2000, FF8_EN.exe)

| Address  | Name       | Role                                                                     |
|----------|------------|--------------------------------------------------------------------------|
| 0x4D5F10 | (info browser update) | Loads TextBox sections (mngrphd entry 128 + section number) and resolves entries via the map |
| 0x1D82E4C | (loaded Seek Map)    | RAM copy of the map: per page {LOWORD: entry offset, HIWORD: section number} |
