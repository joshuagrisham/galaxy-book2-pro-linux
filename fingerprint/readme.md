# Samsung Galaxy Book2 Pro Fingerprint Reader testing on Linux

> Update: I have now succeeded in creating a first draft of a "real" libfprint driver for this device. See [libfprint: EGIS 1C7A:0582 support for Samsung Galaxy Book2 Pro](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/569) and some short instructions that I wrote in the file [libfprint.md](./libfprint.md).

After quite a bit of tracing via a Windows guest in QEMU + Wireshark with `usbmon`, I have created a sort of "PoC" Python driver for the EgisTec `1C7A:0582` fingerprint reader that exists on the Samsung Galaxy Book2 Pro 15".

What I found through packet tracing was that this sensor is a MOC (Match on Chip) type of sensor, so the "driver" will basically send various packets to the device in order to steer various events; the sensor has its own storage and the actual fingerprint data resides and is matched on the device itself. This is in contrast to a MOH (Match on Host) type of sensor, where the device only provides an image of the fingerprint to the host, and all storage and matching logic must occur on the host itself via some kind of driver/software.

In the end (IMO) this makes building a driver for it quite a bit more complicated -- there is a lot more which is needed in order to steer all of the different events. Luckily, this device on the Galaxy Book2 Pro was made with Windows 11 and the "Windows Hello" experience in mind, which means that, from what I can surmise, the type of events are a bit more simplified. For example, instead of a process to remove each individual fingerprint from the device one at a time, it seems to only invoke a more simplified "wipe all" kind of event (assuming per user?).

Based on analysis of the traces and observation of the behavior, I believe there are essentially these kind of events that you would need to drive with the reader:

- Enroll
- Verify
- Wipe

