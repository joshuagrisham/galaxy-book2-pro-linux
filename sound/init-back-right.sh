#!/bin/sh

## Init back right speaker (0x3D)

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x3D

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

## Disable the speaker

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xFF
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x3A
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x80
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

## Init

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xE1
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x12
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x6F
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x14
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1B
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x02
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1D
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x02
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1F
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0xFD
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x21
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x10
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x3D
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x05
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x3F
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x03
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x50
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x2C
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x76
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x0E
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x7C
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x4A
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x81
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x03
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xBA
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x8D
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

## Windows driver sets 0x89 to 0 after initializing the speaker but it seems like the value is already 0 and the speaker seems to work anyway without seting this here?
## But *just in case* and especially with other devices, set 0x89 to 0 again here to be sure...
hda-verb /dev/snd/hwC0D0 0x20 0x500 0x89
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
