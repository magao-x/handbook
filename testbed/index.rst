Testbed Operation
=================
Welcome to the Comprehensive Adaptive Optics and Coronagraph Test Instrument
(CACTI). Here we'll show what you need to do for running CACTI remotely using the
Virtual Machine, which operates very similarly to MagAO-X with some tweaks.

.. figure:: testbed_diagram.png
   :alt: Diagram showing systems on the testbed

   Diagram showing the relationships between systems on the XWCL testbed. Red indicates the AO control loop. :download:`Full-size <testbed_diagram.png>`

**Sections TODO: Config, Python Scripts**

General Safety
--------------
A few things to know for running CACTI safely:

1. Do not power up the bench if there are thunderstorms. Ideally unplug the bench
   from the UPS in case of thunderstorms.

2. Do not power up the deformable mirror if humidity is above 15%.

3. On humid (monsoon) days, it's recommended to check the humidity reading about once every 30 minutes.

4. If over the course of several days the humidity is slowly rising check the
   following things:

   * The airflow from the hose to the DM box
   * The dessicant attached to the air flow pipes.

5. If restarting or shutting down with ``xctrl``, first zero the DM and then release it.

General Troubleshooting
-----------------------

Here are some resources for troubleshooting things that aren't working:

1. For the most part, troubleshooting tips are documented with the command. It's **not** an exhaustive list, though.

2. General and sepcific troubleshooting tips can be found in the :doc:`../troubleshooting` page.

3. If you're not sure how to proceed, please bring up the issue in the ``#lab-activities`` slack channel.


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

Updating the VM
^^^^^^^^^^^^^^^
When testbed code is updated and pushed onto Github, your computer cannot register them until you update
your virtual machine. Ideally, you should update both ``calib`` and ``config``.

1. In terminal, go to the MagAO-X directory::

      $ cd ~/your/path/to/MagAOX/
      
2. Go to the ``vm/`` folder::

      $ cd vm/
      
3. Go to the ``config/`` folder and go ``git pull``::

      $ cd config/
      $ git pull

4. From here, you will see some text about files being downloaded and updated. If there is nothing new,
   then you will get an ``Already up to date.`` response.
   
5. You can update ``calib/`` by moving up to ``vm/`` and following step 3::

      $ cd ..
      $ cd calib/
      $ git pull

After this, your virtual machine will be up to date with the new CACTI code.
      
Startup
^^^^^^^

These directions are not guaranteed to work unless your virtual machine setup is adjusted for CACTI.

1. In terminal, go to the MagAOX directory::

      $ cd ~/your/path/to/MagAOX/

2. Start up the virtual machine::

      $ vagrant up
      $ vagrant ssh

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

To power on a device, slide the bar from left to right. Simiarly, to power off a device,
slide the bar from right to left.

**Troubleshooting tips**:

<<<<<<< HEAD
1. Sometimes nothing shows up in ``pwrGUI``. Exit the ``pwrGUI`` window and enter ``xctrl restart`` to 
=======
1. Sometimes nothing shows up in ``pwrGUI``. Exit the window and enter ``xctrl restart`` to
>>>>>>> b498d66a4a771e98cb715355d951ce35be0fc4a2
   reboot the tmux sessions. Running ``pwrGUI`` should be back to normal.
   
2. Sometimes only one row shows up (either ``pdu`` or ``usb``). Here, we have to go on ``TIC`` to 
   investigate. This will be a very simplified explanation from :doc:`../operating/software/utils/xctrl` section, which contains more details on other troubleshooting instances. 
   
   #. Connect to ``TIC`` from within Vagrant::

         $ ssh tic
         
   #. Run ``xctrl status`` to investigate the various processes. Green means the process is working. Red
      means the process has some problems with it. Other modes are explained in :doc:`../operating/software/utils/xctrl`::

         $ xctrl status
         
   #. For example, say the ``usbdu0`` process is highlighted in red. You can restart it with 
      ``xctrl startup usbdu0``::

         $ xctrl startup usbdu0
         
   #. Check that it got fixed with the ``usbdu0`` process highlighted in green with ``xctrl status``::

         $ xctrl status
         
   #. You should be good to go. Return to Vagrant by typing ``exit`` in ``TIC``.
   
3. If you still have connection problems with Vagrant, exit out of Vagrant and type ``vagrant reload`` in
   the terminal. This will restart your entire virtual machine. This works best when you've left your
   computer on for many days without restarting.
         
rtimv
^^^^^
Real Time Image Viewer GUI. Allows you to view livestreams of the camera. A detailed
explanation for ``rtimv`` can be found in the :doc:`../operating/software/guis/cameras`
section.

There is a little bit of preparation work to do before running ``rtimv``.

1. Power on the cameras you want to use in ``pwrGUI``.

2. Initialize the ``milkzmqClient`` so ``rtimv`` can see them. You can do this with::

      $ milkzmqClient -p 9000 localhost <shmim-1> <shmim-2> ... &

  where each ``<shmim>`` is a device (camera, DM channels). Load up all the cameras
  you want to use. For example,::

      $ milkzmqClient -p 9000 localhost camlgsfp camzwfs camtip &

  will initialize the cameras ``camlgsfp``, ``camzwfs``, and ``camtip``. Note that
  dark frames are considered separate image streams on their own, so a complete
  set would include ``camlgsfp camlgsfp_dark camzwfs camzwfs_dark camtip camtip_dark``.

  The backgrounded job (because we used ``&``) will keep outputting messages to the
  terminal, interfering with the appearance of the shell prompt, but you can
  hit ``Enter`` a few times to get the familiar ``[vagrant@centos7 ~]$`` back.

  **Tip**: If you forgot the ``&`` at the end of the command and the command
  line is hanging, you can press ``ctrl + z`` to go back to the command line
  and then enter ``bg`` to put ``milkzmqClient`` in the background.

  **Tip**: You don't have to have all the cameras loaded at once. You can run another instance
  of ``milkzmqClient`` for another camera without affecting a pre-existing instance.

  Here is an example of ``milkzmqClient`` successfully loading for
  ``camlgsfp``. The ``milkzmqClient: Connected to camlgsfp`` line indicates
  data should be flowing.

  ::

      [vagrant@centos7 ~]$ milkzmqClient -p 9000 localhost camlgsfp &
      [2] 6332
      [vagrant@centos7 ~]$ N: 2
      camlgsfp
      milkzmqClient: Beginning receive at tcp://localhost:9000 for camlgsfp
      milkzmqClient: Connected to camlgsfp
       [ MILK_SHM_DIR ] '/milk/shm'
       [ MILK_SHM_DIR ] '/milk/shm'
       [ MILK_SHM_DIR ] '/milk/shm'



3. Now you can run ``rtimv``. There's two ways you can do this.

   A. To see the camera GUI with the INDI connected display, use::

         $ rtimv -c rtimv_<camera-name>.conf &

      where ``<camera-name>`` is the name of the camera. For example if using ``camlgsfp``,::

         $ rtimv -c rtimv_camlgsfp.conf &

      **Note**: A ``.conf`` file for this ``<camera-name>`` must exist for this to run.
      If it's not present, contact Jared.

   B. If you are not interested in the INDI connected display, use::

         $ rtimv <camera-name> &

      and you should get the ``rtimv`` GUI with no notes on the sides.


**Troubleshooting tips**:

1. Check that ``<camera-name>`` is powered on in ``pwrGUI``.

2. Check that INDI recognizes the camera. If the ``<camera-name>.fsm`` property in ``cursesINDI``
   says ``NODEVICE``, then it is not being detected. Try checking the USB connection.

