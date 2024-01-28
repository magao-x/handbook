System Shutdown
===============

Before `removal of the instrument from the
telescope <../handling/telescope_removal.md>`__, or when shutting the
computers down completely for hardware maintenance, follow these
additional steps.

ICC and RTC Shutdown 
--------------------

After powering off everything but the exceptions mentioned in Daily Shutdown, use `xctrl shutdown --all` on ICC and RTC to stop the MagAO-X apps.

On each of ICC and RTC: Using an account with `sudo` access (in other words, not `xsup`), issue `sudo shutdown -h now` to take the system down.

Total Shutdown (for packing, etc.)
-----------------------------------

After ICC and RTC are shutdown, you can power off the remaining items in the rack using `pwrGUI`.  Note: you must do this before shutting down AOC.

AOC Shutdown
-------------

Note: if AOC is shutdown, you will not have power control of the rack.  Only perform this step if that's ok with you.

On AOC: Close up all the GUIs (hint: `killall rtimv` to close all the image viewers). Then `xctrl shutdown --all` in a terminal. Now, switching to an account with `sudo` access, issue `sudo shutdown -h now` to take the system down.