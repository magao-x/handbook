Accessing data for quick-look purposes
======================================

The Adaptive optics Operator Computer, aka AOC or exao1, has been set up with guest observer quick-look functionality using an account named ``guestobs``.

Preliminaries
-------------

First, you will need an SSH key pair. Generating one is outside the scope of this document, but GitHub has a `good guide <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_. (You can choose Mac, Windows, or Linux, and you need only follow the steps under the first heading: "Generating a new SSH key".)

The key consists of a private half, probably named something like ``id_ed25519``, and a public half, named something like ``id_ed25519.pub``. Send the contents of the ``.pub`` file to the operator, keeping the private part private.

Connecting
----------

When located at Las Campanas, the operator computer can be reached from the ``LCO-STAFF`` network at the address exao1.lco.cl.

Log in using the ``guestobs`` account to verify everything works and that you have access (accepting the key fingerprint if needed)::

    % ssh guestobs@exao1.lco.cl
    The authenticity of host 'exao1.lco.cl (200.28.147.221)' can't be established.
    ED25519 key fingerprint is SHA256:Azbcyun8qHxuhl0GE9AyG1cPajNPnfKlTQCwTfCMFT0.
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
    Warning: Permanently added 'exao1.lco.cl' (ED25519) to the list of known h
    Last login: Thu Apr  7 15:28:49 2022 from 10.8.22.67
    [guestobs@exao1] $

Now, log out::

    [guestobs@exao1] $ logout
    $

Downloading quick-look images
-----------------------------

You can use ``rsync`` to get your images out for quick looking. The path is constructed as follows: ``data/quicklook/<email>/<obs_name>/``. Here's an example::

    $ rsync -av guestobs@exao1.lco.cl:data/quicklook/lclose@as.arizona.edu/testQuicklook/ ./testQuicklook/
    receiving file list ... done
    created directory ./testQuicklook
    ./
    camsci1_20220407193404489182035.fits
    camsci1_20220407193404990275799.fits
    camsci1_20220407193405491005881.fits
    camsci1_20220407193405991612707.fits
    camsci1_20220407193406493350035.fits
    [... many lines omitted ...]
    camsci2_20220405011522327712067.fits
    meta_data.txt

    sent 5016 bytes  received 221150763 bytes  23279555.68 bytes/sec
    total size is 221081847  speedup is 1.00

Re-running this command later in the observation will only sync changed files.