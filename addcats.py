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
import contextlib
import textwrap

###
# From hpclib
###
import linuxutils
from   urdecorators import trap

###
# This project only.
###

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


add_group            = lambda group : f"""sudo /usr/local/sbin/hpcgroupadd {group}"""
add_user_to_group    = lambda user, group : f"""sudo /usr/local/sbin/hpcgpasswd -a {user} {group}"""
drop_user_from_group = lambda user, group : f"""sudo /usr/local/sbin/hpcgpasswd -d {user} {group}"""
manage               = lambda user : f"""sudo /usr/local/sbin/hpcmanage {user}"""
associate            = lambda student, faculty : f"""sudo -u {student} ln -s /home/{faculty}/shared /home/{student}/shared_{faculty}"""

def read_whitespace_file(filename:str) -> tuple:
    """
    This is a generator that returns the whitespace delimited tokens 
    in a text file, one token at a time.
    """

    if not os.path.isfile(filename):
        sys.stderr.write(f"{filename} cannot be found.")
        return os.EX_NOINPUT

    f = open(filename)
    for _ in (" ".join(f.read().split('\n'))).split():
        yield _
    

addcats_help="""

    Explanation:

    The output file will default to stdout if it is not given. Otherwise,
    the output of this program is written to whatever file you name. 

    The input file should be a whitespace delimited file of netids. They
    can be all on one line, or arbitrarily arranged by lines, including
    blank lines. Each of these netids is automatically added to the student 
    group and the managed group.

    There must be a named faculty member who is sponsoring the netids for
    which accounts are being created. The netids in the file will be associated
    with this faculty member. The faculty member's account will be created
    if it does not exist. All faculty are automatically added to the faculty
    group and the managed group.

    You can name one or more groups of additional association. These groups
    will be created if they do not exist.

    **NOTE** Repeatedly adding a user to a group does not create an error.

    Example:

    These two commands both write the result to newusers.sh:

    python addcats.py -f smehkari -i saif.students -g econ -o newusers.sh
    python addcats.py -f smehkari -i saif.students -g econ > newusers.sh

    """


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
    if not linuxutils.group_exists(myargs.faculty):
        print(add_group(myargs.faculty))
        print(add_group(dollar_group))
        print(manage(myargs.faculty))
        print(add_user_to_group(myargs.faculty, myargs.faculty))
        print(add_user_to_group(myargs.faculty, dollar_group))
        print(add_user_to_group(myargs.faculty, 'faculty'))

    for g in myargs.group:
        if not linuxutils.group_exists(g):
            print(add_group(g))
        print(add_user_to_group(myargs.faculty, g))

    for netid in read_whitespace_file(myargs.input):
        print(add_user_to_group(netid, 'student'))
        print(add_user_to_group(netid, dollar_group))
        print(associate(netid, myargs.faculty))
        for g in myargs.group:
            print(add_user_to_group(netid, g))

    return os.EX_OK


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="addcats", 
        description="What addcats does, addcats does best.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(addcats_help))

    parser.add_argument('-f', '--faculty', type=str, required=True,
        help="Name of a faculty member.")
    parser.add_argument('-g', '--group', action='append', default=[],
        help="Name of additional groups to add to the users. Defaults to none.")
    parser.add_argument('-i', '--input', type=str, default="",
        help="Input file name with student netids.")
    parser.add_argument('-o', '--output', type=str, default="",
        help="Output file name; defaults to stdout.")

    myargs = parser.parse_args()

    try:
        outfile = sys.stdout if not myargs.output else open(myargs.output, 'w')
        with contextlib.redirect_stdout(outfile):
            sys.exit(globals()[f"{os.path.basename(__file__)[:-3]}_main"](myargs))

    except Exception as e:
        print(f"Unhandled exception {e}")
