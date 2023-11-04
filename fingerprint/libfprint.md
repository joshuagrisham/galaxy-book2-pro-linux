# libfprint build/setup

## Install dependencies

```sh
sudo apt install meson cmake libgusb-dev libcairo2-dev libgirepository1.0-dev \
  libnss3-dev libgudev-1.0-dev gtk-doc-tools

# install tshark if you want to be able to create new test data captures
sudo apt install tshark

# install valgrind if you want to run the valgrind memleak tests
sudo apt install valgrind
```

Other dependencies might be needed depending on what else you want to do (for example if you want to capture test data, you might also need Wireshark). 

## Fetch and build `libfprint`

```sh
# upstream
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git

# or my fork, which includes egismoc for this device
git clone https://gitlab.freedesktop.org/joshuagrisham/libfprint.git
cd libfprint/

git checkout egismoc

meson setup builddir
cd builddir/
meson compile

# Run unit tests if desired
meson test
# Or just for this driver
meson test egismoc

# Run valgrind tests if desired
meson test --setup=valgrind -v
# Or just for this driver
meson test --setup=valgrind -v egismoc

# Run "examples" to see if the driver is working with your device
sudo ./examples/manage-prints
sudo ./examples/enroll
sudo ./examples/identify
sudo ./examples/verify

# Maybe good to delete all of the prints you enrolled before installing:
sudo ./examples/manage-prints

# Install if desired
sudo meson install

# Add debug messages to fprintd service if desired
echo Environment=G_MESSAGES_DEBUG=all | sudo tee --append /lib/systemd/system/fprintd.service
sudo systemctl restart fprintd.service
```

The last two lines are only relevant if you want to see more information in the log, in which case you can update the file `/lib/systemd/system/fprintd.service` (assuming you are using systemd); specifically you can add or update the `Environment` value to something like this:

```ini
Environment=G_MESSAGES_DEBUG=all
```

If you see an error message like this and your driver does not seem to be loading:

```sh
Launching FprintObject
Initializing FpContext (libfprint version 1.94.6+tod1)
Impossible to load the shared drivers dir Error opening directory “/usr/lib/x86_64-linux-gnu/libfprint-2/tod-1”: No such file or directory
Preparing devices for resume
No driver found for USB device 1D6B:0003
No driver found for USB device 2B7E:C556
No driver found for USB device 1C7A:0582
No driver found for USB device 0930:6544
No driver found for USB device 8087:0033
No driver found for USB device 1D6B:0002
No driver found for USB device 1D6B:0003
No driver found for USB device 1D6B:0002
entering main loop
```

Then I was able to work around this by removing and re-installing `libfprint-2-tod1`

```sh
sudo apt remove libfprint-2-tod1
sudo apt install libfprint-2-tod1
# And then if you see that fprintd was uninstalled, install it again
sudo apt install fprintd
# Add debug messages again and restart fprintd
echo Environment=G_MESSAGES_DEBUG=all | sudo tee --append /lib/systemd/system/fprintd.service
sudo systemctl restart fprintd.service
```

In case you need then you can run the meson install again (but in my case when I checked `journalctl -u fprintd.service -e` it actually started with my installed drivers already at this point!)

```sh
sudo meson install
sudo systemctl restart fprintd.service
```
