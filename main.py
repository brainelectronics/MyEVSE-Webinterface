#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Main script

Do your stuff here, this file is similar to the loop() function on Arduino

Create a ModbusBridge betweeen a RTU client (slave) and act as host (master)
on TCP to provide the data of the client and accept settings of new register
values on it.

The register definitions of the client as well as its connection settings like
bus address and UART communication speed are defined in the JSON file at
'registers/modbusRegisters-MyEVSE.json'.
"""

# system packages
# None

# custom packages
# pip installed packages
from myevse_webinterface.webinterface import Webinterface
from myevse_webinterface import version as webinterface_version

print('Setup MyEVSE Webinterface v{}'.format(webinterface_version.__version__))
webinterface = Webinterface()

# perform "boot" steps
webinterface.init_connection()
webinterface.finish_setup()

# perform "main" steps
webinterface.setup_wifi_connection()
webinterface.setup_modbus_connection()
webinterface.start_webinterface()

# will never get beyond here if no KeyboardInterrupt is received
webinterface.wait_for_irq()

print('Leaving application')
