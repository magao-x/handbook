Instrument computer setup guide
===============================

The setup process for the instrument computers (ICC, RTC, AOC) is
automated (to the extent possible) by scripts in the ``setup/``
folder of `magao-x/MagAOX <https://github.com/magao-x/MagAOX>`__.

Unfortunately, not *everything* can be automated when real hardware is
involved. To set up a new instrument computer, follow the steps below.
Once the BIOS and OS are setup, you can `run the provisioning
scripts <#run-provisioning-scripts>`__.

Once the hardware has been connected up, setup proceeds as follows.

**Important note about reinstalls vs. fresh installs:** At this point in the project, we are unlikely to have a completely fresh set of hardware and drives to set up. The below instructions were written under the assumption of a fresh install, so take care not to perform destructive actions like repartitioning on drives with data you want to **keep**. See :ref:`migration` for examples of what those data might be.

BIOS
----

For a new main board, the BIOS should be updated to the latest version.
This is necessary to ensure that the USB ports behave properly, as well
as to ensure that the iKVM module works.

The following settings should also be changed within the BIOS setup menu (reboot, then press F1 when prompted to enter).

For all of AOC/ICC/RTC
~~~~~~~~~~~~~~~~~~~~~~

::

   Boot
   |
    -- Network Device BBS Priorities -- set all to "disabled"
    -- Hard Drive BBS Priorities -- set "disabled" for all non-boot SSDs

   Advanced
   |
    -- ACPI Settings
      |
       -- Enable Hibernation [Disabled]
       -- ACPI Suspend State [Suspend Disabled]
    -- APM
      |
       -- Restore AC Power Loss [Power OFF]

(Note that the BIOS likes to reshuffle boot order when drives appear and
disappear in testing or RAID swapping. Disabling non-boot drives ensures
it doesn’t accidentally try to boot from them.)

For ICC/RTC
~~~~~~~~~~~

::

   AI Tweaker
   |
    -- Spread Spectrum [Disabled] {This is critical for allowing PCIe expanion to work}

   Advanced
   |
    -- PCI Subsystem Settings
      |
        -- Above 4G Decoding [Enabled] {This is critical for allowing PCIe expansion to work}

   IntelRCSetup
   |
    --Processor Configuration
      |
      -- DCU Mode [32KB 8Way Without ECC] {This is default, ECC not needed for new-style target and host cards}
   |
    --Miscellaneous Configuration
      |
      -- Active Video [Onboard Device] {Prevents sending video to a GPU}

OS Installation
---------------

The computers in MagAO-X run Rocky Linux 9.

**Workstations:** If you are installing a workstation, go to https://rockylinux.org/alternative-images and download the appropriate KDE ISO (x86_64, version 9). (**Note:** As of July 27, 2023, when you get to the installer desktop there is a message about the KDE Connect daemon crashing immediately after boot. It can be safely ignored.)

**Rack computers:** If you are installing one of the rack computers, go to https://rockylinux.org/download and download the appropriate minimal ISO (x86_64, version 9).

Burn it to a USB drive using Balena Etcher, or ``dd``, or similar. Reboot, choosing to enter BIOS setup (F1 key when prompted), then use the arrow keys to switch over to the boot menu. Make your USB device the first-choice boot device. Use F10 to save and exit BIOS and boot. Choose to install Rocky Linux with the arrow keys and hit enter to select.

**Workstations:** Double-click the "Install to Hard Drive" icon at upper left.

**Rack computers:** The image will boot directly into the installer. The installer is graphical, so use the iKVM or a connected VGA monitor plus keyboard and mouse to continue.

At the prompt choose "English (United States)" as the language for the installer. After clicking "Continue" you'll be at the ``Installation Summary`` page. Click on the following headings to make configuration changes before beginning installation:

Network & Hostname
~~~~~~~~~~~~~~~~~~

In the box at lower left, fill in the machine name (i.e. ``exao1`` for AOC, ``exao2`` for RTC, ``exao3`` for ICC). Configuring network adapters will happen after installation, once we change how the adapter names are selected.

Date & Time
~~~~~~~~~~~

-  Timezone: America/Phoenix

Partitions
~~~~~~~~~~

-  Select all disks
-  Select “I will configure partitioning”
-  On 2x 512 drives:

   -  1 GiB ``/boot`` - RAID 1
   -  16 GiB swap - RAID 1
   -  The rest as ``/`` - RAID 1

-  On the data drives (should be 3 or more identical drives):

   -  All space as ``/data`` - RAID 5

Detailed steps
^^^^^^^^^^^^^^

