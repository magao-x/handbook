Shared Memory Transfer
======================

To transfer shared memory images between computers we can use the shmimTCP system.  For example, 

Example
--------

This example shows how to send dmtweeter commands from ICC to RTC

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
