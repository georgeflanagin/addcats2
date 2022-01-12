# addcats
A program to add users to the LDAP groups associated with HPC, 
and then configure the users on spydur and spiderweb

usage: `addcats [-h] [--do-it] -f FACULTY [-g GROUP] [-i INPUT] [-o OUTPUT]`

Create new accounts on Spydur! What addcats does, addcats does best.

optional arguments:
  `-h`, `--help`            show this help message and exit
  `--do-it`               Adding this switch will execute the commands 
                        as the program runs rather than creating a
                        file of commands to be executed.
  `-f FACULTY`, `--faculty FACULTY`
                        Name of a faculty member.
  `-g GROUP`, `--group GROUP`
                        Name of additional groups to add to the users. 
                        Defaults to none.
  `-i INPUT`, `--input INPUT`
                        Input file name with student netids.
  `-o OUTPUT`, `--output OUTPUT`
                        Output file name; defaults to stdout.

Explanation:

FACULTY -- There must be a named faculty member who is sponsoring
the netids for which accounts are being created. A faculty member is
effectively a self-sponsored user. The netids in the INPUT file will be
associated with this faculty member. The faculty member's account will
be created if it does not exist. All faculty are automatically added to
the faculty group and the managed group.

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
as all of the netids in the INPUT file will be added to the named groups.

The OUTPUT "file" will default to stdout if it is not given. Otherwise,
the output of this program is written to whatever file you name.

                        ```**********
                       *** NOTE ***
                        **********```

Ordinary errors are forgiven. For example, repeatedly adding a user to a
group does not create an error or a duplicate entry. Asking for a group
that already exists to be created is ignored. A student netid may be
associated with more than one faculty sponsor. The netids may include
faculty members; thus, co-teaching a class is supported.

An example:

Suppose saif.students contains 'aa1bb bb2cc gflanagi efhutton zz6yy'

These two commands both write the result to newusers.sh:

```
    python addcats.py -f smehkari -i saif.students -g econ -g econ270 -o newusers.sh
    python addcats.py -f smehkari -i saif.students -g econ -g econ270 > newusers.sh
```

smehkari and gflanagi already exist, and smehkari is already a member
of 'econ'.  This is all perfectly OK and logically consistent with the
model of use on both spiderweb and spydur.

- The econ270 group will be created.
- All the named parties will be added to it.
- gflanagi will be added to econ and econ270
- The new faculty member efhutton will be added to all the groups, and will have
    a new account created.
- The student netids will will be added to the groups, have new accounts created,
    and have a link to the shared directory belonging to smehkari, the faculty
    sponsor for this operation.

Sourcing the file "newusers.sh" will make it all happen.

            ```******************************************
            ******** about the --do-it switch ********
            ******************************************```

Regardless of the other arguments, the --do-it switch will cause the
necessary commands to be executed as they are encountered. The execution
takes place in a subprocess that invokes the dorunrun() function in the
HPCLIB. This is most useful when adding a single account where a script
to source is unnecessary.