Using inspiration from this [libfprint issue for the Galaxy Book Pro 360](https://gitlab.freedesktop.org/libfprint/libfprint/-/issues/470) (which is incidentially a MOH device but some of the Python scripts were super helpful as a starting point) and then especially this [ELAN 04F3:0C4C MOC Python POC driver](https://github.com/depau/Elan-Fingerprint-0c4c-PoC) I was able to put together a similar POC for this `1C7A:0582` device (see [egismoc-1c7a-0582.py](./egismoc-1c7a-0582.py)).

> Please note that this is a super not-yet-even-alpha prototype, and I can't promise that it won't damage your device somehow! Use this at your own risk! (yes, I noticed that the sensor can get quite hot during testing/debugging, this might be a real risk!)

## How the PoC and communication with device works

Communication with the device seems to work basically like this:

- Issue various commands / events to a USB BULK OUT in order to drive what kind of behavior you want to occur on the sensor itself.
- Read responses from a USB BULK IN for various information and status of different commands which were sent to the BULK OUT and based on reads of the fingerprint on the actual sensor itself.
- Read from a USB INTERRUPT IN in order to "wait and listen" for a user to place their fingerprint on the sensor.

Based on looking through the traces, in the Windows driver it seems that upon startup a separate thread is started to "listen" on the interrupt address in the background with an infinite timeout, so it is just running all of the time and then being steered in a separate thread by writing/reading to the bulk interfaces.

However, in this PoC, I have tried to keep it a bit more simple, so everything is in one thread and sequentially executed; reads from the sensor's interrupt only happen when needed.

### Packet Payload Structure

Reading/Writing to the bulk in/out seems to have this kind of payload structure:

1. 8 bytes hard-coded prefix depending on out vs in
   - `E G I S 00 00 00 01` for commands to the bulk out
   - `S I G E 00 00 00 01` for responses from the bulk in
2. 2 bytes which seem to be some kind of check bytes for the payload.
3. hardcoded "`00 00 00`"
4. 2 bytes that seem to be some kind of type/subtype for different processes/events
5. then it seems to vary a bit more with additional payload data depending on different type of events; either some kind of payload directly or more "type" kind of stuff either before or after some kind of payload

Thanks to [some guidance from a Stack Exchange user](https://reverseengineering.stackexchange.com/questions/32157/derive-logic-for-2-check-bytes-for-a-usb-fingerprint-reader) I was able to piece together a basic method which looks like it computes these "check bytes" how the device is expecting. Essentially each full payload (including these check bytes) can be converted to "32-bit big-endian words from the 16-bit words", each "word" summed together MOD `0xFFFF` should equal `0` and it seems like this matches what I see in the traces, and the device seems to happily accept the payloads now.

Each "fingerprint" seems to be represented by a unique 32-byte identifier or signuature of some kind. The fingerprints (their 32-byte identifiers) which are currently enrolled can be read from a payload during the initialization sequence, and from what I can tell, it seems like it is the driver software itself that creates each new uniqe ID to send to the device for each new fingerprint during the enrollment process. For now I am just generating a random 32-byte token and the device seems to use them happily.

## How to Use

This PoC requires Python 3 plus the extra packages `pyusb` and `docopt`.

I have not sorted out the right `udev` rules for this, so in order to access the device without getting a permission denied exception, I have just used root / sudo instead.

For debugging with VS Code as root you can do something "unsafe" like this (since by default VS Code will not let you run as root):

```sh
sudo code . --no-sandbox --user-data-dir ~/.vscode/
```

Run the file with a single parameter corresponding to which function you would like to execute, like this:

```sh
# Get command help
sudo python3 egismoc-1c7a-0582.py -h

# Show device info
sudo python3 egismoc-1c7a-0582.py info

# Enroll a fingerprint
sudo python3 egismoc-1c7a-0582.py enroll

# Verify a fingerprint
sudo python3 egismoc-1c7a-0582.py verify

# Wipe all enrolled fingerprints
sudo python3 egismoc-1c7a-0582.py wipe
```

Note that the current PoC is very "chatty" in that it prints bytes of every message sent and received on the bulk interfaces to stdout without really a way to turn this off unless you change the code.

I would probably strongly recommend before using this, to:

- Boot into Windows and remove any/all existing fingerprints from the sensor before testing with this
- Make sure to successfully run the `wipe` function from this before trying to go back to Windows and use the sensor again

There are also some issues and limitations to be aware of -- see the information below.

## Issues / Open Questions

### Intermittent device state issues

It seems like sometimes due to various error conditions (and maybe some [Python-specific issues like this one?](https://stackoverflow.com/a/74221763)) the device intermittently refuses to accept commands and resets itself giving an I/O error. Assuming what you are doing is something that should work, often just running the command again (which will issue another a pyusb `reset()` of the device) can work.

### Multiple Users

When I did some testing with multiple users, it seemed like all of the different users' fingerprint identifiers came on the same packet from the device all at the same time without anything obvious that set them apart from each other. This leads me to believe that which fingerprint identifier is associated with which user account needs to happen on the host / software / driver side, and is not handled by the device at all.

At the same time, when performing a "wipe" of one user's fingerprints in Windows, it only sent the identifiers (and associated count bytes) for the one user's prints. This also leads me to assume that it is in fact possible to delete fingerprints one-at-a-time and maybe the device does not care how many you include at the same time vs not?

### Maximum number of enrolled fingerprints

There are a few instances of "counter" bytes in some of the payloads that seem to increment by `0x20` for each print that exists in the same payload. Based on some quick math this looks to me like it is only a max of 7 fingerprints which can be included in a payload before this byte rolls over past `0xff` and then would become two bytes instead of just one. I am not sure exactly what happens in this scenario -- does the device allow this and the bytes are updated in a different way, or is there only a max of 7 fingerprints that can be enrolled on this device at any time?

I have not done any tests on this but assume that it could be tested in Windows quite easly (just takes time to enroll prints, and due to the size and position of the sensor, it does get a bit tricky and failure-prone ("Move left", "Move up", etc) with certain fingers!).

### Fingerprint location when not in center

In Windows, it seems that the driver can detect when you need to "Move higher", "Move lower", "Move left", and "Move right" if your finger is not directly on the center of the sensor. However, what I have seen in the traces is that it is the exact same payload from the BULK IN in every one of these cases, so I am not sure how the Windows driver is able to differentiate between the different directions. For now in the code I have just written a single generic "please move closer to the center" kind of error message when this response is detected.

### Certificate/information exchange?

In the Windows packet trace there seems to be some kind of certificate and/or information exchange once for each session upon the first new fingerprint enrollment of that session. I am not sure exactly what this is for. I have tried to completely skip this in the PoC and it does not seem to have negatively impacted how it works, but not sure what this is for and/or how to formulate and interpret the payloads for it at this time.

### Wipe one user and/or one fingerprint at a time instead of for all users and all fingerprints

Based on some testing with multiple users (see above) I believe that it is actually possible to remove one fingerprint at a time just as long as you somehow fetch the fingerprint ID (either via first running a "verify" or grabbing it from a local storage of the IDs), then send it for removal by itself. It is just a matter of coding this scenario up (if desired) and/or if this should just be shelved and instead focus on putting the functionality in the libfprint driver later.

## Next steps

Next steps for this in my mind are to try and resolve some of the major issues above (especially regarding check bytes and how to correctly create the payloads and fingerprint identifiers) and then try to port this over as a libpfrint driver.
