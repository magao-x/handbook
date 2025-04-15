Shared Memory Transfer
======================

To transfer shared memory images between computers we can use the shmimTCP system. The goal is to
make a copy or dummy shared memory on one machine that is then synchronized with the other machine
over a dedicated ethernet connection.

Standard Use
------------
For our standard use cases of transferring DM commands, the script `dmdispbridge` will setup the system for you.
For instance, to send `dmtweeter` channel 03 commands from ICC to RTC, on ICC you can run

::

    [xsup@exao3]$ dmdispbridge dm01disp03

The arguments can be any dm channel:

- dm00dispXX for the woofer
- dm01dispXX for the tweeter
- dm61dispXX - dm66dispXX for GMT segments

To send `dmncpc` commands from RTC to ICC, on RTC you can run

::

    [xsup@exao2]$ dmdispbridge dm02disp03



Manual Setup
------------

More complicated and/or new uses require you to perform the steps yourself.

Example 1
~~~~~~~~~

A simple case is to send data from a machine that has the source of the data on it to another machine.  Here
we have a stream named `acc000` that we want to send to another machine.  We start with the receiving machine:

::

   $ tmux new -s sTCPrc-acc00


Then in the tmux terminal run (which you are now in)

::

   $ shmimTCPreceive 8886

You can now exit the tmux session with `ctrl-b` followed by `d`.  Next, on the sending machine run

::

   $ shmimTCPtransmit acc000 192.168.2.2 8886

Where you change the IP address (192.168.2.2) and port (8886) as needed.

Example 2
~~~~~~~~~

This example shows how to send dmtweeter commands from ICC to RTC.  This is subtly different from the above
example b/c ICC is not usually the source of the DM commands, so there is no stream already to use.  Then
the DM commands are written to an already existing stream on RTC. Note that these are the steps
performed by `dmdispbridge` for the same operation above, but this can be adapted to other devices/shmims as needed.

First on RTC:

::

   tmux new -s sTCPrc-dm01disp06

Then in the tmux session:

::

   $ shmimTCPreceive 8886

Second On ICC:

First create the shmim

::

   cacao
   cacao> mk2Dim "s>tf32>dm01disp06" 50 50
   cacao> exit

Then make the connection (no tmux needed)

::

   $ shmimTCPtransmit dm01disp06 192.168.2.2 8886


This example can be modified for other taskes (e.g. sending camtip to RTC)

