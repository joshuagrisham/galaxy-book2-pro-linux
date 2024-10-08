#!/bin/sh

## Some kind of "init" values for various bits and bops; not really sure what all of these are for?
## But they make the coefficient values for wid 0x20 mostly match what you see in Windows so maybe it is good to set them?

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x99
hda-verb /dev/snd/hwC0D0 0x20 0x480 0x00

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x82
hda-verb /dev/snd/hwC0D0 0x20 0x444 0x08

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x32
hda-verb /dev/snd/hwC0D0 0x20 0x43F 0x00

#### Duplicated below; can we just ignore this and set it below instead?
## hda-verb /dev/snd/hwC0D0 0x20 0x500 0x0E
## hda-verb /dev/snd/hwC0D0 0x20 0x46F 0x80

#### Trace sets 0x10 to 0x0E21 here but then later sets to 0x0F21; can we just set to final value here instead?
## hda-verb /dev/snd/hwC0D0 0x20 0x500 0x10
## hda-verb /dev/snd/hwC0D0 0x20 0x40E 0x21
hda-verb /dev/snd/hwC0D0 0x20 0x500 0x10
hda-verb /dev/snd/hwC0D0 0x20 0x40F 0x21

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x55
hda-verb /dev/snd/hwC0D0 0x20 0x480 0x00

#### Duplicated below; can we just ignore this and set it below instead?
## hda-verb /dev/snd/hwC0D0 0x20 0x500 0x08
## hda-verb /dev/snd/hwC0D0 0x20 0x42F 0xCF
## 
## hda-verb /dev/snd/hwC0D0 0x20 0x500 0x08
## hda-verb /dev/snd/hwC0D0 0x20 0x42F 0xCF
## 
## hda-verb /dev/snd/hwC0D0 0x20 0x500 0x2D
## hda-verb /dev/snd/hwC0D0 0x20 0x4C0 0x20

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x19
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x17

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x50
hda-verb /dev/snd/hwC0D0 0x20 0x410 0x00

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x0E
hda-verb /dev/snd/hwC0D0 0x20 0x46F 0x80

#### Duplicated below; can we just ignore this and set it below instead?
## hda-verb /dev/snd/hwC0D0 0x20 0x500 0x08
## hda-verb /dev/snd/hwC0D0 0x20 0x42F 0xCF

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x80
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x2B
hda-verb /dev/snd/hwC0D0 0x20 0x40C 0x10

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x2D
hda-verb /dev/snd/hwC0D0 0x20 0x4C0 0x20

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x03
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x42

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x0F
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x62

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x08
hda-verb /dev/snd/hwC0D0 0x20 0x42F 0xCF

#### In Windows, these 3 are set after all speaker inits are done; can we set them here instead?
hda-verb /dev/snd/hwC0D0 0x20 0x500 0x4F
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x29

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x05
hda-verb /dev/snd/hwC0D0 0x20 0x42B 0xE0

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x30
hda-verb /dev/snd/hwC0D0 0x20 0x424 0x21
