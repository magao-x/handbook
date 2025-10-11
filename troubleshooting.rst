Troubleshooting
===============

.. image:: _static/things_can_go_right.png
   :alt: Illustration of MagAO-X with motto: "Having more things just means more things can go right"
   :align: center
   :scale: 33%


Figuring out what exactly isn't working
---------------------------------------

To narrow down the failing component, use ``xctrl status`` to see if any
MagAO-X apps are not running. The typical MagAO-X app is started by
``xctrl startup`` based on a line in a config file in
``/opt/MagAOX/config/proclist_$MAGAOX_ROLE.txt``. This proclist
determines which application to start and which config file from
``/opt/MagAOX/config`` should be supplied as the ``-n`` option (see
:doc:`Standard options <operating/software/apps/overview>`). It also
uses ``sudo`` to run the process as user ``xsup``, regardless of which
user called ``xctrl startup``.

Many, if not all, MagAO-X apps are intended to run “forever” (i.e until
shutdown). If the process is ``dead``, you can attach to the ``tmux``
session that’s the parent of the process in question with
``xctrl inspect PROCNAME`` (where ``PROCNAME`` is the name of the failed
process). This will occasionally reveal error messages that did not get
to the log.

For example, if ``trippLitePDU`` is started by ``xctrl startup`` with
config specified by ``-n pdu0`` and there’s a syntax error in
``/opt/MagAOX/config/pdu0.conf`` preventing startup, you can attach to
the tmux session with

.. code-block:: bash

   yourlogin$ xctrl inspect pdu0

The errors before exit, if any, will be in the log. The last few lines
of the log can be checked with ``logdump -f pdu0``. The command that
started the app will be of the form
``/opt/MagAOX/bin/$appName -n $configName``. You can use the up-arrow
key in the tmux session to retrieve it from the shell history and try to
relaunch once you’ve corrected whatever error was preventing startup.

Addressing specific issues
--------------------------

.. _missing_lowfs:

Missing ``camflows`` or ``camllowfs``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When booting ICC, ensure that ``camflowfs`` and ``camllowfs`` are already powered on. Otherwise, you will have to reboot ICC to successfully connect.

Things to try:

Hotplugging
^^^^^^^^^^^

   1. begin with both cameras powered off
   2. on exao3/ICC: ``xctrl shutdown camflowfs camllowfs``
   3. power on both cameras
   4. as a non-xsup user, on exao3/ICC, run ``sudo /opt/pvcam/drivers/in-kernel/pcie/hotplug_pcie.sh``
   5. verify the number of "active cameras" it reports, and that none say ``no name found, rescan or PC reboot needed``
   6. on exao3/ICC: ``xctrl startup camflowfs camllowfs``

Outcome 1: successful hotplugging
"""""""""""""""""""""""""""""""""

The ``camflowfs.fsm`` / ``camllowfs.fsm`` property will change to ``OPERATING`` and images will start to appear.

Outcome 2: unsuccessful hotplugging
"""""""""""""""""""""""""""""""""""

When hotplugging is unsuccessful, you will see output like the below that includes ``no name found, rescan or PC reboot needed``.

::

   $ sudo /opt/pvcam/drivers/in-kernel/pcie/hotplug_pcie.sh
   Detected 1 supported card(s)
   0000:41:00.0 - upstream port (Dolphin PXH832 card [10b5:8733])
      0000:42:09.0 - downstream port
         No camera found
      0000:42:08.0 - downstream port
         No camera found

   Found 0 active camera(s)
   cat: /sys/module/pvcam_pcie/refcnt: No such file or directory

   Performing hot-reset of downstream ports...
   0000:42:08.0
   0000:42:09.0
   Removing active cameras...
   Rescanning downstream ports...
   0000:42:08.0
   0000:42:09.0

   Detected 1 supported card(s)
   0000:41:00.0 - upstream port (Dolphin PXH832 card [10b5:8733])
      0000:42:09.0 - downstream port
         0000:44:00.0 - camera rev. 8 (no name found, rescan or PC reboot needed)
      0000:42:08.0 - downstream port
         0000:43:00.0 - camera rev. 8 (no name found, rescan or PC reboot needed)

   Found 2 active camera(s)

