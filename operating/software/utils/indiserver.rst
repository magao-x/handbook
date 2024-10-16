indiserver
==========

Name
----

indiserver − provide socket access to one or more local or remote INDI
drivers

Synopsis
--------

::

   indiserver [options] driver [driver ...]

Description
-----------

indiserver is a TCP server that provides network access to any number of
local INDI Driver programs or INDI Devices running on other indiservers
in a chained fashion.

Options
-------

.. raw:: html

   <table>

.. raw:: html

   <colgroup>

.. raw:: html

   <col width="10%" />

.. raw:: html

   <col width="20%" />

.. raw:: html

   <col width="60%" />

.. raw:: html

   </colgroup>

.. raw:: html

   <tbody>

.. raw:: html

   <tr class="odd">

.. raw:: html

   <td align="left">

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

-l dir

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

enables logging all driver and internal messages to files in the given
directory, otherwise they go to stderr. The file is named
YYYY-MM-DD.islog and thus begins anew each day. Each log entry consists
of the timestamp, the device and the message.

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr class="even">

.. raw:: html

   <td align="left">

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

-m m

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

specifies the maximum number of megabytes a client is allowed to get
behind reading. If the client queue exceeds this amount, the client is
killed. The default value is 50 MB.

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr class="odd">

.. raw:: html

   <td align="left">

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

-n

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

ignore /tmp/noindi

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr class="even">

.. raw:: html

   <td align="left">

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

-p p

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

specifies that the indiserver listen to port p, instead of the default
standard INDI port of 7624.

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   <tr class="odd">

.. raw:: html

   <td align="left">

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

-v

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

arranges for additional trace information to be printed to stderr. These
are cumulative. One (-v) reports each client connect and disconnect and
driver snoops. Two (-vv) adds key information about each message being
sent or received in the form of the client channel or device name; the
toplevel INDI XML element; the device, property name, state, perm and
message attributes as appropriate; then the name and value of each array
member of the INDI element. Three (-vvv) adds the complete XML message.

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   </tr>

.. raw:: html

   </tbody>

.. raw:: html

   </table>

Driver
------

Each additional argument can be either the name of a local program to
run or a specification of an INDI Device on a remote indiserver.

A local program is specified as the path name of the execuble to run
(not the name of the Device it implements). The program is presumed to
implement the INDI protocol on its stdin and stdout channels to
implement exactly one Device. The program may send ad-hoc out-of-band
error or trace messages to its stderr, each line of which will be
prefixed with the name of the Device and a timestamp then is merged in
with the indiserver’s stderr.

A remote Device is given in the form device@host[:port], where device is
the INDI device already available on another running instance of
indiserver, host is the TCP host name on which said instance is running
and the optional port is the port on which to connect if other than the
standard port 7624. Again, remote connections specify the name of the
Device, irrespective of the name of its local driver program. This
remote connection ability is referred to as indiserver “chaining”.

Indiserver will attempt to restart a driver that dies unless the file
/tmp/noindi exists. Automatically restarting drivers helps create a more
robust environment for clients, and allows for easily killing and
restarting a driver any number of times during driver development
without also killing indiserver and restarting clients.

Indiserver queues messages separately for each client and driver in an
attempt to avoid slow consumers from effecting faster consumers.
However, if a client ever gets more than 50MB behind in its queue (or as
set using -m), it is considered hopelessly slow and is shut down.

Exit Status
-----------

``indiserver`` is intended to run forever and so never exits normally.
If it does exit, it prints a message to stderr and exits with status 1.

Examples
--------

In the following discussion, suppose there are driver programs named
``cam``, ``ota`` and ``tmount`` which implement INDI devices Camera, OTA
and Mount, respectively.

Remote ``indiserver`` connections are useful in several scenarios. One
possibility is to allow Drivers to run on platforms most appropriate to
the hardware they are controlling and yet be combined with Devices on
other platforms. For example, suppose a camera device requires a special
hardware connection and dedicated processing so its driver is run on
``host1``. Other devices are simpler and can be run on ``host2``. In
this case, the camera device might be run as follows (the prompt denotes
the host name):

::

   host1: indiserver cam

and combined with other drivers as follows:

::

   host2: indiserver Camera@host1 ota tmount

In this way an INDI client connecting to host2 seemlessly sees all the
devices Camera, OTA and Mount.

This technique can also be used to manage which Devices are available to
INDI clients depending on where they connect. Continuing with the
example before, if a client connects to host1 it will only see device
Camera, but clients connecting to host2 will see Camera, OTA and Mount.
In this way, certain devices can be hidden from, say, external access to
a facility.

See Also
--------

-  `evalINDI <./evalINDI>`__
-  `setINDI <./setINDI>`__
-  `getINDI <./getINDI>`__
-  The `INDI specification v.
   1.7 <http://www.clearskyinstitute.com/INDI/INDI.pdf>`__

--------------

This indiserver.md generated from the man documentation with the
commands:

::

   groff -mandoc -Thtml indiserver.man > indiserver.html
   pandoc -t markdown_github indiserver.html > indiserver.md

and then tweaked for presentation.
