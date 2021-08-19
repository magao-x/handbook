evalINDI
========

Name
----

evalINDI − evaluate an expression of INDI property values

Synopsis
--------

::

   evalINDI [options] [exp]

Description
-----------

evalINDI connects to an indiserver and listens for the values of
properties to evaluate an arithmetic expression. Each property is
specified using three components enclosed in double quotes in the
following form:

::

   "device.property.element"

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

\_STATE

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

the state attribute, where for the purposes of evaluation the usual
keywords Idle, Ok, Busy and Alert are converted to the numeric values of
0, 1, 2 and 3 respectively.

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

evaluate the timestamp attribute as the number of UNIX seconds from
epoch

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

Switch vectors evalute to 0 or 1 based on the state values of Off and
On, respectively. Light vectors evaluate to 0-3 similarly to the
keywords described above for \_STATE.

The arithmetic expression, *exp,* follows the form of that used in the C
programming language. The operators supported include:

::

   ! + - * / && || > >= == != < <=

and the mathematical functions supported include:

``sin(rad)`` ``cos(rad)`` ``tan(rad)`` ``asin(x)`` ``acos(x)``
``atan(x)`` ``atan2(y,x)`` ``abs(x)`` ``degrad(deg)`` ``raddeg(rad)``
``floor(x)`` ``log(x)`` ``log10(x)`` ``exp(x)`` ``sqrt(x)``
``pow(x,exp)``

The value of PI can be specified using a constant named “pi”.

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

-b

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

Ring the terminal bell when expression evaluates as true.

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

``#!/usr/bin/perl``\  ``use Socket;``\  ``use Fcntl;``\ 
``socket(SOCK, PF_INET, SOCK_STREAM, getprotobyname(’tcp’));``\ 
``connect(SOCK, sockaddr_in(7624,inet_aton(’localhost’)));``\ 
``fcntl(SOCK,F_SETFD,0);``\  ``$directfd = fileno(SOCK);``\ 
``&runindi ("./evalINDI", "-d", "$directfd", "\"x.y.z\"==1");``\ 
``sub runindi { if (fork()) { wait(); } else { exec @_; } }``\ 

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

-e

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

print each updated expression value after each evaluation

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

-f

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

print the final expression value

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

-i

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

read the expression from stdin

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

-o

.. raw:: html

   </p>

.. raw:: html

   </td>

.. raw:: html

   <td align="left">

.. raw:: html

   <p>

print each operand each time it changes value in the form property=value

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

wait no longer than t seconds to gather the initial values for all the
specified properties; 0 means forever, the default is 2 seconds.

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

evaluate the expression as many times as necessary until it evaluates to
a value other than zero.

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

Exit Status
-----------

The evalINDI program exits with a statis of 0 if the expression
evaluates to non-0. It exits with 1 if the expression evaluated to 0. It
exits with 2 if there was some other error such as not being able to
connect to the indiserver.

Examples
--------

Print 0/1 whether the Front or Rear elements of the Security property
are in a state of Alert:

::

   evalINDI -f ’"Security.Security.Front"==3 || "Security.Security.Rear"==3’

Exit 0 if the Security property as a whole is in a state of Ok:

::

   evalINDI ’"Security.Security._STATE"==1’

Wait forever for RA and Dec to be near zero and watch their values as
they change:

::

   evalINDI -t 0 -wo ’abs("Mount.EqJ2K.RA")<.01 && abs("Mount.EqJ2K.Dec")<.01’

Wait forever for the wind speed to become larger than 50:

::

   evalINDI -t 0 -w ’"Weather.Wind.Speed">50’

See Also
--------

-  `getINDI <./getINDI>`__
-  `setINDI <./setINDI>`__
-  `indiserver <./indiserver>`__
-  The `INDI specification v.
   1.7 <http://www.clearskyinstitute.com/INDI/INDI.pdf>`__

--------------

This evalINDI.md generated from the man documentation with the commands:

::

   groff -mandoc -Thtml evalINDI.man > evalINDI.html
   pandoc -t markdown_github evalINDI.html > evalINDI.md

and then tweaked for presentation.
