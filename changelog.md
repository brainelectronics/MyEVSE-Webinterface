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

<!-- ## [Unreleased] -->

## Released
## [0.2.0] - 2022-03-05
### Added
- [`data.tpl`](templates/data.tpl) page to show latest Modbus data as table
- [`info.tpl`](templates/info.tpl) page to show latest system data
- `/modbus_data` endpoint to make Modbus data available as JSON
- `/system_data` endpoint to make system data available as JSON
- Section with available webpages introduced in [`README`](README.md)

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
[Unreleased]: https://github.com/brainelectronics/myevse-webinterface/compare/0.2.0...main

[0.2.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.2.0
[0.1.0]: https://github.com/brainelectronics/myevse-webinterface/tree/0.1.0

[ref-pypi]: https://pypi.org/
[ref-pfalcon-picoweb-sdist-upip]: https://github.com/pfalcon/picoweb/blob/b74428ebdde97ed1795338c13a3bdf05d71366a0/sdist_upip.py
