System Startup
===============

Once the instrument has been unpacked and cabled, begin startup from
System Powerup. Subsequent (nightly/daily) re-startup should generally
begin from “Preparing For Operation” below.

The following assumes you're sitting at the AOC workstation, but it
could be done anywhere with appropriate network tunnels. When one must
SSH to different hosts, the one where the command should be run will be
indicated before the prompt, like ``[xsup@exao1 ~]$ ls`` to run ``ls``
on AOC in the ``~`` directory. (Don't type the ``[host $]`` prompt, or
any comment lines starting with ``#``.)

You should run these commands as the user ``xsup`` to ensure you can
read shared memory images (shmims) and ``ssh`` around to RTC and ICC. If
sitting at AOC, it's therefore best to be logged into the desktop as
``xsup``.

If working remotely, note that steps in RTC and ICC power-up must be
done from firefox running on AOC. You can use ``ssh -X`` to accomplish
this with the right command line option in firefox, but using the x2go
virtual desktop is generally easier.

System Powerup
--------------

1. Start the MagAO-X processes on AOC (exao1) to get power control (see
   the `guide to xctrl <./software/utils/xctrl>`__ for more detail)

   ::

      [xsup@exao1 ~]$ xctrl startup
      # you'll see some output as the processes start, wait a little bit
      [xsup@exao1 ~]$ xctrl status
      # verify processes are all green/running

2. You should have power control now. AOC talks over the instrument
   internal LAN to network-controlled power strips (PDUs), which you can
   control over INDI via several different interfaces: ``sup``,
   ``cursesINDI``, or ``pwrGUI``.

   Since you're sitting at AOC, it's simplest to open ``pwrGUI``. You
   should see switches appear.

   ::

      [xsup@exao1 ~]$ pwrGUI &
      # window should pop open with switches

3. The following devices on the *ninja* tab of `pwrGUI` should be powered up, and never powered off
   (unless you know what you're doing):

   -  pdu0.dcpwr
   -  pdu3.blower
   -  pdu3.rackfans
   -  pdu3.instcool
   -  usbdu0.rhtweeter
   -  usbdu1.rhncpc


4. RTC Power-On

   #.  **CRITICAL** ensure that instcool is powered on to provide
       liquid cooling to the RTC.
   #.  using the `pwrGUI` *ninja* tab, power on ``pdu0.comprtc``
   #.  open firefox, and navigate to ``192.168.0.170`` (or use the "Moxa DIO" bookmark)
   #.  login (if required, password provided to those who need it)
   #.  in the left menu, select ``I/O Setting -> DO Channels`` |image1|
   #.  in the main frame, click on ``RTC-PWR``, which will open a new
       window: |image2|
   #.  Under [1. Current Setting], ensure that ``Pulse Output`` is
       selected, and check the box under Pulse Start. Then press the
       ``Submit`` button at the bottom. This remotely presses the ATX
       power button on the RTC.
   #.  Wait for it to come up, and you can ssh in. (You should not need to babysit it over the KVM.)

5. ICC Power-On

   #.  **CRITICAL** ensure that instcool is powered on to provide
       liquid cooling to the ICCC.
   #.  using the 1pwrGUI` *ninja* tab, power on ``pdu0.compicc``
   #.  open firefox, and navigate to ``192.168.0.170`` (or use the "Moxa DIO" bookmark)
   #.  login (if required, password provided to those who need it)
   #.  in the left menu, select ``I/O Setting -> DO Channels`` |image1|
   #.  in the main frame, click on ``ICC-PWR``, which will open a new
       window: |image2|
   #.  Under [1. Current Setting], ensure that ``Pulse Output`` is
       selected, and check the box under Pulse Start. Then press the
       ``Submit`` button at the bottom. This remotely presses the ATX
       power button on the RTC.
   #.  Wait for it to come up, and you can ssh in. (You should not need to babysit it over the KVM.)

Software Startup
----------------

1. RTC

   -  ssh to RTC with ``ssh rtc``

   -  First start cacao processes. This is done with a startup script in the cacao directory:

      ::

         [xsup@exao2 ~]$ cd /opt/MagAOX/cacao
         [xsup@exao2 cacao]$ bash ./startup

   -  Use ``milk-fpsCTRL`` to verify that both ``dmch2disp-00`` and ``dmch2disp-01`` are running:

   -  Now start MagAO-X

      ::

         [xsup@exao2 ~]$ xctrl startup

   -  Use ``xctrl status`` to verify that processes have started.

2. ICC

   -  First start cacao processes. This is done with a startup script in the cacao directory:

      ::

         [xsup@exao3 ~]$ cd /opt/MagAOX/cacao
         [xsup@exao3 cacao]$ bash ./startup

   -  Use ``milk-fpsCTRL`` to verify that ``dmch2disp-02`` is running:

   -  Now start MagAO-X

      ::

         [xsup@exao3 ~]$ xctrl startup

   -  Use ``xctrl status`` to verify that processes have started.

3. It is possible that MagAO-X software startup will not complete
   correctly, and/or need to be re-done. Symptoms include not seeing
   either RTC or ICC (or both) processes in INDI on AOC, or crashed
   xindiserver processes (isICC or isRTC). The cause is elusive. The fix
   is to shutdown and restart MagAO-X software (``xctrl shutdown --all``) on
   each machine – possibly also on AOC. You do not need to shutdown the
   cacao processes.

GUI Setup
---------

- To setup the GUIs on exao1 (AOC) as user ``xsup``, run the command:

   ::

      [xsup@exao1 ~]$ magaox_guis.sh

- Some windows will need to be rearranged.  The DM displays should self-normalize.  If they do not, the following command should fix it:

   ::

      [xsup@exao1 ~]$ bash dmnorm.sh tweeter &

where you replace `tweeter` with either `woofer` or `ncpc` as necessary.

- Set up a :doc:`cursesINDI <./software/guis/cursesINDI>` terminal.

Preparing for Operations
-------------------------

You can now proceed to :doc:`daily_startup` to prepare the instrument for operation.


.. |image1| image:: figures/moxa_dio_do.png
.. |image2| image:: figures/moxa_dialog.png