3. If all else fails, try resetting ``milkzmqClient``:

   1. Kill the ``rtimv`` and ``milkzmqClient`` jobs. At the vm command line, enter ``jobs`` and
      you will see all the jobs running with a number associated with it. ::

         [vagrant@centos7 ~]$ jobs
         [1]   Running                 pwrGUI &
         [2]-  Running                 milkzmqClient -p 9000 localhost camlgsfp &
         [3]+  Running                 rtimv -c rtimv_camlgsfp.conf &

      To stop a job, enter ``kill %n`` where ``n`` is the number. In this example, you need to stop
      the ``milkzmqClient`` on 2 and the ``rtimv`` on 3. ::

         [vagrant@centos7 ~]$ kill %2
         [vagrant@centos7 ~]$ milkzmqClient: Disconnected from camlgsfp

         [2]-  Done                    milkzmqClient -p 9000 localhost camlgsfp
         [vagrant@centos7 ~]$ jobs
         [1]-  Running                 pwrGUI &
         [3]+  Running                 rtimv -c rtimv_camlgsfp.conf &
         [vagrant@centos7 ~]$ kill %3
         [vagrant@centos7 ~]$ jobs
         [1]-  Running                 pwrGUI &
         [3]+  Terminated              rtimv -c rtimv_camlgsfp.conf
         [vagrant@centos7 ~]$ jobs
         [1]+  Running                 pwrGUI &

   2. Reinitialize the ``milkzmqClient``. ::

         [vagrant@centos7 ~]$ milkzmqClient -p 9000 localhost camlgsfp &

   3. Restart the ``vm_tic_milkzmq`` process in ``xctrl`` with ``xctrl restart vm_tic_milkzmq``. ::

         [vagrant@centos7 ~]$ xctrl restart vm_tic_milkzmq
         Waiting for tmux session for vm_tic_milkzmq to exit...
         Waiting for tmux session for vm_tic_milkzmq to exit...
         Ended tmux session for vm_tic_milkzmq
         Session vm_tic_milkzmq does not exist
         Created tmux session for vm_tic_milkzmq
         Executed in vm_tic_milkzmq session: '/opt/MagAOX/bin/sshDigger -n vm_tic_milkzmq'
         [vagrant@centos7 ~]$ milkzmqClient: Connected to camlgsfp
          [ MILK_SHM_DIR ] '/milk/shm'
          [ MILK_SHM_DIR ] '/milk/shm'
          [ MILK_SHM_DIR ] '/milk/shm'

      Here we can see at the last 4 lines that ``camlgsfp`` is restarted in ``milkzmqClient``.

   4. Start up ``rtimv`` like in the previous directions. The GUI should be outputting properly now.


roiGUI
^^^^^^
Region of Interest GUI for ``rtimv``. A detailed explanation for ``roiGUI`` functions can be found
in the :doc:`../operating/software/guis/cameras` section.

To operate, use:

.. code:: text

   $ roiGUI <camera-name> &

where ``<camera-name>`` is the camera you want to edit the ROI for ``rtimv``.

Basic operation for setting up the ROI box:

1. In the ``rtimv`` window, hover a cursor where you want the center of the ROI box located.

2. The bottom left corner of the ``rtimv`` window will be the X and Y pixel coordinates at the cursor.

3. Note these values and input them into the ``X Center`` and ``Y Center`` targets in ``roiGUI``.

4. To set up the box size, you can use the cursor to go to the edge of your ROI in ``rtimv`` and
   do some quick math to determine how box the box size will be.

5. Input these values in the ``Width`` and ``Height`` in ``roiGUI``.

6. At this point, a colored box will show up in ``rtimv``. Play around with the settings to get
   the desired ROI.

7. Once completed, click the ``set`` button and the ``rtimv`` window will change to the ROI.


dmCtrlGUI
^^^^^^^^^
DM Control GUI. Controls the 1K DM. Apply flats, clear channels, release DM.

