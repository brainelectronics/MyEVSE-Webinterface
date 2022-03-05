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

## Get started

### Install required tools

Python3 must be installed on your system. Check the current Python version
with the following command

```bash
python --version
python3 --version
```

Depending on which command `Python 3.x.y` (with x.y as some numbers) is
returned, use that command to proceed.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### Flash firmware

To flash the [MicroPython firmware][ref-upy-firmware-download] as described on
the MicroPython firmware download page, use the `esptool.py` to erase the
flash before flashing the firmware.

```bash
esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART erase_flash
esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART --baud 921600 write_flash -z 0x1000 esp32spiram-20220117-v1.18.bin
```

### Install package on board with pip

Connect to a network

```python
import network
station = network.WLAN(network.STA_IF)
station.connect('SSID', 'PASSWORD')
station.isconnected()
```

and install this MicroPython packages on the device like this

```python
import upip
upip.install('myevse-webinterface')
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

### Available Webpages

| URL            | Description          | Additional info |
|----------------|----------------------|-----------------|
| `/scan_result` | Latest Scan result   | Available networks as JSON |
| `/configure`   | Manage WiFi networks |                            |
| `/data`        | MyEVSE data          | Table of MyEVSE data       |
| `/modbus_data` | Raw Modbus data      | Latest Modbus data as JSON |
| `/reboot`      | Reboot system        | 							 |
| `/select`      | Select WiFi network  | 							 |
| `/setup`       | Setup system         | 							 |
| `/info `       | System info          | 							 |
| `/system_data` | Raw System info      | Latest system data as JSON |

### Available ModBus registers

The available registers are defined by a JSON file and placed inside the
`/pyboard/lib/registers` folder on the board during the pip package
installation. This registers definitions file is loaded by the
[`Webinterface`](myevse_webinterface/webinterface.py) class function
`setup_modbus_connection` to configure the RTU-TCP Modbus bridge.

As an [example the registers](registers/modbusRegisters-MyEVSE.json) of a
[brainelectronics MyEVSE][ref-myevse-be], [MyEVSE on Tindie][ref-myevse-tindie]
board is provided with this repo.

## Configuration

The system can be configured via the [`config.json`](config.json) file. This
file does not contain any sensitive data like network passwords or other keys.

The following things can be configured by the user on the `/setup` webpage.

| Name              | Description     | Default |
|-------------------|-----------------|---------|
| `TCP_PORT`        | ModBus TCP port | `180`   |
| `REGISTERS`       | ModBus registers file, placed inside `/lib/registers` | [`modbusRegisters-MyEVSE.json`](modbusRegisters-MyEVSE.json) |
| `CONNECTION_MODE` | Mode of WiFi connection | `0` |

The `CONNECTION_MODE` supports the following modes

| Value | Mode   | Description |
|-------|--------|-------------|
| `0`   | Setup  | Setup WiFi connection via initial AccessPoint `WiFiManager` |
| `1`   | Client | Connect to the configured networks as client, fallback to an open AccessPoint otherwise |
| `2`   | AP     | Create an open AccessPoint named `MyEVSE` |

<!-- Links -->
[ref-upy-firmware-download]: https://micropython.org/download/
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-myevse-be]: https://brainelectronics.de/
[ref-myevse-tindie]: https://www.tindie.com/stores/brainelectronics/
