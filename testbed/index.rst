Testbed Operation
=================
Welcome to the Comprehensive Adaptive Optics and Coronagraph Test Instrument
(CACTI). Here we'll show what you need to do for running CACTI remotely using the
Virtual Machine, which operates very similarly to MagAO-X with some tweaks.

.. figure:: testbed_diagram.png
   :alt: Diagram showing systems on the testbed

   Diagram showing the relationships between systems on the XWCL testbed. Red indicates the AO control loop. :download:`Full-size <testbed_diagram.png>`

**Sections TODO: Config, Python Scripts, EyeDoctor**

General Safety
--------------
A few things to know for running CACTI safely:

1. Do not power up the bench if there are thunderstorms. Ideally unplug the bench
   from the UPS in case of thunderstorms.

2. Do not power up the deformable mirror if humidity is above 15%.

3. Check the humidity reading about once every 30 minutes.

4. If over the course of several days the humidity is slowly rising check the
   following things:

   * The airflow from the hose to the DM box
   * The dessicant attached to the air flow pipes.

5. If restarting or shutting down with ``xctrl``, first zero the DM and then release it.

Remote operation with a virtual machine (VM)
--------------------------------------------

Create a virtual machine to operate CACTI remotely. The VM handles the control GUIs and the cameras.

Initial Setup
^^^^^^^^^^^^^

0. You will need an SSH key in ECDSA or ED25519 format, and a user account in
   group ``magaox-dev`` on ``exao0`` (a.k.a. TIC) with that key authorized

1. Follow the directions in :doc:`../compute/remote_operation` up to :ref:`check_vm_connectivity`. (Since you will be connecting to the testbed rather than the instrument, we check that connection below.)

2. Connect to the VM by running ``vagrant ssh`` in the MagAOX folder. Your shell prompt will change to::

   [vagrant@centos7] $

3. Verify connectivity to ``exao0``/TIC by connecting to it with ssh (entering ``yes`` if prompted to verify the host key)::

      $ vagrant ssh
      Last login: Fri Jun 11 04:30:39 2021 from 10.0.2.2
      [vagrant@centos7 ~]$ ssh tic
      The authenticity of host 'exao0.as.arizona.edu (128.196.208.81)' can't be established.
      ECDSA key fingerprint is SHA256:7a6jFVxlsQG9X5ZVPX3IHTxmT2c+qKEcStlxbZp4I4g.
      Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
      Warning: Permanently added 'exao0.as.arizona.edu,128.196.208.81' (ECDSA) to the list of known hosts.
      Last login: Wed Jun 23 12:27:16 2021 from example.com
      exao0:~ you$ logout
      Connection to exao0.as.arizona.edu closed.
      [vagrant@centos7 ~]$

4. To get from the vagrant prompt back to your normal prompt, use ``exit`` or ``logout``. Note that the virtual machine is still running in the background, and you can reconnect with ``vagrant ssh``.

5. Navigate to the ``vm/`` folder created within your ``MagAOX/`` folder. You
   need to replace the MagAO-X ``calib`` and ``config`` folders with CACTI's
   ``calib`` and ``config``.

   #. In terminal, go to the ``vm/`` folder::

         $ cd vm/

   #. Delete the original MagAOX config and calib folders::

         $ rm -r calib config

   #. Clone the testbed_calib and testbed_config repositories from GitHub into ``calib/`` and ``config/``::

         $ git clone https://github.com/magao-x/testbed_calib calib
         $ git clone https://github.com/magao-x/testbed_config config

At this point, you should be ready to have regular virtual machine startup for CACTI.

Startup
^^^^^^^

These directions are not guaranteed to work unless your virtual machine setup is adjusted for CACTI.

1. In terminal, go to the MagAOX directory::

      $ cd ~/your/path/to/MagAOX/

2. Start up the virtual machine::

      $ vagrant up
      $ vagrant shh

