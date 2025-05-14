Daily Shutdown
===============

These procedures are used for shutting down MagAO-X at the end of a work period.

Rules to follow:

- do not power off a DM unless it has been released
- do not power off a temperature-controlled camera unless its temp is 20C or higher
- do not power off instCool!
- steps can be done in parrallel, so start warming up cameras, go on, then come back

.. warning::
       You must be monitoring the relative humidity for `dmtweeter` and `dmncpc` any time their power is on.

.. warning::
       `instCool` must be on while the computers are powered.

Lunch Break
-------------
If you are just taking a break and plan to come back to keep working, you only need to
shut off `dmtweeter` and `dmncpc`:

- open the loop if closed (holoop for tweeter, loloop for ncpc)
- press "loop zero"
- zero flat
- zero all ch
- release
- power off `dmtweeter` and `dmncpc`

.. _minimal_shutdown:


Minimal shutdown
----------------

This procedure can be used if you expect to startup in a few hours. The main goal here is to shutoff "the expensive stuff".

    - For each of `camsci1`, `camsci2`, `camwfs`, `camvisx`, but not `camflowfs` and `camllowfs`.

        - close the shutter
        - warm up to 20C (use cameraGUI, change setpoint)
        - wait for it to finish
        - power off

    - **dmtweeter** and **dmncpc**

        - open the loop if closed (holoop for tweeter, loloop for ncpc)
        - press "loop zero"
        - zero flat
        - zero all ch
        - release
        - power off

    - **dmwoofer**

        - turn off woofer offloading if on
        - zero woofer offloading
        - zero flat
        - zero all ch
        - release
        - power off

    - **ttmmod**

        - if modulating, first press `set` in *Pupil Alignment GUI*
        - press `rest`
        - power off

    - **ttmpupil**

        - press `rest` in *Pupil Alignment GUI*
        - power off

    - **ttmperi**

        - press rest in *Pupil Alignment GUI*
        - power off

    - Others

        - power off **camtip** and **camacq** (they are just heaters)
        - power off **source**
        - power off **tableair**

    - Remaining devices such as focus stages and filter wheels can be left on, which will make alignment easier next time.

Standard Daily Shutdown
-----------------------

If MagAO-X will be unused for a longer period of time (overnight or a weekend), we typically shut down everything but computers, networking and cooling.

  - Follow the steps in :ref:`minimal_shutdown` above.
  -  Everything on the *user* tab of **pwrGUI** should be off. Items can be shutdown in any order.  Occassional errors in the logs during shutdown may occur.
  -  Everything on the *ninja* tab of **pwrGUI** should be on (with the possible exception of `camflowfs` and `camllowfs`)

.. warning::
       Do not power off `instCool`.