**IMPORTANT**: Before powering the DM in ``pwrGUI`` and operating ``dmCtrlGUI``, you must verify the
1K DM humidity is below 15%. See :ref:`humidity_check` for instructions on checking the humidity.

To operate, use: ::

    $ dmCtrlGUI dmkilo &

This will open a GUI window.

1. Initialize the DM by clicking on the ``initialize`` at the top right. Sometimes, the GUI starts
   pre-initialized.

2. To load a DM flat, choose which file you'd like from the top drop down menu.

3. Click on ``set_flat`` to load the flat.

4. When you are done using the 1K DM, please click on ``zero flat`` then  ``release`` before powering it
   down in ``pwrGUI``.
<<<<<<< HEAD
   
**Troubleshooting tips**:

Sometimes the GUI claims the DM is off, despite it being powered on in ``pwrGUI``. Here's some steps to take to investigate:

1. **Verify that the power is working.** Go on ``cursesINDI`` and type ``pdu0.`` to the search portion.
   Scroll down until you find ``dmkilo`` in the second column. Check that the ``state`` and ``target`` bits are ``On`` in 
   the rightmost column.

2. **Restart the driver process.** Log into ``exao0`` as ``xsup`` and type ``xctrl status``. Look for the ``dmkilo`` 
   session on the list. If it is red, then the process is not running. If it's green, then the process is running. Either
   way, reset the driver with: ::
   
      $ xctrl restart dmkilo 
    
   From here, this will reconnect the device and ``dmCtrlGUI`` should be active again.

   
dmModeGUI
^^^^^^^^^
DM Modes GUI. You can apply up to +/-1 wavelength of low order Zernike modes. Useful for manual dialing.

To operate, use: ::

    $ dmModeGUI kiloModes &

This will open a GUI window with a list of low order Zernikes and a slider bar.

1. You can manually enter a number in the box at the right side, then hit enter to apply it.

2. You can move the slider bar to apply aberration.

3. You may see some values already in place. They are retained in the virtual machine.
    
=======

>>>>>>> b498d66a4a771e98cb715355d951ce35be0fc4a2
Commands run on ``exao0``
-------------------------

To startup exao0, open a new terminal and ssh with your account into exao0. Always run it in xsup.

.. code:: text

   $ ssh exao0
   $ su xsup

Startup and shutdown with ``xctrl``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From here, you can start running the various processes with :doc:`../operating/software/utils/xctrl`.

.. _humidity_check:

Humidity Sensing
^^^^^^^^^^^^^^^^

The Arduino humidity sensor has been moved from ``corona`` to ``exao0``. The humidity
sensor is connected via USB to ``/dev/ttyACM0`` which can be monitored with ``screen``
provided that you are in the ``dialout`` user group on ``exao0``.

If you are not in the ``dialout`` group, get someone to do ``sudo gpasswd -a USERNAME dialout``
and log in again.

Open a separate terminal and log into ``exao0`` **with your account** (not ``xsup``).

If you are starting from a fresh (re)boot:

.. code:: text

   $ screen /dev/ttyACM0

If the session already exists (i.e. was disconnected without killing it):

.. code:: text

   $ screen -rd

The screen should now show a bunch of environmental monitoring information that looks like this: ::

   Humidity: 10.70 %	Temperature: 22.80 *C 73.04 *F	Heat index: 21.41 *C 70.55 *F

Please actively check the humidity levels every 30 minutes or so.

**Do not operate the 1K DM if the humidity is above 15%!!**

If somoene else is viewing the humidity monitor, even if they are "detached" from ``screen``,
you won't be able to open it until they have killed their screen session (after reattaching if needed).

**To kill (exit) the humidity monitor**: ``Ctrl + a``, release, then "k", then "y" to confirm.

   * This releases the device for other users.

**To detatch**: ``Ctrl + a``, release, then "d".

   * This makes it easy to reattach with ``screen -rd``

.. _cursesINDI:   

cursesINDI
^^^^^^^^^^

