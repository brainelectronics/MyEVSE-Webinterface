#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from setuptools import setup
import pathlib
import sdist_upip

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

# load elements of version.py
exec(open(here / 'myevse_webinterface' / 'version.py').read())

setup(
    name='myevse-webinterface',
    version=__version__,
    description="MyEVSE Webinterface based on MicroPython",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/brainelectronics/MyEVSE-Webinterface',
    author=__author__,
    author_email='info@brainelectronics.de',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='micropython, brainelectronics, wifi, modbus, myevse',
    project_urls={
        'Bug Reports': 'https://github.com/brainelectronics/MyEVSE-Webinterface/issues',
        'Source': 'https://github.com/brainelectronics/MyEVSE-Webinterface',
    },
    license='MIT',
    cmdclass={'sdist': sdist_upip.sdist},
    packages=['myevse_webinterface'],
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/distutils/setupscript.html#installing-additional-files
    #
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    data_files=[
        (
            'registers',
            [
                'registers/modbusRegisters-MyEVSE.json',
            ]
        ),
        (
            'templates',
            [
                'templates/reboot.tpl',
                'templates/setup.tpl',
            ]
        )
    ],
    install_requires=[
        'micropython-modbus',
        'micropython-winbond',
        'micropython-brainelectronics-helpers',
        'micropython-esp-wifi-manager',
    ]
)