-  *If this is a reinstall:*

   -  Click on the arrow next to “CentOS Linux…” to expand the list of
      existing partitions.
   -  Click one to select and click the ``-`` button at the bottom of
      the list
   -  Check the box saying
      ``Delete all filesystems which are only used by CentOS Linux ...``
      and confirm

-  Choose partitioning scheme = Standard Partition in drop down menu
-  Then press ``+`` button:

   -  Mount Point: ``/boot``
   -  Desired Capacity: ``1 GiB``
   -  Now press ``Modify``

      -  Select the 2x 500 GB O/S drives (Ctrl-click)
      -  Press select

   -  Device Type: ``RAID - RAID 1``
   -  File System: ``XFS``

-  Press ``Update Settings``
-  Then press ``+`` button:

   -  Mount Point: swap
   -  Desired Capacity: 16 GiB
   -  Now press ``Modify``

      -  Select the 2 500 GB O/S drives (Ctrl-click)
      -  Press select

   -  Device Type: ``RAID - RAID 1``
   -  File System: ``XFS``
   -  Press ``Update Settings``

-  Then press ``+`` button:

   -  Mount Point: ``/``
   -  Desired Capacity: **blank**
   -  Now press ``Modify``

      -  Select the 2x 500 GB O/S drives (Ctrl-click)
      -  Press select

   -  Device Type: ``RAID - RAID 1``
   -  File System: ``XFS``
   -  Change Desired Capacity to **blank** (again)
   -  Press Update Settings

      -  should be using all available space for ``/``

-  Then press ``+`` button:

   -  Mount Point: ``/data``
   -  Desired Capacity: **blank**
   -  Now press ``Modify``

      -  Ctrl-click to select all the data drives (>500GB)
      -  Press select

   -  Device Type: ``RAID - RAID 5``
   -  File System: ``XFS``
   -  Change Desired Capacity to **blank** (again)
   -  Press Update Settings

      -  Should now have the full capacity for RAID 5 (N-1)

If you are prompted for a location to install the UEFI boot loader, you
have somehow booted in UEFI mode instead of Legacy Boot / BIOS mode.
(This has been observed booting from a liveUSB, despite UEFI boot being
disabled in BIOS, but it goes away after reordering boot options in the
BIOS interface and attempting to boot again.)

Software
~~~~~~~~

**ICC/RTC:**

From the list on the Left:

-  Select “Minimal install”

**AOC:**

From the list on the Left:

-  Select “KDE Plasma Workspaces”

From the list on the right:

-  Select “Development Tools”

Begin the installation
~~~~~~~~~~~~~~~~~~~~~~

Users
~~~~~

-  Set ``root`` password, choose to ``Lock root account`` so it cannot be used to log in
-  Create ``xdev`` user account (full name "MagAO-X Developer", but xdev to friends) for use after reboot. Use the usual password. **Check "Make this user administrator".**

After OS installation
---------------------

**Note:** For AOC, multiple monitors seem to confuse the default NVIDIA
drivers. Stick to the VGA output until the NVIDIA drivers are set up
(see below).

Update
~~~~~~

-  Log in as ``root``
-  Run ``dnf update -y``. You may also be prompted to accept some signing keys with ``y``.
-  Install a few essentials ``dnf install -y git tmux vim nano curl``

Check RAID status
~~~~~~~~~~~~~~~~~

Check RAID mirroring status: ``cat /proc/mdstat``. On new installs, it
takes some time for the initial synchronization of the drives. (Like,
“leave it overnight” time.)

Configure network interface naming
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SystemD, udev, and Dell have conspired to implement something called
“predictable network interface names” that could more accurately be
called “unpredictable network interface names”.

**Rocky 9.2:**

The old way seems to have gone, but there are now ""`SystemD Link Files <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/configuring_and_managing_networking/consistent-network-interface-device-naming_configuring-and-managing-networking#assigning-additional-names-to-network-interface-using-systemd-link-files_consistent-network-interface-device-naming>`_"?

1. ``sudo mkdir -p /etc/systemd/network && sudo vim /etc/systemd/network/10-ethernet-mac-addr-names.link``

2. Enter, for example::

      [Match]
      OriginalName=*

      [Link]
      NamePolicy=mac

3. **Reboot and verify the existence of /dev/en<hex mac>**

Configure network connections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Names for network interfaces are now tied to their hardware MAC address,
not their location on the PCI bus. The flip side is that replacing a NIC
with a new card will require repeating the below process, probably from
a seat at the computer. (However, this happens much less often than
rearranging GPUs and confusing NetworkManager with renumbered ``enXpY``
devices.)