*This section TODO*

Shared memory image problems with “No space left on device” errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When starting MagAO-X apps or CACAO apps that use shared memory images,
the ImageStreamIO library will try to create shared memory images on
``/milk/shm``. This can fail with an error like:

::

   ERROR [ FILE: /opt/MagAOX/source/cacao/src/ImageStreamIO/ImageStreamIO.c   FUNCTION: ImageStreamIO_createIm_gpu   LINE: 521 ]
   C Error: No space left on device

Indeed, if you use ``df -h``, you’ll see that ``/milk/shm`` is full:

.. code-block:: bash

   $ df -h
   Filesystem      Size  Used Avail Use% Mounted on
   [...]
   tmpfs            63G   63G     0 100% /milk/shm
   [...]

The solution is to :doc:`shut down <operating/shutdown>` and then clear
``/milk/shm``.

.. code-block:: bash

   you$ xsupify
   xsup$ cd /milk/shm
   xsup$ rm *

If rerunning ``df -h`` *still* doesn’t show any space available,
something is probably holding a reference to the files. (See `this
SuperUser
question <https://superuser.com/questions/1100059/tmpfs-deleting-files-wont-free-the-space>`__.)
You should reboot the computer with ``sudo reboot`` (having already shut
down / rested any hardware).

Loop failing to close for no apparent reason and/or intermittent failures of CACAO calibration process
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Believe it or not, this can be a sign of insufficient disk space.
Consult ``df -h`` and see if any of the filesystems have ``Use%`` of
100%.  This can also be checked in INDI with the sysMonitor process for the relevant compute (sysMonRTC, sysMonICC).

.. _missing_gpu:

Lockup / Missing GPUs / ``nvidia-smi`` errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our computers with PCIe expansion cards will occassionally lock up, or will lose a GPU (``GPU has fallen off
the bus`` errors). Sometimes running ``nvidia-smi`` fails with ``Unable to determine the device handle for GPU 0000:8C:00.0: GPU is lost.  Reboot the system to recover this GPU.`` GPU telemetry will also disappear from the monitoring dashboard.

1. If the system is responding:

   1. If you were using the system, rest any attached hardware and begin camera warmup. (You don't have to wait for them to reach the warmup temperature.) (For RTC: woofer, tweeter, ttmmod, ttmpupil, and camwfs.)

   2. Shutdown (requires sudo)

      .. code-block:: bash

         [user@exaoN ~]$ sudo shutdown -h now

   3. Now "press the power button" using the Moxa IO unit (see the ICC or RTC Power-On section for that computer in the :doc:`System Power On <operating/startup>` procedure)

2. If the system is not responding, GPUs continue to fall off the bus, or ``nvidia-smi`` errors persist after
   following the procedure above:

   1. If you can, perform steps 1.1 and 1.2 above to bring the system down in an orderly fashion.
   2. Power down ``pdu0.comprtc`` or ``pdu.compicc`` (e.g. with **pwrGUI**)
   3. Wait at least 10 seconds.
   4. Now perform all of the ICC or RTC Power-On steps from the :doc:`System Power On <operating/startup>` procedure.

OCAM connectivity / bad data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OCAM connects over two CameraLink connections. CameraLink #1 carries
serial communication with the detector, so if you’re able to command the
camera but your data appear bad in ``rtimv camwfs``, the culprit is
likely the CameraLink #2 cable. Reseat, on ICC do
``xctrl restart camwfs``, and restart ``rtimv``.

Alpao DM not responding
~~~~~~~~~~~~~~~~~~~~~~~

Make sure it has been initialized. There is an ``initialize_alpao``
systemd unit that runs at boot and initializes the interface card.
Successful execution looks like this in
``systemctl status initialize_alpao`` output:

.. code-block:: bash

   $ systemctl status initialize_alpao
   ● initialize_alpao.service - Initialize Alpao interface card
      Loaded: loaded (/opt/MagAOX/config/initialize_alpao.service; enabled; vendor preset: disabled)
      Active: active (exited) since Sun 2019-09-29 11:18:34 MST; 20min ago
     Process: 4449 ExecStart=/opt/MagAOX/config/initialize_alpao.sh (code=exited, status=0/SUCCESS)
    Main PID: 4449 (code=exited, status=0/SUCCESS)
      CGroup: /system.slice/initialize_alpao.service

   Sep 29 11:18:34 exao3.as.arizona.edu systemd[1]: Started Initialize Alpao interface card.
   Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: ====================================================================
   Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: Ref.ID | Model                          | RSW1 |  Type | Device No.
   Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: --------------------------------------------------------------------
   Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: 1 | PEX-292144                     |    0 |    DI |    17
   Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: --------------------------------------------------------------------
   Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: 2 | PEX-292144                     |    0 |    DO |    18
   Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: ====================================================================

The script is saved at ``/opt/MagAOX/config/initialize_alpao.sh``, if
you want to see what it’s doing. Note that executing it again will
appear to fail with a message about not finding cards to initialize if
the cards have been previously initialized.

DM Latency and Communication Troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are various ways that the shared memory interprocess communication
between the deformable mirrors, loop control(s), and the hardware
control processes can stop functioning properly.

Examples with known fixes:
^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Inability to set or zero flat or test from the dm control gui

   -  This likely points to a bad semaphore. Simply release DM, then
      re-initialize, and it usually clears. If not, go to more general
      steps below.

-  Excessive latency, occurs especially for ALPAOs

   -  This usually requires a power cycle of the driver itself. Release
      the DM, then use the power control GUI to turn off, then on the DM
      driver.

-  Skipped commands

   -  This is possibly caused by collisions on a semaphore, meaning more
      than one process is monitoring a given semaphore. This can be
      diagnosed with ``streamCTRL``. If this is not the case, a full
      software shutdown (both cacao and magao-x) and clearing the
      /milk/shm and /dev/shm directories (rm \*), then restarting,
      should clear the problem. See step 5 below.

General Troubleshooting
^^^^^^^^^^^^^^^^^^^^^^^

General troubleshooting steps, in order of severity (try the lower ones
first if you don’t have a clear idea what the problem is): 1) release,
then initialize from the ``dmCtrl`` GUI 2) release, then restart the DM
controller software, e.g. for the woofer:

