#!/bin/sh

## Enable front right speaker (0x39)

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x39

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x3A
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x81
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xFF
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11
