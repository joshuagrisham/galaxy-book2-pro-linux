# Linux on the Samsing Galaxy Book2 Pro

I am running Ubunutu 22.10 with the Ubuntu-packaged kernel version 5.19 on my [Samsung Galaxy Book2 Pro (NP950XED-KA2SE)](https://www.samsung.com/se/business/computers/galaxy-book/galaxy-book2-pro-15inch-i7-16gb-512gb-np950xed-ka2se/). This repository contains various notes different configurations which I am using.

```sh
$ sudo dmesg
[    0.000000] microcode: microcode updated early to revision 0x421, date = 2022-06-15
[    0.000000] Linux version 5.19.0-28-generic (buildd@lcy02-amd64-027) (x86_64-linux-gnu-gcc-12 (Ubuntu 12.2.0-3ubuntu1) 12.2.0, GNU ld (GNU Binutils for Ubuntu) 2.39) #29-Ubuntu SMP PREEMPT_DYNAMIC Thu Dec 15 09:37:06 UTC 2022 (Ubuntu 5.19.0-28.29-generic 5.19.17)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.19.0-28-generic root=UUID=51750a71-2075-49d1-b42a-895d4b9c3ebb ro quiet splash i915.enable_dpcd_backlight=3 vt.handoff=7
...
[    0.000000] DMI: SAMSUNG ELECTRONICS CO., LTD. 950XED/NP950XED-KA2SE, BIOS P08RGF.054.220817.ZQ 08/17/2022
...

$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 22.10
Release:	22.10
Codename:	kinetic
```

In order to install Linux on the laptop you will need to adjust the BIOS setting for SecureBoot to allow more than just Windows to run (forget the setting but there are 2 choices you can make -- completely turn off SecureBoot or change to the setting which allows "additional partner" operating systems such as kernels built by Ubuntu but still signed by the Microsoft SecureBoot certificate issuer).

## Display Backlight

To add support for the OLED display backlight you can add the following boot parameter: `i915.enable_dpcd_backlight=3`

For example with Grub you would modify the file `/etc/default/grub` and add it to the `GRUB_CMDLINE_LINUX_DEFAULT` value, run `sudo update-grub`, and then reboot.

TODO: Try to create patch? (maybe with some kind of quirk or something in i915 module)

## Display Out including with Thunderbolt 3/4 Dock

Using a Thunderbolt Dock only works with the USB-C port closer to the back (near the HDMI port).

I am using a "Lenovo ThinkPad Thunderbolt 3 Dock" but there are some issues with the display out. Here is the only combination that I have found to work:

- Add these kernel options:
  - `i915.enable_dp_mst=0`
  - `i915.enable_psr2_sel_fetch=1`

(For example by updating `/etc/default/grub`, running `update-grub`, and rebooting)

- Plug your external display into the HDMI port of the TB dock (I could never get it to work with DisplayPort).
- Ideally have the dock plugged in before you power on the computer (otherwise see below).

It is the combination of `enable_dp_mst=0` and using the HDMI port that was the only way I could get this to work.

One big downside to disabling MST and using HDMI is that you cannot get as good of refresh rates. I normally like to run at least 100 Hz on my monitor (ideally 144 but it even supports up to 165), but with this configuration the max is 75 Hz.

There is still a "quirk" if you do not start up the kernel while the dock is already connected, or if you disconnect and reconnect the dock after the kernel is already loaded and running. Basically the display does not seem to come on immediately, but if you follow this procedure (assuming GNOME but similar could be done with CLI or another desktop environment?) then it seems to "come back on":

1. Under Settings > Displays, click on the external display.
1. Press/toggle the "on" button to turn the display output off.
1. Press "Apply" and then "Keep changes".
1. Press/toggle the display to turn the display back on, and "Keep changes" again.
1. Now when you go back to the external display it should still be marked as off, and might have a reduced max resolution and refresh rate -- go ahead and press/toggle "on" again even at this lower resolution.
1. Press "Apply" and "Keep changes" even though the display does not come on yet again.
1. Now when you go back to the external display settings, it should again show that the display is still off, but now the resolution and refresh rate should show the correct values. Now when you toggle on the display and click "Keep changes" it should work and the display should come on.

It is super weird and I have not dug deeper into what exactly is going on (nothing really useful shows in `dmesg` or `journalctl` that I have seen so far) but I have repeated this several times with success.

Note the above did not work before I added the option `i915.enable_psr2_sel_fetch=1`; instead I received a set of errors in the journal like this:

```sh
[ 1033.535161] i915 0000:00:02.0: [drm] *ERROR* [CRTC:80:pipe A] mismatch in has_psr (expected yes, found no)
[ 1033.535167] i915 0000:00:02.0: [drm] *ERROR* [CRTC:80:pipe A] mismatch in has_psr2 (expected yes, found no)
[ 1033.535168] i915 0000:00:02.0: [drm] *ERROR* [CRTC:80:pipe A] mismatch in enable_psr2_sel_fetch (expected yes, found no)
```

## Keyboard Backlight

TODO keyboard and OS setting are not working

- "Always on" which is cool, but maybe we would want to turn it off sometimes?
- No LED device present for it in `/sys/class/leds/` ?
- The Fn key (Fn+F9) is not recognized

```sh
[ 7441.642453] atkbd serio0: Unknown key pressed (translated set 2, code 0xac on isa0060/serio0).
[ 7441.642465] atkbd serio0: Use 'setkeycodes e02c <keycode>' to make it known.
```

## Fingerprint Reader

TODO not working

## Sound

Audio works over bluetooth, with the 3.5mm audio jack, or with the USB-A or C ports, but not out-of-the-box with the speakers.

There is quite a bit of discourse online about this issue, IMO the best collection of information is in this Github Issue posted on the SOF project here: https://github.com/thesofproject/linux/issues/4055 (including a reference to the Manjaro thread here: https://forum.manjaro.org/t/howto-set-up-the-audio-card-in-samsung-galaxy-book/37090)

There I have even posted a pastebin of my file [necessary-verbs.txt](sound/necessary-verbs.txt).

If you want you can run the script [necessary-verbs.sh](sound/necessary-verbs.sh) to "turn on" the speakers but note that you will need to run this periodically and/or create some kind of service that runs it in the background on certain events or a certain schedule (a bit like is shown in the Manjaro thread linked above).

Some of the config files and other logs from my capturing of this list (essentially: running Windows in a QEMU container, mapping the audio devices to the QEMU container, installing the audio drivers within the virtual Windows environment, playing sound from within the QEMU container, and capturing the output into a log file) you can find in the [sound](./sound/) folder of this repository.

TODO how to continue narrowing down the necessary verb list and then package it for an upstream patch?

## Battery

I typically get around 5-7 hours of battery life in Linux. Here are some tips:

- Turn off Bluetooth if you do not need to regularly use it.
- Install `powertop` and then run both `powertop --auto-tune` and `powertop --calibrate` (note that calibration does take some time and does funny stuff with the screen brightness!).
- Either in Windows or in the BIOS turn on the setting which stops charging at around ~80-85%
- Charge when battery gets near 20%