3. One you are in the virtual machine, bring up xctrl::

      $ xctrl startup

   From here, this should start up the following tmux sessions:

   .. code:: text

      vm_tic_indi
      toc_tic_milkzmq
      toc_tic_jupyterlab

Your VM is now connected to the testbed control computer and you can go about your work.

VM Commands
-----------
These commands allow you to turn on various GUIs through the VM.

pwrGUI
^^^^^^
Power Control GUI. Allows you to turn on and off the cameras, lasers, DM, etc.

To operate, use:

.. code:: text

    $ pwrGUI &

dmCtrlGUI
^^^^^^^^^
DM Control GUI. Controls the 1K DM. Apply flats, clear channels, release DM.

To operate, use:

.. code:: text

    $ dmCtrlGUI dmkilo &

rtimv
^^^^^
Real Time Image Viewer GUI. Allows you to view livestreams of the camera.

To operate, use:

.. code:: text

    $ rtimv <shmim name> &

where ``<shmim name>`` is the name of the device. For example if using camsci,

.. code:: text

    $ rtimv camsci &

**Tips for rtimv**: If the stream is not live, it could be an indicator that:

   * The camera is off.
   * The process on exao0 has crashed. Check in the exao0 terminal with ``xctrl status``.
   * ``milkmxmq`` server is down. Check in exao0 terminal with ``xctrl status``.
   * You didn't start the ``milkmxmq`` client in the VM.

Commands run on ``exao0``
-------------------------

To startup exao0, open a new terminal and ssh with your account into exao0. Always run it in xsup.

.. code:: text

   $ ssh exao0
   $ su xsup

Startup and shutdown with ``xctrl``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From here, you can start running the various processes with :doc:`../operating/software/utils/xctrl`.

Humidity Sensing
^^^^^^^^^^^^^^^^

The Arduino humidity sensor has been moved from ``corona`` to ``exao0``. The humidity
sensor is connected via USB to ``/dev/ttyACM0`` which can be monitored with ``screen``
provided that you are in the ``dialout`` user group on exao0.

If you are not in the ``dialout`` group, get someone to do ``sudo gpasswd -a USERNAME dialout`` and log in again.

Open a separate terminal and log into ``exao0``.

If you are starting from a fresh (re)boot:

.. code:: text

   $ screen /dev/ttyACM0

If the session already exists (i.e. was disconnected without killing it):

.. code:: text

   $ screen -rd

The screen should now show a bunch of environmental monitoring information that looks like this::

   Humidity: 10.70 %	Temperature: 22.80 *C 73.04 *F	Heat index: 21.41 *C 70.55 *F

Please actively check the humidity levels every 30 minutes or so.

**Do not operate the 1K DM if the humidity is above 15%!!**

If somoene else is viewing the humidity monitor, even if they are "detached" from ``screen``, you won't be able to open it until they have killed their screen session (after reattaching if needed).

**To kill (exit) the humidity monitor**: ``Ctrl + a``, release, then "k", then "y" to confirm.

   * This releases the device for other users.

**To detatch**: ``Ctrl + a``, release, then "d".

   * This makes it easy to reattach with ``screen -rd``

cursesINDI
^^^^^^^^^^

Allows you to set exposure times, ROI, etc directly.

To start cursesINDI, enter it in the exao0 terminal when in xsup:

.. code:: text

   $ cursesINDI

For general use:

1. Enter the name of device and it will search for it.

   * Tip: Sometimes there are multiple versions of the device. Add "." at the end
     of your device name to minimize scrolling.

2. Once at the list, curse over "target" in second to right hand column. Hit "e" for edit, enter a new number, and then "y" for yes.

3. For ROI you will need to toggle the ``set_roi`` processes by hitting "t" for toggle.

4. To exit, hit ``Ctrl + c``.

The Eye Doctor for CACTI
^^^^^^^^^^^^^^^^^^^^^^^^

**TODO**

Consult :doc:`../operating/software/utils/eyedoctor` for general information.
