Power control devices
=====================

Power control devices share some common functionality through the
MagAO-X
`outletController <https://github.com/magao-x/MagAOX/blob/master/libMagAOX/app/dev/outletController.hpp>`__.

Common INDI properties
----------------------

Read/write Properties
~~~~~~~~~~~~~~~~~~~~~

Channel states are reported by the property with the channel name, and
state changes can be requested by the same property. The ``target``
element contains the last requested state until the ``state`` element,
which is the current state, matches it. Changing either ``state`` or
``target`` will request a state change in that channel.

::

   <name>.<channelName>.state = On | Int | Off
   <name>.<channelName>.target = On | Off | [empty]

Read-only Properties
~~~~~~~~~~~~~~~~~~~~

The status property gives the reported device status. This does not
appear to be useful.

::

   <name>.status.value = ?

The ``load`` property gives the line frequency, line voltage, and drawn
current as reported by the device.

::

   <name>.load.frequency = [Hz]
   <name>.load.voltage = [V]
   <name>.load.current = [A]

Each outlet has a property which indicates its current state.

::

   <name>.outlet<N>.state = On | Int | Off

Channel Configuration
---------------------

The outlets are controlled in channels, which consist of at least one
outlet. Channels are configured as sections in the configuration file.
Any section name, say ``[channel1]``, which has either a ``oulet=`` or
``outlets=`` keyword will be treated as a channel specification.

The ``oulet=`` or ``outlets=`` keyword=value pair specifies which outlet
or outlets are controlled by this channel. Multiple outlets are
specified in an comma separated list.

You can also specify the order in which the outlets are turnned on with
the ``onOrder`` and ``offOrder`` keywords. The values contain indices in
the vector specified by the ``outlet``/``outlets`` keyword, not the
outlet numbers. So if you have ``outlets=7,8`` you would then have
``onOrder=1,0`` to turn on outlet 8 first, then outlet 7.

You can use ``onDelays`` and ``offDelays``, to specify the delays
between outlet operations in milliseconds. The first entry is always
ignored, then the second entry specifies the delay between the first and
second outlet operation, etc.

An example config file section is:

::

   [sue]           #this channel will be named sue
   outlets=4,5     #this channel uses outlets 4 and 5
   onOrder=1,0     #outlet 5 will be turned on first
   offOrder=0,1    #Outlet 4 will be turned off first
   onDelays=0,150  #a 150 msec delay between outlet turn on
   offDelays=0,345 #a 345 msec delay between outlet turn off

trippLitePDU
------------

``trippLitePDU`` provides an interface to a Tripp Lite power
distribution unit. INDI properties provide the status of each outlet, as
well as line power status.

Driver-specific options
~~~~~~~~~~~~~~~~~~~~~~~

