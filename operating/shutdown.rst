System Shutdown
===============

Before `removal of the instrument from the
telescope <../handling/telescope_removal.md>`__, or when shutting the
computers down completely for hardware maintenance, follow these
additional steps.

ICC and RTC Shutdown
--------------------

    - After powering off everything but the exceptions mentioned in Daily Shutdown, use ``xctrl shutdown --all`` on ICC and RTC to stop the MagAO-X apps.

    - Next on each of ICC and RTC, cd to `/opt/MagAOX/cacao` and run the shutdown script.

    - On each of ICC and RTC: Using an account with ``sudo`` access (in other words, not ``xsup``), issue ``sudo shutdown -h now`` to take the system down.

Total Shutdown (for packing, etc.)
-----------------------------------

    - After ICC and RTC are shutdown (but **before** shutting down AOC) you can power off **almost** all of the remaining items in the rack using ``pwrGUI``. Do not shut down ``swinst`` yet, or you'll lose the ability to toggle power.

    - As the last step, power off ``swinst``.

AOC Shutdown
------------

On AOC: Close up all the GUIs (hint: ``killall rtimv`` to close all the image viewers). Then ``xctrl shutdown --all`` in a terminal. Now, switching to an account with ``sudo`` access, issue ``sudo shutdown -h now`` to take the system down.
