getINDI
=======

Name
----

getINDI − get INDI property values

Synopsis
--------

::

   getINDI [options] [device.property.element ...]

Description
-----------

getINDI connects to an indiserver and reports the current value of one
or more properties. Each property is specified using three components in
the form:

::

   device.property.element

Any component may be an asterisk, “\*”, to serve as a wild card that
matches all names in that component of the specification. If no property
is specified, then all properties match, i.e., it is as if the
specification “\*.*.\*” were given.

The last component of the property specification is usually the element
name, but may be a reserved name to indicate an attribute of the
property as a whole. These reserved names are as follows:

.. raw:: html

   <table>

.. raw:: html

   <colgroup>

.. raw:: html

   <col width="10%" />

.. raw:: html

   <col width="30%" />

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

\_LABEL

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

report the label attribute

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

\_GROUP

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

report the group attribute

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

\_STATE

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

report the state attribute

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

\_PERM

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

report the permission attribute

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

\_TO

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

report the timeout attribute

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

\_TS

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

report the timestamp attribute

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

Options
-------

.. raw:: html

   <table>

.. raw:: html

   <colgroup>

.. raw:: html

   <col width="10%" />

.. raw:: html

   <col width="30%" />

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

-1

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

print just the value if expectiong exactly one matching property

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

-B

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

enable downloading BLOBs

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

-d <f>

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

use file descriptor f already open as a socket to the indiserver. This
is useful for scripts to make a session connection one time then reuse
it for each invocation. If the file descriptor seems to be being closed,
check that the close-on-exec flag is off; for example in perl use
something like:

.. raw:: html

   </p>

``#!/usr/bin/perl`` ``use Socket;``\  ``use Fcntl;``\ 
``socket(SOCK, PF_INET, SOCK_STREAM, getprotobyname(’tcp’));``\ 
``connect(SOCK, sockaddr_in(7624,inet_aton(’localhost’)));``\ 
``fcntl(SOCK,F_SETFD,0);``\  ``$directfd = fileno(SOCK);``\ 
``%props = split (/[=0/, ’getINDI -d $directfd’);``\ 

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

-h <h>

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

connect to alternate host h; the default is localhost.

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

-m

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

continue to monitor for subsequent changes to each specified property
until timeout.

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

-p <p>

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

connect using alternate port p; the default is 7624.

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

-q

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

suppress some error message.

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

-t <t>

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

wait no longer than t seconds of no activity to gather the values for
all the specified properties; the default is 2 seconds. Specify 0 to
wait forever.

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

-v

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

generate additional information on stderr. This is cumulative in that
specifying more -v options will generate more output.

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

-w

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

Usually only readable properties are shown. If this flag is set, then
all properties, including those that are write-only, are shown.

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

Output Format
-------------

For properties that are not BLOBs, the output of getINDI is one line per
property. Unless the -1 option is given, each line is of the form:

::

   property=value

A property that is a BLOB is saved in a file name
device.property.element.format. Z compression is handled automatically,
other formats are left unchanged. Note that BLOBs are not read by
default, only when the -B option is used.

Exit Status
-----------

The getINDI program exits with a status of 0 if it suceeded in finding
the value for each specified property. It exits with 1 if there was at
least one property for which no value was found within the given timeout
period. It exits with 2 if there was some other error such as not being
able to connect to the indiserver.

Examples
--------

In a perl script, gather all properties for the default indiserver and
save them in an associative array %props which can then be used to look
up a property value by name:

::

   %props = split (/[=0/, ’getINDI’);

Wait up to ten seconds to get the values of all properties from the
Mount device on the given host and non-standard port:

::

   getINDI -h indihost -p 7655 -t 10 "Mount.\*.\*"

Print just current value of the wind speed element from the weather
device:

::

   getINDI -1 Weather.Wind.Speed

See ALso
--------

-  `evalINDI <./evalINDI>`__
-  `setINDI <./setINDI>`__
-  `indiserver <./indiserver>`__
-  The `INDI specification v.
   1.7 <http://www.clearskyinstitute.com/INDI/INDI.pdf>`__

--------------

This getINDI.md generated from the man documentation with the commands:

::

   groff -mandoc -Thtml getINDI.man > getINDI.html
   pandoc -t markdown_github getINDI.html > getINDI.md

and then tweaked for presentation.
