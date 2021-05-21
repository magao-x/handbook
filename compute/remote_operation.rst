Remote operation
================

The MagAO-X software is designed for use on Linux with CentOS 7, and the
included `provisioning
script <https://github.com/magao-x/MagAOX/blob/master/setup/provision.sh>`__
will automatically set up a fresh install on a computer running that OS.
However, most of us don’t use CentOS 7 on our personal computers.
Furthermore, the provisioning script will create users and groups, applying
configuration you probably don't want!

If you don't fancy installing the full set of dependencies by hand,
or you're on a Windows or macOS machine, you should use a virtual
machine (VM). A virtual machine is a simulated computer (running
whatever “guest OS” you like) that runs as a program on your computer’s
OS (which we call the “host OS”). This virtual machine can then be used
to operate all the normal MagAO-X GUI and CLI tools and control the real
instrument.

Conceptually, you just create a virtual CentOS computer and go through
the normal installation process on it. To automate this process, and
make certain customizations for speed and convenience, there’s
`Vagrant <https://www.vagrantup.com/>`__. Vagrant can start a virtual
machine from a pre-made image, run your install script, and configure
things like forwarding network ports from the VM to your host OS.

As it happens, MagAO-X has a
`Vagrantfile <https://github.com/magao-x/MagAOX/blob/master/Vagrantfile>`__
specifying the setup process to minimize the number of manual steps.

Prerequisites
-------------

-  ``git`` — Preinstalled on most Linuxes, install with
   ``xcode-select --install`` on macOS, see
   `below <#additional-notes-for-windows-users>`__ for Windows
-  `VirtualBox <https://www.virtualbox.org/>`__ — Preferred
   virtualization backend, available for free. (`download <https://www.virtualbox.org/wiki/Downloads>`__, `install instructions <https://www.virtualbox.org/manual/ch02.html>`__)
-  `Vagrant <https://www.vagrantup.com/>`__ — Program to automate
   creation / provisioning of development VMs (`download <https://www.vagrantup.com/downloads>`__, `install instructions <https://www.vagrantup.com/docs/installation>`__)

.. warning::

   **Linux users, do not use** ``apt`` **or** ``yum`` **to install Vagrant or VirtualBox.**

   From the Vagrant `docs <https://learn.hashicorp.com/tutorials/vagrant/getting-started-install?in=vagrant/getting-started#caveats>`__:
   "Some operating system distributions include a vagrant package in their upstream package repos.
   Please do not install Vagrant in this manner. Typically these packages are
   missing dependencies or include very outdated versions of Vagrant. If you
   install via your system's package manager, it is very likely that you will
   experience issues. Please use the official installers on the `downloads page <https://www.vagrantup.com/downloads>`__."

Additional notes for Windows users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Windows use isn’t tested automatically, and things may break
unexpectedly…*

1. It’s probably easiest to get ``git`` from
   `Anaconda <https://docs.anaconda.com/anaconda/install/windows/>`__ if
   you’re already using it (use ``conda install git`` at the Anaconda
   command line)
2. ``git`` needs to be configured not to alter line endings. After
   installing git, you should do
   ``git config --global core.autocrlf false`` *before* cloning MagAOX.
   (However, if you use ``git`` for other things, you may not want this
   to be a global setting.)
3. The existence of a ``windows_host.txt`` advisory file is **required**
   for provisioning to succeed. (Its presence tells the scripts to work
   around functionality that is missing on Windows hosts.)
4. The section below on `Using GUIs in the VM <#Using-GUIs-in-the-VM>`__
   needs to be expanded with instructions for Windows. (Basically, we
   need to figure out which of the X11 servers for Windows works with
   ``vagrant ssh`` in the current configuration.) Until then, no GUIs in
   Windows.

Setup
-----

1. Ensure ``vagrant`` command is available:

   .. code:: text

      $ vagrant --help
      Usage: vagrant [options] <command> [<args>]
      ...

2. Clone `magao-x/MagAOX <https://github.com/magao-x/MagAOX>`__ (if
   necessary) and ``cd`` into MagAOX

   .. code:: text

      $ git clone https://github.com/magao-x/MagAOX.git
      Cloning into 'MagAOX'...
      ...

      $ cd MagAOX

3. **Windows only:** Create a new blank file named ``windows_host.txt``
   in the MagAOX folder.

4. Run ``vagrant up``

   .. code:: text

      $ vagrant up

   If prompted, enter your password to configure NFS exports. (See `this
   doc <https://www.vagrantup.com/docs/synced-folders/nfs.html#root-privilege-requirement>`__
   for information on eliminating that prompt.)

   **Note:** The ``vagrant up`` step is CPU and bandwidth intensive the
   first time, as it will download an OS image and all of the MagAO-X
   dependencies, then compile them. Subsequent ``vagrant up``\ s will
   just boot the existing machine.

Don’t be alarmed by the output from ``vagrant up``. Provisioning is very
noisy, and messages in red aren’t necessarily errors. Successful
provisioning will end with the message

::

   Provisioning complete

What to do if you don’t see ``Provisioning complete``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most likely that means an error occurred running the provisioning
scripts and they did not finish. That can happen if a big download gets
interrupted, for example. It’s always safe to run ``vagrant provision``
and it’ll re-run only necessary steps, which may be enough to get you to
``Provisioning complete``.

