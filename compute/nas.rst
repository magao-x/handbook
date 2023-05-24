Network Attached Storage
========================

Network attached storage (NAS), sometimes simply called "the file server" is a place we can store large amounts of data that is administered by the Steward Observatory Computer Support Group for common use by astronomy research groups (while keeping the data private).

The Steward NAS is on the Steward wired network at ``matrix.as.arizona.edu`` (``10.130.133.220``) exposed over SMB/CIFS. Currently (May 2023), we are allocated 15 TB of space.

Connecting a server to the Steward NAS
--------------------------------------

Assuming a CentOS-like Linux server, you will need to install CIFS tools to get ``mount.cifs``::

    sudo yum install cifs-utils

Or, on Ubuntu::

    apt install cifs-utils

Make a new file in ``/root`` and lock down its permissions::

    sudo su
    cd
    touch steward_nas.credentials
    chmod 0600 steward_nas.credentials

Now, edit the file you just created. Within ``steward_nas.credentials`` the only contents should be::

    username=ASTR-MagAO-X
    password=12345678abcdef
    domain=BLUECAT

The current password for the ``ASTR-MagAO-X`` service account is obtainable from the Computer Support Group or another server's ``/root/steward_nas.credentials`` file (if accessible).

Next, create the mountpoint at ``/srv/nas``::

    mkdir -p /srv/nas

These instructions are designed for a MagAO-X machine, with an ``xsup`` user account and ``magaox`` user group. Obtain the numerical uid and gid for these entities::

    # id xsup
    uid=1000(xsup) gid=1000(xsup) groups=1000(xsup),10(wheel),100(users),1011(magaox),1012(magaox-dev)

Finally, put the mount information (and the large number of mount options) into ``/etc/fstab``. The line below should be modified to replace ``uid=1000,gid=1011`` with the numbers from the last step, if different. These options have the effect of making every file appear to be owned by ``xsup``/``magaox``, with permissions for all ``magaox`` group users to modify it. (This is necessary because the user database on MagAO-X is separate from the University of Arizona directory.) ::

    //10.130.133.220/jrmales  /srv/nas  cifs  noauto,x-systemd.automount,nofail,x-systemd.device-timeout=10s,x-systemd.requires=network.target,vers=default,credentials=/root/steward_nas.credentials,uid=1000,gid=1011,forceuid,forcegid,file_mode=0660,dir_mode=0770  0 0

This specifies that ``/srv/nas`` should point to ``//10.130.133.220/jrmales``, the per-group folder we were given in the Steward NAS. The options ``noauto,x-systemd.automount,nofail,x-systemd.device-timeout=10s,x-systemd.requires=network.target`` try to minimize the annoyance of (re-)booting the machine in a situation where it cannot reach ``matrix.as.arizona.edu``.

Use ``systemctl daemon-reload`` and then ``systemctl start srv-nas.automount``. Check if the mount came up by doing ``ls /srv/nas``::

    [root@exao0 ~]# ls -la /srv/nas
    total 55705
    drwxrwx---. 2 xsup magaox         0 Apr 24 09:43 .
    drwxr-xr-x. 3 xsup magaox        17 Apr 17 16:58 ..
    drwxrwx---. 2 xsup magaox         0 Apr 24 09:43 fits
    drwxrwx---. 2 xsup magaox         0 Apr 24 09:38 obs

Connecting your own computer to the Steward NAS
-----------------------------------------------

Your first step should be to install :doc:`tailscale` following instructions for your operating system. Then, to connect:

**macOS:** On macOS, open Finder and then go to the "Go" menu and select "Connect to Server..." (alternatively, hit command-K). The top text box accepts a URL for connection, which should be ``smb://YOURNETID@10.130.133.220/jrmales`` where ``YOURNETID`` is, well, your NetID from University of Arizona. You can "favorite" the url using the "+" button at lower left. Click "Connect". You will be prompted for a password, which is just your NetID password.

This will pop open a window with the contents of the ``jrmales`` share on the NAS. You'll also have a new entry in the sidebar of your Finder window labeled ``10.130.133.220``. (Clicking that takes you to the top level list of shares, from which you can drill down into ``jrmales``.)

You can also drag icons from the Finder onto a terminal to get their full path, so you can do things like::

    % fitsheader /Volumes/jrmales/obs/2023A/2023-03-08_09/jdl@fastmail.com/20230309T094454_camacq_walking_in/camacq/camacq_20230309094657696886820.fits

This lets you view the header of a file without explicitly copying it to the local machine first.

**Linux:** You may need to install additional tools to access CIFS/SMB shares from Linux. These are usually called something like "samba" or "cifs-utils". Consult documentation for your Linux distribution or the ever-helpful Google.

**Windows:** Consult Sebastiaan Haffert, Ph.D., the best Windowser in astronomy.