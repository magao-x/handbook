Users and Permissions
====================================================

This document describes the users and permissions structure, and rationale behind it, used on
standard MagAO-X computers.  The software system is designed to make use of this structure and maintain the separation
between the ``operator`` and the ``develoer`` described below.

Users and Groups
++++++++++++++++++++++

xsup: The Operator
------------------------

Only one user, `xsup`, is allowed to operate the MagAO-X instrument.  Here "operate" means starting and stopping
software and issuing commands via the command line, and so doing things such as powering on components and
closing the loop.  It explicitly excludes changing the software configuration
(editing config files) or building and installing software.

It is possible for a non-`xsup` user to change the status of the instrument using INDI,
i.e. with `setINDI` or by running a MagAO-X GUI (whether from a local desktop or connected via ssh tunnel).
While this is obviously "operating" MagAO-X, the key point is that the software that receives and executes
the command, interacting with the hardware, is running under `xsup`.

`xsup` does not have `sudo` privileges.

**Enforcement**: The policy that only `xsup` can run the software is enforced at runtime by verifying that
the user who started the software is the user that owns the **logs** directory, usually under
`/opt/MagAOX/logs`.  MagAO-X applications will exit with an error if this verification fails on startup.

Rationale:
~~~~~~~~~~~~~~~~

    1. It is assumed that `xsup` is relatively untrusted, for instance a visiting astronomer with no expectation to
    change configuration or compile software.  This is the user for which a password is given out, and who is
    typically logged in on the operator workstation (`AOC``).  Thus `xsup` allows us to give needed operator
    access without enabling untrained personnel to make changes that alter the instrument configuration.

    2. Allowing trained and trusted users other than `xsup` to operate the software, while fine from a trust
    perspective, causes many logistical problems with, e.g., varying ownership and permissions of log files
    depending on the user who started the logging process.  This policy helps to avoid these issues.

magaox: The Operator Group
------------------------------

The group `magaox` has filesystem permissions equivalent to user `xsup`.  `xsup` is in group `magaox`,
as are "developers".  A user in `magaox` can not "operate" the software, but can read things such
as logs and recorded images, just as `xsup` can.

Rationale:
~~~~~~~~~~~~~~

    1. This enables the maintainers of the instrument to perform actions such as data backups, inspection of logs,
    and other tasks useful for instrument maintenance.

magaox-dev: The Developer Group
----------------------------------

Only users in the group `magaox-dev` can compile and install instrument software or make changes to the
configuration files.  These users are required to follow the :doc:`standard workflow<hacking>`.

Users in `magaox-dev` have `sudo` privileges.

Rationale:
~~~~~~~~~~~~~~~~~~

    1. This provides a way to control who can make fundamental changes to the way MagAO-X works and control
    access to such privileges.

xdev: The Main Developer
-----------------------------------

The user `xdev` should be the only user who updates software in the main source tree (normally under
`/opt/MagaOX/source`) and compiles software there.

`xdev` has sudo privileges.

Note that users in `magaox-dev` do not need to become `xdev` to install from their `$HOME` directories per
the :doc:`standard workflow<hacking>`.  But they do need to switch to `xdev` to update and install from
`/opt/MagaOX/source`.  Because they have `sudo`, `magaox-dev` users are capable of changing permissions and
ownership in `/opt/MagaOX/source` to bypass this policy.  They shall not do this.

Rationale:
~~~~~~~~~~~~~~~

    1. The main reason for this requirement is that `git` is not well structured for simultaneous multi-user
    development on the same source instance (hence our  :doc:`standard workflow<hacking>`).

    2. This practice also ensures there is a master source of software on each machine to fall back to when
    needed for troubleshooting.

Directories and Permissions
++++++++++++++++++++++++++++++++++++

On a MagAO-X machine `/opt/MagAOX/bin` has the following standard directory structure::

    drwxr-xr-x.    root    root          bin/
    drwxr-xr-x.    xsup    magaox        cacao/
    drwxrwsr-x.    xsup    magaox        calib/
    drwxrwsr-x.    xdev    magaox-dev    config/
    dr-xr-xr-x.    root    root          cpuset/
    drwxrwsr-x.    root    magaox        drivers/
    drwxrwxr-x.    root    magaox        drivers/fifos/
    drwxrwsr-x.    xsup    magaox-dev    logs/
    drwxrwsr-x.    xsup    magaox-dev    rawimages/
    drwx--x--x.    root    root          secrets/
    drwxrwsr-x.    root    magaox-dev    source/
    drwxr-xr-x.    root    root          sys/
    drwxrwsr-x.    xsup    magaox-dev    telem/

The definitive specification for these permissions is maintained in `ensure_dirs_and_perms.sh`_.  Refer to that script
for the most up-to-date setup.

.. _ensure_dirs_and_perms.sh: https://github.com/magao-x/magao-x-setup/blob/main/steps/ensure_dirs_and_perms.sh

setuid
++++++++++

MagAO-X applications are installed with `setuid`.  This enables them to elevate privileges when needed to perform task such as
accessing and configuring a `tty` (USB), changing real-time priority, configuring a thread and moving it to a cpuset,
and other tasks which require root privileges.

The application framework (the MagAOXApp class) mitigates many of the security concerns with `setuid` by always dropping to the
calling user's `uid` (which must be `xsup`) upon construction, and using C++ RAII to scope the elevation when needed.
A wrapper around the system calls for privilege management allows any escalation to be confined to the calling thread rather than
affecting the entire process per POSIX conventions.

One important ramification of this choice is that applications must generally be installed to be executed and tested.  While one
could in principle install to `$HOME/bin`, for instance, we generally just install to `/opt/MagAOX/bin` for testing.
