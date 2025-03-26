Running MagAO-X from macOS
==========================

Obtaining a copy of the MagAO-X software and virtual machine
------------------------------------------------------------

The MagAO-X setup scripts in https://github.com/joseph-long/magao-x-setup/ are used to generate a virtual machine image on a regular schedule.

Starting the virtual machine
--------------------------

On macOS, the virtual machine is packaged as a UTM bundle. Install UTM `from its website <https://mac.getutm.app/>`_ (free) or the `Mac App Store <https://apps.apple.com/us/app/utm-virtual-machines/id1538878817>`_ ($).

Move the MagAO-X VM bundle you downloaded out of your downloads folder and into a more permanent home. Double click it to open in UTM, and it will boot to a graphical desktop with ``xsup`` logged in.

Install an SSH key
------------------

Connections to MagAO-X are secured with SSH keys. To connect from a virtual machine, you must have a key pair that is present within the virtual machine and installed on MagAO-X. How you do this is up to you, but one option is to copy the key pair you're using on your host computer (if it's already installed on MagAO-X).

You will need the IP address of the virtual machine. Use the system settings, or run this command *within the VM*::

   $ ip route
   default via 192.168.64.1 dev enp0s1 proto dhcp src 192.168.64.45 metric 100
   192.168.64.0/24 dev enp0s1 proto kernel scope link src 192.168.64.45 metric 100

In the above example ``192.168.64.45`` is the IP address on which the guest is visible to the host. Using this address (or whatever it happens to be for your setup), copy your SSH key into place. From *outside the VM*, go to the directory containing the VM bundle and a file called ``xvm_key``. Using this default key, connect to the VM::

   $ ssh -i ./xvm_key xsup@REPLACE_WITH_IP_ADDRESS

You may be prompted to accept/authorize the VM's SSH key with ``yes``. ::

   % ssh -i ./xvm_key xsup@192.168.64.45
   The authenticity of host '192.168.64.45 (192.168.64.45)' can't be established.
   ED25519 key fingerprint is SHA256:gSJgdHAWSK1GWQL/1GYswPg3to4Od3B/R1+yeSULYDs.
   This key is not known by any other names.
   Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
   Warning: Permanently added '192.168.64.45' (ED25519) to the list of known hosts.
   xsup@192.168.64.45's password:
   [xsup@xvm ~]$

.. note::

   If you get a message like this::

      % ssh -i ./xvm_key xsup@192.168.64.45
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      @    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
      Someone could be eavesdropping on you right now (man-in-the-middle attack)!
      It is also possible that a host key has just been changed.
      The fingerprint for the ED25519 key sent by the remote host is
      SHA256:gSJgdHAWSK1GWQL/1GYswPg3to4Od3B/R1+yeSULYDs.
      Please contact your system administrator.
      Add correct host key in /Users/user/.ssh/known_hosts to get rid of this message.
      Offending RSA key in /Users/user/.ssh/known_hosts:161
      Host key for 192.168.64.45 has changed and you have requested strict checking.
      Host key verification failed.
   
   You need to open ``~/.ssh/known_hosts`` and remove the offending key on the given line (here, line 161). Then, try the above steps again.

Using ``exit``, return to your host shell prompt::

   [xsup@xvm ~]$ exit
   $

Now you can copy your key into place. Let's assume you have an Ed25519 key saved in ``~/.ssh/id_ed25519``. From the host machine::

   $ scp -i ./xvm_key ~/.ssh/id_ed25519 xsup@REPLACE_WITH_IP_ADDRESS:.ssh/
   id_ed25519                                   100%  411   531.6KB/s   00:00

   $ scp -i ./xvm_key ~/.ssh/id_ed25519.pub xsup@REPLACE_WITH_IP_ADDRESS:.ssh/
   id_ed25519.pub                               100%  100   129.2KB/s   00:00

Configure your SSH username
---------------------------

