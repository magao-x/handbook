Accessing data as a guest observer
==================================

The Adaptive optics Operator Computer, aka AOC or ``exao1``, has been set up with guest observer data access functionality using an account named ``guestobs``.

Note that ``exao1`` is part of the instrument, and ships back and forth to Chile for observing runs. That means two things:

1. It will not be available for several weeks while it is in transit, and
2. It has a different IP and host-name when it's at University of Arizona than when it's at Las Campanas Observatory.

Preliminaries
-------------

First, you will need an SSH key pair. Generating one is outside the scope of this document, but GitHub has a `good guide <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_. (You can choose Mac, Windows, or Linux, and you need only follow the steps under the first heading: "Generating a new SSH key".)

The key consists of a private half, probably named something like ``id_ed25519``, and a public half, named something like ``id_ed25519.pub``. Send the contents of the ``.pub`` file to the operator, keeping the private part private.

(Note: ``id_rsa`` and ``id_dsa`` keys are not usable with MagAO-X. You may use ECDSA or ED25519 keys.)

Connecting
----------

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

You will need a user account on exao0, a computer in our lab at The University of Arizona, which has firewall rules permitting access to the Las Campanas Observatory machines.

You can SSH via exao0 if your SSH client supports the ``-J`` option (which most do)::

    yourComputer$ ssh -J 'ssh myusername@exao0.as.arizona.edu' guestobs@exao1.lco.cl

Browsing the data
-----------------

The quicklook data are rooted in ``/data/users/guestobs/quicklook/``. So, for example, ``/data/users/guestobs/quicklook/XXXXXX/`` will contain::

    [guestobs@exao1] $ ls /data/users/guestobs/quicklook/XXXXXX/
    YYYYY
    ZZZZZ

and an individual group will contain a folder per science camera::

    [guestobs@exao1] $ ls /data/users/guestobs/quicklook/XXXXXX/YYYYY/
    camsci1
    camsci2

You can use your favorite tool to browse, but we recommend ``rsync`` to get quick-look images. (See below.) You may log out of exao1::

    [guestobs@exao1] $ logout
    $

Downloading quick-look images
-----------------------------

You can use ``rsync`` to get your images out for quick looking. The path is constructed as follows: ``/data/users/guestobs/quicklook/<email>/<obs_name>/``.

When MagAO-X is in the lab
^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's an example::

    $ rsync -a --progress \
        guestobs@exao1.as.arizona.edu:/data/users/guestobs/quicklook/jrmales@arizona.edu/testQuicklook/ \
        ./testQuicklook/

    receiving file list ... done
    created directory ./testQuicklook
    camsci1/camsci1_20220417230302255087061.fits
        8640 100%   31.25kB/s    0:00:00 (xfer#3429, to-check=1436/4867)
    camsci1/camsci1_20220417230302258540922.fits
        8640 100%   31.13kB/s    0:00:00 (xfer#3430, to-check=1435/4867)
    [... many lines omitted ...]

    sent 5016 bytes  received 221150763 bytes  23279555.68 bytes/sec
    total size is 221081847  speedup is 1.00

Re-running this command will only sync changed files.

When MagAO-X is at Las Campanas, and so are you
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's an example::

    $ rsync -a --progress \
        guestobs@exao1.lco.cl:/data/users/guestobs/quicklook/jrmales@arizona.edu/testQuicklook/ \
        ./testQuicklook/

    receiving file list ... done
    created directory ./testQuicklook
    camsci1/camsci1_20220417230302255087061.fits
        8640 100%   31.25kB/s    0:00:00 (xfer#3429, to-check=1436/4867)
    camsci1/camsci1_20220417230302258540922.fits
        8640 100%   31.13kB/s    0:00:00 (xfer#3430, to-check=1435/4867)
    [... many lines omitted ...]

    sent 5016 bytes  received 221150763 bytes  23279555.68 bytes/sec
    total size is 221081847  speedup is 1.00

Re-running this command will only sync changed files.

When MagAO-X is at Las Campanas, and you are off-site
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here's an example::

    $ rsync -a --progress -e 'ssh -J jlong@exao0.as.arizona.edu' \
        guestobs@exao1.lco.cl:/data/users/guestobs/quicklook/jrmales@arizona.edu/testQuicklook/ \
        ./testQuicklook/

    receiving file list ... done
    created directory ./testQuicklook
    camsci1/camsci1_20220417230302255087061.fits
        8640 100%   31.25kB/s    0:00:00 (xfer#3429, to-check=1436/4867)
    camsci1/camsci1_20220417230302258540922.fits
        8640 100%   31.13kB/s    0:00:00 (xfer#3430, to-check=1435/4867)
    [... many lines omitted ...]

    sent 5016 bytes  received 221150763 bytes  23279555.68 bytes/sec
    total size is 221081847  speedup is 1.00

Re-running this command will only sync changed files.
