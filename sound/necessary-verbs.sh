#!/bin/sh

BOLDRED='\033[1;31m'
NOCOLOR='\033[0m'
echo "${BOLDRED}"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! IMPORTANT NOTE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo "!!! This script should only be used for troubleshooting and as a temporary solution while !!!"
echo "!!! waiting for your device's support to be implemented in the kernel.                    !!!"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo ""
echo "This script will attempt to init and enable 4 speaker amps, but your device may only have 2, "
echo "or it might not even have the speaker amp identifiers given in this script!"
echo ""
echo "For more information, see: https://github.com/joshuagrisham/galaxy-book2-pro-linux/tree/main/sound"
echo "and/or: https://github.com/thesofproject/linux/issues/4055#issuecomment-2323411911"
echo "${NOCOLOR}"
echo ""

echo "Init front left speaker (0x38)"

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x38

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
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1D
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1F
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0xFE
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x21
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
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
hda-verb /dev/snd/hwC0D0 0x20 0x423 0x99
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x03
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xA4
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0xB5
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xA5
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xBA
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x94
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

## Windows driver sets 0x89 to 0 after initializing the speaker but it seems like the value is already 0 and the speaker seems to work anyway without seting this here?
## But *just in case* and especially with other devices, set 0x89 to 0 again here to be sure...
hda-verb /dev/snd/hwC0D0 0x20 0x500 0x89
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00

echo "Init front right speaker (0x39)"

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x39

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
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x02 # 0x02 for right instead of 0x01 like on left
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1D
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x02 # 0x02 for right instead of 0x01 like on left
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1F
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0xFD # 0xFD for right instead of 0xFE like on left
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x21
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01 # 0x01 for right instead of 0x00 like on left
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
hda-verb /dev/snd/hwC0D0 0x20 0x423 0x99
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x03
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xA4
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0xB5
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xA5
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x423 0xBA
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x94
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

## Windows driver sets 0x89 to 0 after initializing the speaker but it seems like the value is already 0 and the speaker seems to work anyway without seting this here?
## But *just in case* and especially with other devices, set 0x89 to 0 again here to be sure...
hda-verb /dev/snd/hwC0D0 0x20 0x500 0x89
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00

echo "Init back left speaker (0x3C)"

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x3C

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
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1D
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x01
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x1F
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0xFE
hda-verb /dev/snd/hwC0D0 0x20 0x4B0 0x11

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x23
hda-verb /dev/snd/hwC0D0 0x20 0x420 0x21
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x00
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

echo "Init back right speaker (0x3D)"

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

echo "Enable front left speaker (0x38)"

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x38

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

echo "Enable front right speaker (0x39)"

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

echo "Enable back left speaker (0x3C)"

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x3C

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

echo "Enable back right speaker (0x3D)"

hda-verb /dev/snd/hwC0D0 0x20 0x500 0x22
hda-verb /dev/snd/hwC0D0 0x20 0x400 0x3D

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