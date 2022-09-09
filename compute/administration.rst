System Maintenance & Administration
===================================

Adding a new user or developer account
--------------------------------------

User accounts on the RTC, ICC, and AOC machines are members of
``magaox``. Developer accounts are additionally members of
``magaox-dev`` and ``wheel``.

``/opt/MagAOX/source/MagAOX/setup/`` contains scripts to help you
remember which groups and what permissions the ``~/.ssh`` folder should
have.

``add_a_user.sh``
~~~~~~~~~~~~~~~~~

Creates a new user account in the group ``magaox``, creates ``.ssh``
(``u=rwx,g=r,o=r``), and ``.ssh/authorized_keys`` (``u=rw,g=,o=``).

Example:

::

   $ /opt/MagAOX/source/MagAOX/setup/add_a_user.sh klmiller

``add_a_developer.sh``
~~~~~~~~~~~~~~~~~~~~~~

Just like ``add_a_user.sh`` (in fact, uses it). Additionally adds the
new account to the ``wheel`` (RTC/ICC) or ``sudo`` (AOC) group and
``magaox-dev`` groups.

Configuring git for a new user account
--------------------------------------

We use GitHub Personal Access Tokens coupled with HTTPS push to
synchronize changes on the instrument. Configuration is required for
your credentials to be remembered.

1. Log in to the computer (AOC, RTC, ICC, vm, etc) where you want to
   configure git

2. Change directories to a repository (e.g. ``cd /opt/MagAOX/calib``)
   and verify it is set up for HTTPS push:

   ::

      $ cd /opt/MagAOX/calib
      $ git remote -v
      origin   https://github.com/magao-x/calib.git (fetch)
      origin   https://github.com/magao-x/calib.git (push)

3. If you haven’t already for this machine, configure your name and
   email address:

   ::

      $ git config --global user.email "youremailusernamehere@youremaildomainhere.com"
      $ git config --global user.name "Your Name Here"

4. Configure the ‘store’ credential helper, which will store your
   credentials so you do not have to re-enter them:

   ::

      $ git config --global credential.helper store

5. Create (or retrieve from your password manager) a GitHub Personal
   Access Token. If you don’t have one, log in to GitHub and visit
   https://github.com/settings/tokens.

6. Attempt to push, and enter/paste your username and **personal access
   token as password**:

   ::

      $ git push
      Username for 'https://github.com/magao-x/calib.git': your-github-user-name
      Password for 'https://your-github-user-name@github.com/magao-x/calib.git':

   (Note that even if you don’t see it, your key is being entered.)

7. Attempt to push again. You should not be prompted for credentials a
   second time.

Upgrading NVIDIA CUDA and drivers
---------------------------------

The CUDA install script at
https://github.com/magao-x/MagAOX/blob/master/setup/steps/install_cuda.sh
will install CUDA on a new system (provided that
`pre_provision.sh <https://github.com/magao-x/MagAOX/blob/master/setup/pre_provision.sh>`__
is run first, and the system is rebooted).

Upgrading CUDA is more involved, as the systems stubbornly insist on
loading the driver even when asked nicely not to, and the installer
won’t work if the driver is loaded.

1.  (on AOC only) Default to text-based boot:
    ``systemctl set-default multi-user.target``

2.  Disable all the driver modules.

    Open ``/etc/default/grub`` and append the following to the line
    beginning ``GRUB_CMDLINE_LINUX_DEFAULT`` (inside the quotes):

    ::

       nvidia_modeset.blacklist=1 nvidia_uvm.blacklist=1 nvidia.blacklist=1 rd.driver.blacklist=nvidia_modeset,nvidia_uvm,nvidia

3.  Install the new config with
    ``sudo grub2-mkconfig -o /boot/grub2/grub.cfg``

4.  Reboot, verify with ``lsmod | grep nv`` that no driver modules
    loaded

5.  Use ``sudo /usr/bin/nvidia-uninstall`` to uninstall the driver
    (choosing “No” when asked whether to “attempt restoration of the
    original X configuration file”)

