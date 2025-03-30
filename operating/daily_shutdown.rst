Daily Shutdown
===============

These procedures are used for shutting down MagAO-X at the end of a work day.  

Rules to follow:

- do not power off a DM unless it has been released
- do not power off a temperature-controlled camera unless its temp is 20C or higher
- do not power off instcool!
- steps can be done in parrallel, so start warming up cameras, go on, then come back


Lunch Break
-------------
If you are just taking a break and plan to come back to keep working, you only need to
shut off `dmtweeter` and `dmncpc`:

- open the loop if closed (holoop for tweeter, loloop for ncpc)
- press "loop zero"
- zero flat
- zero all ch
- release
- power off


.. _minimal_shutdown:


Minimal shutdown
----------------

This procedure can be used if you expect to startup in a few hours, right away the next day, etc.

The main goal here is to shutoff "the expensive stuff".  Namely:

- dmtweeter
- dmwoofer
- dmncpc
- camwfs
- camsci1
- camsci2
- camlowfs
- ttmmod
- ttmpupil
- ttmperi

Cameras
~~~~~~~

For each of camsci1 camsci2 camwfs, camvisx, but not camflowfs and camllowfs.

- close the shutter
- warm up to 20C (use cameraGUI, change setpoint)
- wait for it to finish
- power off
- note: for camlowfs, power off under both pdu1 and usbdu0.

dmtweeter and dmncpc
~~~~~~~~~~~~~~~~~~~~

- open the loop if closed (holoop for tweeter, loloop for ncpc)
- press "loop zero"
- zero flat
- zero all ch
- release
- power off

dmwoofer
~~~~~~~~

- zero flat
- zero all ch
- release
- power off

ttmmod
~~~~~~

- if modulating, first press set in Pupil Alignment GUI
- press rest
- power off in Power GUI

ttmpupil
~~~~~~~~

- press rest in Pupil Alignment GUI
- power off

ttmperi
~~~~~~~

- press rest in Pupil Alignment GUI
- power off

Others
~~~~~~

- power off camtip (its just a heater)
- power off source
- power off tableair

Remaining devices such as focus stages and filter wheels can be left on, which will make alignment easier next time.

Standard Daily Shutdown
-----------------------

If MagAO-X will be unused for a longer period of time (say a weekend), we typically shut down everything but computers, networking and cooling.  

At the end of this, the following things will still be on:

- pdu0.compicc
- pdu0.comprtc
- pdu0.dcpwr
- pdu0.swinst
- pdu3.blower 
- pdu3.fanaux
- pdu3.fanmain
- pdu3.instcool 

**Note:** it is critical that you not shutdown instcool while compicc and/or comprtc are on!

Follow the steps in :ref:`minimal_shutdown` above.

fwtelsim and fwscind:

- first power off on usbdu0
- then power off on dcdu1

Everything else (except the items listed above) can be shutdown in any order.  Occassional errors in the logs during shutdown may occur. 