-  Use ``ip a`` or ``nmcli`` to verify the new network names.

-  Unplug the ``instrument`` and other interfaces and run ``nmcli`` again,
   noting which of the interfaces shows up as connected

-  Copy the full name (``enxaabbccddeeff``) of the interface that is
   showing up as connected

-  In ``sudo nmtui``, rename or delete connections as necessary until
   there is only ``www-ua``, ``www-lco``, and ``instrument`` (**Note:**
   ICC has ``icc-to-rtc`` and RTC has ``rtc-to-icc`` to configure, which
   are a pair of NICs for low-latency transfer. ICC additionally has
   ``camsci1`` and ``camsci2``. Consult the :doc:`../networking` doc for their config.)

-  Edit the ``www-*`` connections to ensure the “Device” field is set to
   the interface name you just copied

-  Copy the full name for the instrument interface, plug its cable back
   in, and repeat the last step for the ``instrument`` connection

-  Activate the appropriate connections in ``nmtui`` (or with
   ``nmcli con down www-lco; nmcli con up www-ua; nmcli con up instrument``,
   swap ``www-ua`` and ``www-lco`` if necessary)

-  Choose ``Edit a connection`` in ``nmtui``

-  Highlight ``instrument`` and hit ``Enter``

   -  Under ``IPv4 CONFIGURATION`` ensure
      ``Never use this network for default route`` **is** checked with
      an ``[X]``
   -  At the bottom of the list, ensure ``Automatically connect`` and
      ``Available to all users`` **are** checked

-  Highlight ``www-ua`` and hit ``Enter``

   -  Under ``IPv4 CONFIGURATION`` ensure
      ``Never use this network for default route`` is **not** checked
   -  At the bottom of the list, ensure ``Available to all users`` **is** checked
   -  Ensure ``Automatically connect`` **is** checked, unless you are at the telescope

-  Highlight ``www-lco`` and hit ``Enter``

   -  At the bottom of the list, ensure ``Automatically connect`` is **not** checked (unless you are at the telescope)

-  Trust connections internal to the instrument:
   ``sudo nmcli con modify instrument connection.zone trusted``

-  Verify they are both active with the appropriate connection profile
   in ``nmcli``. Example from AOC:

   ::

      $ nmcli
      enx2cfda1c61ddf: connected to www-lco
              "Intel I210"
              ethernet (igb), 2C:FD:A1:C6:1D:DF, hw, mtu 1500
              ip4 default
              inet4 200.28.147.221/24
              route4 200.28.147.0/24
              route4 0.0.0.0/0
              inet6 fe80::f8dd:82f0:237d:a4f1/64
              route6 fe80::/64
              route6 ff00::/8

      enx2cfda1c61dde: connected to instrument
              "Intel I210"
              ethernet (igb), 2C:FD:A1:C6:1D:DE, hw, mtu 1500
              inet4 192.168.0.10/24
              route4 192.168.0.0/24
              inet6 fe80::e992:1899:f32c:95cf/64
              route6 ff00::/8
              route6 fe80::/64

-  Verify that the internet is reachable from the instrument
   (e.g. ``ping 8.8.8.8``) and the new config works to ping the machine
   from outside

Configure Tailscale
~~~~~~~~~~~~~~~~~~~

See the :doc:`../tailscale` section of the handbook for install instructions.

If this is a migration from an old install, you will need ``/var/lib/tailscale/tailscaled.state`` from the old machine. See :ref:`migration`.

You should also trust the `tailscale0` interface in the firewall::

   sudo firewall-cmd --zone trusted --add-interface tailscale0 && sudo firewall-cmd --zone trusted --add-interface tailscale0 --permanent

Configure ``/data`` array options
---------------------------------

We should be able to boot with zero of the drives in the ``/data`` array
without systemd dropping to a recovery prompt.

Edit ``/etc/fstab``, and on the line for ``/data`` replace ``defaults``
with the options ``noauto,x-systemd.automount``.

Setup ssh
---------

-  Install a key for at least one user in their ``.ssh`` folder, and
   make sure they can log in with it without requiring a password.

-  Now configure ``sshd`` to require key-based authentication. Do this by creating a file with ``sudo vim /etc/ssh/sshd_config.d/disable_password.conf``::

      PasswordAuthentication no

-  And finally, reload the sshd ``systemctl reload sshd``

Setup network attached storage (NAS)
------------------------------------

Follow the steps in :doc:`../nas` to create the ``/srv/nas`` mount.

AOC only: GPU drivers setup
---------------------------