The default contents of ``~/.ssh/config`` inside the VM are::

   Host aoc exao1
      HostName exao1.magao-x.org
   Host rtc exao2
      HostName rtc
   ProxyJump aoc
      Host icc exao3
   HostName icc
      ProxyJump aoc
   Host *
      User YOURMAGAOXUSERNAME

Edit this file in your favorite editor. As you might guess, ``YOURMAGAOXUSERNAME`` must be replaced with your MagAO-X username (the one used to log in to exao1/2/3).

Next, within the VM, test that you can connect to exao1/AOC::

   [xsup@xvm ~]$ ssh aoc
   [YOURMAGAOXUSERNAME@exao1]$ exit

Connect tunnels
---------------

The proclist for a workstation lives in ``/opt/MagAOX/config/proclist_workstation.txt``. It only has some SSH tunnels to start, which you can start with ``xctrl startup`` within the VM.

You can inspect the status of the tunnels by doing ``xctrl status``, which should show something like this::

   workstation_aoc_indi: running (pid: 1234)
   workstation_aoc_milkzmq: running (pid: 1235)

To test that INDI is actually connecting, ``getINDI`` from the command line will print all the (many) MagAO-X properties.

Connect viewer
--------------

To open camsci1, for example, open a terminal and type ``rtimv -c rtimv_camsci1.conf -Z -p 9000``.

.. image:: figures/rtimv_in_vm.png

The ``rtimv`` command looks just like it does on the instrument, except for the ``-Z -p 9000`` options. These options have rtimv connect directly to the MilkZMQ relay, rather than requiring a local MilkZMQ client.

.. note::

   The "Age:" overlay in rtimv is unreliable when running remotely due to network congestion and clock synchronization issues. In other words, if images are always 3 seconds old, there is no technical issue with the viewer. You may have to wait that long to see your actions reflected, though.

.. warning::

   Every viewer open on anyone's remote workstation is receiving a high-bandwidth stream from the cameras. If the network connection gets saturated, you can get distorted or corrupted images. This doesn't indicate a hardware problem, and will go away if the network connection gets less congested.

   You may be able to help by closing viewers you aren't currently using.

Updating the virtual machine
----------------------------

You will need to keep the virtual machine up-to-date. In general, this means updating the ``/opt/MagAOX/config`` repository and ``/opt/MagAOX/source/MagAOX`` codebase. If you know what needs to be updated, you can save time by updating those parts specifically.

If you don't know what needs to be updated, you have two options:

1. You can discard your existing VM **and any data saved on it**, or 
2. you can re-run provisioning.

If you choose Option 1, just delete the virtual machine and follow the above instructions again.

If you choose Option 2, connect to your virtual machine and open a terminal.

1. Update the setup scripts on the virtual machine::

   cd /opt/MagAOX/source/magao-x-setup/
   git pull

2. Repeat provisioning::

   bash provision.sh

This will repeat the installation steps with updated versions of the various MagAO-X software packages. In some cases there will be 

Manually Create the virtual machine
-------------------------------------

**Windows users note:** you should run ``multipass set local.privileged-mounts=true`` to enable file transfers. Read `here <https://multipass.run/docs/privileged-mounts>`_ about the security implications this setting has for Windows.

In a new terminal window, to create a VM with Ubuntu version 24.04::

   $ multipass launch -n magao-x-vm 24.04
   Launched: magao-x-vm

You should mount your home directory into the VM::

   $ multipass mount $HOME magao-x-vm:/home/ubuntu/Home

Next, verify you can connect to the VM and get a shell prompt::

   $ multipass shell magao-x-vm
   [... some lines omitted ...]
   ubuntu@magao-x-vm:~$

Notice that the shell prompt has changed to ``ubuntu@magao-x-vm:~$``. Commands within the VM will be prefixed with ``ubuntu@magao-x-vm:~$`` (though ``~`` may change), and "host" commands will continue to be prefixed with ``$``. Your home directory will be available inside the VM under ``~/Home``. This is one way to get files into and out of the VM. ::

   $ ls ~/Home
   [... list of all your files ...]

Now, exit the VM shell::

   ubuntu@magao-x-vm:~$ exit
   $

