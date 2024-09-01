# Linux on the Samsung Galaxy Book2 Pro

I am running Ubunutu 23.04 (previously 22.10) with the Ubuntu-packaged kernel version 6.2.x on my [Samsung Galaxy Book2 Pro (NP950XED-KA2SE)](https://www.samsung.com/se/business/computers/galaxy-book/galaxy-book2-pro-15inch-i7-16gb-512gb-np950xed-ka2se/). This repository contains various notes on different configurations and custom drivers which I am using.

```sh
$ sudo dmesg
[    0.000000] microcode: microcode updated early to revision 0x42c, date = 2023-04-18
[    0.000000] Linux version 6.2.0-34-generic (buildd@lcy02-amd64-025) (x86_64-linux-gnu-gcc-12 (Ubuntu 12.3.0-1ubuntu1~23.04) 12.3.0, GNU ld (GNU Binutils for Ubuntu) 2.40) #34-Ubuntu SMP PREEMPT_DYNAMIC Mon Sep  4 13:06:55 UTC 2023 (Ubuntu 6.2.0-34.34-generic 6.2.16)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-6.2.0-34-generic root=UUID=048b3a23-f56e-4447-8d23-59f889235454 ro quiet splash i915.enable_dpcd_backlight=3 vt.handoff=7
...
[    0.000000] DMI: SAMSUNG ELECTRONICS CO., LTD. 950XED/NP950XED-KA2SE, BIOS P11RGF.057.230404.ZQ 04/04/2023
...

$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 23.04
Release:	23.04
Codename:	lunar
```

In order to install Linux on the laptop you will need to adjust the BIOS setting for Secure Boot to either
- With `Secure Boot Control` set to `On`, set `Secure Boot Certificate keyset` to `Secure Boot Supported OS` if you wish to run Linux but only with kernels signed with the certificate to support Secure Boot (including those from Ubuntu's default kernel packages).
- or just set `Secure Boot Control` to `Off` if you want to run unsigned kernels (such as if you wish to compile the kernel yourself).

## Linux Platform Driver

I have created the start of a Linux Kernel platform driver for the device called "Samsung Galaxybook" which you can find here: <https://github.com/joshuagrisham/samsung-galaxybook-extras>

It is likely that this driver can actually support many of the recent Samsung Galaxy Book series notebooks (not just the Galaxy Book2 Pro like I have).

With this driver, there is expected to be the possibility to control at least the following features:

- Keyboard backlight
- "Dolby Atmos" mode for the speakers
- Performance modes (High performance, Optimized, Quiet, Silent)
- Battery saver (stop charging at 85%)
- Start device automatically when opening lid
- USB ports provide charging when device is turned off

## Display Backlight

To add support for controlling the OLED display backlight you can add the following boot parameter: `i915.enable_dpcd_backlight=3`

For example with Grub you would modify the file `/etc/default/grub` and add it to the `GRUB_CMDLINE_LINUX_DEFAULT` value, run `sudo update-grub`, and then reboot.

I have created an issue to try and drive an upstream fix here: [freedesktop.org: Wrong backlight control type on Samsung Galaxy Book 2 Pro](https://gitlab.freedesktop.org/drm/intel/-/issues/7972).

## Fingerprint Reader

A draft libfprint driver is available for this device. See [fingerprint/libfprint.md](./fingerprint/libfprint.md) for information on how to download, test, and install it. Hopefully it will be merged in soon!

Background:

I have opened an issue with the libfprint project for support for this device (see [libfprint: EGIS 1C7A:0582 support for Samsung Galaxy Book2 Pro](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/569)) and have done the following:

- reverse-engineered and started a PoC in Python that is a start for how a driver could be built for the EgisTec `1C7A:0582` device on this laptop. See [fingerprint/readme.md](./fingerprint/readme.md) for more details.
- created a first version of a working driver which I am now running on my laptop as the first "tester" I guess you could say (see [gitlab.freedesktop.org/joshuagrisham/libfprint](https://gitlab.freedesktop.org/joshuagrisham/libfprint.git))
- created libfprint Merge Request: [Add Egis Technology (LighTuning) Match-On-Chip driver (egismoc)](https://gitlab.freedesktop.org/libfprint/libfprint/-/merge_requests/451)

## Sound

Audio works over bluetooth, with the 3.5mm audio jack, or with the USB-A or C ports, but not out-of-the-box with the speakers.

> **Huge caveat here:** read and test the below at your own risk! No idea if this can or should work, and there have been reports of "funny smells", "funny sounds", and speakers stopping to work entirely. You have been warned!

There is quite a bit of discourse online about this issue, IMO the best collection of information is in this Github Issue posted on the SOF project here: https://github.com/thesofproject/linux/issues/4055 (including a reference to the Manjaro thread here: https://forum.manjaro.org/t/howto-set-up-the-audio-card-in-samsung-galaxy-book/37090)

There I have even posted a pastebin of my file [necessary-verbs.txt](sound/necessary-verbs.txt).

If you like, you can run the script [necessary-verbs.sh](sound/necessary-verbs.sh) to "turn on" the speakers but note that you will need to run this periodically and/or create some kind of service that runs it in the background on certain events or a certain schedule (a bit like is shown in the Manjaro thread linked above).

Some of the config files and other logs from my capturing of this list (essentially: running Windows in a QEMU container, mapping the audio devices to the QEMU container, installing the audio drivers within the virtual Windows environment, playing sound from within the QEMU container, and capturing the output into a log file) you can find in the [sound](./sound/) folder of this repository.

TODO how to continue narrowing down the necessary verb list and then package it for an upstream patch?

## Battery

I typically get around 5-7 hours of battery life in Linux. Here are some tips:

- Turn off Bluetooth if you do not need to regularly use it.
- Install `powertop` and then run both `powertop --auto-tune` and `powertop --calibrate` (note that calibration does take some time and does funny stuff with the screen brightness!).
- Either in the Windows Samsung app or in the BIOS turn on the setting which stops charging at around 85%
- Charge when battery gets near 20%, and remove the cable once it stops at 85%

## Using a Thunderbolt Dock

There is only one Thunderbolt port on this laptop (USB-C port closer to the front, by the power/charging light). Even when using this port I have had some intermittent problems and can give a few tips:

- Make sure to use a high quality cable which specifically supports Thunderbolt 3 or 4 (depending on your dock).
- Occasionally Power Delivery (through the dock via the same USB-C cable) does not seem to start. It can work to remove and re-insert the cable one or more times, or to turn off and back on the dock.
- I have had some trouble using an HDMI port on the dock with the Thunderbolt port of this laptop, but when I use the dock's DisplayPort to my monitor then it seems to work much more reliably.
- It can help to lower the refresh rate of your display (e.g. if your display supports 144+ Hz, maybe try 75 or 100).

I have also actually had some success driving a dock from the non-Thunderbolt port of this device (the USB-C port closer to the back, by the full-size HDMI port) as long as you make sure to connect the display to an HDMI port of the dock (and not a DisplayPort), and add the following kernel boot parameters:
- `i915.enable_dp_mst=0`
- `i915.enable_psr2_sel_fetch=1`

(For example by updating `/etc/default/grub`, running `update-grub`, and rebooting)

This works pretty well if you boot the kernel with the cable already connected, but it can be a little tricky to force the display to come on if you connect afterwards (you basically have to enable/disable output multiple times in a certain sequence before it will come on). And also in this case, it can help to lower the refresh rate.