Allows you to directly set exposure times, investigate the status of various components, etc.

To start cursesINDI, enter it in the ``exao0`` terminal when in ``xsup``:

.. code:: text

   $ cursesINDI

For general use:

1. Enter the name of device and it will search for it.

   * Tip: Sometimes there are multiple prefix versions of the device (such as camera darks). Add "." 
     at the end of your device name to minimize scrolling.

2. Once at the list, curse over "target" in second to right hand column. Hit "e" for edit, enter a new
   number, and then "y" for yes.

3. To exit, hit ``Ctrl + c``.

**Tip**: You can also run ``cursesINDI`` in the virtual machine instead through ``xsup@exao0``.

The Eye Doctor for CACTI
^^^^^^^^^^^^^^^^^^^^^^^^

Consult :doc:`../operating/software/utils/eyedoctor` for general information.

Before running eye doctor, make sure that the PSF on the camera is not oversaturated or else the solution
will not turn out well. Go on ``cursesINDI`` to adjust the camera exposure time or add an ND filter to
CACTI.

Run eye doctor in the ``exao0`` terminal under ``xsup``. The general form of the command is:

.. code:: text

   $ dm_eye_doctor <portINDI> <dmModes> <camera-name> <psf_core_radius_pixels> <modes_to_optimize> <amplitude_search_range> --skip 1

For example, if you want to run ``dm_eye_doctor`` for the 1K DM using the ``camlgsfp`` camera and
correct the lower order modes, it would be:

.. code:: text

   $ dm_eye_doctor 7626 kiloModes camlgsfp 8 2...10 0.1 --skip 1

If you want to go on higher order modes, change the ``<modes_to_optimize>`` value:

.. code:: text

   $ dm_eye_doctor 7626 kiloModes camlgsfp 8 10...30 0.1 --skip 1

Once you have a DM flat that produces a nice PSF, you can save the flat with:

.. code:: text

   $ dm_eye_doctor_update_flat kilo

And it will save a new flat in the ``dmCtrlGUI`` list at the very bottom with the date stamped on it.
To run the new flat, you need to update ``dmCtrlGUI`` to zero the flat, select the new flat, and then
set it.

**Note**: Occasionally, Eye Doctor doesn't give you the best solved flat. This may be remedied by going
on ``dmModeGUI`` to manually dial out the lower order modes. 

Running Python to control ``exao0``
--------------------------------------------

There are a myriad of commands you can use to do things with ``exao0``, such as saving data and
running control loops.

Running Jupyter Notebook (Python)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To access Jupyter Notebook from ``exao0``, you need to ssh into ``exao0`` with another terminal:

.. code:: text

   $ ssh -L 9990:localhost:9999 exao0

**Note**: if your computer has a different access code for getting into ``exao0``, use that in
place of the ``exao0`` portion of the command above.

Once connected through ssh, you can navigate to ``localhost:9990`` on your internet browser. This
will open up the jupyter notebook directory page under ``xsup``. If a password is required, ask
someone who has access for it.

From here, you can create your own directories and jupyter notebooks to run your python code.

.. _ImageStream:

Saving Camera Images with ``magpyx``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There's two ways to save images from the cameras, either through ``cursesINDI`` or using the
``ImageStream`` function within the ``magpyx`` python code. This section will cover how to use
``magpyx``. More information on ``magpyx`` can be found `here <https://github.com/magao-x/magpyx>`_.

In jupyter, you need to import ``ImageStream``:

.. code:: text

   $ from magpyx.utils import ImageStream

To declare a camera, set the name of the camera in ``<camera-name>``:

.. code:: text

   $ cam = ImageStream(<camera-name>)

From here, you can do multiple types of tasks with the camera. Commands for using ``ImageStream``
can be found in the `source code <https://github.com/magao-x/magpyx/blob/master/magpyx/utils.py#L88>`_.
When you collect data for the camera, it will use the settings for that camera that have been declared
in ``cursesINDI`` and ``roiGUI``.