.. code-block:: bash

   rtc$ xctrl restart dmwoofer

1. restart the CACAO process that combines the DM shmims:

   -  first stop the DM controller (see above)
   -  restart ``dmcomb`` (or testbed equivalent) using ``fpsCTRL``

      -  run ``fpsCTRL``
      -  select process to restart with arrow keys
      -  hit lower-case ``r`` to stop the process
      -  hit upper-case ``R`` to start it again

   -  restart the DM controller (see above)

   Note: this may cause problems in some other processes due to shmim
   recreation.

2. Power cycle the DM

   -  release from the ``dmCtrl`` GUI
   -  turn off the power with the ``pwrCtrl`` GUI, then turn it back on
   -  if it doesn’t happen automatically, initialize the DM from the GUI
      when it has power
   -  if this does not fix the problem, try steps 1-3 again.

3. Full Software Restart

   -  Place all hardware controlled from this computer in a safe
      condition

      -  rest ``modttm`` and ``ttmpupil``
      -  start camera warmup (in case you can’t get software back up)
      -  release all DMs controlled from this computer

   -  Shutdown all software with:

      .. code-block:: bash

         rtc$ xctrl shutdown
         rtc$ tmux kill-server  # for cacao processes not managed by xctrl

   -  Clear all shared memory:

      .. code-block:: bash

          rtc$ cd /milk/shm
          rtc$ sudo rm *
          rtc$ cd /dev/shm
          rtc$ sudo rm *

   -  Now restart software and restore hardware to operating condition

4. Reboot

   -  This is a last resort. This may be necessary if a problem has
      developed in the device driver for instance.
   -  Follow procedure for computer reboot. Ensure all hardware is in a
      safe condition, including powered-off if needed, before rebooting.

