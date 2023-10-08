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

## Fetch and build `libfrint`

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
