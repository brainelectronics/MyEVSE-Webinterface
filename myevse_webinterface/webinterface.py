#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
MyEVSE Webinterface

This class combines all required packages and modules into one simple class.
It handles the LED and Neopixel, WiFi connections and does the Modbus Bridge
setup before starting the actual Webinterface
"""

# system packages
import gc
import json
import machine
import network
import time

# custom modules
# pip installed packages
# https://github.com/miguelgrinberg/microdot
from microdot.microdot_asyncio import Request, Response, send_file
from microdot.microdot_utemplate import render_template, init_templates

# https://github.com/brainelectronics/micropython-modules
from be_helpers import version as be_helpers_version
from be_helpers.generic_helper import GenericHelper
from be_helpers.led_helper import Led, Neopixel
from be_helpers.modbus_bridge import ModbusBridge
from be_helpers.path_helper import PathHelper
from wifi_manager import version as wifi_manager_version
from wifi_manager import WiFiManager
from . import version as webinterface_version


class WebinterfaceError(Exception):
    """Base class for exceptions in this module."""
    pass


class Webinterface(object):
    """docstring for Webinterface"""
    SETUP_MODE = 0
    CLIENT_MODE = 1
    ACCESSPOINT_MODE = 2

    Response.default_content_type = 'text/html'

    def __init__(self, logger=None, quiet=False, name=__name__):
        # setup and configure logger if none is provided
        if logger is None:
            logger = GenericHelper.create_logger(
                logger_name=self.__class__.__name__)
            GenericHelper.set_level(logger, 'debug')
        self.logger = logger
        self.logger.disabled = quiet

        self._led = Led()
        self._pixel = Neopixel()
        self._station = network.WLAN(network.STA_IF)

        # turn Neopixel off, keep onboard LED active
        self._led.turn_on()
        self._pixel.clear()

        self._boot_time_ticks = time.ticks_ms()
        self._boot_duration = self._boot_time_ticks
        self._free_ram_after_boot = 0
        self._restart_cause = 0
        self._connection_result = False

        self._config_file_path = 'config.json'
        self._rtu_pins = (25, 26)     # (TX, RX)
        self._connection_mode = 0
        self._register_file = 'lib/registers/modbusRegisters-MyEVSE.json'
        self._tcp_port = 180
        self._config_data = {
            "TCP_PORT": self._tcp_port,
            "REGISTERS": self._register_file,
            "CONNECTION_MODE": self._connection_mode
        }

        self._pixel.color = 'blue'
        self._pixel.intensity = 20

        self._update_complete = False
        self._update_ongoing = False

        init_templates(template_dir='lib/templates')
        self.load_config()

        # default level is 'warning', may use custom logger to get initial log
        self._mb_bridge = ModbusBridge(register_file=self.register_file)
        GenericHelper.set_level(self._mb_bridge.logger, 'info')

        self._wm = WiFiManager()
        GenericHelper.set_level(self._wm.logger, 'info')
        self.add_additional_webpages()

        # run garbage collector at the end to clean up
        gc.collect()

        self.logger.debug('Finished Webinterface init')

    @property
    def config_data(self) -> dict:
        """
        Get system config data

        :returns:   System configuration data
        :rtype:     dict
        """
        return self._config_data

    @config_data.setter
    def config_data(self, value: dict) -> None:
        """
        Set system config data

        :param      value:  The system config
        :type       value:  dict
        """
        if isinstance(value, dict):
            self._config_data = value
            self._update_config_properties()
        else:
            raise WebinterfaceError('Config data shall type dict, not: {}'.
                                    format(type(value)))

    @property
    def config_file_path(self) -> str:
        """
        Get system config file path

        :returns:   Path to system config file
        :rtype:     str
        """
        return self._config_file_path

    @property
    def connection_mode(self) -> int:
        """
        Get connection mode as specified in system config file

        :returns:   Connection mode, 0: Setup, 1: Client, 2: AccessPoint
        :rtype:     int
        """
        return self._connection_mode

    @connection_mode.setter
    def connection_mode(self, value: int) -> None:
        """
        Set connection mode

        :param      value:  The value
        :type       value:  int
        """
        if isinstance(value, int):
            self._connection_mode = value
        else:
            raise WebinterfaceError('Connection mode shall type int, not: {}'.
                                    format(type(value)))

    @property
    def register_file(self) -> str:
        """
        Get register file path

        :returns:   Path to Modbus register JSON file
        :rtype:     str
        """
        return self._register_file

    @register_file.setter
    def register_file(self, value: str) -> None:
        """
        Set path to Modbus register JSON file

        :param      value:  The value
        :type       value:  str
        """
        if PathHelper.exists(path=value):
            self._register_file = value
        else:
            self.logger.info('Configured register file does not exist')

    @property
    def tcp_port(self) -> int:
        """
        Get configured Modbus TCP port

        :returns:   The TCP port the device is listening for Modbus requests
        :rtype:     int
        """
        return self._tcp_port

    @tcp_port.setter
    def tcp_port(self, value: int) -> None:
        """
        Set Modbus TCP port

        :param      value:  TCP port of device listening for Modbus requests
        :type       value:  int
        """
        if isinstance(value, int):
            self._tcp_port = value
        else:
            raise WebinterfaceError('TCP port shall type int, not: {}'.
                                    format(type(value)))

    @property
    def boot_duration(self) -> int:
        """
        Get time all boot steps took

        :returns:   Boot duration in milliseconds
        :rtype:     int
        """
        return self._boot_duration

    @property
    def restart_cause(self) -> int:
        """
        Get the restart cause

        :returns:   Restart cause
        :rtype:     int
        """
        return self._restart_cause

    @property
    def connection_result(self) -> bool:
        """
        Get connection result

        :returns:   Connection result
        :rtype:     bool
        """
        return self._connection_result

    @connection_result.setter
    def connection_result(self, value: bool) -> None:
        """
        Set connection result

        :param      value:  The value
        :type       value:  bool
        """
        self._connection_result = value

    @property
    def update_complete(self) -> bool:
        """
        Get update complete flag

        :returns:   True on update completed, False otherwise
        :rtype:     bool
        """
        return self._update_complete

    @update_complete.setter
    def update_complete(self, value: bool) -> None:
        """
        Set update complete result

        :param      value:  The value
        :type       value:  bool
        """
        self._update_complete = value

    @property
    def update_ongoing(self) -> bool:
        """
        Get update status flag

        :returns:   True while update ongoing, False otherwise
        :rtype:     bool
        """
        return self._update_ongoing

    @update_ongoing.setter
    def update_ongoing(self, value: bool) -> None:
        """
        Set update ongoing result

        :param      value:  The value
        :type       value:  bool
        """
        self._update_ongoing = value

    def load_config(self) -> None:
        """
        Load system configuration from JSON file.

        The @see config_file_path is used as loading location. If no file is
        found at that location, the default data of @see config_data is saved
        to that location.

        All configurable properties are set to the values loaded from the file
        """
        cfg = self.config_data
        cfg_file_path = self.config_file_path

        if PathHelper.exists(path=cfg_file_path):
            self.logger.debug('Found JSON config file "{}"'.
                              format(cfg_file_path))
            cfg = GenericHelper.load_json(path=cfg_file_path, mode='r')
            self.logger.debug('Config loaded as: {}'.format(cfg))
            self.config_data = cfg
        else:
            self.logger.info('JSON config file {} does not exist'.
                             format(cfg_file_path))
            GenericHelper.save_json(data=cfg, path=cfg_file_path)
            self.logger.debug('Created file with default values: {}'.
                              format(cfg))

        self._update_config_properties()

    def _update_config_properties(self) -> None:
        """Update config properties saved in config JSON file"""
        try:
            # WiFi connection mode
            self.connection_mode = int(self.config_data['CONNECTION_MODE'])
        except Exception as e:
            self.logger.warning('Failed to load CONNECTION_MODE as int: {}'.
                                format(e))

        try:
            # TCP port for Modbus connection
            self.tcp_port = int(self.config_data['TCP_PORT'])
        except Exception as e:
            self.logger.warning('Failed to load TCP_PORT as int: {}'.
                                format(e))

        try:
            # Modbus registers file path
            self.register_file = self.config_data['REGISTERS']
        except Exception as e:
            self.logger.warning('Failed to set REGISTERS path: {}'.
                                format(e))

    def init_connection(self) -> None:
        """
        Initializes the WiFi connection.

        Currently active connections are disconnected and the WiFi is turned
        off to avoid old connection issues and states
        """
        if self._station.active() and self._station.isconnected():
            self._station.disconnect()
            time.sleep(1)
        self._station.active(False)
        time.sleep(1)
        self._station.active(True)

    def finish_setup(self) -> None:
        """
        Finish the initial setup.

        Turn off the onboad LED and the Neopixel, collect the reset cause and
        available RAM after all initial steps
        """
        self._pixel.clear()

        self._restart_cause = machine.reset_cause()
        self.logger.debug('Restart cause: {}'.format(self.restart_cause))

        self._free_ram_after_boot = GenericHelper.free(full=True)
        self.logger.debug('RAM info: {}'.format(self._free_ram_after_boot))

        self._boot_duration = time.ticks_diff(time.ticks_ms(),
                                              self._boot_time_ticks)

        self.logger.debug('Finished "boot" steps after: {}ms'.
                          format(self._boot_duration))

    def add_additional_webpages(self) -> None:
        """
        Add additional webpages to the WiFi Manager webserver.

        Add system setup and reboot pages to the list of available URLs
        """
        self._wm.add_url_rule(url='/setup', func=self.system_config)
        self._wm.add_url_rule(url='/reboot', func=self.reboot_system)
        self._wm.add_url_rule(url='/save_system_config',
                              func=self.save_system_config,
                              methods=['POST'])
        self._wm.add_url_rule(url='/perform_reboot_system',
                              func=self.perform_reboot_system,
                              methods=['POST'])

        self._wm.add_url_rule(url='/system_data', func=self.system_data)
        self._wm.add_url_rule(url='/info', func=self.system_info)

        # add the new "Setup" and "Reboot" page to the index page
        self._wm.available_urls = {
            "/setup": {
                "title": "Setup system",
                "color": "text-white bg-success",
                "text": "Configure Modbus TCP port, register file and WiFi connection mode",    # noqa: E501
            },
            "/reboot": {
                "title": "Reboot",
                "color": "text-white bg-warning",
                "text": "Reboot system",
            },
            "/info": {
                "title": "System info",
                "color": "text-white bg-primary",
                "text": "Show latest system data as table",
            },
            "/system_data": {
                "title": "System data",
                "color": "text-white bg-info",
                "text": "Latest system data as JSON",
            },
        }

        # add Modbus data pages only if device is setup as client or AP
        if self.connection_mode in [self.CLIENT_MODE, self.ACCESSPOINT_MODE]:
            self._wm.add_url_rule(url='/data', func=self.device_data)
            self._wm.add_url_rule(url='/modbus_data', func=self.modbus_data)
            self._wm.add_url_rule(url='/modbus_data_table',
                                  func=self.modbus_data_table)

            self._wm.available_urls.update({
                "/data": {
                    "title": "MyEVSE data",
                    "color": "text-white bg-primary",
                    "text": "Show latest MyEVSE data as table",
                },
                "/modbus_data": {
                    "title": "Modbus data",
                    "color": "text-white bg-info",
                    "text": "Latest MyEVSE modbus data as JSON",
                },
            })

        # add update page only in client mode
        if self.connection_mode in [self.CLIENT_MODE]:
            self._wm.add_url_rule(url='/update', func=self.update_system)
            self._wm.add_url_rule(url='/perform_system_update',
                                  func=self.perform_system_update,
                                  methods=['POST'])

            self._wm.available_urls.update({
                "/update": {
                    "title": "Update",
                    "color": "text-white bg-warning",
                    "text": "Update system",
                },
            })

    async def _save_system_config(self, data: dict) -> None:
        """
        Update and save the system configuration to file

        :param      data:  The data
        :type       data:  dict
        """
        self.logger.debug('Updating existing cfg {} with {}'.
                          format(json.dumps(self.config_data),
                                 json.dumps(data)))

        data_decoded = dict()
        for key, val in data.items():
            try:
                val_decoded = int(val)
            except Exception:
                val_decoded = val
            data_decoded[key] = val_decoded

        try:
            existing_data = self.config_data
            existing_data.update(data_decoded)
            self.config_data = existing_data
        except Exception as e:
            self.logger.debug('Failed to update config_data with new data: {}'.
                              format(e))

        self.logger.debug('Saving JSON config {} to {}'.
                          format(json.dumps(self.config_data),
                                 self.config_file_path))
        GenericHelper.save_json(data=self.config_data,
                                path=self.config_file_path)

    def setup_wifi_connection(self) -> None:
        """
        Setup WiFi connection

        Try to load existing WiFi connection definitions and create an
        AccessPoint if configured by the system config file or in case the
        connection to all configured networks failed
        """
        self.logger.debug('WiFi connection timeout: {} sec'.
                          format(self._wm.connection_timeout))
        self.logger.debug('WiFi connection result: {}'.
                          format(self._wm.connection_result))
        self.logger.debug('Default CONNECTION_MODE: {}'.
                          format(self.connection_mode))

        connection_mode = self.connection_mode
        connection_result = False

        if connection_mode == self.SETUP_MODE:
            # device connection not yet configured
            self._wm.start_config()
        elif connection_mode == self.CLIENT_MODE:
            # device connection configured
            connection_result = self._wm.load_and_connect()
        elif connection_mode == self.ACCESSPOINT_MODE:
            # device configured as AccessPoint
            # abuse connection_result variable to create an AccessPoint later
            connection_result = False
        else:
            # unknown connection mode, create an AccessPoint later on
            connection_result = False

        self.logger.debug('Connection result: {}'.format(connection_result))
        self.connection_result = connection_result

        # failed to connect to a configured network
        if connection_result is False:
            # disconnect as/from station and disable WiFi for it
            try:
                self._station.disconnect()
            except Exception as e:
                self.logger.info('Error on disconnecting station: {}'.
                                 format(e))

            self._station.active(False)
            time.sleep(1)

            # create a true AccessPoint without any active Station mode
            ap_name = 'MyEVSE_{}'.format(
                GenericHelper.get_uuid(-4).decode('ascii'))
            self.logger.info('Starting MyEVSE in AccessPoint mode named "{}"'.
                             format(ap_name))
            self._wm.wh.create_ap(ssid=ap_name,
                                  password='',
                                  channel=11,
                                  timeout=5)

    def setup_modbus_connection(self) -> None:
        """
        Setup the Modbus connection (bridge) between the MyEVSE as RTU and the
        data provisioning interface on TCP

        Connection settings to the MyEVSE are defined in the registers JSON
        file. The TCP port is taken from the system config file.

        The data collection thread as well as the data provision thread is
        finally started.
        """
        # for testing use 'debug' level
        # for beta testing with full BE32-01 board use 'info' level
        # for production use 'warning' level, default
        # GenericHelper.set_level(mb_bridge.logger, 'info')

        self.logger.debug('Register file: {}'.
                          format(self._mb_bridge.register_file))
        self.logger.debug('Connection settings:')
        self.logger.debug('\t Host: {}'.
                          format(self._mb_bridge.connection_settings_host))
        self.logger.debug('\t Client: {}'.
                          format(self._mb_bridge.connection_settings_client))
        self.logger.debug('\t Host Unit: {}'.
                          format(self._mb_bridge.host_unit))
        self.logger.debug('\t Client Unit: {}'.
                          format(self._mb_bridge.client_unit))

        # define and apply Modbus TCP host settings
        host_settings = {
            'type': 'tcp',
            'unit': self.tcp_port,
            'address': -1,
            'baudrate': -1,
            'mode': 'master'
        }
        self._mb_bridge.connection_settings_host = host_settings

        self.logger.debug('Updated connection settings:')
        self.logger.debug('\t Host: {}'.
                          format(self._mb_bridge.connection_settings_host))
        self.logger.debug('\t Client: {}'.
                          format(self._mb_bridge.connection_settings_client))
        self.logger.debug('\t Host Unit: {}'.
                          format(self._mb_bridge.host_unit))
        self.logger.debug('\t Client Unit: {}'.
                          format(self._mb_bridge.client_unit))

        # setup Modbus connections to host and client
        # IP infos shall be available before calling this function
        self._mb_bridge.setup_connection(pins=self._rtu_pins)

        self.logger.debug('Modbus instances:')
        self.logger.debug('\t Act as Host: {} on {}'.
                          format(self._mb_bridge.host,
                                 self._mb_bridge.host_unit))
        self.logger.debug('\t Act as Client: {} on {}'.
                          format(self._mb_bridge.client,
                                 self._mb_bridge.client_unit))

        # start collecting latest RTU client data in thread and TCP data
        # provisioning in another thread
        self._mb_bridge.collecting_client_data = True
        self._mb_bridge.provisioning_host_data = True

    def start_webinterface(self) -> None:
        """
        Start the actual webinterface

        Run the WiFi Manager webserver in an async thread. This function does
        not return until the webserver finished running, usually never.

        All setup steps have to be performed before calling this function.
        """
        self.logger.debug('Collect latest client data every {} seconds'.
                          format(self._mb_bridge.collection_interval))
        self.logger.debug('Synchronize Host-Client every {} seconds'.
                          format(self._mb_bridge.synchronisation_interval))

        self._led.turn_off()
        self._pixel.color = 'green'

        # set scanning interval, scan is started on property access
        self._wm.scan_interval = 10000

        device_ip = self._mb_bridge._get_network_ip()
        self._wm.run(host=device_ip, port=80, debug=True)

        self.logger.debug('Beyond WiFiManager run function')

    def wait_for_irq(self) -> None:
        """
        Backup function to keep device in an endless loop.

        In case a KeyboardInterrupt is received the active threads of the
        Modbus data collection and provision are stopped. Any active WiFi
        scanning thread is stopped as well.
        """
        pass
        # new endpoint '/shutdown' has been introduced with Micropython ESP
        # WiFi Manager 1.10.0
        # This function has to be available as the main.py file is not updated
        # with any updates and is calling this function at some point in time

    @property
    def system_infos(self) -> dict:
        """
        Get available system infos

        :returns:   System infos in humand readable format
        :rtype:     dict
        """
        sys_info = GenericHelper.get_system_infos_human()
        sys_info['version'] = webinterface_version.__version__
        sys_info['version_be_helpers'] = be_helpers_version.__version__
        sys_info['version_wifi_manager'] = wifi_manager_version.__version__

        return sys_info

    # -------------------------------------------------------------------------
    # Webserver functions

    # @app.route('/setup')
    async def system_config(self, req: Request) -> None:
        connection_mode = self.connection_mode

        setup_checked = ""
        client_checked = ""
        ap_checked = ""

        if connection_mode == self.SETUP_MODE:
            setup_checked = "checked"
        elif connection_mode == self.CLIENT_MODE:
            client_checked = "checked"
        elif connection_mode == self.ACCESSPOINT_MODE:
            ap_checked = "checked"

        return render_template(template='setup.tpl',
                               req=None,
                               tcp_port=self.tcp_port,
                               register_file=self.register_file,
                               setup_checked=setup_checked,
                               client_checked=client_checked,
                               ap_checked=ap_checked)

    # @app.route('/reboot_system')
    async def reboot_system(self, req: Request) -> None:
        """Reboot the system"""
        res = send_file('/lib/templates/reboot.tpl')
        res.headers["Content-Type"] = "text/html"

        return res

    # @app.route('/perform_reboot_system')
    async def perform_reboot_system(self, req: Request) -> None:
        """Process system reboot"""
        # perform soft reset, like CTRL+D
        await machine.soft_reset()

        return None, 204, {'Content-Type': 'application/json; charset=UTF-8'}

    # @app.route('/save_system_config')
    async def save_system_config(self, req: Request) -> None:
        """Process saving the specified system configs"""
        form_data = req.json

        # Whether form data comes from GET or POST request, once parsed,
        # it's available as req.form dictionary
        self.logger.debug('System config user input content: {}'.
                          format(form_data))
        # {
        #     'TCP_PORT': '180',
        #     'CONNECTION_MODE': '1',
        #     'REGISTERS': 'modbusRegisters-MyEVSE.json'
        # }

        await self._save_system_config(data=form_data)

        # empty response to avoid any redirects or errors due to none response
        return None, 204, {'Content-Type': 'application/json; charset=UTF-8'}

    async def _render_modbus_data(self, device_data: dict) -> str:
        """
        Render HTML table of given device data

        :param      device_data:    All device register data
        :type       device_data:    dict

        :returns:   Sub content of Modbus data page
        :rtype:     str
        """
        content = ""

        for reg_type, reg_type_data in sorted(device_data.items()):
            reg_type_table = """
            <h5>{}</h5><table class="table table-striped table-bordered table-hover"><thead class="thead-dark"><tr><th scope="col">Register</th><th scope="col">Name</th><th scope="col">Value</th></tr></thead><tbody>
            """.format(reg_type)    # noqa: E501

            # iterage e.g. IREGS, sorted by register
            for register, register_data in sorted(reg_type_data.items(),
                                                  key=lambda item: item[1]['register']):    # noqa: E501
                register_value = register_data['val']

                if (isinstance(register_data['val'], list) and
                        len(register_data['val']) == 2):
                    # actual a uint32_t value, reconstruct it
                    register_value = register_data['val'][0] << 16 | register_data['val'][1]    # noqa: E501

                reg_type_table += """
                <tr><th scope="row">{register}</th><td>{register_name}</td><td>{register_value}</td></tr>
                """.format(register=register_data['register'],  # noqa: E501
                           register_name=register,
                           register_value=register_value)

            # finish this table
            reg_type_table += "</tbody></table><br>"

            # add this register typte table to the overall content
            content += reg_type_table

        return content

    async def _render_system_info(self, system_data: dict) -> str:
        """
        Render HTML fieldset of given system data

        :param      system_data:    All system data
        :type       system_data:    dict

        :returns:   Sub content of system info page
        :rtype:     str
        """
        content = "<fieldset disabled>"

        for key, description in sorted(system_data['description'].items()):
            try:
                content += """
                <div class="mb-3">
                  <label for="{key}Text" class="form-label">{label}</label>
                  <input class="form-control" for="{key}Text" type="text" value="{value}" disabled readonly></div>
                """.format(key=key, label=description, value=system_data[key])  # noqa: E501
            except Exception:
                pass

        # finish this fieldset
        content += "</fieldset>"

        return content

    # @app.route('/data')
    async def device_data(self, req: Request) -> None:
        """Provide webpage listing the latest device data as table"""
        latest_data = self._mb_bridge.client_data
        content = await self._render_modbus_data(device_data=latest_data)

        return render_template(template='data.tpl', req=None, content=content)

    # @app.route('/modbus_data')
    async def modbus_data(self, req: Request) -> None:
        """Provide latest modbus data as JSON"""
        # https://microdot.readthedocs.io/en/latest/intro.html#json-responses
        return self._mb_bridge.client_data

    # @app.route('/modbus_data_table')
    async def modbus_data_table(self, req: Request) -> None:
        """Provide latest modbus data table HTML code"""
        latest_data = self._mb_bridge.client_data
        content = await self._render_modbus_data(device_data=latest_data)

        return content

    # @app.route('/info')
    async def system_info(self, req: Request) -> None:
        """Provide webpage listing the latest device data"""
        latest_data = self.system_infos

        # this defines which content is rendered on the webpage
        # the keys listed here will be added with the description provided
        latest_data['description'] = {
            'df': 'Free disk space',
            'free_ram': 'Free RAM',
            'total_ram': 'Total RAM',
            'percentage_ram': 'Percentage of free RAM',
            'frequency': 'System frequency',
            'version': 'Software version Webinterface',
            'version_be_helpers': 'Software version helpers',
            'version_wifi_manager': 'Software version WiFiManager',
            'uptime': 'System uptime'
        }

        content = await self._render_system_info(system_data=latest_data)

        return render_template(template='system.tpl', req=0, content=content)

    # @app.route('/system_data')
    async def system_data(self, req: Request) -> None:
        """Provide latest system data as JSON"""
        # https://microdot.readthedocs.io/en/latest/intro.html#json-responses
        return self.system_infos

    # @app.route('/update')
    async def update_system(self, req: Request) -> None:
        """Provide system update page"""
        res = send_file('/lib/templates/update.tpl')
        res.headers["Content-Type"] = "text/html"

        return res

    # @app.route('/perform_system_update')
    def perform_system_update(self, req: Request) -> None:
        """Process system update"""
        form_data = req.json

        # Whether form data comes from GET or POST request, once parsed,
        # it's available as req.form dictionary
        self.logger.debug('System config user input content: {}'.
                          format(form_data))
        # {
        #     'start_update': True,
        #     'ADDITIONAL_PACKAGES': '',
        #     'UPDATE_TYPE': '1'    # 0: stable, 1: test versions
        # }

        # stop data collection and provisioning threads
        self._mb_bridge.collecting_client_data = False
        self._mb_bridge.provisioning_host_data = False

        # stop WiFi scanning thread
        self._wm.scanning = False

        self._pixel.color = 'yellow'

        # wait a bit to safely finish the may still running threads
        time.sleep(5)

        gc.collect()

        self._update_ongoing = True

        import upip
        index_urls = [
            "https://micropython.org/pi",
            "https://pypi.org/pypi"
        ]
        if form_data.get('UPDATE_TYPE', '0') == '1':
            # 1: test versions
            # if a package is not found on listed indexes the official
            # 'pypi.org/pypi' and 'micropython.org/pi' indexes will be used
            index_urls = [
                'https://test.pypi.org/pypi',
            ] + index_urls
        elif form_data.get('UPDATE_TYPE', '0') == '2':
            # 2: custom pypi server
            index_urls = [
                'http://192.168.178.105:8089',
                'https://test.pypi.org/pypi',
            ] + index_urls
        upip.index_urls = index_urls
        upip.install('myevse-webinterface')
        # 125.147ms, approx. 2 min

        if form_data.get('ADDITIONAL_PACKAGES', ''):
            for package in form_data['ADDITIONAL_PACKAGES'].split(','):
                self.logger.debug('Installing additional custom package: {}'.
                                  format(package.strip()))
                upip.install(package.strip())

        # remove already rendered template to ensure updated ones are shown
        import os
        templates_path = '/lib/templates/'
        for ele in os.listdir(templates_path):
            if ele.endswith('_tpl.py'):
                os.remove(templates_path + ele)

        self.update_complete = True

        return {'success': True}
