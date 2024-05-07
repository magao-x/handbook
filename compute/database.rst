Telemetry and File Inventory Database
=====================================

The MagAO-X telemetry database is a PostgreSQL database running on AOC that collects device telemetry from the ``.bintel`` and ``.ndjson.gz`` files produced by instrument devices across the computers in MagAO-X. It also tracks the inventory of files for replication to backup volumes and remote sites.

The database is designed to be a central repository for all telemetry data produced by the instrument, and to provide a simple interface for querying and visualizing that data.

First, you will need to set up the database as described in :ref:`setup_telemetry_database`.

.. _maintenance:

Maintenance
-----------

Backfilling existing data
~~~~~~~~~~~~~~~~~~~~~~~~~

There are a couple of times you may want to backfill the database. If you're starting from scratch with an empty database, or if the ``dbIngest`` processes are interrupted and need to catch up, you can perform the backfill with:

1. ``xtelemdb inventory``

2. ``xtelemdb ingest``

On hosts other than exao1/AOC, supply the hostname: e.g. ``xtelemdb inventory database.host=aoc``.

Repeat these steps on every instrument computer that needs to be caught up.

Reinitialize the database
~~~~~~~~~~~~~~~~~~~~~~~~~

If the database gets messed up, it's no big deal. The contents should be entirely reproducible given the same set of files on the three instrument computers. (How to fill in data that's already been shunted off to backup drives... is another matter. TODO)

Level 1: Remove data from tables, keeping tables/indices/views the same
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``TRUNCATE TABLE`` command lets you keep the table definitions but reset them to contain no rows.

Using ``sudo -u postgres psql xtelem`` to connect to the ``xtelem`` database as superuser, you can do::

    TRUNCATE TABLE telem CASCADE;
    TRUNCATE TABLE file_origins CASCADE;
    COMMIT;