The first thing to do after creating the VM is to stop it (which is just like shutting down a "real" physical computer) and adjust some settings::

   $ multipass stop magao-x-vm
   $ multipass set local.magao-x-vm.disk=20GiB
   $ multipass set local.magao-x-vm.cpus=4
   $ multipass set local.magao-x-vm.memory=8G

This ensures you have enough space in the VM to install the MagAO-X software. (You can change the number of CPUs allocated to the VM to a number other than four if you want.)

Now, boot the virtual machine::

   $ multipass start magao-x-vm

You will see the message "Starting magao-x-vm" and a loading spinner. When the VM has started, you will be back at your host shell prompt. Wait a minute for the VM to start, then connect your terminal to the VM with::

   $ multipass shell magao-x-vm
   ubuntu@magao-x-vm:~$

Authentication Error
~~~~~~~~~~~~~~~~~~~~
Also, in the unlikely event you encounter this error (maybe upon reinstalling multipass)::

   The client is not authenticated with the Multipass service.
   Please use 'multipass authenticate' before proceeding.

this `forum post <https://discourse.ubuntu.com/t/unable-to-authorize-the-client-and-cannot-set-a-passphrase-workaround/28321>`_ explains recovery steps.


Resetting the VM
----------------

If you need to reset the VM, start by copying any data you need out of it (e.g. to ``~/Home``). Then, to **delete it forever**, use these commands::

   $ multipass stop magao-x-vm
   $ multipass delete magao-x-vm
   $ multipass purge

To recreate the VM, follow the instructions from the top of the page again.

.. _sw_install:

Manually Install MagAO-X Software
-----------------------------------

Note: you do not need to do this if the automated creation script worked above.

Next, within the VM, obtain a copy of the MagAO-X software and install scripts. Using ``git`` we clone the MagAOX repository::

   ubuntu@magao-x-vm:~$ git clone --depth=1 https://github.com/magao-x/MagAOX.git
   Cloning into 'MagAOX'...
   remote: Enumerating objects: 1040, done.
   remote: Counting objects: 100% (1040/1040), done.
   remote: Compressing objects: 100% (907/907), done.
   remote: Total 1040 (delta 166), reused 642 (delta 100), pack-reused 0
   Receiving objects: 100% (1040/1040), 2.13 MiB | 1.04 MiB/s, done.
   Resolving deltas: 100% (166/166), done.

Go to the ``setup`` subdirectory::

   ubuntu@magao-x-vm:~$ cd MagAOX/setup/

Run the pre-provisioning script to establish the workstation role::

   ubuntu@magao-x-vm:~/MagAOX/setup$ MAGAOX_ROLE=workstation ./pre_provision.sh

You need to reload the ubuntu user's groups, so now logout::

   ubuntu@magao-x-vm:~/MagAOX/setup$ exit

And log back in::

   $ multipass shell magao-x-vm

You can now run the provisioning script::

   ubuntu@magao-x-vm:~/MagAOX/setup$ bash provision.sh

Now, wait a while. Don't be alarmed by the amount of output! Provisioning is very
noisy, and messages in red aren't necessarily errors. Successful
provisioning will end with the message

::

   Provisioning complete
   You now need to log out and back in for group changes to take effect

As the message says, you should exit the VM with ``exit``, and return to your host command prompt. Now, on to :ref:`vm_usage`.

What to do if you don't see ``Provisioning complete``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most likely that means an error occurred running the provisioning
scripts and they did not finish. That can happen if a big download gets
interrupted, for example. It's always safe to run ``bash provision.sh``
again. It'll re-run only necessary steps, which may be enough to get you to
``Provisioning complete``.

If that doesn't resolve the issue, you'll need the complete provisioning
output to get help. The following command will save it to a file
``provision.log`` in your home folder on the host machine, which you can then email or Slack to someone who can help. ::

   ubuntu@magao-x-vm:~/MagAOX/setup$ bash provision.sh | tee ~/Home/provision.log


.. _vm_usage:

Usage
-----

