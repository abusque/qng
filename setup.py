#!/usr/bin/env python3
import sys

import setuptools

# Minimum setuptools version required to parse setup.cfg metadata.
_SETUPTOOLS_MIN_VERSION = '30.3'

if setuptools.__version__ < _SETUPTOOLS_MIN_VERSION:
    print('Error: setuptools version {} '
          'or greater is required'.format(_SETUPTOOLS_MIN_VERSION))
    sys.exit(1)

setuptools.setup()
