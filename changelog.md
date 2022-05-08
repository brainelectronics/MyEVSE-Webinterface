# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [x.y.z] - yyyy-mm-dd
### Added
### Changed
### Removed
### Fixed
-->
<!--
RegEx for release version from file
r"^\#\# \[\d{1,}[.]\d{1,}[.]\d{1,}\] \- \d{4}\-\d{2}-\d{2}$"
-->

<!-- ## [Unreleased] -->

## Released
## [0.8.3] - 2022-05-08
### Fixed
- Respond with `204 No Conent` on favicon request to avoid `404` on webpages,
  see [#12][ref-issue-12]

## [0.8.2] - 2022-05-06
### Fixed
- Use last 4 characters of UUID as unique AccessPoint name, see additional
  comment in [#14][ref-issue-14]

## [0.8.1] - 2022-04-20
### Changed
- Form post of `/setup` changed to vanilla JavaScript JSON post

### Fixed
- Increase spinner time at `/reboot` from 45 to 60 seconds to ensure a full
  reboot of the device, see [#16][ref-issue-16]
- Prevent redirection to POST URL on `/reboot` and `/setup` pages

## [0.8.0] - 2022-04-18
### Changed
- `/setup` and `/reboot` pages show success banner after posting new config
  data and triggering a reboot . `/setup` does not redirect anymore after
  submitting the config. The reboot of the system is done after the response
  has been sent to from the system. A circular progressbar is shown as long as
  the reboot progress is active and redirects to the index page after 45 sec
  which should be enough to fully reboot the system, see [#16][ref-issue-16]

## [0.7.0] - 2022-04-17
### Changed
- AccessPoint of MyEVSE is named `MyEVSE_xxxx` with `xxxx` as the first four
  characters of the UUID of the device, see [#14][ref-issue-14]

## [0.6.0] - 2022-04-16
### Changed
- Modbus data pages are only available in client or access point mode, update
  page only in client mode, see [#10][ref-issue-10]

### Fixed
- Added missing steps to copy [`boot.py`](boot.py) and [`main.py`](main.py)
  files in [Quickstart](QUICKSTART.md) guide

## [0.5.0] - 2022-03-20
### Added
- Versions of [WiFi Manager][ref-wifi-manager] and
  [micropython be helpers][ref-micropython-modules] added to system info dict
- [Quickstart](QUICKSTART.md) guide

### Changed
- Scanning thread is no longer started by webinterface.
  [WiFi Manager 1.4.0][ref-wifi-manager-1.4.0] is starting the thread on the
  property access

## [0.4.1] - 2022-03-13
### Fixed
- System setup card text and color content were mixed up

## [0.4.0] - 2022-03-13
### Changed
- All `_tpl.py` inside `/lib/templates/` will be removed after an update to
  ensure the usage and display of the latest templates content
- All threads are stopped before a PyPi update
- Available URLs dictionary has been updated to new
  [WiFi Manager 1.3.0][ref-wifi-manager-1.3.0] style and usage
- Data webpage is no longer automatically updated every 10 seconds to reduce
  system load and to avoid `EOF on request start`, see [#4][ref-issue-4]
- CPU clock speed increased from default 160MHz to 240MHz

### Fixed
- Register file path is set initially to correct path

## [0.3.0] - 2022-03-11
### Added
- [`update.tpl`](templates/update.tpl) page to perform system update

### Changed
- MyEVSE webinterface version is printed after boot steps finished
- POST call to `/perform_reboot_system` returns success JSON, instead of
  redirecting to landing page

### Fixed
- Removed undefined variable in [`data.tpl`](templates/data.tpl)

## [0.2.0] - 2022-03-07
### Added
- [`data.tpl`](templates/data.tpl) page to show latest Modbus data as table
- [`info.tpl`](templates/info.tpl) page to show latest system data
- `/modbus_data` endpoint to make Modbus data available as JSON
- `/system_data` endpoint to make system data available as JSON
- Section with available webpages introduced in [`README`](README.md)
- Custom logger is handed over to WiFi Manager run function to use `WARNING`
  logging level compared to default `DEBUG` level for Picoweb

### Changed
- WiFi manager scan interval increased from 5 to 10 seconds
- Modbus bridge and WiFi manager logger level increased from `DEBUG` to `INFO`
- Neopixel changes from blue to green as soon as webinterface is running

## [0.1.0] - 2022-02-27
### Added
- This changelog file
- [`.gitignore`](.gitignore) file
- [`MIT License`](LICENSE)
- [`requirements.txt`](requirements.txt) file to setup tools for board
  interactions
- Example JSON file to change some values of the Modbus
  [register definitions file for MyEVSE](registers/modbusRegisters-MyEVSE.json)
- Usage instructions in [`README`](README.md) updated
- [`myevse_webinterface`](myevse_webinterface/) package
- [`setup.tpl`](templates/setup.tpl) and [`reboot.tpl`](templates/reboot.tpl)
  pages to configure the system values and reboot the system via Webserver
- [`setup.py`](setup.py) and [`sdist_upip.py`](sdist_upip.py) taken from
  [pfalcon's picoweb repo][ref-pfalcon-picoweb-sdist-upip] and PEP8 improved

<!-- Links -->
[Unreleased]: https://github.com/brainelectronics/myevse-webinterface/compare/0.8.3...main

[0.8.3]: https://github.com/brainelectronics/myevse-webinterface/tree/0.8.3
[0.8.2]: https://github.com/brainelectronics/myevse-webinterface/tree/0.8.2
[0.8.1]: https://github.com/brainelectronics/myevse-webinterface/tree/0.8.1
[0.8.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.8.0
[0.7.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.7.0
[0.6.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.6.0
[0.5.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.5.0
[0.4.1]: https://github.com/brainelectronics/myevse-webinterface/tree/0.4.1
[0.4.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.4.0
[0.3.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.3.0
[0.2.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.2.0
[0.1.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.1.0

[ref-issue-12]: https://github.com/brainelectronics/MyEVSE-Webinterface/issues/12
[ref-issue-17]: https://github.com/brainelectronics/MyEVSE-Webinterface/issues/17
[ref-issue-16]: https://github.com/brainelectronics/MyEVSE-Webinterface/issues/16
[ref-issue-14]: https://github.com/brainelectronics/MyEVSE-Webinterface/issues/14
[ref-issue-10]: https://github.com/brainelectronics/MyEVSE-Webinterface/issues/10
[ref-wifi-manager]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager
[ref-wifi-manager-1.4.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/releases/tag/1.4.0
[ref-micropython-modules]: https://github.com/brainelectronics/micropython-modules
[ref-wifi-manager-1.3.0]: https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager/releases/tag/1.3.0
[ref-issue-4]: https://github.com/brainelectronics/MyEVSE-Webinterface/issues/4
[ref-pypi]: https://pypi.org/
[ref-pfalcon-picoweb-sdist-upip]: https://github.com/pfalcon/picoweb/blob/b74428ebdde97ed1795338c13a3bdf05d71366a0/sdist_upip.py
