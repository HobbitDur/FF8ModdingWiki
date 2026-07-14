---
layout: default
title: Junctionable Abilities unlocker
parent: List
permalink: /technical-reference/list/junctionable-abilities-unlocker/
---

{: .warning }
>Despite the page name, these values are the **"level/prereq" byte** of a GF ability slot (byte+1),
>which is the *actual* unlock condition read by `BuildGFAbilityList`. The byte the kernel struct
>calls the "unlocker" (byte+0) is **not** read for learning and is `0` in every retail GF — see
>[Junctionable GFs]({{site.baseurl}}/technical-reference/main/kernel/junctionable-gfs/).

`0x00` = none / `0x01`–`0x64` = the GF must reach that level; `0x65`–`0x79` = instead of a level,
the ability in slot `(value − 0x65)` on this same GF must be fully learned first (a same-GF unlock
chain — e.g. SumMag+20% requires SumMag+10%).

| ID   | Description  |
|------|--------------|
| 0x00 | None         |
| 0x01 | GF Level 1   |
| 0x02 | GF Level 2   |
| 0x03 | GF Level 3   |
| 0x04 | GF Level 4   |
| 0x05 | GF Level 5   |
| 0x06 | GF Level 6   |
| 0x07 | GF Level 7   |
| 0x08 | GF Level 8   |
| 0x09 | GF Level 9   |
| 0x0A | GF Level 10  |
| 0x0B | GF Level 11  |
| 0x0C | GF Level 12  |
| 0x0D | GF Level 13  |
| 0x0E | GF Level 14  |
| 0x0F | GF Level 15  |
| 0x10 | GF Level 16  |
| 0x11 | GF Level 17  |
| 0x12 | GF Level 18  |
| 0x13 | GF Level 19  |
| 0x14 | GF Level 20  |
| 0x15 | GF Level 21  |
| 0x16 | GF Level 22  |
| 0x17 | GF Level 23  |
| 0x18 | GF Level 24  |
| 0x19 | GF Level 25  |
| 0x1A | GF Level 26  |
| 0x1B | GF Level 27  |
| 0x1C | GF Level 28  |
| 0x1D | GF Level 29  |
| 0x1E | GF Level 30  |
| 0x1F | GF Level 31  |
| 0x20 | GF Level 32  |
| 0x21 | GF Level 33  |
| 0x22 | GF Level 34  |
| 0x23 | GF Level 35  |
| 0x24 | GF Level 36  |
| 0x25 | GF Level 37  |
| 0x26 | GF Level 38  |
| 0x27 | GF Level 39  |
| 0x28 | GF Level 40  |
| 0x29 | GF Level 41  |
| 0x2A | GF Level 42  |
| 0x2B | GF Level 43  |
| 0x2C | GF Level 44  |
| 0x2D | GF Level 45  |
| 0x2E | GF Level 46  |
| 0x2F | GF Level 47  |
| 0x30 | GF Level 48  |
| 0x31 | GF Level 49  |
| 0x32 | GF Level 50  |
| 0x33 | GF Level 51  |
| 0x34 | GF Level 52  |
| 0x35 | GF Level 53  |
| 0x36 | GF Level 54  |
| 0x37 | GF Level 55  |
| 0x38 | GF Level 56  |
| 0x39 | GF Level 57  |
| 0x3A | GF Level 58  |
| 0x3B | GF Level 59  |
| 0x3C | GF Level 60  |
| 0x3D | GF Level 61  |
| 0x3E | GF Level 62  |
| 0x3F | GF Level 63  |
| 0x40 | GF Level 64  |
| 0x41 | GF Level 65  |
| 0x42 | GF Level 66  |
| 0x43 | GF Level 67  |
| 0x44 | GF Level 68  |
| 0x45 | GF Level 69  |
| 0x46 | GF Level 70  |
| 0x47 | GF Level 71  |
| 0x48 | GF Level 72  |
| 0x49 | GF Level 73  |
| 0x4A | GF Level 74  |
| 0x4B | GF Level 75  |
| 0x4C | GF Level 76  |
| 0x4D | GF Level 77  |
| 0x4E | GF Level 78  |
| 0x4F | GF Level 79  |
| 0x50 | GF Level 80  |
| 0x51 | GF Level 81  |
| 0x52 | GF Level 82  |
| 0x53 | GF Level 83  |
| 0x54 | GF Level 84  |
| 0x55 | GF Level 85  |
| 0x56 | GF Level 86  |
| 0x57 | GF Level 87  |
| 0x58 | GF Level 88  |
| 0x59 | GF Level 89  |
| 0x5A | GF Level 90  |
| 0x5B | GF Level 91  |
| 0x5C | GF Level 92  |
| 0x5D | GF Level 93  |
| 0x5E | GF Level 94  |
| 0x5F | GF Level 95  |
| 0x60 | GF Level 96  |
| 0x61 | GF Level 97  |
| 0x62 | GF Level 98  |
| 0x63 | GF Level 99  |
| 0x64 | GF Level 100 |
| 0x65 | Ability 1    |
| 0x66 | Ability 2    |
| 0x67 | Ability 3    |
| 0x68 | Ability 4    |
| 0x69 | Ability 5    |
| 0x6A | Ability 6    |
| 0x6B | Ability 7    |
| 0x6C | Ability 8    |
| 0x6D | Ability 9    |
| 0x6E | Ability 10   |
| 0x6F | Ability 11   |
| 0x70 | Ability 12   |
| 0x71 | Ability 13   |
| 0x72 | Ability 14   |
| 0x73 | Ability 15   |
| 0x74 | Ability 16   |
| 0x75 | Ability 17   |
| 0x76 | Ability 18   |
| 0x77 | Ability 19   |
| 0x78 | Ability 20   |
| 0x79 | Ability 21   |