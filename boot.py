#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Boot script

Do initial stuff here, similar to the setup() function on Arduino
"""

# system packages
import esp
import machine

# disable ESP os debug output
esp.osdebug(None)

# set clock speed to 240MHz instead of default 160MHz
machine.freq(240000000)
