Daily Startup
=============

The steps below assume that the steps in "System Powerup" are complete. This will
generally be the instrument state on a daily basis.

1. On the `pwrGUI` ninja tab, verify the following items are on:

   -  pdu3.blower
   -  pdu3.fanaux
   -  pdu3.fanmain
   -  pdu3.instcool
   -  usbdu0.rhtweeter
   -  usbdu1.rhncpc

If any of these are off, stop and investigate.  These are safety issues and you should not go on.

2.  On the `pwrGUI` ninja tab, verify that the following items are on:

   -  pdu0.compicc
   -  pdu0.comprtc
   -  pdu0.dcpwr
   -  pdu0.swinst

If any of these are off, the instrument probably won't work.

3. Ensure MagAO-X processes are started on AOC, ICC and RTC.  We do this by running `xctrl status` on each machine.

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

4. On actual MagAO-X, you should have all of the needed GUIs open.  On a remote machine, you will need
   to setup GUIs to your liking.

5. On the ``pwrGUI`` user tab, power up the MagAO-X components:

   -  dcdu0: all devices
   -  dcdu1: all devices
   -  pdu0: source, ttmperi (other devices are already on as above)
   -  pdu1: check that relative humidity is below 15% before powering dmncpc and dmtweeter, then power on all other devices
   -  pdu2: 
         - if using ``camflowfs`` / ``camllowfs`` and they are not already powered up:
            - begin with both cameras powered off
            - on exao3/ICC: ``xctrl shutdown camflowfs camllowfs``
            - power on both cameras
            - as a non-xsup user, on exao3/ICC, run ``sudo /opt/pvcam/drivers/in-kernel/pcie/hotplug_pcie.sh``, verify the number of "active cameras" it reports
            - on exao3/ICC: ``xctrl startup camflowfs camllowfs``
         - power on all other devices
   -  pdu3: flippers, tableair.  camvisx and stageff are maybe. (other devices are already on as above)
   -  pduhcat: if you are using GMT HCAT, all devices on. (only in lab, won't show up at telescope)
   -  usbdu0: all devices
   -  usbdu1: all devices except camvisx (unless using VIS-X!)

6. Set the flat on the ``dmwoofer``, ``dmtweeter``, and ``dmncpc``. (Note: this assumes :doc:`CACAO <cacao>` was already started up.)

7. For lab work, put `stagepickoff` in `lab`.  At the telescope it must be in `tel` to see a star.

8. Now on the Alignment GUI:
   - ``set`` the pyramid modulator under "Modulaion"
   - enter the correct frequency and radius (e.g. 2000 Hz, 3 lambda / D) for your loop speed and hit enter (Note that your newly entered values won't appear until modulation begins.)
   - click ``modulate``
   - ``set`` TTM Pupil
   - ``set`` TTM Peri

9. **Optional, but recommended** Set the toggles on ``sysMonRTC.set_latency.toggle`` and ``sysMonICC.set_latency.toggle`` to "On".

9. On the camwfs GUI, toggle ``synchro`` to "on", take a dark, and open the wavefront sensor shutter

10. At this point you should see a PSF image on `camtip`.   If you do not, use the system block diagram to troubleshoot. The most likely causes are that you forgot to power something on (the source?) or that `stagepickoff` is in the wrong position.

11. The cameras with temperature control will start cooling themselves down immediately on software startup, and should be cold by now. Check on them.

**Now you can proceed to** :doc`alignment <./alignment>`

.. |image1| image:: figures/moxa_dio_do.png
.. |image2| image:: figures/moxa_dialog.png
