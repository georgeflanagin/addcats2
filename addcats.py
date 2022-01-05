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

###
# This project only.
###
from facultydata import departments
from shellcommands import *

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2021'
__credits__ = None
__version__ = 0.1
__maintainer__ = 'George Flanagin'
__email__ = ['me@georgeflanagin.com', 'gflanagin@richmond.edu']
__status__ = 'in progress'
__license__ = 'MIT'


def read_whitespace_file(filename:str) -> tuple:
    with open(filename) as f:
        data = f.read()
    return tuple(" ".join(data.split('\n')).split())
    
    

@trap
def addcats_main(myargs:argparse.Namespace) -> int:
    """
    Generate a file of commands based on the input.
    """
    
    # Each faculty member should have an eponymous group.
    # If this faculty member does not, then we need to
    # setup the faculty user before we do anything else.
    # Faculty also get a shared group (with the "$" 
    # appended).
    
    dollar_group = f"{myargs.faculty}$"
    if not linux_utils.group_exists(myargs.faculty):
        print(add_group(myargs.faculty))
        print(add_group(dollar_group))

    print(manage(myargs.faculty))
    print(add_user_to_group(myargs.faculty, myargs.faculty))
    print(add_user_to_group(myargs.faculty, dollar_group))
    print(add_user_to_group(myargs.faculty, 'faculty'))
    for g in myargs.group:
        if not linux_utils.group_exists(g):
            add_group(g)
        add_user_to_group(myargs.faculty, g)

    netids = whitespace_file(myargs.input)
    for netid in whitespace_file(myargs.input):
        add_user_to_group(netid, 'student')
        add_user_to_group(netid, dollar_group)
        for g in myargs.group:
            add_user_to_group(netid, g)

    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="addcats", 
        description="What addcats does, addcats does best.")

    parser.add_argument('-f', '--faculty', type=str, required=True,
        help="Name of a faculty member.")
    parser.add_argument('-g', '--group', action='append',
        help="Name of additional groups to add to the users.")
    parser.add_argument('-i', '--input', type=str, default="",
        help="Input file name.")
    parser.add_argument('-o', '--output', type=str, default="",
        help="Output file name")
    parser.add_argument('-v', '--verbose', action='store_true', 
        help="Be chatty about what is taking place -- on a scale of 0 to 3")


    myargs = parser.parse_args()
    myargs.verbose and linuxutils.dump_cmdline(myargs)
    if myargs.nice: os.nice(myargs.nice)

    try:
        vm_callable = "{}_main".format(os.path.basename(__file__)[:-3])
        sys.exit(globals()[vm_callable](myargs))

    except Exception as e:
        print(f"Unhandled exception {e}")