Since we actually use the AOC GPU for **graphics** (shockingly enough),
you will need to install NVIDIA’s CUDA package with drivers before the
monitors will work right. **You’ll want ``ssh`` access in case anything
goes wrong, so make sure it’s working!**

0.  Before starting, make sure everything’s up to date:
    ``yum update -y``

1.  Download CUDA 10.1 from
    https://developer.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda_10.1.168_418.67_linux.run
    (or whatever version is current in
    `setup/steps/install_cuda.sh <https://github.com/magao-x/MagAOX/blob/master/setup/steps/install_cuda.sh>`__)
    and take note of where it is saved

2.  Install prerequisites:
    ``sudo yum install -y kernel-devel kernel-headers``

3.  As root, edit the line in ``/etc/default/grub`` that reads

    ::

       GRUB_CMDLINE_LINUX="[parts omitted] rhgb quiet"

    to read

    ::

       GRUB_CMDLINE_LINUX="[parts omitted] rhgb quiet rd.driver.blacklist=nouveau nouveau.modeset=0"

4.  Install the new grub config with
    ``sudo grub2-mkconfig -o /boot/grub2/grub.cfg``

5.  Create /etc/modprobe.d/blacklist-nouveau.conf with the contents

    ::

       blacklist nouveau
       options nouveau modeset=0

6.  Execute ``sudo systemctl set-default multi-user.target``

7.  Shut down

8.  Disconnect all monitors from the NVIDIA card

9.  Connect a monitor to the VGA port from the motherboard’s onboard
    graphics

10. Reboot to a text-mode prompt

11. Log in as ``root``

12. Run CUDA installer with
    ``bash cuda_10.1.168_418.67_linux.run --silent --driver --toolkit --samples``
    (or whatever version is downloaded)

13. Default to graphical boot:
    ``systemctl set-default graphical.target``

14. Shut down

15. Disconnect the VGA port, reconnect the battle station monitors

16. Open up System Settings -> Display & Monitor and arrange the monitor
    geometry to reflect reality

17. Edit ``/etc/default/grub`` to remove
    ``rd.driver.blacklist=nouveau nouveau.modeset=0`` from
    ``GRUB_CMDLINE_LINUX`` and run
    ``grub2-mkconfig -o /boot/grub2/grub.cfg``

18. Once everything’s working satisfactorily, we want to lock the kernel
    version (so that we don’t end up accidentally removing graphical
    boot capabilities with a ``yum update -y``):

    1. ``sudo yum install -y yum-versionlock``
    2. ``sudo yum versionlock kernel kernel-headers kernel-devel``

.. _automated_provisioning:

Perform (mostly) automated provisioning
---------------------------------------

Log in via ``ssh`` as a normal user with ``sudo`` access.

1. Clone `magao-x/MagAOX <https://github.com/magao-x/MagAOX>`__ into
   your home directory (**not** into ``/opt/MagAOX``, yet)

   ::

      $ cd
      $ git clone https://github.com/magao-x/MagAOX.git

2. Switch to the ``setup`` subdirectory in the MagAOX directory you
   cloned (in this example: ``~/MagAOX/setup``) to perform
   pre-provisioning steps (i.e. steps requiring a reboot to take effect)

   ::

      $ cd ~/MagAOX/setup
      $ ./pre_provision.sh

   This sets up an ``xsup`` user and the ``magaox`` and ``magaox-dev``
   groups. Because this step adds whoever ran it to ``magaox-dev``, you
   will have to **log out and back in**.

   On ICC and RTC, this step also installs the CentOS realtime kernel
   and updates the kernel command line for ALPAO compatibility reasons.
   It also adds settings to disable the open-source ``nouveau`` drivers
   for the NVIDIA card. This is so that the CUDA install proceeds
   without errors. You must reboot before continuing.

3. Reboot, verify groups

   ::

      $ sudo reboot
      [log in again]
      $ groups
      yourname magaox-dev ...

4. *(optional)* Install ``tmux`` for convenience

   ``tmux`` allows you to preserve a running session across ssh
   disconnection and reconnection. (Ten second tutorial: Running
   ``tmux`` with no arguments starts a new self-contained session.
   ``Ctrl-b`` followed by ``d`` detatches from it, while any scripts you
   started continue to run. The ``tmux attach`` command reattaches.)

   ::

      $ sudo yum install -y tmux

   (It’s used by the system, so it’ll get installed anyway, but you
   might want it when you run the install.)

   To start a new session for the installation:

   ::

      $ tmux

