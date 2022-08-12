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
import functools
import getpass
import socket
import sqlite3
import textwrap
import time

###
# From hpclib
###
from   dorunrun import dorunrun
import fileutils
import linuxutils
import sqlitedb
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

addcats_help="""

    Explanation:

    FACULTY -- There must be a named faculty member who is sponsoring
    the netids for which accounts are being created. A faculty member
    is effectively a self-sponsored user. The netids in the INPUT file will
    be associated with this faculty member. The faculty member's account
    will be created if it does not exist. All faculty are automatically
    added to the faculty group and the managed group.

    The INPUT file should be a whitespace delimited file of netids. They
    can be all on one line, or arbitrarily arranged by lines, including
    blank lines. Each of these netids is automatically added to the student 
    group and the managed group. The file is searched for in the following
    locations: $PWD, $OLDPWD, $HOME, and /scratch/{user-running-program}.

    If the INPUT file cannot be found, the program assumes that it is the
    netid of a single user to be processed. IOW, "-i netids" where the
    netids file contains only "gflanagi" is the same as "-i gflanagi". This
    feature makes it easier to support adding single users in an add-drop
    situation.

    You can name one or more GROUPs of additional association. These groups
    will be created if they do not exist, and the FACULTY sponsor as well
    as all of the netids in the INPUT file will be added to the named
    groups.

    The OUTPUT "file" will default to stdout if it is not given. Otherwise,
    the output of this program is written to whatever file you name. 

                            **********
                           *** NOTE *** 
                            **********

    Ordinary errors are forgiven. For example, repeatedly adding a user to 
    a group does not create an error or a duplicate entry. Asking for a
    group that already exists to be created is ignored. A student netid
    may be associated with more than one faculty sponsor. The netids may
    include faculty members; thus, co-teaching a class is supported.

    An example:

    Suppose saif.students contains 'aa1bb bb2cc gflanagi efhutton zz6yy'

    These two commands both write the result to newusers.sh:

        python addcats.py -f smehkari -i saif.students -g econ -g econ270 -o newusers.sh

        python addcats.py -f smehkari -i saif.students -g econ -g econ270 > newusers.sh

    smehkari and gflanagi already exist, and smehkari is already a member of 'econ'.
    This is all perfectly OK and logically consistent with the model of use on
    both spiderweb and spydur. 

    - The econ270 group will be created.
    - All the named parties will be added to it.
    - gflanagi will be added to econ and econ270
    - The new faculty member efhutton will be added to all the groups, and will have
        a new account created.
    - The student netids will will be added to the groups, have new accounts created,
        and have a link to the shared directory belonging to smehkari, the faculty 
        sponsor for this operation.

    Sourcing the file "newusers.sh" will make it all happen.     

                            ******************************************
                            ******** about the --do-it switch ********
                            ******************************************
    
    Regardless of the other arguments, the --do-it switch will cause the necessary
    commands to be executed as they are encountered. The execution takes place
    in a subprocess that invokes the dorunrun() function in the HPCLIB. This is
    most useful when adding a single account where a script to source is unnecessary.  

    """
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

foo = object
this_is_the_webserver = socket.gethostname() == 'spdrweb.richmond.edu'
this_is_the_cluster   = not this_is_the_webserver


SQL = linuxutils.SloppyDict({ 
    "newfaculty":"INSERT INTO faculty_master VALUES (?)",
    "facultypartition":"INSERT INTO faculty_partitions VALUES (?, ?)",
    "facultystudent":"INSERT INTO faculty_student VALUES (?, ?)"
    })


@trap
def addfaculty(db:sqlitedb.SQLiteDB, netid:str) -> bool:
    """
    Perform the addition, and trap any exceptions so that one
    can forgive duplicates and simply return False.
    """
    global foo
    dollar_group = f"{netid}$"

    try:
        db.execute_SQL(SQL.newfaculty, netid)            
        db.execute_SQL(SQL.facultypartition, netid, 'basic')
        db.execute_SQL(SQL.facultypartition, netid, 'medium')
        db.execute_SQL(SQL.facultypartition, netid, 'large')
        db.execute_SQL(SQL.facultypartition, netid, 'ML')
        db.execute_SQL(SQL.facultypartition, netid, 'sci')
        foo(add_group(netid))
        foo(add_group(dollar_group))
        foo(manage(netid))
        foo(add_user_to_group(netid, netid))
        foo(add_user_to_group(netid, dollar_group))
        foo(add_user_to_group(netid, 'faculty'))
        foo(chmod_home_dir(netid))
        this_is_the_cluster and foo(make_shared_dir(netid))
        this_is_the_cluster and foo(chgrp_shared_dir(netid))
        this_is_the_cluster and foo(chmod_shared_dir(netid))
        
        result = db.commit()

    except sqlite3.IntegrityError as e:
        print(f"Faculty member {netid} is already in faculty_master")
        # Forgive a duplicate
        return True

    except sqlite3.OperationalError as e:
        print(f"While adding {netid}, this happened: {e}")
        return False

    except Exception as e:
        print(f"While adding {netid}, this happened: {e}")
        sys.exit(os.EX_IOERR)

    else:
        if not result:
            print("commit failed adding new faculty")
            sys.exit(os.EX_IOERR)
            return False

    return True


