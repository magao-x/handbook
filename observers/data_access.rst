Accessing data as a guest observer
==================================

MagAO-X (but not all visiting instruments) record data in a compressed format. Standard FITS-formatted data with full headers is produced during observations, becoming available within a few minutes of the start of the observation. This document explains how to access it.

**Extremely short version, for those who just need a refresher:** ``rsync -kaz --progress guestobs@exao1.lco.cl:/data/obs/vizzy@xwcl.science/ ./my_obs/``

Observation data are exported to the Adaptive optics Operator Computer, aka AOC or ``exao1``. Note that ``exao1`` is part of the instrument, and ships back and forth to Chile for observing runs. That means two things:

1. It will not be available for several weeks while it is in transit, and
2. It has a different IP and host-name when it's at University of Arizona than when it's at Las Campanas Observatory.

Guest observers will access exao1 with SSH and (preferably) rsync. (Users on Windows may be able to use WinSCP or rclone.)

Preliminaries
-------------

First, you will need an SSH key pair. Generating one is outside the scope of this document, but GitHub has a `good guide <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_. (You can choose Mac, Windows, or Linux, and you need only follow the steps under the first heading: "Generating a new SSH key".)

The key consists of a private half, probably named something like ``id_ed25519``, and a public half, named something like ``id_ed25519.pub``. (Note: ``id_rsa`` and ``id_dsa`` keys are not usable with MagAO-X. You may use ECDSA or ED25519 keys.)

**Send the ".pub" file to the MagAO-X team, keeping the private part private.**

Connecting
----------

This is **different** depending on whether MagAO-X is in Tucson or at LCO.

When MagAO-X is in the lab
^^^^^^^^^^^^^^^^^^^^^^^^^^

Log in using the ``guestobs`` account to verify everything works and that you have access (accepting the key fingerprint if needed)::

    % ssh guestobs@exao1.as.arizona.edu
    The authenticity of host 'exao1.as.arizona.edu (128.196.208.35)' can't be established.
    ED25519 key fingerprint is SHA256:Azbcyun8qHxuhl0GE9AyG1cPajNPnfKlTQCwTfCMFT0.
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    Warning: Permanently added 'exao1.as.arizona.edu' (ED25519) to the list of known h
    Last login: Thu Apr  7 15:28:49 2022 from 10.8.22.67
    [guestobs@exao1] $


When MagAO-X is at Las Campanas, and so are you
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When located at Las Campanas, the operator computer can be reached from the ``LCO-STAFF`` network at the address exao1.lco.cl.

Log in using the ``guestobs`` account to verify everything works and that you have access (accepting the key fingerprint if needed)::

    % ssh guestobs@exao1.lco.cl
    The authenticity of host 'exao1.lco.cl (200.28.147.221)' can't be established.
    ED25519 key fingerprint is SHA256:Azbcyun8qHxuhl0GE9AyG1cPajNPnfKlTQCwTfCMFT0.
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    Warning: Permanently added 'exao1.lco.cl' (ED25519) to the list of known h
    Last login: Thu Apr  7 15:28:49 2022 from 10.8.22.67
    [guestobs@exao1] $

When MagAO-X is at Las Campanas, and you are off-site
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Contact the MagAO-X team for updated instructions.*

Browsing the data
-----------------

Your data are rooted in ``/data/obs/your@email.com/``. So, for example, ``/data/obs/jrmales@arizona.edu/2022B/`` will contain::

    [guestobs@exao1] $ ls /data/obs/jrmales@arizona.edu/2022B/
    2022-10-22_23
    [... and so on ...]

and an individual night will contain a folder per target::

    [guestobs@exao1] $ ls /data/obs/jrmales@arizona.edu/2022B/2022-12-02_03
    tet01OriC
    [... and so on ...]

When there is no catalog target active, the observations will be grouped under the folder ``UNKNOWN``. (In rare cases there could be no catalog header at all, which will result in a ``_no_target_`` folder name.)

Within the target folder are folders for every observation interval (i.e. toggle of the "recording" switch)::

    [guestobs@exao1] $ ls /data/obs/jrmales@arizona.edu/2022B/2022-12-02_03/tet01OriC/
    camacq-astrom_20221203T071725
    tet1Orib-astrometry-50-50-infocus_20221203T082958
    [... and so on ...]

Note that the UT start timestamp is appended to the name to prevent collisions. Within those folders, there is a folder for each science camera that was actively recording (usually just camsci1 and camsci2)::

    [guestobs@exao1] $ ls /data/obs/jrmales@arizona.edu/2022B/2022-12-02_03/tet01OriC/tet1Orib-astrometry-50-50-infocus_20221203T082958/
    camsci1
    camsci2

You can use your favorite tool to browse, but we recommend ``rsync`` to handle the large numbers of images. (See the following section.)

Downloading science data
------------------------

You can use ``rsync`` to get your images out. Here's an example to download/update all images (from all semesters) for the observer ``vizzy@xwcl.science``, skipping those you already have::

    $ rsync -kaz --progress \
        guestobs@exao1.magao-x.org:/data/obs/vizzy@xwcl.science/ \
        ./my_magao-x_obs/

    receiving file list ... done
    created directory ./my_magao-x_obs
    camsci1/camsci1_20220417230302255087061.fits
        8640 100%   31.25kB/s    0:00:00 (xfer#3429, to-check=1436/4867)
    camsci1/camsci1_20220417230302258540922.fits
        8640 100%   31.13kB/s    0:00:00 (xfer#3430, to-check=1435/4867)
    [... many lines omitted ...]

    sent 5016 bytes  received 221150763 bytes  23279555.68 bytes/sec
    total size is 221081847  speedup is 1.00

The ``-k`` option ensures directories are copied with their full contents (rather than symbolic links). The ``-a`` "archives" (copies recursively, preserving metadata). The ``-z`` option compresses the files in transit.

Re-running this command will only sync changed files. During an observation, new frames will be processed in chunks as they are written, so you may want to re-run this command periodically.

The paths are constructed as follows: ``/data/obs/<observer email>/<semester>/<datestamp>/<catalog name of object>/<purpose>_<start UT>/<device>/``.

So, for example, here's mock output of ``tree /data/obs/ -L 4``::

    /data/obs/
    ├── 2022B
    │   ├── 2022-12-02_03
    │   │   └── tet01OriC
    │   │       └── jrmales@arizona.edu
    │   └── 2022-12-03_04
    │       ├── gam02Vel
    │       │   └── jrmales@arizona.edu
    │       ├── HD20121
    │       │   └── warrenbfoster@arizona.edu
    │       └── PDS201
    │           └── lclose@as.arizona.edu
    ├── jrmales@arizona.edu
    │   └── 2022B
    │       ├── 2022-12-02_03
    │       │   └── tet01OriC -> /data/obs/2022B/2022-12-02_03/tet01OriC/jrmales@arizona.edu
    │       └── 2022-12-03_04
    │           └── gam02Vel -> /data/obs/2022B/2022-12-03_04/gam02Vel/jrmales@arizona.edu
    ├── lclose@as.arizona.edu
    │   └── 2022B
    │       └── 2022-12-03_04
    │           └── PDS201 -> /data/obs/2022B/2022-12-03_04/PDS201/lclose@as.arizona.edu
    ├── lookyloo_success.txt
    └── warrenbfoster@arizona.edu
        └── 2022B
            └── 2022-12-03_04
                └── HD20121 -> /data/obs/2022B/2022-12-03_04/HD20121/warrenbfoster@arizona.edu

Datestamps are in a format that suggests the fact they span a day boundary: ``2022-04-11_12`` contains observations from the night of April 11 (Chilean local time) through the morning of April 12. (This matches the naming of our observing logs.)

