# Installation

Install the library on MicroPython boards

---------------

## Install package via network

This section describes the installation of the library on network capable
boards.

```{note}
Not all MicroPython board have a network support, like the classic Raspberry
Pi Pico or the pyboard. Please check the port specific documentation.
```

This is an example on how to connect to a wireless network.

```python
import network
station = network.WLAN(network.STA_IF)
station.connect('SSID', 'PASSWORD')
# wait some time to establish the connection
station.isconnected()
```

### Install with mip

`mip` has been added in MicroPython 1.19.1 and later. For earlier MicroPython
versions check the [upip section below](#install-with-upip)

```{eval-rst}
.. epigraph::
	`mip` ("mip installs packages") is similar in concept to Python's `pip`
	tool, however it does not use the PyPI index, rather it uses
	micropython-lib as its index by default.
```

As this library is pushed to [PyPi][ref-myevse-webinterface-pypi] and
[TestPyPi][ref-myevse-webinterface-test-pypi], but not the default
[micropython-lib index](https://micropython.org/pi/v2) the additional index
has to be specified explicitly.

```python
import mip
mip.install('myevse-webinterface', index='https://pypi.org/pypi')
```

In order to install the latest release candidate version, set the index to
`'https://test.pypi.org/pypi'`

```python
import mip
mip.install('myevse-webinterface', index='https://test.pypi.org/pypi')
```

### Install with upip

```python
import upip
upip.install('myevse-webinterface')
```

In order to install the latest release candidate version, use the following
commands

```python
import upip
# overwrite index_urls to only take artifacts from test.pypi.org
upip.index_urls = ['https://test.pypi.org/pypi']
upip.install('myevse-webinterface')
```

## Install package without network

### mpremote

As of January 2022 the [`mpremote`][ref-mpremote] tool is available via `pip`
and can be used to install packages on a connected device from a host machine.

As described in the `Install required tools` section of [SETUP](SETUP.md), the
tool will be installed with the provided `requirements.txt` file. Please
follow the [mpremote documentation][ref-mpremote-doc] to connect to a
MicroPython device.

To install the latest officially released library version use the following
command

```bash
mpremote connect /dev/tty.SLAB_USBtoUART mip install --index https://pypi.org/pypi myevse-webinterface
```

In order to install the latest release candidate version, use the following
command

```bash
mpremote connect /dev/tty.SLAB_USBtoUART mip install --index https://test.pypi.org/pypi myevse-webinterface
```

### Manually

Copy all files of the
[myevse-webinterface module][ref-myevse-webinterface-module] to the MicroPython
board using [Remote MicroPython shell][ref-remote-upy-shell] or
[mpremote][ref-mpremote]

#### mpremote

Perform the following command to copy all files and folders to the device

```bash
mpremote connect /dev/tty.SLAB_USBtoUART cp -r myevse_webinterface/ :
```

#### rshell

Open the remote shell with the following command. Additionally use `-b 115200`
in case no CP210x is used but a CH34x.

```bash
rshell -p /dev/tty.SLAB_USBtoUART --editor nano
```

Perform the following command to copy all files and folders to the device

```bash
mkdir /pyboard/lib
mkdir /pyboard/lib/myevse_webinterface

cp myevse_webinterface/* /pyboard/lib/myevse_webinterface
```

## Additional MicroPython packages for examples

To use this package with the provided [`boot.py`][ref-package-boot-file] and
[`main.py`][ref-package-boot-file] file, additional modules are required,
which are not part of this repo/package.

```bash
rshell -p /dev/tty.SLAB_USBtoUART --editor nano
```

Install the additional packages `micropython-modbus`,
`micropython-brainelectronics-helpers`, `micropython-winbond` and
`micropython-esp-wifi-manager` as described in the previous section on the
MicroPython device or download the
[brainelectronics MicroPython Helpers repo][ref-github-be-mircopython-modules]
and copy it to the device.

Perform the following command to copy all files and folders to the device

```bash
mkdir /pyboard/lib/be_helpers

cp be_helpers/* /pyboard/lib/be_helpers
```

Additionally check the latest instructions of the
[brainelectronics MicroPython modules][ref-github-be-mircopython-modules],
[MicroPython Modbus][ref-github-be-mircopython-modbus] and
[MicroPython ESP WiFi Manager][ref-github-be-mircopython-esp-wifi-manager]
README for further instructions.

<!-- Links -->
[ref-myevse-webinterface-test-pypi]: https://test.pypi.org/project/myevse-webinterface/
[ref-myevse-webinterface-pypi]: https://pypi.org/project/myevse-webinterface/
[ref-mpremote]: https://docs.micropython.org/en/v1.19.1/reference/mpremote.html#mpremote
[ref-mpremote-doc]: https://docs.micropython.org/en/v1.19.1/reference/mpremote.html
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-umodbus-module]: https://github.com/brainelectronics/myevse-webinterface/tree/develop/umodbus
[ref-package-boot-file]: https://github.com/brainelectronics/myevse-webinterface/blob/c45d6cc334b4adf0e0ffd9152c8f08724e1902d9/boot.py
[ref-package-main-file]: https://github.com/brainelectronics/myevse-webinterface/blob/c45d6cc334b4adf0e0ffd9152c8f08724e1902d9/main.py
[ref-github-be-mircopython-modules]: https://github.com/brainelectronics/micropython-modules
[ref-github-be-mircopython-modbus]: https://github.com/brainelectronics/micropython-modbus
[ref-github-be-mircopython-esp-wifi-manager]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager
