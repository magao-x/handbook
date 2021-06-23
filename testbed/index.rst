Testbed Operation
=================
Welcome to the Comprehensive Adaptive Optics and Coronagraph Test Instrument
(CACTI). Here we'll show what you need to do for running CACTI remotely using the
Virtual Machine, which operates very similarly to MagAO-X with some tweaks.

.. figure:: testbed_diagram.png
   :alt: Diagram showing systems on the testbed

   Diagram showing the relationships between systems on the XWCL testbed. Red indicates the AO control loop. :download:`Full-size <testbed_diagram.png>`


IN PROGRESS (As Jhen experiences parts of CACTI)



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
   
5. If restarting or shutting down XCTRL, first zero the DM and then release it.

Virtual Machine (VM)
--------------------

Initialize the virtual machine before running exao0 on CACTI. The VM handles the control GUIs and the cameras.

Setup (if first time)
^^^^^^^^^^^^^^^^^^^^^

1. Follow the directions for setting up the MagAO-X instrument. https://magao-x.org/docs/handbook/compute/remote_operation.html#setup

2. Verify that your ssh keys are good.
   https://magao-x.org/docs/handbook/compute/remote_operation.html#remotely-controlling-magao-x

3. You need to edit the ssh configuration to add another Host for ``tic``. This is
   an example of what the configuration file should look like:

   .. code:: text

      IdentityFile /vagrant/vm/ssh/magaox_ssh_key
      Host aoc
        HostName exao1.magao-x.org
      Host rtc
        HostName rtc
        ProxyJump aoc
      Host icc
        HostName icc
        ProxyJump aoc
      Host *
        User YOURUSERNAME
      Host tic
        HostName exao0.as.arizona.edu

4. You need to set the CACTI's calib and config folders in the vm folder.
   
   #. In terminal, go to the vm folder:
   
      .. code:: text

         $ cd .../MagAOX/vm

   #. Download the testbed_calib and testbed_config folders from github:
   
      .. code:: text

         $ git clone https://github.com/magao-x/testbed_calib
         $ git clone https://github.com/magao-x/testbed_config


   #. Delete the original MagAOX config and calib folders:
   
      .. code:: text

         $ rm -r calib config
         
   #. Rename the testbed_calib and testbed_config folders to calib and config:
   
      .. code:: text

         $ mv testbed_calib calib
         $ mv testbed_config config
         
At this point, you should be ready to have regular virtual machine startup for CACTI.

Startup
^^^^^^^

These directions are not guaranteed to work unless your virtual machine setup is adjusted for CACTI.

1. In terminal, go to the MagAOX directory:
   
   .. code:: text
   
      $ cd .../MagAOX/
      
2. Start up the virtual machine:
   
   .. code:: text
   
      $ vagrant up
      $ vagrant shh
      
3. One you are in the virtual machine, bring up xctrl:
   
   .. code:: text
   
      $ xctrl startup
      
   From here, this should start up the following tmux sessions:
   
   .. code:: text
      
      vm_tic_indi
      toc_tic_milkzmq
      toc_tic_jupyterlab
      
Now you can go about with your various tasks.

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

Exao0
-----

To operate CACTI, you must be in exao0.

To startup exao0, open a new terminal and ssh with your account into exao0. Always run it in xsup.

.. code:: text
   
   $ ssh exao0
   $ su xsup
   
From here, you can start running the various processes.

Humidity Sensing
^^^^^^^^^^^^^^^^

The arduino humidity sensor has been moved from corona to exao0. The humidity
sensor is connected via USB to /dev/ttyACM0 which can be monitored with “screen” 
provided that you are in the “dialout” group.

If you are not in the "dialout" group, get someone to do ``sudo gpasswd -a USERNAME dialout``.

Open a separate terminal and log into exao0.

If you are starting from a fresh boot:

.. code:: text
   
   $ screen /dev/ttyACM0
   
If the session already exists (i.e. was disconnected without killing it):

.. code:: text
   
   $ screen -rd
   
This will open up another terminal window which will output all humidity levels. The humidity levels are updated every 5 minutes. Please actively check the humidity levels every 30 minutes or so.

**Do not operate the 1K DM if the humidity is above 15%!!**

If somoene else is using the device, you won't be able to open it until they have killed their screen session (after reattaching if needed).

**To kill**: ``Ctrl + a``, release, then "k", then "y" to confirm.

   * This releases the device for other users.

**To detatch**: ``Ctrl + a``, release, then "d".

   * This makes it easy to reattached with ``screen -rd``

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
   
TODO: Config, Python Scripts, EyeDoctor

