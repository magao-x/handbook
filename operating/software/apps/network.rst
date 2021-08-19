Networking
==========

Networking apps manage communication internal to the instrument. (They
are distinct from utilities in that they run until killed.)

sshDigger
---------

``sshDigger`` uses the ``autossh`` utility to form a robust ``SSH``
tunnel or port forward to a remote host. In addition, the forked
``autossh`` process is monitored, and if it dies a new one is created.

The base configuration is normally located at
``/opt/MagAOX/config/sshTunnels.conf`` (`view in
magao-x/config <https://github.com/magao-x/config/blob/master/sshTunnels.conf>`__).
It should contain options applicable to all tunnels, as well as the
tunnel definitions themselves.

The tunnel name must be specified with the ``-n`` command line option.
The ``tunnel_name`` denotes the section in the configuration file(s)
which contains the specification of the tunnel. ``sshDigger`` is
normally configured via a base configuration file, hence all other
command-line arguments are optional.

This app does not require that an instance of specific configuration
``tunnel_name.conf`` be available. If one is available matching the name
given with the ``-n tunnel_name`` option, then any settings contained
therein will override those given in the base config file.

Tunnel Specification
~~~~~~~~~~~~~~~~~~~~

Tunnels are specified by a section in the configuration files, normally
the base ``sshTunnels.conf`` file. The section must have the following
members

::

   [tunnel_name]
   remoteHost=resolvable_name
   localPort=X
   remotePort=Y
   compression=true-or-false

Where - ``resolvable_name`` is an ip address or host name. This can
include a user name ``user@`` at the beginning if needed. - ``X``
denotes the integer local port number. - ``Y`` denotes the integer
remote port number - ``true-or-false`` should be either ``true`` or
``false``, and specifies whether this tunnel will use compression, see
below.

This results in ``ssh`` being started with

::

   $ ssh -nNTL X:localhost:Y resolvable_name

by the ``autossh`` utility.

For example, to create an SSH tunnel for ``magaox_aoc_to_rtc_indi``:

::

   $ /opt/MagAOX/bin/sshDigger -n magaox_aoc_to_rtc_indi

Which expects a configuration entry of the form:

::

   [magaox_aoc_to_rtc_indi]
   remoteHost=rtc
   localPort=7630
   remotePort=7624

This then securely forwards traffic from ``localhost:7630`` to the INDI
server on ``rtc:7624``.

Compression
~~~~~~~~~~~

The INDI protocol uses XML, and can therefore be a heavy user of
bandwidth. Tunnels for INDI should normally be compressed for remote
connections, and may be compressed depending on performance for
instrument LAN tunnels.

Tunnels for milkzmq image transfer should NOT be compressed. The images
are already compressed if possible, and the algorithm used by ssh will
not provide significant compression of this type of data. This would
just consume CPU resources without benefit.

xindiserver
-----------

``xindiserver`` wraps the standard ``indiserver`` program in a MagAO-X
interface. This includes exposing configuration options, and capturing
logs which are reformatted in the ``flatlogs`` binary logging system.

Options
~~~~~~~