EDT Framegrabber Problems (camwfs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The EDT PCIe framegrabber occassionally stops responding. The main
symptom of this is no data from ``camwfs``, and no response on the
serial over camera link.

If ``camwfs`` stops responding on serial (evident in logs, probably frame corruption), first
shutdown the controlling application.

.. code-block:: bash

   $ xctrl shutdown camwfs

You will next need to switch from user ``xsup`` to yourself:

.. code-block:: bash

   $ su <your-user-name>
   <password>

then do these steps to reload the EDT driver:

.. code-block:: bash

   $ cd /opt/EDTpdv
   $ sudo ./edt_unload
   $ sudo ./edt_load

This will reset the kernel module and restore operation. Now return to ``xsup`` and restart the
controlling application:

.. code-block:: bash

   $ exit
   $ xctrl startup camwfs #<-change if a different camera

After this occurs, you will need to re-start the CACAO loop processes so they re-connect to the camwfs shmim.

Camsci1/2 not responding
~~~~~~~~~~~~~~~~~~~~~~~~

If ``camsci1`` and/or ``camsci2`` stop responding, first attempt to restart the control software with ``xctrl restart``.  If this does not restore operation, the PICam library needs to be reset.  Perform the following steps:

1. Turn power off for both cameras.  Note that you will not be able to verify detector temperature but this can not be avoided.
2. Stop both ``camsci`` control processes.  Either use xctrl or go to the tmux session and use ctrl-c.
3. In a terminal on ICC, go to ``/opt/MagAOX/source/MagAOX/apps/picamCtrl`` and run the script ``cleanPI.sh`` as root.  This removes lock files.
4. Re-start both control processes.
5. Power up both cameras

Camsci1/2 not cooling
~~~~~~~~~~~~~~~~~~~~~~~~

If ``camsci1`` and/or ``camsci2`` stop cooling, with possible symptom that the camera stays at 25C and reports
"UNLOCKED", or that temperature control reports "FAULT" or  "UNKNOWN", check the following things:

1. Turn power off for both cameras (warming to 20 C if you can), and shut down the software with `xctrl shutdown camsci1 camsci2`
2. Verify all cables are securely connected, including at the power supply, at the rack and instrument feed-throughs, and the cable between rack and instrument, and on the camera
3. Power up both cameras and restart the software.  Wait until the cameras are connected and check the status of temperature control.
4. If not fixed, check the power supply fuses per the procedure stored on Box under "manuals/Princeton Instruments EMCCD"
5. If still not fixed, contact Teledyne for assistance.

.. warning::
    These cameras are export controlled items and can not be removed from MagAO-X except by US Persons under controlled circumstances.  Do not remove them and attempt to return them to the USA without approval.

rtimv not updating
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If `rtimv` is not showing images:

    #. If remote, check that you have opened the right tunnel.  Usually to port 9000 on AOC.
    #. Check that the camera is actually updating.  You can use:

        .. code-block:: bash

            [icc/rtc]$ milk-shmimmon camname

        on the computer which hosts the camera. If not, try restarting the camera control software and then take camera specific troubleshooting steps.
    #. Check that the `mzmqServer` process on the computer which hosts the camera is alive
    #. Check that the `mzmqClient` process for the computer which hosts the camera is alive on AOC
    #. Check that frames are arriving on AOC with:

        .. code-block:: bash

            aoc$ milk-shmimmon camname

    #. If remote, check that `mzmqServerAOC` is alive on AOC
    #. If you are using the `-Z` option with rtimv (milkzmq direct), try:

        a. Start a `milkzmqClient` instance:

           .. code-block:: bash

            $ milkzmqClient -p 9000 localhost camname #assumes you have the tunnel open

         it will tell you if it begins receiving images and you will see a file show up in `/milk/shm`.

        b. Next try using `milk-shmimmon camname` or `rtimv camname`.


Killing INDI zombies
~~~~~~~~~~~~~~~~~~~~

If the ``indiserver`` crashes uncleanly (itself a subprocess of
`xindiserver <operating/software/apps/network.html#xindiserver>`_), the associated ``xindidriver`` processes may become
orphans (i.e. reparented to PID 1 (init)). This will prevent
`xindiserver <operating/software/apps/network.html#xindiserver>`_ from starting again until these processes have been
killed. (There will be output in logdump suggesting you
``kill the zombies``.)

Often using `xctrl` to restart the INDI server will fail due to the zombies. You can restart the INDI server efficiently by
going to the tmux session for it:

.. code-block:: bash

    $ tmux a -t isRTC

where you change `isRTC` to the correct process name, such as `isAOC` or `isICC`.  You need to be `xsup`.  If the INDI server is down
you will see error messages followed by a prompt.  The following script will kill the zombies:

.. code-block:: bash

    $ killIndiZombies

Now you can up-arrow to find the INDI server command.  It should be:

.. code-block:: bash

    $ /opt/MagAOX/bin/xindiserver -n isRTC

Hit enter to startup the server.  Once it is running you exit the tmux session with `ctrl-b` then `d`.  Now you can test the INDI server is running with

.. code-block:: bash

    $ getINDI

which should return all the INDI properties on that machine.

Difficulties with NVIDIA proprietary drivers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. When installing, ensure you have
   ``systemctl set-default multi-user.target`` and a display is
   connected **only** to the VGA header provided by the motherboard
2. If NVIDIA graphical output did work, and now doesn’t: Your kernel may
   have been updated, requiring a rebuild of the NVIDIA driver. Having
   ``dkms`` installed *should* prevent needing to do this, but an
   uninstall and reinstall over SSH will also remedy it.
3. Runfile installs can be uninstalled with
   ``/usr/local/cuda/bin/cuda-uninstaller``. This may leave a vestigial
   ``/usr/local/cudaXX.YY`` folder (where ``XX.YY`` is a version number)
   that can most likely be safely removed. (It's probably just some
   temporary files that the installer didn't create and is too polite
   to remove.)

Computer Fails to Boot
~~~~~~~~~~~~~~~~~~~~~~

There may be several reasons for this.

Examples with known fixes:
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Startup screen frozen at "initalizing" and Q-Code A9

  - This probably means that the BIOS has lost its setup, and is trying to use a GPU for video display
  - Shutdown and fully power down.
  - If you have a new mobo CR2032 battery, replace it now
  - Remove GPUs (i.e. by disconnecting the PCIe expansion cable from the host card on the mobo).
  - Install the VGA cable on the mobo (see manual for location)
  - Alternatively, you may be able to plug a monitor into the GPU
  - Boot, and press the del key over and over again until you see "Enter Setup" in the lower right corner.
  - Follow the BIOS setup guide
  - Reboot (F10, save settings).
  - Now shutdown, fully power down, and reinstall/reconnect all GPUS.
  - Reboot.

USB Device Communication Problems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If USB controlled devices, such as filter wheels, focus stages, and rotation stages, have errors such as::

   ERRNO: -42001 [Unknown error -42001] >TTY: tcgetattr returned error

or::

   USB Device 0403:6001:A9EF0AMU not found in udev

or similar, try these things:

.. note::
   As of 2024A we are seeing occasional near-total scrambling of USB communications at LCO, probably due to grounding
   problems.  If many, essentially all, USB devices appear to be having problems skip to step 3.

1. Power cycle the problem device.

   - Note that not all USB devices have power control.  In this case skip to step 2.
   - Be sure to power cycle both main power and the USB power if necessary

2. If power cycling the device did not fix it (or it doesn't have power control), next restart the software controller.
   This may be necessary after power-cycling if the USB device was re-enumerated on the motherboard.

   - Use `xctrl restart xxxx` where xxxx is the name of the device
   - watch the logs to see if the device is "found in udev"

3. If the above steps do not work, the USB hub associated with the device may need to be reset.

   - The following devices are not on the main USB hub, but plugged directly into the computer

     - rhtweeter (RTC)
     - ttmpupil (RTC)
     - usbdu0 (RTC)
     - rhncpc (ICC)
     - temprack: lower and upper (ICC)
     - usbdu1 (ICC)

     For these devices you can try unplugging and replugging their USB cables directly on the motherboard

   - If the above direct connection devices are not fixed by re-plugging, the computer will have to be rebooted.
     Follow the procedure for doing so.

   - Most USB devices are connected to the main 16-port USB hub.  This can be remotely power cycled to reboot it.

     - Power off `dcpwr` from the pdu using **pwrGUI**.  Wait a couple seconds, and power it back on.
     - This will cause all of the USB devices to get new addresses/tty numbers, so the software will have to be
       restarted.It's probably easiest at this point to use `xctrl restart all` on ICC instead of restarting them
       one-by-one.



