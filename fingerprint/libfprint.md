# libfprint build/setup

## Install dependencies

```sh
sudo apt install python3-mesonpy
sudo apt install cmake
sudo apt install libgusb-dev
sudo apt install libcairo2-dev
sudo apt install libgirepository1.0-dev
sudo apt install libnss3-dev
sudo apt install libgudev-1.0-dev
sudo apt install gtk-doc-tools
```

Other dependencies might be needed depending on what else you want to do (for example if you want to capture test data you will need Wireshark + tshark). 

## Fetch and build `libfprint`

```sh
# upstream
git clone https://gitlab.freedesktop.org/libfprint/libfprint.git
# or my fork, which includes egismoc for this device
git clone https://github.com/joshuagrisham/libfprint.git

cd libfprint/
meson setup builddir
cd builddir/
meson compile

# Run unit tests if desired
meson test

# Install if desired
sudo meson install
```

If you want to see more information in the log then you can update the file `/lib/systemd/system/fprintd.service` (assuming you are using systemd); specifically you can add or update the `Environment` value to something like this:

```ini
Environment=G_MESSAGES_DEBUG=all
```
