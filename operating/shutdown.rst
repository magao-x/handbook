System shutdown
===============

End-of-work shutdown
--------------------

After a night of observing or a day of lab work, follow these steps.

 - Close camera shutters
 - Stop cooling / begin warming up cameras to 20ºC
 - Zero all DM channels, release DM
 - Power down DM
 - From the pupil alignment interface, make sure that the modulation and centering (tip/tilt modulation) is in "RIP" status, or click "rest" to make it Rest In Peace
 - Likewise, the pupil steering mirror should be rested
 - Wait for cameras to warm to ≥20ºC
 - Power down cameras
 - Power down everything else, except for:
    - computers (``compicc``, ``comprtc``)
    - cooling (``instcool``)
    - network switch (``swinst``)
    - blower (``blower``)
    - **Note:** Until fixed, leave ``fwscind`` and ``fwtelsim`` on both USB and DC power to avoid unplanned ICC shutdown.

Full shutdown
-------------

Before `removal of the instrument from the
telescope <../handling/telescope_removal.md>`__, or when shutting the
computers down completely for hardware maintenance, follow these
additional steps.

TODO
