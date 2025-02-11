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

#####################################################
# dn: cn=dbagrp,ou=groups,dc=richmond,dc=edu
# changetype: modify
# add: memberuid
# memberuid: adam
#####################################################

add_group            = lambda group : f"""sudo /usr/local/sbin/hpcgroupadd {group}"""
add_user_to_group    = lambda user, group : f"""sudo /usr/local/sbin/hpcgpasswd -a {user} {group}"""
drop_user_from_group = lambda user, group : f"""sudo /usr/local/sbin/hpcgpasswd -d {user} {group}"""
manage               = lambda user : f"""sudo /usr/local/sbin/hpcmanage {user}"""
associate            = lambda student, faculty : f"""sudo -u {student} ln -s /home/{faculty}/shared /home/{student}/shared_{faculty}"""
make_shared_dir      = lambda faculty : f"""sudo -u {faculty} mkdir -p /home/{faculty}/shared"""
chgrp_shared_dir     = lambda faculty : f"""sudo -u {faculty} chgrp {faculty}$ /home/{faculty}/shared"""
chmod_shared_dir     = lambda faculty : f"""sudo -u {faculty} chmod 2770 /home/{faculty}/shared"""
chmod_home_dir       = lambda u : f"""sudo -u {u} chmod 2711 /home/{u}"""

make_mailbox         = lambda faculty : f"""sudo -u {faculty} mkdir -p /home/{faculty}/mailbox"""
chmod_mailbox        = lambda faculty : f"""sudo -u {faculty} chmod 2730 /home/{faculty}/mailbox"""
chgrp_mailbox        = lambda faculty : f"""sudo -u {faculty} chgrp {faculty}$ /home/{faculty}/mailbox"""