@trap
def addcats_main(myargs:argparse.Namespace) -> int:
    """
    Generate a file of commands based on the input.
    """
    db = sqlitedb.SQLiteDB(myargs.db)

    # Eliminate duplicate groups.
    myargs.group = list(set(myargs.group))

    # This is a hack. The jupyterhub group is a slightly fictional
    # group that allows users to run jupyterhub.
    if this_is_the_webserver and 'jupyterhub' not in myargs.group: 
        myargs.group.append('jupyterhub')
    elif this_is_the_cluster and 'jupyterhub' in myargs.group:
        myargs.group.remove('jupyterhub')
    else:
        pass
    
    #####
    # Each faculty member should have an eponymous group.
    # If this faculty member does not, then we need to
    # setup the faculty user before we do anything else.
    # Faculty also get a shared group (with the "$" 
    # appended).
    #
    # Several operations produce bad results on spiderweb
    # because of the restricted file system. Thus the use
    # of "this_is_the_cluster and" preceding some operations.
    # 
    # every faculty member is a part of the faculty group, so if the
    # the named netid is only a member of 'people', then we need to
    # create this account also.
    #####
    if not linuxutils.is_faculty(myargs.faculty):
        print(f"{myargs.faculty} does not appear to be faculty.")
        print(f"Please add {myargs.faculty} manually, and then re-run this program.")
        sys.exit(os.EX_NOUSER)

    # If a netid is valid but there is no existing account, 
    # then the netid will be a member of people (only).
    addfaculty(db, myargs.faculty)

    # Let's check to see if we need to add groups.
    for g in myargs.group:
        not linuxutils.group_exists(g) and foo(add_group(g))
        # No need to check on this; if a user is already in a group,
        # adding the user a second time will make no difference.
        foo(add_user_to_group(myargs.faculty, g))
        

    # The input is either a file of netids, or it /is/ the netid,
    # and there is only one of them. This is to make it easier
    # to add only one user which during add-drop and mid-semester
    # is a fairly common event.
    if (f := fileutils.home_and_away(myargs.input)):
        netids = fileutils.read_whitespace_file(f)
    else:
        netids = (myargs.input,)

    # Adding non-faculty is much simpler than adding faculty. Non-faculty
    # get their authorizations from faculty associations.
    for netid in netids:
        # Again, if the netid is already managed, this is not an error.
        foo(manage(netid))
        try:
            db.execute_SQL(SQL.facultystudent, myargs.faculty, netid)
            db.commit()
        except sqlite3.IntegrityError as e:
            pass

            
        foo(chmod_home_dir(netid))
        foo(add_user_to_group(netid, 'student'))
        foo(add_user_to_group(netid, f'{myargs.faculty}$'))
        this_is_the_cluster and foo(associate(netid, myargs.faculty))
        for g in myargs.group:
            foo(add_user_to_group(netid, g))

    return os.EX_OK


if __name__ == '__main__':
    
    if getpass.getuser() not in ('root', 'installer'):
        sys.stderr.write('You must log in as "installer" to execute the output of this program!\n')
        time.sleep(5)

    parser = argparse.ArgumentParser(prog="addcats", 
        description="Create new accounts on Spydur!\nWhat addcats does, addcats does best.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(addcats_help))


    parser.add_argument('--do-it', action='store_true', 
        help="Adding this switch will execute the commands \
as the program runs rather than creating a file \
of commands to be executed.")
    parser.add_argument('-f', '--faculty', type=str, required=True,
        help="Name of a faculty member.")
    parser.add_argument('-g', '--group', action='append', default=[],
        help="Name of additional groups to add to the users. Defaults to none.")
    parser.add_argument('-i', '--input', type=str, default="",
        help="Input file name with student netids.")
    parser.add_argument('-o', '--output', type=str, default="",
        help="Output file name; defaults to stdout.")
    parser.add_argument('--db', type=str, default="/home/installer/addcats/affinity.db")

    myargs = parser.parse_args()
    ###
    # Note what this does. foo will always be the name we call. Sometimes it
    # prints the command and sometimes it executes the command.
    ###
    foo = functools.partial(dorunrun, return_datatype=str) if myargs.do_it else print

    try:
        outfile = sys.stdout if not myargs.output else open(myargs.output, 'w')
        with contextlib.redirect_stdout(outfile):
            sys.exit(globals()[f"{os.path.basename(__file__)[:-3]}_main"](myargs))

    except Exception as e:
        print(f"Unhandled or leaked exception {e}")
