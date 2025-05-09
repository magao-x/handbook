Daily Startup
=============

The steps below assume that the steps in :doc:`startup` are complete. This will
generally be the instrument state on a daily basis.

1. Ensure MagAO-X processes are started on AOC, ICC and RTC.  We do this by running `xctrl status` on each machine.

   ::

      # starting with AOC:
      [xsup@exao1 ~]$ xctrl status
      # verify processes are all green/running
      # next on ICC:
      [xsup@exao1 ~]$ ssh icc
      [xsup@exao3 ~]$ xctrl status
      # verify processes are all green/running
      [xsup@exao3 ~]$ exit
      # now for RTC:
      [xsup@exao1 ~]$ ssh rtc
      [xsup@exao2 ~]$ xctrl status
      # verify processes are all green/running
      [xsup@exao2 ~]$ exit

.. note::
     All software on all machines should be up and running with good INDI communications. If it is not you can not begin to power up because you won't be able to observe what happens.

2. Ensure that you have working GUIs which are connected to INDI.

.. note::
     This must include a display of the log stream that you are able to see at all times.

3. On the `pwrGUI` *ninja* tab, verify the following items are on:

   -  pdu3.blower
   -  pdu3.rackfans
   -  pdu3.instcool
   -  usbdu0.rhtweeter
   -  usbdu1.rhncpc

.. warning::
    If any of these indicate off, stop and investigate.  These are safety issues and you should not go on.

4.  On the `pwrGUI` *ninja* tab, verify that the following items are on:

   -  pdu0.dcpwr
   -  pdu0.compicc
   -  pdu0.comprtc

.. note::
    If any of these are off, the instrument probably won't work.

.. warning::
       You must be monitoring the relative humidity for `dmtweeter` and `dmncpc` any time their power is on.

5. Use the ``pwrGUI`` to power up the MagAO-X components

   - Verify that humidity for both `rhtweeter` and `rhncpc` are below 15%.

   - On the user tab power everything on.
        - camvisx and stageff can be left off if not needed
        - If you are using GMT HCAT, all devices on `pduhcat` can be powered on (you won't see this at LCO)

   - If you plan to use either ``camflowfs`` or ``camllowfs``, check their power in the *ninja* tab.  If they are not powered up:
            - begin with both cameras powered off
            - on exao3/ICC: ``xctrl shutdown camflowfs camllowfs``
            - power on one or both cameras
            - as a non-xsup user, on exao3/ICC, run ``sudo /opt/pvcam/drivers/in-kernel/pcie/hotplug_pcie.sh``, verify the number of "active cameras" it reports
            - on exao3/ICC: ``xctrl startup camflowfs camllowfs``

6. Once power up is complete, switch to lab mode by running the `xlabmode` script as `xsup` on `aoc`:

    ::

      # Run on AOC:
      [xsup@exao1 ~]$ xlabmode

    This will move `stagepickoff` to the lab position and ensure the ADCs and K-mirror are in the correct position.

7. Set the flat on the ``dmwoofer``, ``dmtweeter``, and ``dmncpc``.

8. Now on the Alignment GUI:

   - ``set`` the pyramid modulator under "Modulaion"
   - click ``modulate``
   - ``set`` TTM Pupil
   - ``set`` TTM Peri

9. At this point you should see a reasonable but aberrated PSF image on `camtip`.   If you do not, use the system block diagram to troubleshoot. The most likely causes are that you forgot to power something on (the source?) or that `stagepickoff` is in the wrong position.


10. Setup camwfs using the On the `camwfsCtrl` GUI:

    - set the FPS to your desired loop speed
    - toggle ``synchro`` to "on"
    - close the shutter
    - take a dark
    - open the shutter

11. Begin modulating: enter the correct frequency and radius (e.g. 2000 Hz, 3 lambda / D) for `camwfs` FPS and hit enter (Note that your newly entered values won't appear until modulation begins.)

12. The cameras with temperature control will start cooling themselves down immediately on software startup, and should be cold by now. Check on them.

13. **Optional, but recommended** Set the toggles on ``sysMonRTC.set_latency.toggle`` and ``sysMonICC.set_latency.toggle`` to "On".

14. Setup CACAO for closing the HO loop as in :doc:`cacao`

15. Now align the system as in :doc:`alignment <./alignment>`

.. |image1| image:: figures/moxa_dio_do.png
.. |image2| image:: figures/moxa_dialog.png
