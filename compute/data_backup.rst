Using the file inventory database to synchronize backups
--------------------------------------------------------

The lifecycle of a MagAO-X data file:

1. Empty file is created on one of the MagAO-X instrument computers
2. Data are written to this file (either all at once, or slowly over many hours)
3. The file is closed by the creator process and never modified again

After the file is "finished", it can (and should) be replicated to a backup volume or offsite. Unfortunately, with e.g. ``bintel`` 
files, we can't trivially tell whether a file has been "finished". So, we use the ``mtime`` and ``size`` attributes of files.

The lifecycle of a MagAO-X file **replica**:

1. The need for a new replica is identified
    a. by the creation of a new replica in the replica set (which will initially have no files)
    b. by the creation of a new file record in the inventory (which will initially have no replicas, only the original copy)
    c. by a discrepancy between the ``mtime`` or ``size`` for a file inventory record and the corresponding replica record
2. The file is copied to the replica
3. The table of file replicas is updated to reflect the ``mtime`` and ``size`` of the source file

There is also a "reverse" process to populate the origins table given e.g. a backup volume. As long as the backup is organized 
into folders by origin host, it is possible to use file creation time metadata and file names to work backwards to the origin 
host and path. Since the origin record must exist before the replica record is created, enrolling files from a backup follows 
this process:

1. For every top-level per-host directory (e.g. ``exao1``) under the backup prefix (e.g. ``/backup/prefix``), set the notional 
host to that directory's name.
2. Within the directory, walk through all paths and create file origin records. Using the absolute path of the backup file, 
replace the backup prefix and host (e.g. ``/backup/prefix/exao1``) with ``/`` to get the origin path.
3. Create the replica record and point it to the origin record.

Adding / refreshing a replica
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``xtelemdb add_replica prefix=/mnt/backup``

``xtelemdb add_replica host=popeye prefix=ceph/magao-x/ import_origins=true``

``xtelemdb replica_list``

``xtelemdb sync continuous=true``

::

    [replicas."/mnt/backup"]
    local = true

    [replicas."ssh://popeye/ceph/magao-x/"]
