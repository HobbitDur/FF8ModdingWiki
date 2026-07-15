---
layout: default
parent: Menu
title: Mngrp String Section
permalink: /technical-reference/menu/mngrp-string-section/
---
# Header String Offsets

Offset with value **0x0000** must be ignored when reading, but they must stay in place when writting, they cannot be removed.

| Type                    | Size               | Value         | Description                                                                   |
|-------------------------|--------------------|---------------|-------------------------------------------------------------------------------|
| UInt16                  | 2                  | Offset\_Count | Number of offsets before strings start                                        |
| UInt16\[Offset\_Count\] | 2 \* Offset\_count | Offsets       | The offset value points to start of a string. <br/> **0x0000** must be ignored. |

# String

They are in [FF8 String]({{site.baseurl}}/FF8/TechnicalReference/Miscellaneous/FF8String) format 

**\[Start of string location\]** = **\[Start of section\]** + **\[String offset value\]**

# How the engine reads the section

`getMenuString` **never reads Offset_Count**: it indexes the offset table directly with
`2 * text_id + variant` (the offsets work in pairs) and returns an empty string when the offset is **0x0000**.
This is why offsets are positional: a string is identified by its offset slot, so zero offsets must stay in place
and offsets cannot be reordered or removed.

## Function addresses

| Function | Address | Description |
|---|---|---|
| `getMenuString` | 0x4BD630 | Two-level positional string lookup (ignores Offset_Count; entry = 2·text_id+variant) |


# Test seed cases

For test seed cases, the string start with either a 0 or 1 that is the expected result of the test (0 for yes, 1 for no). New values can be added with new cursor locaation id and the first byte can be set to any value instead of just 0 or 1.
