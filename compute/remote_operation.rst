Remote operation
================

MagAO-X can be operated entirely remotely as long as the prerequisites (power, dry air, networking) are met. The easiest way to adjust settings is with the web UI, but for full control you will want a virtual machine (VM).

Configuring the virtual machine is done from the command line. Example commands are shown after a ``$`` or ``ubuntu@primary:~$`` (which you don't type yourself as part of the command), and output is on un-prefixed lines.

You will want to first install Multipass, a virtual machine manager specifically for Ubuntu Linux VMs. Follow the `instructions on their website <https://multipass.run/install>`_ to install.

Create the virtual machine
--------------------------

**Windows users note:** you should run ``multipass set local.privileged-mounts=true`` to enable file transfers. Read `here <https://multipass.run/docs/privileged-mounts>`_ about the security implications this setting has for Windows.

In a new terminal window, to create a VM with Ubuntu version 22.04::

   $ multipass launch -n primary 22.04
   Launched: primary
   Mounted '/Users/YOURUSERNAME' into 'primary:Home'

Verify you can connect to it::

   $ multipass shell
   [... some lines omitted ...]
   ubuntu@primary:~$

Notice that the shell prompt has changed to ``ubuntu@primary:~$``. Commands within the VM will be prefixed with ``ubuntu@primary:~$`` (though ``~`` may change), and "host" commands will continue to be prefixed with ``$``. Your home directory will be available inside the VM under ``~/Home``. This is one way to get files into and out of the VM. ::

   $ ls ~/Home
   [... list of all your files ...]

Now, exit the VM shell::

   ubuntu@primary:~$ exit
   $

The first thing to do after creating the VM is to stop it (which is just like shutting down a "real" physical computer) and adjust some settings::

   $ multipass stop
   $ multipass set local.primary.disk=20GiB
   $ multipass set local.primary.cpus=4
   $ multipass set local.primary.memory=8G

This ensures you have enough space in the VM to install the MagAO-X software. (You can change the number of CPUs allocated to the VM to a number other than four if you want.)

Now, boot the virtual machine::

   $ multipass start

Notice that we didn't specify ``-n primary``. The name ``primary`` is special, and is used as the default for many commands when nothing else is specified.

Wait a minute for the VM to start, then connect your terminal to the VM with::

   $ multipass shell
   ubuntu@primary:~$

Next, within the VM, obtain a copy of the MagAO-X software and install scripts. Using ``git`` we clone the MagAOX repository::

   ubuntu@primary:~$ git clone --depth=1 https://github.com/magao-x/MagAOX.git
   Cloning into 'MagAOX'...
   remote: Enumerating objects: 1040, done.
   remote: Counting objects: 100% (1040/1040), done.
   remote: Compressing objects: 100% (907/907), done.
   remote: Total 1040 (delta 166), reused 642 (delta 100), pack-reused 0
   Receiving objects: 100% (1040/1040), 2.13 MiB | 1.04 MiB/s, done.
   Resolving deltas: 100% (166/166), done.

Go to the ``setup`` subdirectory::

   ubuntu@primary:~$ cd MagAOX/setup/

Run the provisioning script::

   ubuntu@primary:~/MagAOX/setup$ bash provision.sh

Now, wait a while. Don't be alarmed by the amount of output! Provisioning is very
noisy, and messages in red aren't necessarily errors. Successful
provisioning will end with the message

::

   Provisioning complete

Now, on to :ref:`vm_usage`.

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

   ubuntu@primary:~/MagAOX/setup$ bash provision.sh | tee ~/Home/provision.log

Resetting the VM
~~~~~~~~~~~~~~~~

If you need to reset the VM, start by copying any data you need out of it (e.g. to ``~/Home``). Then, to **delete it forever**, use these commands::

   $ multipass stop primary
   $ multipass delete primary
   $ multipass purge

To recreate the VM, follow the instructions from the top of the page again.

Also, in the unlikely event you encounter this error (maybe upon reinstalling multipass)::

   The client is not authenticated with the Multipass service.
   Please use 'multipass authenticate' before proceeding.

this `forum post <https://discourse.ubuntu.com/t/unable-to-authorize-the-client-and-cannot-set-a-passphrase-workaround/28321>`_ explains recovery steps.


.. _vm_usage:

Usage
-----

Configuring the VM to connect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you can remotely control MagAO-X, a little post-provisioning
configuration is required. You must have a user account on MagAO-X with
an SSH key file configured. For the preconfigured tunnels to work, that key must not have a passphrase.

If you have a key pair named ``id_ed25519`` in your computer's ``~/.ssh/`` folder, this appears at ``~/Home/.ssh/`` in the VM. Copy it into place::


   $ multipass shell
   ubuntu@primary:~$ cp ~/Home/.ssh/id_ed25519 ~/.ssh/id_ed25519
   ubuntu@primary:~$ chmod 600 ~/.ssh/id_ed25519

Next, you will need to edit the VM's ``~/.ssh/config`` file to add your username. Open a text editor::

   $ multipass shell
   ubuntu@primary:~$ nano ~/.ssh/config

At the end of the file, the line ``User YOURUSERNAME`` should be changed to reflect your MagAO-X username. Save and exit.

Connecting to the VM
^^^^^^^^^^^^^^^^^^^^

The ``multipass shell`` command we have been using above connects you to the VM. The following should be done within a VM except where otherwise noted.

Note: under some circumstances you will get a worrying-sounding message about ``Xauthority``. As long as things are working, it should be ignored.

.. _check_vm_connectivity:

Check connectivity to MagAO-X
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To ensure everything's configured correctly, from a ``multipass shell``
session run ``ssh aoc``, verify your shell prompt changes to ``exao1``, then ``exit``::

   ubuntu@primary:~$ ssh aoc
   [you@exao1] $ exit
   ubuntu@primary:~$

Start tunnels
^^^^^^^^^^^^^

The ``xctrl`` script is installed during provisioning, and a default set
of apps is configured to run on ``xctrl startup``. These apps launch SSH
tunnels to the instrument.

The proclist for VM usage is in
`magao-x/config/proclist_vm.txt <https://github.com/magao-x/config/blob/master/proclist_vm.txt>`__.

Running ``xctrl startup`` to start the tunnels should result in output
like::

   ubuntu@primary:~$ xctrl startup
   Session vm_aoc_milkzmq does not exist
   Session vm_aoc_indi does not exist
   Created tmux session for vm_aoc_milkzmq
   Created tmux session for vm_aoc_indi
   Executed in vm_aoc_milkzmq session: '/opt/MagAOX/bin/sshDigger -n vm_aoc_milkzmq'
   Executed in vm_aoc_indi session: '/opt/MagAOX/bin/sshDigger -n vm_aoc_indi'

And you can check their status with ``xctrl status`` or ``xctrl peek``.

::

   ubuntu@primary:~$ xctrl status
   vm_aoc_indi: running (pid: 6147)
   vm_aoc_milkzmq: running (pid: 6148)

Using GUIs in the VM
~~~~~~~~~~~~~~~~~~~~

The VM is configured to be “headless”, meaning there's no graphical
display window. However, we can still build and run MagAO-X GUIs as long
as your host OS has an X11 server (most Linux systems do by default, but
you will need `XQuartz <https://www.xquartz.org/>`__ on macOS).

If you're unfamiliar with SSH X forwarding, the short version is that
the app runs on the VM but the window pops up like any other window on
your own computer (the host). SSH (i.e. ``multipass shell``) is the
transport that moves information about the window back and forth to the
GUI app, which is still running inside the VM.

.. code:: text

   +------------------------------------------+
   |                  +----------------------+|
   |    Host OS       |          VM          ||
   |                  |                      ||
   |  [GUI window] <-SSH-> [MagAO-X GUI app] ||
   |                  +----------------------+|
   +------------------------------------------+

Assuming you have an SSH key on your host computer already, we need to teach multipass about it::

   $ multipass exec primary -- bash -c "echo `cat ~/.ssh/id_ed25519.pub` >> ~/.ssh/authorized_keys"

This adds the key as an authorized one for connecting to the VM. (We were connecting a different way when we did ``multipass shell`` earlier.)

The following incantation will connect a GUI-capable SSH session to your multipass VM and leave you at a VM prompt::

   $ ssh -Y ubuntu@$(multipass exec primary -- hostname -I | awk '{ print $1 }' )
   ubuntu@primary:~$

So, to start the ``coronAlignGUI``, you could do...

::

   $ ssh -Y ubuntu@$(multipass exec primary -- hostname -I | awk '{ print $1 }' )
   ubuntu@primary:~$ coronAlignGUI

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

After confirming the tunnel ``vm_aoc_milkzmq`` is running
(``xctrl status``), start a ``milkzmqClient``. For this example we'll
connect to ``camwfs`` and ``camwfs_dark``:

::

   ubuntu@primary:~$ milkzmqClient -p 9000 localhost camwfs camwfs_dark &

(We've used ``&`` at the end of the command to background the client, so
just hit enter again to get a normal prompt back after its startup
messages.)

The configuration in ``/opt/MagAOX/config`` includes ``rtimv`` config
files named for the various cameras (see the ``shmim_name`` options in
those files for hints about which images to replicate for a given
camera).

Start the viewer with

::

   ubuntu@primary:~$ rtimv -c rtimv_camwfs.conf

and it should pop up a window like this:

.. figure:: example_rtimv_xrif2shmim.png
   :alt: Example of rtimv viewer with 4 wavefront sensor pupils

   Example of rtimv viewer with 4 wavefront sensor pupils

For instructions on rtimv, consult its `user
guide <https://github.com/jaredmales/rtimv/blob/master/doc/UserGuide.md#rtimv>`__.