5. **RTC/ICC only:** Obtain proprietary / non-redistributable software
   from the team Box folder

   Go to
   `MagAO-X/vendor_software/ <https://arizona.box.com/s/dhmxrhjv00yh8lz4m0j7meivfaoyn9cn>`__
   *(invite required)*, click the “…” on ``bundle`` and choose
   “Download”. Save ``bundle.zip`` in ``MagAOX/setup/`` next to
   ``provision.sh``.

   .. figure:: download_bundle.png
      :alt: Screenshot of Box interface to download bundle

      Screenshot of Box interface to download bundle

   This bundle includes software for the Andor, ALPAO, and Boston
   Micromachines hardware.

6. Run the provisioning script as a normal user

   ::

      $ cd ~/MagAOX/setup
      $ bash ./provision.sh

   If you installed and invoked ``tmux`` in the previous step, this
   would be a good time to ``Ctrl-b`` + ``d`` and go get a coffee.

Successful provisioning will end with the message “Finished!” and
installed copies of MagAOX and its dependencies.

A lot of the things this script installs need environment variables set,
so ``source /etc/profile.d/*.sh`` to keep working in the same terminal
(or just log in again).

Perform ``xsup`` key management
-------------------------------

A new installation will generate new SSH keys for ``xsup``.

If you have
an existing ``.ssh`` folder for the machine role (ICC, RTC, AOC) you’re
setting up, you can just copy its contents over the new
``/home/xsup/.ssh/`` (taking care not to change permissions). See :ref:`migration`.

If not, you must ensure passwordless SSH works bidirectionally by
installing other servers’ ``xsup`` keys and installing your own in their
``/home/xsup/.ssh/authorized_keys``.

In the guide below, ``$NEW_ROLE`` is the role we just set up and
``$OTHER_ROLE`` is each of the other roles in turn. (For example, if we
just set up the RTC, ``$NEW_ROLE == RTC`` and ``$OTHER_ROLE`` would be
ICC and AOC.)

Step-by-step
~~~~~~~~~~~~

For each of the ``$OTHER_ROLE``\ s:

1. On ``$NEW_ROLE``, copy ``/home/xsup/.ssh/id_ed25519.pub`` to the
   clipboard
2. Connect to ``$OTHER_ROLE`` with your normal user account over SSH
3. Become ``xsup`` on ``$OTHER_ROLE`` and edit
   ``/home/xsup/.ssh/authorized_keys`` to insert the one you copied
4. On ``$OTHER_ROLE``, copy ``/home/xsup/.ssh/id_ed25519.pub`` to the
   clipboard
5. Back on ``$NEW_ROLE``, append the key you just copied to
   ``/home/xsup/.ssh/authorized_keys``
6. On ``$NEW_ROLE``, test you can ``ssh $OTHER_ROLE`` as ``xsup``
   (potentially amending ``~/.ssh/known_hosts``)
7. On ``$OTHER_ROLE``, test you can ``ssh $NEW_ROLE`` as ``xsup``
   (potentially amending ``~/.ssh/known_hosts``)

Verify bootloader installation / RAID correctness
-------------------------------------------------

-  Ensure RAID arrays are fully built with ``cat /proc/mdstat``
-  ``shutdown``
-  Pop one of the two boot drives from the SSD cage
-  Boot, verify that 1) ``grub`` appears and 2) the OS comes up (after a
   longer boot delay)
-  Replace that boot drive, reboot
-  Ensure RAID arrays are fully **rebuilt** with ``cat /proc/mdstat``
-  Pop the other drive
-  Repeat verification steps
-  Replace boot drive
-  Boot with both in place
-  Shutdown, pop **all** data drives
-  Ensure boot proceeds without dropping to recovery prompt
-  Replace all data drives, boot with everything in place

.. _migration:

Migrating data from a previous installation
-------------------------------------------

There are several very important files to retain when reinstalling the operating system.

  - ``/var/lib/tailscale/tailscaled.state`` -- this file allows the machine to keep its name and IP address on the tailnet
  - ``/etc/ssh/ssh_host_*_key*`` -- these files allow clients to connect over SSH without triggering a scary warning and requiring manual intervention
  - ``/home/xsup/.ssh/{authorized_keys,id_ed25519,id_ed25519.pub,known_hosts}`` -- these files allow ``xsup`` to connect to other MagAO-X machines without prompting for host key verification
  - ``/etc/{passwd,group,shadow}`` -- these files contain the UID and GID mappings and user passwords to restore
  - ``/etc/systemd/system/renew_certificates.service.d/override.conf`` -- API credentials used by the ``lego`` command to renew HTTPS certificates used by the web UI

You may additionally want to back up the user home directories to retain their configuration files, though they should store data on the `/data` partition.