# libfprint build/setup

## Install dependencies

```sh
sudo apt install meson cmake libgusb-dev libcairo2-dev libgirepository1.0-dev libnss3-dev libgudev-1.0-dev gtk-doc-tools

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

# Install if desired
sudo meson install
```

If you want to see more information in the log then you can update the file `/lib/systemd/system/fprintd.service` (assuming you are using systemd); specifically you can add or update the `Environment` value to something like this:

```ini
Environment=G_MESSAGES_DEBUG=all
```
