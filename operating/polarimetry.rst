Polarimetry
===========

Point of contact: Miles Lucas <mileslucas@arizona.edu>

.. WARNING:: 
    WIP: This document is a work in progress. I recommend emailing me if you plan to do polarimetry.

Introduction
------------


Devices and Stages
------------------

Polarizing beamsplitter (PBS)
~~~~~~~~~~~~~~~~~~~~~~~


Half-wave plate (HWP)
~~~~~~~~~~~~~~~


Dual rotating quarter-wave plate compensator (DQWP)
~~~~~~~~~~~~~~~~~


Operation
---------

1. Make sure the PBS is selected in ``stagescibs``
1. Make sure both science cameras are in the same filter, ``r`, `i`, or `z``.
.. 1. (Optional) Insert the DQWP
..     a. Make sure AO loops are open since we will occult the beam
..     a. ``stageqwplin` to preset `in``
..     a. (TODO; code doesn't exist yet) ``qwptrack`` start tracking
1. Ensure the science cameras are synchronized via the ``synchro`` property
1. Insert the HWP
    a. Make sure ``stagezaber` power is on and `stagepollin` USB is on in the ninja tab of `pwrGui``
    a. Move ``stagepollin` to preset `in``
    a. Turn ``stagezaber` power off and `stagepollin`` USB off
1. Prepare the HWP
    a. Make sure ``stagepolrot` power and USB are on in `pwrGui``

At this point, all optics are ready for polarimetry. Polarimetry is run via the ``hwpSequencer`` app or inside the ``hwpSequencerGUI``.

