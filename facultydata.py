# -*- coding: utf-8 -*-
import typing
from   typing import *

min_py = (3, 8)

###
# Standard imports, starting with os and sys
###
import os
import sys
if sys.version_info < min_py:
    print(f"This program requires Python {min_py[0]}.{min_py[1]}, or higher.")
    sys.exit(os.EX_SOFTWARE)

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2022, 2025'
__credits__ = None
__version__ = 1.1
__maintainer__ = 'George Flanagin'
__email__ = ['gflanagin@richmond.edu', 'me@georgeflanagin.com']
__status__ = 'in progress'
__license__ = 'MIT'

# This is a list of the valid, 4-letter codes for department
# affinities within HPC. They do not map exactly to the
# University's concept of departments.
departments = (
    'biol', 'chem', 'csci', 'dhum', 'econ', 'lang',
    'laws', 'maps', 'math', 'musi', 'phys', 'psyc'
    )

partitions = ('basic', 'medium', 'large', 'sci', 'ML')