Configuring the VM to connect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you can remotely control MagAO-X, a little post-provisioning
configuration is required. You must have a user account on MagAO-X with
an SSH key file configured. For the preconfigured tunnels to work, that key must not have a passphrase.

If you have a key pair in your computer's ``~/.ssh/`` folder, this appears at ``~/Home/.ssh/`` in the VM. (Note: RSA keys are not allowed.) Copy it into place::


   $ multipass shell magao-x-vm
   ubuntu@magao-x-vm:~$ cp ~/Home/.ssh/id_* ~/.ssh/
   ubuntu@magao-x-vm:~$ chmod u=r,g=,o= ~/.ssh/id_*

Next, you will need to edit the VM's ``~/.ssh/config`` file to add your username. Still within the VM, open a text editor::

   ubuntu@magao-x-vm:~$ nano ~/.ssh/config

At the end of the file, the line ``User YOURUSERNAME`` should be changed to reflect your MagAO-X username. Save and exit.

Connecting to the VM
^^^^^^^^^^^^^^^^^^^^

The rest of this section should be done within a VM except where otherwise noted.

Note: under some circumstances you will get a worrying-sounding message about ``Xauthority``. As long as things are working, it should be ignored.

.. _check_vm_connectivity:

Check connectivity to MagAO-X
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To ensure everything's configured correctly, from a ``multipass shell``
session run ``ssh aoc``, verify your shell prompt changes to ``exao1``, then ``exit``::

   ubuntu@magao-x-vm:~$ ssh aoc
   [you@exao1] $ exit
   ubuntu@magao-x-vm:~$

Start tunnels
^^^^^^^^^^^^^

The ``xctrl`` script is installed during provisioning, and a default set
of apps is configured to run on ``xctrl startup``. These apps launch SSH
tunnels to the instrument.

The proclist for VM usage is in
`magao-x/config/proclist_vm.txt <https://github.com/magao-x/config/blob/master/proclist_vm.txt>`__.

Running ``xctrl startup`` to start the tunnels should result in output
like::

   ubuntu@magao-x-vm:~$ xctrl startup
   Session vm_aoc_milkzmq does not exist
   Session vm_aoc_indi does not exist
   Created tmux session for vm_aoc_milkzmq
   Created tmux session for vm_aoc_indi
   Executed in vm_aoc_milkzmq session: '/opt/MagAOX/bin/sshDigger -n vm_aoc_milkzmq'
   Executed in vm_aoc_indi session: '/opt/MagAOX/bin/sshDigger -n vm_aoc_indi'

And you can check their status with ``xctrl status`` or ``xctrl peek``.

::

   ubuntu@magao-x-vm:~$ xctrl status
   vm_aoc_indi: running (pid: 6147)
   vm_aoc_milkzmq: running (pid: 6148)

