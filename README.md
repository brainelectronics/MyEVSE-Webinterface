# MyEVSE Webinterface

[![Downloads](https://pepy.tech/badge/myevse-webinterface)](https://pepy.tech/project/myevse-webinterface)
![Release](https://img.shields.io/github/v/release/brainelectronics/myevse-webinterface?include_prereleases&color=success)
![MicroPython](https://img.shields.io/badge/micropython-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MicroPython based Webinterface of MyEVSE

---------------

## General

This is the webinterface of the MyEVSE

<a href="https://www.tindie.com/stores/brainelectronics/?ref=offsite_badges&utm_source=sellers_brainelectronics&utm_medium=badges&utm_campaign=badge_medium"><img src="https://d2ss6ovg47m0r5.cloudfront.net/badges/tindie-mediums.png" alt="I sell on Tindie" width="150" height="78"></a>

The current implementation does only run on a board with external SPI RAM. As
of now up to 300kB of RAM are required. This is more than an ESP32-D4 Pico
provides by default.

📚 The latest documentation is available at
[MyEVSE Webinterface ReadTheDocs][ref-rtd-myevse-webinterface] 📚

<!-- MarkdownTOC -->

- [Quickstart](#quickstart)
	- [Install package on board with mip or upip](#install-package-on-board-with-mip-or-upip)
	- [Upload additional files to board](#upload-additional-files-to-board)
- [Usage](#usage)

<!-- /MarkdownTOC -->

## Quickstart

This is a quickstart to install the `myevse-webinterface` library on a
MicroPython board.

A more detailed guide of the development environment can be found in
[SETUP](SETUP.md), further details about the usage can be found in
[USAGE](USAGE.md), descriptions for testing can be found in
[TESTING](TESTING.md) and several examples in [EXAMPLES](EXAMPLES.md)

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Install package on board with mip or upip

```bash
rshell -p /dev/tty.SLAB_USBtoUART --editor nano
```

Inside the [rshell][ref-remote-upy-shell] open a REPL and execute these
commands inside the REPL

```python
import machine
import network
import time
import mip
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('SSID', 'PASSWORD')
time.sleep(1)
print('Device connected to network: {}'.format(station.isconnected()))
mip.install('myevse-webinterface', index='https://pypi.org/pypi')
print('Installation completed')
machine.soft_reset()
```

For MicroPython versions below 1.19.1 use the `upip` package instead of `mip`

```python
import machine
import network
import time
import upip
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect('SSID', 'PASSWORD')
time.sleep(1)
print('Device connected to network: {}'.format(station.isconnected()))
upip.install('myevse-webinterface')
print('Installation completed')
machine.soft_reset()
```

### Upload additional files to board

Copy the [`boot.py`](boot.py) and [`main.py`](main.py) files to the
MicroPython board as shown below using
[Remote MicroPython shell][ref-remote-upy-shell]

Open the remote shell with the following command. Additionally use `-b 115200`
in case no CP210x is used but a CH34x.

```bash
rshell -p /dev/tty.SLAB_USBtoUART --editor nano
```

Perform the following command to copy all files to the device

```bash
cp main.py /pyboard
cp boot.py /pyboard
```

## Usage

See [USAGE](USAGE.md) and [DOCUMENTATION](DOCUMENTATION.md)

<!-- Links -->
[ref-rtd-myevse-webinterface]: https://myevse-webinterface.readthedocs.io/en/latest/
[ref-upy-firmware-download]: https://micropython.org/download/
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-myevse-be]: https://brainelectronics.de/
[ref-myevse-tindie]: https://www.tindie.com/stores/brainelectronics/
