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
   
   a. The airflow from the hose to the DM box
   
   b. The dessicant attached to the air flow pipes.
   
5. If restarting or shutting down XCTRL, first zero the DM and then release it.


Setup (if first time)
---------------------

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
-------

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

TODO: Humidity checking, running XSUP, cursesINDI, Config, Python Scripts, EyeDoctor