+-----+-----------------+--------------------+-----------------+-----+
| Sh  | Long            | Config-File \*     | Type            | De  |
| ort |                 |                    |                 | scr |
|     |                 |                    |                 | ipt |
|     |                 |                    |                 | ion |
+=====+=================+====================+=================+=====+
| ``- |                 | indiserver.m       | int             | i   |
| m`` |                 |                    |                 | ndi |
|     |                 |                    |                 | ser |
|     |                 |                    |                 | ver |
|     |                 |                    |                 | ki  |
|     |                 |                    |                 | lls |
|     |                 |                    |                 | cli |
|     |                 |                    |                 | ent |
|     |                 |                    |                 | if  |
|     |                 |                    |                 | it  |
|     |                 |                    |                 | g   |
|     |                 |                    |                 | ets |
|     |                 |                    |                 | m   |
|     |                 |                    |                 | ore |
|     |                 |                    |                 | t   |
|     |                 |                    |                 | han |
|     |                 |                    |                 | t   |
|     |                 |                    |                 | his |
|     |                 |                    |                 | m   |
|     |                 |                    |                 | any |
|     |                 |                    |                 | MB  |
|     |                 |                    |                 | b   |
|     |                 |                    |                 | ehi |
|     |                 |                    |                 | nd, |
|     |                 |                    |                 | d   |
|     |                 |                    |                 | efa |
|     |                 |                    |                 | ult |
|     |                 |                    |                 | 50  |
+-----+-----------------+--------------------+-----------------+-----+
| ``- |                 | indiserver.N       | bool            | in  |
| N`` |                 |                    |                 | dis |
|     |                 |                    |                 | erv |
|     |                 |                    |                 | er: |
|     |                 |                    |                 | ign |
|     |                 |                    |                 | ore |
|     |                 |                    |                 | /tm |
|     |                 |                    |                 | p/n |
|     |                 |                    |                 | oin |
|     |                 |                    |                 | di. |
|     |                 |                    |                 | Ca  |
|     |                 |                    |                 | pit |
|     |                 |                    |                 | ali |
|     |                 |                    |                 | zed |
|     |                 |                    |                 | to  |
|     |                 |                    |                 | av  |
|     |                 |                    |                 | oid |
|     |                 |                    |                 | co  |
|     |                 |                    |                 | nfl |
|     |                 |                    |                 | ict |
|     |                 |                    |                 | w   |
|     |                 |                    |                 | ith |
|     |                 |                    |                 | `   |
|     |                 |                    |                 | `-- |
|     |                 |                    |                 | nam |
|     |                 |                    |                 | e`` |
+-----+-----------------+--------------------+-----------------+-----+
| ``- |                 | indiserver.p       | int             | in  |
| p`` |                 |                    |                 | dis |
|     |                 |                    |                 | erv |
|     |                 |                    |                 | er: |
|     |                 |                    |                 | alt |
|     |                 |                    |                 | ern |
|     |                 |                    |                 | ate |
|     |                 |                    |                 | IP  |
|     |                 |                    |                 | po  |
|     |                 |                    |                 | rt, |
|     |                 |                    |                 | d   |
|     |                 |                    |                 | efa |
|     |                 |                    |                 | ult |
|     |                 |                    |                 | 7   |
|     |                 |                    |                 | 624 |
+-----+-----------------+--------------------+-----------------+-----+
| ``- |                 | indiserver.v       | int             | in  |
| v`` |                 |                    |                 | dis |
|     |                 |                    |                 | erv |
|     |                 |                    |                 | er: |
|     |                 |                    |                 | log |
|     |                 |                    |                 | v   |
|     |                 |                    |                 | erb |
|     |                 |                    |                 | osi |
|     |                 |                    |                 | ty, |
|     |                 |                    |                 | -v, |
|     |                 |                    |                 | -vv |
|     |                 |                    |                 | or  |
|     |                 |                    |                 | -   |
|     |                 |                    |                 | vvv |
+-----+-----------------+--------------------+-----------------+-----+
| ``- |                 | indiserver.x       | bool            | e   |
| x`` |                 |                    |                 | xit |
|     |                 |                    |                 | af  |
|     |                 |                    |                 | ter |
|     |                 |                    |                 | l   |
|     |                 |                    |                 | ast |
|     |                 |                    |                 | cli |
|     |                 |                    |                 | ent |
|     |                 |                    |                 | di  |
|     |                 |                    |                 | sco |
|     |                 |                    |                 | nne |
|     |                 |                    |                 | cts |
|     |                 |                    |                 | –   |
|     |                 |                    |                 | FOR |
|     |                 |                    |                 | PRO |
|     |                 |                    |                 | FIL |
|     |                 |                    |                 | ING |
|     |                 |                    |                 | O   |
|     |                 |                    |                 | NLY |
+-----+-----------------+--------------------+-----------------+-----+
| ``- | ``--local``     | local.drivers      | vector of       | L   |
| L`` |                 |                    | strings         | ist |
|     |                 |                    |                 | of  |
|     |                 |                    |                 | lo  |
|     |                 |                    |                 | cal |
|     |                 |                    |                 | d   |
|     |                 |                    |                 | riv |
|     |                 |                    |                 | ers |
|     |                 |                    |                 | to  |
|     |                 |                    |                 | sta |
|     |                 |                    |                 | rt. |
+-----+-----------------+--------------------+-----------------+-----+
| ``- | ``--remote``    | remote.drivers     | vector of       | L   |
| R`` |                 |                    | string          | ist |
|     |                 |                    |                 | of  |
|     |                 |                    |                 | rem |
|     |                 |                    |                 | ote |
|     |                 |                    |                 | d   |
|     |                 |                    |                 | riv |
|     |                 |                    |                 | ers |
|     |                 |                    |                 | to  |
|     |                 |                    |                 | sta |
|     |                 |                    |                 | rt, |
|     |                 |                    |                 | in  |
|     |                 |                    |                 | the |
|     |                 |                    |                 | f   |
|     |                 |                    |                 | orm |
|     |                 |                    |                 | of  |
|     |                 |                    |                 | n   |
|     |                 |                    |                 | ame |
|     |                 |                    |                 | @ho |
|     |                 |                    |                 | stn |
|     |                 |                    |                 | ame |
|     |                 |                    |                 | w   |
|     |                 |                    |                 | ith |
|     |                 |                    |                 | out |
|     |                 |                    |                 | the |
|     |                 |                    |                 | po  |
|     |                 |                    |                 | rt. |
|     |                 |                    |                 | Ho  |
|     |                 |                    |                 | stn |
|     |                 |                    |                 | ame |
|     |                 |                    |                 | ne  |
|     |                 |                    |                 | eds |
|     |                 |                    |                 | an  |
|     |                 |                    |                 | en  |
|     |                 |                    |                 | try |
|     |                 |                    |                 | in  |
|     |                 |                    |                 | rem |
|     |                 |                    |                 | ote |
|     |                 |                    |                 | .ho |
|     |                 |                    |                 | sts |
+-----+-----------------+--------------------+-----------------+-----+
| ``- | ``--hosts``     | remote.hosts       | vector of       | L   |
| H`` |                 |                    | string          | ist |
|     |                 |                    |                 | of  |
|     |                 |                    |                 | rem |
|     |                 |                    |                 | ote |
|     |                 |                    |                 | hos |
|     |                 |                    |                 | ts, |
|     |                 |                    |                 | in  |
|     |                 |                    |                 | the |
|     |                 |                    |                 | f   |
|     |                 |                    |                 | orm |
|     |                 |                    |                 | of  |
|     |                 |                    |                 | ``  |
|     |                 |                    |                 | hos |
|     |                 |                    |                 | tna |
|     |                 |                    |                 | me[ |
|     |                 |                    |                 | :re |
|     |                 |                    |                 | mot |
|     |                 |                    |                 | e_p |
|     |                 |                    |                 | ort |
|     |                 |                    |                 | ]:l |
|     |                 |                    |                 | oca |
|     |                 |                    |                 | l_p |
|     |                 |                    |                 | ort |
|     |                 |                    |                 | ``. |
|     |                 |                    |                 | ``r |
|     |                 |                    |                 | emo |
|     |                 |                    |                 | te_ |
|     |                 |                    |                 | por |
|     |                 |                    |                 | t`` |
|     |                 |                    |                 | is  |
|     |                 |                    |                 | op  |
|     |                 |                    |                 | tio |
|     |                 |                    |                 | nal |
|     |                 |                    |                 | if  |
|     |                 |                    |                 | it  |
|     |                 |                    |                 | is  |
|     |                 |                    |                 | the |
|     |                 |                    |                 | I   |
|     |                 |                    |                 | NDI |
|     |                 |                    |                 | de  |
|     |                 |                    |                 | fau |
|     |                 |                    |                 | lt. |
+-----+-----------------+--------------------+-----------------+-----+