(For the SSH tunnel apps, this can be misleading, as "running" doesn't necessarily mean "connected". That is why we checked that ``ssh aoc`` worked separately, above.)

Using GUIs in the VM
~~~~~~~~~~~~~~~~~~~~

The VM is configured to be “headless”, meaning there's no graphical display window. It is possible to run a virtual desktop with multipass, as `described in their docs for "Using RDP" <https://multipass.run/docs/set-up-a-graphical-interface#heading--using-rdp>`_. However, it's better to show MagAO-X software in windows that you can move around like other applications on your computer.

The way to do this is with X11 (the `next section <https://multipass.run/docs/set-up-a-graphical-interface#heading--using-x11-forwarding>`_ of their docs). Most Linux systems support X11 applications by default, but you will need to install `XQuartz <https://www.xquartz.org/>`__ on macOS, if you haven't already.

Windows users should consult the `Multipass docs <https://multipass.run/docs/set-up-a-graphical-interface#heading--x11-on-windows>`_ for their options. It appears that VcXsrv is the most up-to-date free option for a Windows X11 server, downloadable `here <https://github.com/marchaesen/vcxsrv/releases/download/21.1.10/vcxsrv-64.21.1.10.0.installer.exe>`_.

If you're unfamiliar with SSH X forwarding, the short version is that
the app runs on the VM but the window pops up like any other window on
your own computer (the host). SSH (i.e. ``multipass shell``) is the
transport that moves information about the window like mouse clicks and keypresses back and forth to the
GUI app, which lives inside the VM.

.. code:: text

   +------------------------------------------+
   |                  +----------------------+|
   |    Host OS       |          VM          ||
   |                  |                      ||
   |  [GUI window] <-SSH-> [MagAO-X GUI app] ||
   |                  +----------------------+|
   +------------------------------------------+

Assuming you have an SSH key on your host computer already, we need to teach multipass about it. Back on the host computer, we do::

   $ multipass exec magao-x-vm -- bash -c "echo `cat ~/.ssh/id_ed25519.pub` >> ~/.ssh/authorized_keys"

(Note the difference between the backtick quote and the straight single quote is important here.)

This adds the key as an authorized one for connecting to the VM. (We were connecting a different way when we did ``multipass shell`` earlier.)

The following incantation will connect a GUI-capable SSH session to your multipass VM and leave you at a VM prompt::

   $ ssh -Y ubuntu@$(multipass exec magao-x-vm -- hostname -I | awk '{ print $1 }' )
   ubuntu@magao-x-vm:~$

(If prompted with ``Are you sure you want to continue connecting (yes/no/[fingerprint])?`` just say ``yes``.)

So, to start the ``coronAlignGUI``, you could do...

::

   $ ssh -Y ubuntu@$(multipass exec magao-x-vm -- hostname -I | awk '{ print $1 }' )
   ubuntu@magao-x-vm:~$ coronAlignGUI

…and the coronagraph alignment GUI will come up like any other window on
your host machine.

Be careful! Anything you do with these GUIs **controls the real
instrument** (which is sort of the point, but it bears reiterating).

Viewing camera outputs
~~~~~~~~~~~~~~~~~~~~~~

The realtime image viewer ``rtimv`` is built during provisioning. To get
up-to-date imagery from the instrument, we can use
`jaredmales/milkzmq <https://github.com/jaredmales/milkzmq>`__, a set of
programs that relay shared memory image buffers from one computer to
another.

The AOC workstation runs a ``mzmqServer`` process that re-serves the
images it replicates from the rest of the instrument using compression
and a limit of 1 FPS. This ensures it doesn't overwhelm your home
internet connection.

(Napkin math: 1024 \* 1024 \* 16 bit, or one ``camsci1`` frame, is ~2
MB. 2 MByte / second is 16 Mbit / second, more than compressed HD video
streams. And that's just one camera!)

The list of images re-served by AOC is kept in
``/opt/MagAOX/config/mzmqServerAOC.conf`` (`view on
GitHub <https://github.com/magao-x/config/blob/master/mzmqServerAOC.conf>`__).

Establish a milkzmq connection for the cameras you want
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After confirming the tunnel ``vm_aoc_milkzmq`` is running
(``xctrl status``), start a ``milkzmqClient``. For this example we'll
connect to ``camwfs`` and ``camwfs_dark``:

::

   ubuntu@magao-x-vm:~$ milkzmqClient -p 9000 localhost camwfs camwfs_dark &

(We've used ``&`` at the end of the command to background the client, so
just hit enter again to get a normal prompt back after its startup
messages.)

Launch rtimv
^^^^^^^^^^^^

The configuration in ``/opt/MagAOX/config`` includes ``rtimv`` config
files named for the various cameras (see the ``shmim_name`` options in
those files for hints about which images to replicate for a given
camera).

Start the viewer with

::

   ubuntu@magao-x-vm:~$ rtimv -c rtimv_camwfs.conf

and it should pop up a window like this:

.. figure:: example_rtimv_xrif2shmim.png
   :alt: Example of rtimv viewer with 4 wavefront sensor pupils

   Example of rtimv viewer with 4 wavefront sensor pupils

For instructions on rtimv, consult its `user
guide <https://github.com/jaredmales/rtimv/blob/master/doc/UserGuide.md#rtimv>`__.
