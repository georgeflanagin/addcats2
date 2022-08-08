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
# Other standard distro imports
###
import argparse

###
# From hpclib
###
import linuxutils
from   urdecorators import show_exceptions_and_frames as trap

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2022'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'George Flanagin'
__email__ = ['gflanagin@richmond.edu', 'me@georgeflanagin.com']
__status__ = 'in progress'
__license__ = 'MIT'

add_group         = lambda group : f"""sudo /usr/local/sbin/hpcgroupadd {group}"""
add_user_to_group   = lambda user, group : f"""sudo /usr/local/sbin/hpcgpasswd -a {user} {group}"""
drop_user_from_group = lambda user, group : f"""sudo /usr/local/sbin/hpcgpasswd -d {user} {group}"""
manage           = lambda user : f"""sudo /usr/local/sbin/hpcmanage {user}"""
