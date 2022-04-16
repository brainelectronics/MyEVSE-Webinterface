# MyEVSE Webinterface

[![Downloads](https://pepy.tech/badge/myevse-webinterface)](https://pepy.tech/project/myevse-webinterface)
![Release](https://img.shields.io/github/v/release/brainelectronics/myevse-webinterface?include_prereleases&color=success)
![MicroPython](https://img.shields.io/badge/micropython-Ok-green.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MicroPython based Webinterface of MyEVSE

---------------

## Get started

This is a quickstart guide o flash the
[MicroPython firmware][ref-upy-firmware-download], connect to a network and
install the MyEVSE Webinterface package on the board

### Flash firmware

```bash
esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART erase_flash
esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART --baud 921600 write_flash -z 0x1000 esp32spiram-20220117-v1.18.bin
```

### Install package on board with pip

```bash
rshell -p /dev/tty.SLAB_USBtoUART --editor nano
```

Inside the rshell

```bash
cp main.py /pyboard
cp boot.py /pyboard
repl
```

Inside the REPL

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

### Stop all threads

```python
# stop data collection and provisioning threads
webinterface._mb_bridge.collecting_client_data = False
webinterface._mb_bridge.provisioning_host_data = False

# stop WiFi scanning thread
webinterface._wm.scanning = False
```

<!-- Links -->
[ref-upy-firmware-download]: https://micropython.org/download/