If you want to get the immediate frame, you can run:

.. code:: text

   $ image = cam.grab_latest()

If you want to get a cube of images for ``n`` number frames, you can do:

.. code:: text

   $ imagecube = cam.grab_many(n)

When you are done with the camera, please close it off:

.. code:: text

   $ cam.close()

**Tips for running** ``ImageStream``:

1. If you want to save an image with ``cam.grab_latest()`` after a change occured, a short delay before
   grabbing the frame is required. Here is some example code for setting a delay: ::
   
      $ import time
      $ # do a command here
      $ time.sleep(0.5) # in seconds; can be shorter pending on camera exposure time
      $ image = cam.grab_latest()

2. It's generally better to leave the ``ImageStream`` on if you're going to do multiple things
   instead of constantly opening and closing it.

<<<<<<< HEAD
3. If you make a change on the ROI, you will need to close and re-open ``ImageStream`` for it 
   to work. Otherwise, a segfault and **no one** likes that.
   
4. If the camera isn't actively collecting data, you can change the exposure time in ``cursesINDI`` 
=======
2. If you make a change on the ROI, you will need to close and re-open ``ImageStream`` for it
   to work. Otherwise, a segfault and **no one** likes that.

3. If the camera isn't actively collecting data, you can change the exposure time in ``cursesINDI``
   and ``ImageStream`` will update to the new value.


Applying DM commands with ``magpyx``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you would like to apply DM commands through python, you can do so using ``ImageStream`` similarly
as saving a camera image with some simple changes. The main difference is that you will need to initialize
``ImageStream`` for each DM channel you want to access. What shows up on the DM is the summed command
across each of the channels.

In jupyter, you need to import ``ImageStream``:

.. code:: text
   
   $ from magpyx.utils import ImageStream
   
To declare the DM channel, set the name of the DM and channel in ``<dm-channel-name>``:

.. code:: text
   
   $ dm = ImageStream(<dm-channel-name>)
   
Generally, ``<dm-channel-name>`` follows a specific format of ``dmXXdispYY`` where ``XX`` is the DM number
and ``YY`` is the channel number. 

On CACTI, there are two DM options that are available to use.

  * The BMC 1K is ``00``, making it ``dm00``.
  * If the IrisAO segmented DM is in use, it would be ``dm01``.

Despite different DMs, they each have 12 channels available for use. However, note that some channels are
used for specific activities in CACAO. Here are some channels generally used for specific activities:
  
  * Pre-set flat is in ``disp00``. This generally is initialized once in ``dmCtrlGUI`` and not touched in python.
  * The turbulence/aberration channel is ``disp11``.
  * The AO channel is ``disp03``. Note that any AO correction needs to be multiplied by ``-1`` to work properly.

Therefore, an example of initializing the BMC 1K DM's turbulence and AO channels would be:

.. code:: text
   
   $ dm_turb = ImageStream('dm00disp11')
   $ dm_ao = ImageStream('dm00disp03')
   
From here, you can write the commands to the DM using the ``write`` function. 

.. code:: text
   
   $ dm_turb.write(<dm_com_mat>)

Where ``<dm_com_mat>`` is the DM command matrix parameter to pass in. Note that ``<dm_com_mat>`` will be different
based on the DM being used. 

  * The BMC 1K is a ``32x32`` matrix which assumes the units are in ``microns``. Try to avoid using the edge actuators.
  * The IrisAO segmented DM is a ``37x3`` matrix where each row is a specific segment and the 1st column is piston (in 
    ``microns``), the 2nd is tip, and the 3rd is tilt (each in ``milliradians``).
    
For every new DM command you want to enter, you can keep updating it with the ``write`` function.

When you are done with the DM, close it similar to saving an image:

.. code:: text
   
   $ dm_turb.close()
   $ dm_ao.close()