6.  Use ``sudo /usr/local/cuda/bin/cuda-uninstaller`` to uninstall CUDA
    (checking all available options before choosing “Done”) This may leave a
    vestigial ``/usr/local/cudaXX.YY`` folder (where ``XX.YY`` is a version
    number) that can most likely be safely removed. (It's probably just some
    temporary files that the installer didn't create and is too polite
    to remove.)

7.  Remove the boot options that disable the driver.

    Open ``/etc/default/grub`` and remove the added options from
    ``GRUB_CMDLINE_LINUX_DEFAULT``.

8.  Install the new config with
    ``sudo grub2-mkconfig -o /boot/grub2/grub.cfg``

9.  Reboot again! Verify no driver is loaded again!

10. Install CUDA using
    ``sudo bash -x /opt/MagAOX/source/MagAOX/setup/steps/install_cuda.sh``

11. (on AOC only) Default to graphical boot again with
    ``systemctl set-default graphical.target`` and complete boot to
    graphical desktop with ``systemctl isolate graphical.target``

12. Rebuild MAGMA with the new version of CUDA:

::

   cd /opt/MagAOX/vendor/magma-X.Y.Z
   make clean
   make -j 32
   make install

Upgrading the RT kernel
-----------------------

The CentOS 7 RT kernel includes backported patches from the mainline
kernel to 3.10.0 where CentOS 7 was frozen, plus the PREEMPT RT patch
set and bug fixes from newer versions of that. On occasion a new version
will appear in the `CentOS 7 RT package
repository <http://mirror.centos.org/centos/7/rt/x86_64/Packages/>`__
and it may be worth upgrading to see if any of our bugs are fixed.

1. Remove ``versionlock`` (if any): ``yum versionlock delete kernel-rt``

2. ``sudo yum update kernel-rt kernel-rt-devel``

3. Reboot, verify new version in ``uname -a``

4. Reinstall drivers with kernel modules:

   -  NVIDIA (all machines)

      1. ``sudo /usr/bin/nvidia-uninstall``
      2. Use ``sudo /usr/local/cuda/bin/cuda-uninstaller`` to uninstall CUDA
         (checking all available options before choosing “Done”) This may leave a
         vestigial ``/usr/local/cudaXX.YY`` folder (where ``XX.YY`` is a version
         number) that can most likely be safely removed. (It's probably just some
         temporary files that the installer didn't create and is too polite
         to remove.)
      3. ``cd /opt/MagAOX/vendor/cuda`` and
         ``bash cuda_11.1.1_455.32.00_linux.run --extract=/tmp/cuda11``
         (or as appropriate for the version of CUDA you have)
      4. Become root: ``/usr/bin/sudo -i``
      5. ``cd /tmp/cuda11``
      6. Verify ``realpath $(which cc)`` is ``/usr/bin/gcc`` (and not
         the DevToolset-7 one)
      7. ``export IGNORE_PREEMPT_RT_PRESENCE=1``
      8. Run the installer: ``bash NVIDIA-Linux-x86_64-455.32.00.run``
      9. On next reboot, verify ``nvidia-smi`` works and shows all cards

   -  EDT (RTC, ICC)

      1. ``cd /opt/MagAOX/source/MagAOX/setup/steps``
      2. ``sudo mv /opt/EDTpdv /opt/EDTpdv.oldkernel``
      3. ``sudo bash install_edt.sh``

   -  ALPAO (RTC, ICC)

      1. ``cd /opt/MagAOX/source/MagAOX/setup/steps``
      2. ``sudo bash install_alpao.sh``

   -  BMC (RTC)

      1. ``cd /opt/MagAOX/vendor/bmc``
      2. ``sudo bash install.sh``

   -  Andor (ICC)

      1. ``cd /opt/MagAOX/source/MagAOX/setup/steps``
      2. ``bash install_andor.sh``

5. Reboot, verify hardware is working (e.g. ``nvidia-smi``, cameras all
   connecting, etc)
