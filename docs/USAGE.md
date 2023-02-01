# Usage

Overview to use this `myevse-webinterface` library

---------------

```{note}
The onwards described steps assume a successful setup as described in the
[setup chapter](SETUP.md)

Further examples are available in the [examples chapter](EXAMPLES.md)
```

## Webpages

### Available webpages

| URL            | Description          | Additional info |
|----------------|----------------------|-----------------|
| `/configure`   | Manage WiFi networks |                      |
| `/data`        | MyEVSE data          | Table of MyEVSE data |
| `/reboot`      | Reboot system        |                      |
| `/select`      | Select WiFi network  |                      |
| `/setup`       | Setup system         | See setup section    |
| `/info `       | System info          |                      |

### Available endpoints

| URL            | Description          | Additional info |
|----------------|----------------------|-----------------|
| `/scan_result` | Latest Scan result   | Available networks as JSON |
| `/modbus_data` | Raw Modbus data      | Latest Modbus data as JSON |
| `/reboot`      | Reboot system        |                            |
| `/system_data` | Raw System info      | Latest system data as JSON |

### Available ModBus registers

The available registers are defined by a JSON file and placed inside the
`/pyboard/lib/registers` folder on the board during the pip package
installation. This registers definitions file is loaded by the
[**`setup_modbus_connection`**](myevse_webinterface.webinterface.Webinterface.setup_modbus_connection)
function to configure the RTU-TCP Modbus bridge.

By default, and with the installation, the
[brainelectronics MyEVSE registers][ref-myevse-register-file] of the
[brainelectronics MyEVSE][ref-myevse-be], [sold on Tindie][ref-myevse-tindie]
board is provided with this repo.

## Configuration

The system can be configured via a `config.json` file. This file does not
contain any sensitive data like network passwords or other keys.

The following things can be configured by the user on the `/setup` webpage.

| Name              | Description     | Default |
|-------------------|-----------------|---------|
| `TCP_PORT`        | ModBus TCP port | `180`   |
| `REGISTERS`       | ModBus registers file, placed inside `/lib/registers` | [`modbusRegisters-MyEVSE.json`][ref-myevse-register-file] |
| `CONNECTION_MODE` | Mode of WiFi connection | `0` |

The `CONNECTION_MODE` supports the following modes

| Value | Mode   | Description |
|-------|--------|-------------|
| `0`   | Setup  | Setup WiFi connection via initial AccessPoint `WiFiManager` |
| `1`   | Client | Connect to the configured networks as client, fallback to an open AccessPoint otherwise |
| `2`   | AP     | Create an open AccessPoint named `MyEVSE` |
<!-- | `3`   | Managed     | Managed by a higher level device, for multi device usage | -->

<!-- links -->
[ref-myevse-register-file]: https://github.com/brainelectronics/myevse-webinterface/tree/develop/registers/modbusRegisters-MyEVSE.json