Adjust as needed for other tables. (Use ``\dt`` at the ``xtelem=#`` prompt to list.) Continue with the :ref:`backfill procedure <maintenance>`.

Level 2: Remove tables and views
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using ``sudo -u postgres psql xtelem`` to connect to the ``xtelem`` database as superuser, you can do::

    DROP TABLE telem CASCADE;
    DROP TABLE file_origins CASCADE;
    COMMIT;

Use the ``xtelemdb setup`` command to re-create the tables and views, then continue with the :ref:`backfill procedure <maintenance>`.

Level 3: Remove database and roles (users)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using ``sudo -u postgres psql xtelem`` to connect to the ``xtelem`` database as superuser, you can do::

    DROP DATABASE xtelem;
    DROP ROLE xsup;
    DROP ROLE xtelem;

Next, use ``setup/steps/configure_postgresql.sh`` in the MagAOX repository to create the database. Then, use the ``xtelemdb setup`` command to re-create the tables and views, and continue with the :ref:`backfill procedure <maintenance>`.


.. _setup_telemetry_database:

Setup
-----

This is for setting up on the instrument (most likely AOC / exao1). For use on a non-instrument computer or a cluster, see :ref:`setup_telemetry_database_nosudo`.

Prerequisites
~~~~~~~~~~~~~

PostgreSQL version 14 or newer should be installed. The setup shell scripts include a `configure_postgresql.sh <https://github.com/magao-x/MagAOX/blob/dev/setup/steps/configure_postgresql.sh>`_ script to run on AOC which does several things. It:

* adds a line to the ``/etc/postgresql/14/main/pg_hba.conf`` file telling it to search ``/etc/postgresql/14/main/pg_hba.conf.d/*.conf`` for additional configuration,
* creates that directory and a file within it that enables network access to the PostgreSQL server from the instrument LAN,
* enables the postgresql SystemD service, starts it (if needed), and reloads the configuration files
* creates a `tablespace <https://www.postgresql.org/docs/current/manage-ag-tablespaces.html>`_ to locate the telemetry database on the ``/data`` partition
* creates the database named ``xtelem`` with the appropriate tablespace
* using `setup_users.sql <https://github.com/magao-x/MagAOX/blob/dev/setup/sql/setup_users.sql>`_, creates the roles ``xsup`` (read-only), and ``xtelem`` (read-write) with access to the ``xtelem`` database.

There is also another script called `configure_postgresql_pass.sh <https://github.com/magao-x/MagAOX/blob/dev/setup/steps/configure_postgresql_pass.sh>`_ that creates a new secret in ``/opt/MagAOX/secrets``. (This is a separate script as it will be run on all the instrument computers, not just the one with the database server.)

These scripts can be run on their own from ``/opt/MagAOX/source/MagAOX/setup`` if they were not run by ``provision.sh``.

After running them, ensure:

1. PostgreSQL is running on localhost:5432 (``systemctl status postgresql`` on AOC)
2. There is a ```data_array`` tablespace to put the database in::

    $ sudo -u postgres psql
    psql (14.10 (Ubuntu 14.10-0ubuntu0.22.04.1))
    Type "help" for help.
    postgres=# \db+
                                        List of tablespaces
        Name    |  Owner   |    Location    | Access privileges | Options |  Size  | Description
    ------------+----------+----------------+-------------------+---------+--------+-------------
    data_array | postgres | /data/postgres |                   |         | 824 MB |
    pg_default | postgres |                |                   |         | 33 MB  |
    pg_global  | postgres |                |                   |         | 576 kB |
    (3 rows)

2. The database 'xtelem' exists::

    $ sudo -u postgres psql xtelem
    psql (14.10 (Ubuntu 14.10-0ubuntu0.22.04.1))
    Type "help" for help.

    xtelem=# exit;

3. The appropriate user accounts have been created and can connect::

    $ sudo -u xsup psql xtelem
    psql (14.10 (Ubuntu 14.10-0ubuntu0.22.04.1))
    Type "help" for help.

    xtelem=> exit;

4. Login over TCP is enabled, and the firewall has been configured to allow this

Setup from CLI
~~~~~~~~~~~~~~

Code to interact with the telemetry database is centralized in ``magaox`` Python package, which is maintained in the main magao-x/MagAOX repository. On AOC, the package is installed in the default conda environment. To update the installed version, run ``make python_install`` in ``/opt/MagAOX/source/MagAOX`` with a developer account.

After installation, there is an ``xtelemdb`` command available::

    $ xtelemdb
    usage: xtelemdb {setup,inventory,backfill} ...

    subcommands:
    valid subcommands

    {setup,inventory,backfill}

We want to set up the database, so run ``xtelemdb setup``. Note that you will have to do this step as ``xsup`` or else get the message ``ERROR Tried to get password from /opt/MagAOX/secrets/xtelemdb_password`` and a ``PermissionError``. That could look like this::

    $ xsupify
    xsup@exao1:~$ xtelemdb setup
    2024-04-22 19:06:43 exao1 magaox.db.cli.commands.setup[657990] INFO Success!
    xsup@exao1:~$

Check that the tables you expect were created::

    xsup@exao1:~$ psql xtelem
    psql (14.10 (Ubuntu 14.10-0ubuntu0.22.04.1))
    Type "help" for help.

    xtelem=> \dt
                List of relations
    Schema |       Name        | Type  | Owner
    --------+-------------------+-------+--------
    public | file_ingest_times | table | xtelem
    public | file_origins      | table | xtelem
    public | file_replicas     | table | xtelem
    public | telem             | table | xtelem
    (4 rows)

    xtelem=> exit;

Start device processes
~~~~~~~~~~~~~~~~~~~~~~

The proclist for each instrument computer will launch a ``dbIngest`` device process at ``xctrl startup``. (These are named ``dbIngestAOC``, ``dbIngestRTC``, and ``dbIngestICC``.) If they were started before the database became available, they will probably have crashed. Use ``xctrl restart dbIngestAOC`` to start the device on AOC, and modify accordingly for the other two machines.


.. _setup_telemetry_database_nosudo:

Setup a personal copy of the database
-------------------------------------

PostgreSQL is a full database system which generally requires administrator access to install. However, in cluster computing settings where you don't have ``sudo``, you may still install a database using ``conda`` / ``mamba``.

Installing a personal PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

0. Install ``mamba`` and ensure it's available in your terminal. If you prefer to use the ``conda`` command, replace ``mamba`` with ``conda`` in the instructions below and it should just work. (Detailed installation instructions are beyond the scope of this document, but the "Install" section of the `miniforge <https://github.com/conda-forge/miniforge?tab=readme-ov-file#install>`_ readme should help you.)
1. Create an isolated environment for database installation: ``mamba create -n db python=3.10 postgresql`` (as of this writing, Python 3.10 was current on exao1) and answer ``Y`` when prompted
2. Activate the environment: ``mamba activate db``
3. Decide where to store the database files. In this example, I'm using ``/home/jlong/postgres``. Note that you should not create this folder yourself; the next step does it for you.
4. Initialize the database with ``initdb /home/jlong/postgres`` (substituting your own data directory)
5. Start the database server and give it a log filename to write to (I used ``/home/jlong/postgres.log``): ``pg_ctl -D /home/jlong/postgres/ -l /home/jlong/postgres.log start``
6. Now, if you check your running processes, you will see several PostgreSQL processes::

    $ ps aux | grep postgres
    jlong     106393  0.0  0.0 437524 26224 ?        Ss   11:43   0:00 /mnt/home/jlong/miniforge3/envs/db/bin/postgres -D /home/jlong/postgres
    jlong     106394  0.0  0.0 437524  8208 ?        Ss   11:43   0:00 postgres: checkpointer
    jlong     106395  0.0  0.0 437524  5264 ?        Ss   11:43   0:00 postgres: background writer
    jlong     106397  0.0  0.0 437524  9368 ?        Ss   11:43   0:00 postgres: walwriter
    jlong     106398  0.0  0.0 438548  8260 ?        Ss   11:43   0:00 postgres: autovacuum launcher
    jlong     106399  0.0  0.0 438548  6428 ?        Ss   11:43   0:00 postgres: logical replication launcher
    jlong     107124  0.0  0.0 221964  1120 pts/1    S+   12:00   0:00 grep --color=auto postgres

7. Connect to the ``postgres`` database as yourself to verify it worked (use Ctrl-D to exit)::

    $ psql postgres
    psql (16.2)
    Type "help" for help.

    postgres=#

8. Run ``CREATE DATABASE xtelem;`` to create the database.

Setting up the MagAO-X telemetry database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For a single-user instance we will not bother setting up roles other than the one for your own user account. (See https://github.com/magao-x/MagAOX/tree/dev/setup/sql for what the provisioning process would do.)

0. Clone the MagAO-X system software somewhere convenient::

    $ git clone https://github.com/magao-x/MagAOX.git

1. Install the MagAO-X Python library (n.b. you should still be in the ``db`` conda environment we created)::

    $ cd MagAOX/python
    $ pip install -e .
    $ xtelemdb
    usage: xtelemdb {backfill,inventory,setup} ...

    subcommands:
      valid subcommands

      {backfill,inventory,setup}

2. Create a configuration file to simplify later steps::

    $ cat xtelemdb.conf.toml
    data_dirs = [
        "/mnt/ceph/users/jlong/magao-x/archive/aoc/logs",
        "/mnt/ceph/users/jlong/magao-x/archive/aoc/rawimages",
        "/mnt/ceph/users/jlong/magao-x/archive/aoc/telem",
        "/mnt/ceph/users/jlong/magao-x/archive/rtc/logs",
        "/mnt/ceph/users/jlong/magao-x/archive/rtc/rawimages",
        "/mnt/ceph/users/jlong/magao-x/archive/rtc/telem",
        "/mnt/ceph/users/jlong/magao-x/archive/icc/logs",
        "/mnt/ceph/users/jlong/magao-x/archive/icc/rawimages",
        "/mnt/ceph/users/jlong/magao-x/archive/icc/telem",
    ]
    [database]
    user = "jlong"

3. Perform setup::

    $ xtelemdb setup -c xtelemdb.conf.toml

4. Perform inventory::

    $ xtelemdb inventory -c xtelemdb.conf.toml

5. Perform backfill::

    $ xtelemdb backfill -c xtelemdb.conf.toml

Note that in this configuration there are no MagAO-X apps like ``dbIngestAOC`` keeping the database up-to-date, so you will have to run ``inventory`` and ``backfill`` again whenever you add new data.