+-----+-------------------------+----------------------+------------+---+
| Sh  | Long                    | Config-File          | Type       | D |
| ort |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | c |
|     |                         |                      |            | r |
|     |                         |                      |            | i |
|     |                         |                      |            | p |
|     |                         |                      |            | t |
|     |                         |                      |            | i |
|     |                         |                      |            | o |
|     |                         |                      |            | n |
+=====+=========================+======================+============+===+
| ``- | ``--device.address``    | device.address       | string     | T |
| a`` |                         |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | d |
|     |                         |                      |            | e |
|     |                         |                      |            | v |
|     |                         |                      |            | i |
|     |                         |                      |            | c |
|     |                         |                      |            | e |
|     |                         |                      |            | a |
|     |                         |                      |            | d |
|     |                         |                      |            | d |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | s |
|     |                         |                      |            | . |
+-----+-------------------------+----------------------+------------+---+
| ``- | ``--device.port``       | device.port          | string     | T |
| p`` |                         |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | d |
|     |                         |                      |            | e |
|     |                         |                      |            | v |
|     |                         |                      |            | i |
|     |                         |                      |            | c |
|     |                         |                      |            | e |
|     |                         |                      |            | p |
|     |                         |                      |            | o |
|     |                         |                      |            | r |
|     |                         |                      |            | t |
|     |                         |                      |            | . |
+-----+-------------------------+----------------------+------------+---+
| ``- | ``--device.username``   | device.username      | string     | T |
| u`` |                         |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | d |
|     |                         |                      |            | e |
|     |                         |                      |            | v |
|     |                         |                      |            | i |
|     |                         |                      |            | c |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | o |
|     |                         |                      |            | g |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | u |
|     |                         |                      |            | s |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | n |
|     |                         |                      |            | a |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | . |
+-----+-------------------------+----------------------+------------+---+
|     | ``--device.passfile``   | device.passfile      | string     | T |
|     |                         |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | d |
|     |                         |                      |            | e |
|     |                         |                      |            | v |
|     |                         |                      |            | i |
|     |                         |                      |            | c |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | o |
|     |                         |                      |            | g |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | p |
|     |                         |                      |            | a |
|     |                         |                      |            | s |
|     |                         |                      |            | s |
|     |                         |                      |            | w |
|     |                         |                      |            | o |
|     |                         |                      |            | r |
|     |                         |                      |            | d |
|     |                         |                      |            | f |
|     |                         |                      |            | i |
|     |                         |                      |            | l |
|     |                         |                      |            | e |
|     |                         |                      |            | ( |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | a |
|     |                         |                      |            | t |
|     |                         |                      |            | i |
|     |                         |                      |            | v |
|     |                         |                      |            | e |
|     |                         |                      |            | t |
|     |                         |                      |            | o |
|     |                         |                      |            | s |
|     |                         |                      |            | e |
|     |                         |                      |            | c |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | t |
|     |                         |                      |            | s |
|     |                         |                      |            | d |
|     |                         |                      |            | i |
|     |                         |                      |            | r |
|     |                         |                      |            | ) |
|     |                         |                      |            | . |
+-----+-------------------------+----------------------+------------+---+
|     | `                       | device.readTimeout   | int        | t |
|     | `--device.readTimeout`` |                      |            | i |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | o |
|     |                         |                      |            | u |
|     |                         |                      |            | t |
|     |                         |                      |            | f |
|     |                         |                      |            | o |
|     |                         |                      |            | r |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | a |
|     |                         |                      |            | d |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | g |
|     |                         |                      |            | f |
|     |                         |                      |            | r |
|     |                         |                      |            | o |
|     |                         |                      |            | m |
|     |                         |                      |            | d |
|     |                         |                      |            | e |
|     |                         |                      |            | v |
|     |                         |                      |            | i |
|     |                         |                      |            | c |
|     |                         |                      |            | e |
+-----+-------------------------+----------------------+------------+---+
|     | ``                      | device.writeTimeout  | int        | t |
|     | --device.writeTimeout`` |                      |            | i |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | o |
|     |                         |                      |            | u |
|     |                         |                      |            | t |
|     |                         |                      |            | f |
|     |                         |                      |            | o |
|     |                         |                      |            | r |
|     |                         |                      |            | w |
|     |                         |                      |            | r |
|     |                         |                      |            | i |
|     |                         |                      |            | t |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | g |
|     |                         |                      |            | t |
|     |                         |                      |            | o |
|     |                         |                      |            | d |
|     |                         |                      |            | e |
|     |                         |                      |            | v |
|     |                         |                      |            | i |
|     |                         |                      |            | c |
|     |                         |                      |            | e |
+-----+-------------------------+----------------------+------------+---+
|     | ``--time                | timeo                | int        | T |
|     | outs.outletStateDelay`` | uts.outletStateDelay |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | m |
|     |                         |                      |            | a |
|     |                         |                      |            | x |
|     |                         |                      |            | i |
|     |                         |                      |            | m |
|     |                         |                      |            | u |
|     |                         |                      |            | m |
|     |                         |                      |            | t |
|     |                         |                      |            | i |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | t |
|     |                         |                      |            | o |
|     |                         |                      |            | w |
|     |                         |                      |            | a |
|     |                         |                      |            | i |
|     |                         |                      |            | t |
|     |                         |                      |            | f |
|     |                         |                      |            | o |
|     |                         |                      |            | r |
|     |                         |                      |            | a |
|     |                         |                      |            | n |
|     |                         |                      |            | o |
|     |                         |                      |            | u |
|     |                         |                      |            | t |
|     |                         |                      |            | l |
|     |                         |                      |            | e |
|     |                         |                      |            | t |
|     |                         |                      |            | t |
|     |                         |                      |            | o |
|     |                         |                      |            | c |
|     |                         |                      |            | h |
|     |                         |                      |            | a |
|     |                         |                      |            | n |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | t |
|     |                         |                      |            | a |
|     |                         |                      |            | t |
|     |                         |                      |            | e |
|     |                         |                      |            | [ |
|     |                         |                      |            | m |
|     |                         |                      |            | s |
|     |                         |                      |            | e |
|     |                         |                      |            | c |
|     |                         |                      |            | ] |
|     |                         |                      |            | . |
|     |                         |                      |            | D |
|     |                         |                      |            | e |
|     |                         |                      |            | f |
|     |                         |                      |            | a |
|     |                         |                      |            | u |
|     |                         |                      |            | l |
|     |                         |                      |            | t |
|     |                         |                      |            | = |
|     |                         |                      |            | 5 |
|     |                         |                      |            | 0 |
|     |                         |                      |            | 0 |
|     |                         |                      |            | 0 |
+-----+-------------------------+----------------------+------------+---+
|     | `                       | limits.freqLowWarn   | int        | T |
|     | `--limits.freqLowWarn`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | o |
|     |                         |                      |            | w |
|     |                         |                      |            | - |
|     |                         |                      |            | f |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | q |
|     |                         |                      |            | u |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | w |
|     |                         |                      |            | a |
|     |                         |                      |            | r |
|     |                         |                      |            | n |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | g |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``                      | limits.freqHighWarn  | int        | T |
|     | --limits.freqHighWarn`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | f |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | q |
|     |                         |                      |            | u |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | w |
|     |                         |                      |            | a |
|     |                         |                      |            | r |
|     |                         |                      |            | n |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | g |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``                      | limits.freqLowAlert  | int        | T |
|     | --limits.freqLowAlert`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | o |
|     |                         |                      |            | w |
|     |                         |                      |            | - |
|     |                         |                      |            | f |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | q |
|     |                         |                      |            | u |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | a |
|     |                         |                      |            | l |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | t |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``-                     | limits.freqHighAlert | int        | T |
|     | -limits.freqHighAlert`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | f |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | q |
|     |                         |                      |            | u |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | a |
|     |                         |                      |            | l |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | t |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``                      | limits.freqLowEmerg  | int        | T |
|     | --limits.freqLowEmerg`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | o |
|     |                         |                      |            | w |
|     |                         |                      |            | - |
|     |                         |                      |            | f |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | q |
|     |                         |                      |            | u |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | e |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``-                     | limits.freqHighEmerg | int        | T |
|     | -limits.freqHighEmerg`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | f |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | q |
|     |                         |                      |            | u |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | e |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | `                       | limits.voltLowWarn   | int        | T |
|     | `--limits.voltLowWarn`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | o |
|     |                         |                      |            | w |
|     |                         |                      |            | - |
|     |                         |                      |            | v |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | t |
|     |                         |                      |            | a |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | w |
|     |                         |                      |            | a |
|     |                         |                      |            | r |
|     |                         |                      |            | n |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | g |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``                      | limits.voltHighWarn  | int        | T |
|     | --limits.voltHighWarn`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | v |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | t |
|     |                         |                      |            | a |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | w |
|     |                         |                      |            | a |
|     |                         |                      |            | r |
|     |                         |                      |            | n |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | g |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``                      | limits.voltLowAlert  | int        | T |
|     | --limits.voltLowAlert`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | o |
|     |                         |                      |            | w |
|     |                         |                      |            | - |
|     |                         |                      |            | v |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | t |
|     |                         |                      |            | a |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | a |
|     |                         |                      |            | l |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | t |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``-                     | limits.voltHighAlert | int        | T |
|     | -limits.voltHighAlert`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | v |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | t |
|     |                         |                      |            | a |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | a |
|     |                         |                      |            | l |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | t |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``                      | limits.voltLowEmerg  | int        | T |
|     | --limits.voltLowEmerg`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | l |
|     |                         |                      |            | o |
|     |                         |                      |            | w |
|     |                         |                      |            | - |
|     |                         |                      |            | v |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | t |
|     |                         |                      |            | a |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | e |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``-                     | limits.voltHighEmerg | int        | T |
|     | -limits.voltHighEmerg`` |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | v |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | t |
|     |                         |                      |            | a |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | e |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``--limits.currWarn``   | limits.currWarn      | int        | T |
|     |                         |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | c |
|     |                         |                      |            | u |
|     |                         |                      |            | r |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | t |
|     |                         |                      |            | w |
|     |                         |                      |            | a |
|     |                         |                      |            | r |
|     |                         |                      |            | n |
|     |                         |                      |            | i |
|     |                         |                      |            | n |
|     |                         |                      |            | g |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``--limits.currAlert``  | limits.currAlert     | int        | T |
|     |                         |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | c |
|     |                         |                      |            | u |
|     |                         |                      |            | r |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | t |
|     |                         |                      |            | a |
|     |                         |                      |            | l |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | t |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+
|     | ``--limits.currEmerg``  | limits.currEmerg     | int        | T |
|     |                         |                      |            | h |
|     |                         |                      |            | e |
|     |                         |                      |            | h |
|     |                         |                      |            | i |
|     |                         |                      |            | g |
|     |                         |                      |            | h |
|     |                         |                      |            | - |
|     |                         |                      |            | c |
|     |                         |                      |            | u |
|     |                         |                      |            | r |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | t |
|     |                         |                      |            | e |
|     |                         |                      |            | m |
|     |                         |                      |            | e |
|     |                         |                      |            | r |
|     |                         |                      |            | g |
|     |                         |                      |            | e |
|     |                         |                      |            | n |
|     |                         |                      |            | c |
|     |                         |                      |            | y |
|     |                         |                      |            | t |
|     |                         |                      |            | h |
|     |                         |                      |            | r |
|     |                         |                      |            | e |
|     |                         |                      |            | s |
|     |                         |                      |            | h |
|     |                         |                      |            | o |
|     |                         |                      |            | l |
|     |                         |                      |            | d |
+-----+-------------------------+----------------------+------------+---+

Troubleshooting
~~~~~~~~~~~~~~~

Device not responding
^^^^^^^^^^^^^^^^^^^^^

If the device stops responding on the CLI port. A fix is to login via
ssh, e.g.

::

   $ ssh localadmin@x.x.x.x

You will need the current password for this device. Once logged in,
navigate to the menu choice to ``Restart PowerAlert``.

::

   2- System Configuration

      7- Restart PowerAlert

         1- Restart PowerAlert Now

This can take a loooooong time to reboot.

If the software reboot doesn’t fix it, reset the device using the
recessed reset button under the ethernet adapter.

If that doesn’t work, you need to completely unplug the device to force
a full reset.

xt1121DCDU
----------

``xt1121DCDU`` provides an interface to a xt1121-based D.C. distribution
unit. This is an Electronics-Salon D-228 relay module controlled by an
Acromag xt1121 digital I/O module.

.. _driver-specific-options-1:

Driver-specific options
~~~~~~~~~~~~~~~~~~~~~~~

+-----+------------------------+---------------------+-------------+---+
| Sh  | Long                   | Config-File \*      | Type        | D |
| ort |                        |                     |             | e |
|     |                        |                     |             | s |
|     |                        |                     |             | c |
|     |                        |                     |             | r |
|     |                        |                     |             | i |
|     |                        |                     |             | p |
|     |                        |                     |             | t |
|     |                        |                     |             | i |
|     |                        |                     |             | o |
|     |                        |                     |             | n |
+=====+========================+=====================+=============+===+
|     | ``--power.device``     | power.device        | string      | D |
|     |                        |                     |             | e |
|     |                        |                     |             | v |
|     |                        |                     |             | i |
|     |                        |                     |             | c |
|     |                        |                     |             | e |
|     |                        |                     |             | c |
|     |                        |                     |             | o |
|     |                        |                     |             | n |
|     |                        |                     |             | t |
|     |                        |                     |             | r |
|     |                        |                     |             | o |
|     |                        |                     |             | l |
|     |                        |                     |             | l |
|     |                        |                     |             | i |
|     |                        |                     |             | n |
|     |                        |                     |             | g |
|     |                        |                     |             | p |
|     |                        |                     |             | o |
|     |                        |                     |             | w |
|     |                        |                     |             | e |
|     |                        |                     |             | r |
|     |                        |                     |             | f |
|     |                        |                     |             | o |
|     |                        |                     |             | r |
|     |                        |                     |             | t |
|     |                        |                     |             | h |
|     |                        |                     |             | i |
|     |                        |                     |             | s |
|     |                        |                     |             | a |
|     |                        |                     |             | p |
|     |                        |                     |             | p |
|     |                        |                     |             | ’ |
|     |                        |                     |             | s |
|     |                        |                     |             | d |
|     |                        |                     |             | e |
|     |                        |                     |             | v |
|     |                        |                     |             | i |
|     |                        |                     |             | c |
|     |                        |                     |             | e |
|     |                        |                     |             | ( |
|     |                        |                     |             | I |
|     |                        |                     |             | N |
|     |                        |                     |             | D |
|     |                        |                     |             | I |
|     |                        |                     |             | n |
|     |                        |                     |             | a |
|     |                        |                     |             | m |
|     |                        |                     |             | e |
|     |                        |                     |             | ) |
|     |                        |                     |             | . |
+-----+------------------------+---------------------+-------------+---+
|     | ``--power.channel``    | power.channel       | string      | C |
|     |                        |                     |             | h |
|     |                        |                     |             | a |
|     |                        |                     |             | n |
|     |                        |                     |             | n |
|     |                        |                     |             | e |
|     |                        |                     |             | l |
|     |                        |                     |             | o |
|     |                        |                     |             | n |
|     |                        |                     |             | d |
|     |                        |                     |             | e |
|     |                        |                     |             | v |
|     |                        |                     |             | i |
|     |                        |                     |             | c |
|     |                        |                     |             | e |
|     |                        |                     |             | f |
|     |                        |                     |             | o |
|     |                        |                     |             | r |
|     |                        |                     |             | t |
|     |                        |                     |             | h |
|     |                        |                     |             | i |
|     |                        |                     |             | s |
|     |                        |                     |             | a |
|     |                        |                     |             | p |
|     |                        |                     |             | p |
|     |                        |                     |             | ’ |
|     |                        |                     |             | s |
|     |                        |                     |             | d |
|     |                        |                     |             | e |
|     |                        |                     |             | v |
|     |                        |                     |             | i |
|     |                        |                     |             | c |
|     |                        |                     |             | e |
|     |                        |                     |             | ( |
|     |                        |                     |             | I |
|     |                        |                     |             | N |
|     |                        |                     |             | D |
|     |                        |                     |             | I |
|     |                        |                     |             | n |
|     |                        |                     |             | a |
|     |                        |                     |             | m |
|     |                        |                     |             | e |
|     |                        |                     |             | ) |
|     |                        |                     |             | . |
+-----+------------------------+---------------------+-------------+---+
|     | ``--power.element``    | power.element       | string      | I |
|     |                        |                     |             | N |
|     |                        |                     |             | D |
|     |                        |                     |             | I |
|     |                        |                     |             | e |
|     |                        |                     |             | l |
|     |                        |                     |             | e |
|     |                        |                     |             | m |
|     |                        |                     |             | e |
|     |                        |                     |             | n |
|     |                        |                     |             | t |
|     |                        |                     |             | n |
|     |                        |                     |             | a |
|     |                        |                     |             | m |
|     |                        |                     |             | e |
|     |                        |                     |             | . |
|     |                        |                     |             | D |
|     |                        |                     |             | e |
|     |                        |                     |             | f |
|     |                        |                     |             | a |
|     |                        |                     |             | u |
|     |                        |                     |             | l |
|     |                        |                     |             | t |
|     |                        |                     |             | i |
|     |                        |                     |             | s |
|     |                        |                     |             | “ |
|     |                        |                     |             | s |
|     |                        |                     |             | t |
|     |                        |                     |             | a |
|     |                        |                     |             | t |
|     |                        |                     |             | e |
|     |                        |                     |             | ” |
|     |                        |                     |             | , |
|     |                        |                     |             | o |
|     |                        |                     |             | n |
|     |                        |                     |             | l |
|     |                        |                     |             | y |
|     |                        |                     |             | n |
|     |                        |                     |             | e |
|     |                        |                     |             | e |
|     |                        |                     |             | d |
|     |                        |                     |             | t |
|     |                        |                     |             | o |
|     |                        |                     |             | s |
|     |                        |                     |             | p |
|     |                        |                     |             | e |
|     |                        |                     |             | c |
|     |                        |                     |             | i |
|     |                        |                     |             | f |
|     |                        |                     |             | y |
|     |                        |                     |             | i |
|     |                        |                     |             | f |
|     |                        |                     |             | d |
|     |                        |                     |             | i |
|     |                        |                     |             | f |
|     |                        |                     |             | f |
|     |                        |                     |             | e |
|     |                        |                     |             | r |
|     |                        |                     |             | e |
|     |                        |                     |             | n |
|     |                        |                     |             | t |
|     |                        |                     |             | . |
+-----+------------------------+---------------------+-------------+---+
|     | ``--device.name``      | device.name         | string      | T |
|     |                        |                     |             | h |
|     |                        |                     |             | e |
|     |                        |                     |             | d |
|     |                        |                     |             | e |
|     |                        |                     |             | v |
|     |                        |                     |             | i |
|     |                        |                     |             | c |
|     |                        |                     |             | e |
|     |                        |                     |             | I |
|     |                        |                     |             | N |
|     |                        |                     |             | D |
|     |                        |                     |             | I |
|     |                        |                     |             | n |
|     |                        |                     |             | a |
|     |                        |                     |             | m |
|     |                        |                     |             | e |
|     |                        |                     |             | . |
+-----+------------------------+---------------------+-------------+---+
|     | ``--d                  | de                  | vector      | T |
|     | evice.channelNumbers`` | vice.channelNumbers |             | h |
|     |                        |                     |             | e |
|     |                        |                     |             | c |
|     |                        |                     |             | h |
|     |                        |                     |             | a |
|     |                        |                     |             | n |
|     |                        |                     |             | n |
|     |                        |                     |             | e |
|     |                        |                     |             | l |
|     |                        |                     |             | n |
|     |                        |                     |             | u |
|     |                        |                     |             | m |
|     |                        |                     |             | b |
|     |                        |                     |             | e |
|     |                        |                     |             | r |
|     |                        |                     |             | s |
|     |                        |                     |             | t |
|     |                        |                     |             | o |
|     |                        |                     |             | u |
|     |                        |                     |             | s |
|     |                        |                     |             | e |
|     |                        |                     |             | f |
|     |                        |                     |             | o |
|     |                        |                     |             | r |
|     |                        |                     |             | t |
|     |                        |                     |             | h |
|     |                        |                     |             | e |
|     |                        |                     |             | o |
|     |                        |                     |             | u |
|     |                        |                     |             | t |
|     |                        |                     |             | l |
|     |                        |                     |             | e |
|     |                        |                     |             | t |
|     |                        |                     |             | s |
|     |                        |                     |             | , |
|     |                        |                     |             | i |
|     |                        |                     |             | n |
|     |                        |                     |             | o |
|     |                        |                     |             | r |
|     |                        |                     |             | d |
|     |                        |                     |             | e |
|     |                        |                     |             | r |
|     |                        |                     |             | . |
+-----+------------------------+---------------------+-------------+---+