If that doesn’t resolve the issue, you’ll need the complete provisioning
output to get help. The following command will save it to a file
``provision.log``, which you can then email or Slack to someone who can
help.

::

   $ vagrant provision | tee provision.log

Usage
-----

Connecting
~~~~~~~~~~

To connect to the VM, use ``vagrant ssh``. You’ll be logged in as user
``vagrant`` with no password, and the command prompt in your shell will
change to something like this:

::

   [vagrant@centos7] $

The rest of the commands in this section are to be run in a
``vagrant ssh`` session, unless otherwise noted.

Remotely controlling MagAO-X
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you can remotely control MagAO-X, a little post-provisioning
configuration is required. You must have a user account on MagAO-X with
an SSH key file configured. (This will probably be called something like
``~/.ssh/id_ecdsa`` on your host computer, with the corresponding file
``~/.ssh/id_ecdsa.pub`` added to your authorized keys on the MagAO-X
computers.)

With the username and key file handy, go to the folder where you cloned
the ``MagAOX`` repository. There will be a subfolder called ``vm/``
where the provisioning process placed a lot of files. In ``vm/ssh/``
edit the ``config`` file. At the end you will see

::

   Host *
     User YOURUSERNAME

which you should update with the username you use on MagAO-X computers.
Notice the line at the top that says
``IdentityFile /vagrant/vm/ssh/magaox_ssh_key``. This tells the VM to
use the key file at ``vm/ssh/magaox_ssh_key`` from the host to
authenticate you. Copy the key file you identified before and rename it
to ``magaox_ssh_key`` and store it in the same directory as ``config``.

Check connectivity
^^^^^^^^^^^^^^^^^^

To ensure everything’s configured correctly, from a ``vagrant ssh``
session run ``ssh rtc``, then ``exit``:

::

   [vagrant@centos7] $ ssh rtc
   [you@exao2] $ exit
   [vagrant@centos7] $

Start tunnels
^^^^^^^^^^^^^

The ``xctrl`` script is installed during provisioning, and a default set
of apps is configured to run on ``xctrl startup``. These apps launch SSH
tunnels to the instrument.

The proclist for VM usage is in
`magao-x/config/proclist_vm.txt <https://github.com/magao-x/config/blob/master/proclist_vm.txt>`__.

Running ``xctrl startup`` to start the tunnels should result in output
like:

::

   [vagrant@centos7 ~]$ xctrl startup
   Session vm_aoc_milkzmq does not exist
   Session vm_aoc_indi does not exist
   Created tmux session for vm_aoc_milkzmq
   Created tmux session for vm_aoc_indi
   Executed in vm_aoc_milkzmq session: '/opt/MagAOX/bin/sshDigger -n vm_aoc_milkzmq'
   Executed in vm_aoc_indi session: '/opt/MagAOX/bin/sshDigger -n vm_aoc_indi'

And you can check their status with ``xctrl status`` or ``xctrl peek``.

::

   [vagrant@centos7 ~]$ xctrl status
   vm_aoc_indi: running (pid: 6147)
   vm_aoc_milkzmq: running (pid: 6148)

Using GUIs in the VM
~~~~~~~~~~~~~~~~~~~~

The VM is configured to be “headless”, meaning there’s no graphical
display window. However, we can still build and run MagAO-X GUIs as long
as your host OS has an X11 server (most Linux systems do by default, but
you will need `XQuartz <https://www.xquartz.org/>`__ on macOS).

If you’re unfamiliar with SSH X forwarding, the short version is that
the app runs on the VM but the window pops up like any other window on
your own computer (the host). SSH (i.e. ``vagrant ssh``) is the
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

So, to start the ``coronAlignGUI``, you could do…

::

   host$ vagrant ssh
   vm$ coronAlignGUI

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
and a limit of 1 FPS. This ensures it doesn’t overwhelm your home
internet connection.

(Napkin math: 1024 \* 1024 \* 16 bit, or one ``camsci1`` frame, is ~2
MB. 2 MByte / second is 16 Mbit / second, more than compressed HD video
streams. And that’s just one camera!)

The list of images re-served by AOC is kept in
``/opt/MagAOX/config/mzmqServerAOC.conf`` (`view on
GitHub <https://github.com/magao-x/config/blob/master/mzmqServerAOC.conf>`__).

After confirming the tunnel ``vm_aoc_milkzmq`` is running
(``xctrl status``), start a ``milkzmqClient``. For this example we’ll
connect to ``camwfs`` and ``camwfs_dark``:

::

   milkzmqClient -p 9000 localhost camwfs camwfs_dark &

(We’ve used ``&`` at the end of the command to background the client, so
just hit enter again to get a normal prompt back after its startup
messages.)

The configuration in ``/opt/MagAOX/config`` includes ``rtimv`` config
files named for the various cameras (see the ``shmim_name`` options in
those files for hints about which images to replicate for a given
camera).

Start the viewer with

::

   rtimv -c rtimv_camwfs.conf

and it should pop up a window like this:

.. figure:: example_rtimv_xrif2shmim.png
   :alt: Example of rtimv viewer with 4 wavefront sensor pupils

   Example of rtimv viewer with 4 wavefront sensor pupils

For instructions on rtimv, consult its `user
guide <https://github.com/jaredmales/rtimv/blob/master/doc/UserGuide.md#rtimv>`__.