Driver Specifications
~~~~~~~~~~~~~~~~~~~~~

Lists of driver names are passed to ``xindiserver`` via the
configuration system. Drivers can be either local or remote.

Driver names can not be repeated, whether local or remote.

Local Drivers
^^^^^^^^^^^^^

Drivers running on the same machine are specified by their names only.
On the command line this would be

::

   --local=driverX,driverY,driverZ

and in the configuration file this would be

::

   [local]
   drivers=driverX,driverY,driverZ

Remote Drivers
^^^^^^^^^^^^^^

Drivers running a remote machine are specified by their names and the
name of the SSH tunnel to that machine. ``xindiserver`` parses the
``sshTunnels.conf`` config file as part of configuration.

NOTE: the tunnel specification is by the tunnel name (the section in the
config file), not the host name.

On the command line this would be

::

   --remote=driverR@tunnel_name_1,driverS@tunnel_name_2,driverT@tunnel_name_1

and in the configuration file this would be

::

   [remote]
   drivers=driverR@tunnel_name_1,driverS@tunnel_name_2,driverT@tunnel_name_1

In both cases it must be true that ``sshTunnels.conf`` contains a valid
tunnel specification for ``tunnel_name_1`` and ``tunnel_name_2``.

Exit Status
~~~~~~~~~~~

If there are no errors ``xindiserver`` runs until killed.

If the specified port is already in use, i.e. due to a previously
running ``indiserver``, then ``xindiserver`` will produce a log entry,
change to state FAILURE, and exit.

If the ``indiserver`` process exits for any reason, then ``xindiserver``
will produce a log entry, change to state FAILURE, and exit.

If the ``xindidriver`` program for a driver reports that it can not get
a lock, which indicates that another instance of ``xindidriver`` already
has the FIFO open, then ``xindiserver`` will produce a log entry, change
to state FAILURE, and exit.

Troubleshooting
~~~~~~~~~~~~~~~

If ``indiserver`` exits abnormally (this is extremly rare, and is not
expected except due to operator error!), it can leave the
``xindidriver`` processes running. A subsequent attempt to restart will
fail when new instances of ``xindidriver`` can not lock the FIFOs. The
solution is manually kill each of the ``xindidriver`` processes, which
will have the symlinked names of the ``MagAOXApp`` they are
communicating with. Instructions can be found in the `troubleshooting
guide. <../../troubleshooting.html#killing-indi-zombies>`__
