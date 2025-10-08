Creating a new MagAO-X app with Python
======================================

PurePyINDI2 provides an interface from Python to the Instrument-Neutral Distributed Interface, which MagAO-X uses as a network transport for latency-tolerant commanding. (Low-latency commands are relayed with MILK shared-memory images, or shmims.)

Creating the app
----------------

When we say "app" in MagAO-X, we mean a long-lived software process responsible for communicating with a device, monitoring the system, or exposing controls over INDI to other parts of the system.

In the ``MagAOX`` software repository, the apps live under ``apps/`` (surprise!). Choose an app name based on the function, assuming that some day there may be more than one of whatever it is you're adding. For example, if you add a flip mirror for acquisition, you might be tempted to call its app "acquisitionFlipper". However, a more general name might be "flipperCtrl". Then, later, when you add another flip mirror for an unrelated purpose, you don't need to rename the app folder.

The name that **does** match its function in the system is the "device name". More on that :ref:`later <plumbing-device>`.

Having decided on a name—for our purposes, let's call it ``yourNewApp``—you will need to take a few steps:

1. Copy a template app into place under the new name in ``apps/``. There is a folder ``apps/pythonIndiExample/`` with a minimal Python example.

2. Update the template.

    1. ``apps/yourNewApp/Makefile`` will have a line saying ``APP=pythonIndiExample``. Update that to ``APP=yourNewApp``
    2. The ``apps/yourNewApp/yourNewApp.py`` file contains a line that reads ``class PythonIndiExample(XDevice):``. Replace ``PythonIndiExample`` with ``YourNewApp``. (By Python convention, classes are capitalized, even though the app was called ``pythonIndiExample`` without the initial capital.)
    3. The ``apps/yourNewApp/pyproject.toml`` file needs a few changes. It will look something like this::

        [build-system]
        requires = ["hatchling"]
        build-backend = "hatchling.build"

        [project]
        name = "pythonIndiExample"
        description = "Python INDI device implementation example"
        version = "2023.12.21"

        authors = [
        {name = "Joseph D. Long", email = "me@joseph-long.com"},
        ]

        [project.scripts]
        pythonIndiExample = "pythonIndiExample:PythonIndiExample.console_app"

       Find-and-replace ``pythonIndiExample`` with ``yourNewApp``. Similarly, replace ``PythonIndiExample`` with ``YourNewApp``.
    4. Finally, you need to rename ``apps/yourNewApp/pythonIndiExample.py`` to ``apps/yourNewApp/yourNewApp.py``.

At this point, you should install your new app. Go into ``apps/yourNewApp/`` and run ``make install``. This registers a link from the ``yourNewApp`` command to the implementation in ``yourNewApp.py``.

You can try to run it with this command: ``/opt/MagAOX/bin/yourNewApp -h`` and get something like this::

    $ /opt/MagAOX/bin/yourNewApp -h
    /opt/MagAOX/bin/yourNewApp: Example Python INDI device for MagAO-X

    usage: yourNewApp [-c CONFIG_FILE] [-h] [-v] [--dump-config] [-n NAME] [-a] [vars ...]

    positional arguments:
        vars                  Config variables set with 'key.key.key=value' notation

    options:
        -c CONFIG_FILE, --config-file CONFIG_FILE
                                Path to config file, repeat to merge multiple, last one wins for repeated top-
                                level keys
        -h, --help            Print usage information
        -v, --verbose         Enable debug logging
        --dump-config         Dump final configuration state as TOML and exit
        -n NAME, --name NAME  Device name for INDI
        -a, --all-verbose     Set global log level to DEBUG

    configuration keys:
        sleep_interval_sec
            float
            Main loop logic will be run every `sleep_interval_sec` seconds
            (default: 1.0)
        configurable_doodad_1
            str
            Configurable doodad 1 (default: 'abc')

Defining configurable properties
--------------------------------

The ``configuration keys:`` section maps onto this block in the example::


    @xconf.config
    class ExampleConfig(BaseConfig):
        """Example Python INDI device for MagAO-X
        """
        configurable_doodad_1 : str = xconf.field(default="abc", help="Configurable doodad 1")

The docstring (in the ``"""``) provides the beginning of the help text and can be as long and detailed as you wish.

Clearly, ``configurable_doodad_1`` is from the last line in ``ExampleConfig``. Where is ``sleep_interval_sec``? That (and possibly more broadly-useful attributes over time) will come from the BaseConfig class from ``python/magaox/indi/device.py``.

Every configuration field is written as a name, type annotation, and field specification. For examples, see the `demo for xconf <https://github.com/xwcl/xconf/blob/main/demo.py>`_. You can get pretty far by copying the line above and swapping bits out. For example, a numeric config value with no default would be specified with::

    myvalue : float = xconf.field(help="spicy new config")

This configuration system lets you nest options, have collections of primitive types (like lists of integers, dictionaries mapping strings to floats, etc.) or collections of config class types. It's pretty powerful, just saying.

Currently in this example there are only config values with a defaults, so you can also dump out an example configuration file::

    $ /opt/MagAOX/bin/yourNewApp --dump-config
    sleep_interval_sec = 1.0
    configurable_doodad_1 = "abc"

These config files are in TOML format, similar to (but not exactly identical to) config files for C++ MagAO-X apps.

Tell the build system about your app
------------------------------------

MagAO-X has a big top-level ``Makefile`` with lists of apps to install for different roles. If your app belongs on AOC, find the block starting with ``apps_aoc = \`` and tack your app onto the end of the list. Make sure to add a ``\`` to the end of the penultimate line if there isn't one.

Now, ``make`` in the top level ``MagAOX`` folder will install your app too.

.. _plumbing-device:

Plumbing the device processs into MagAO-X
-----------------------------------------

MagAO-X starts processes based on the ``$MAGAOX_ROLE`` environment variable and the contents of ``/opt/MagAOX/config/proclist_${MAGAOX_ROLE}.txt``. Your new app is now present in ``/opt/MagAOX/bin`` (right?), so you can add it to the proclist. **This** is where the "device name" comes in. Every process has a device name (like ``flipacq``) and an app name (like ``flipperCtrl``). The process launcher then invokes the app with the device name, which tells it where to read its configuration.

Say you want to add a device called ``mydoodad``. If you do ``xctrl status mydoodad`` you will see xctrl doesn't know about it yet::

    $ xctrl status mydoodad
    Unknown process names: {'mydoodad'}

We can use ``--dump-config`` to jumpstart a new device config file::

    $ /opt/MagAOX/bin/yourNewApp --dump-config > /opt/MagAOX/config/mydoodad.conf

Now add a line to the end of ``proclist_${MAGAOX_ROLE}.txt``::

    mydoodad    yourNewApp

Now, if you do ``xctrl status mydoodad`` you will see xctrl knows about it.

There's one final step: configuring the indiserver. The indiserver is named ``is${MAGAOX_ROLE}`` (i.e. ``isAOC``, ``isICC``, etc.). Open ``/opt/MagAOX/config/is${MAGAOX_ROLE}.conf`` in your favorite editor. Find the local drivers section, which will look like::

    [local]
    drivers=thingamajig,chimichanga

Add your device to the comma-separated list, and save::

    [local]
    drivers=thingamajig,chimichanga,mydoodad

Starting your device
--------------------

Usually ``xctrl startup mydoodad`` will be enough. However, sometimes you will have to restart the INDI server process too.

The integration in ``python/magaox/indi/`` lets the Python app report its status with a PID file, same as the C++ ones. So, ``xctrl status mydoodad`` should behave as expected.

Hacking on your device
----------------------

The default install (i.e. from the template Makefile) is **editable**, meaning when you edit your app in the ``/opt/MagAOX/source/MagAOX/apps/`` folder, there is no further install step required for your changes to take effect. Just restart your app.

You can connect to the device running as ``xsup`` to view log outputs, Ctrl-C and restart, or what-have-you. First become xsup::

    $ xsupify

Then attach to the tmux session as you would for any other app::

    $ tmux at -t mydoodad

.. note::

    After hitting Ctrl-C to kill your app, give it a second to cleanly exit and deregister from the indiserver. That way you have a better chance of starting up next time without needing to restart the indiserver process as well.

.. warning::

    Remember to **add** and commit your new ``apps/yourNewApp`` folder and the ``mydoodad.conf`` file in ``/opt/MagAOX/config``, and to push your changes to GitHub.

Logging to console and disk
---------------------------

Python XDevices log to ``/opt/MagAOX/logs/`` with some differences from their C++ brethren. Logs for a particular device are grouped in a "folder", a filesystem construct frequently used to organize logically related files.

Considering again our example ``mydoodad`` device, its logs will be found in ``/opt/MagAOX/logs/mydoodad/``. After starting the app a few times, you will notice that the latest log file is the only one with a name ending in ``.log`` (e.g. ``mydoodad_2024-01-14T122245.log``) and the rest end in ``.gz`` (e.g. ``mydoodad_2024-01-14T122231.log.gz``). Every time the device starts, it compresses old logs with ``gzip`` to save a little space. On Linux and macOS there is a ``zcat`` command that decompresses and outputs the log file in one step.

**Examples:**

* ``zcat mydoodad_2024-01-14T122231.log.gz`` -- decompress and output ``mydoodad_2024-01-14T122231.log.gz`` to the terminal
* ``zcat mydoodad_2024-01-14T122231.log.gz | less`` -- decompress and review ``mydoodad_2024-01-14T122231.log.gz`` with a scrolling pager
* ``tail -f $(ls /opt/MagAOX/logs/mydoodad/ | tail -n 1)`` -- when the device is running, watch the file log as it is written. (Note that restarting the device will open a new log file, so you'll have to Ctrl-C and run this command again.)

**So, how do you add your own output to these logs?** You use the Python :py:mod:`logging` module. The XDevice has a logger instance available in your ``loop()`` method as ``self.log``, so ``self.log.debug("Wow!")`` will result in a line like ``2024-01-14T19:36:16.734742000 DEBUG Wow! (mydoodad:loop:123)`` in your log file.

.. note::

    Using ``self.log.debug(...)`` is a shorter way of saying ``logging.getLogger(self.name).debug(...)``.

The allowed levels are ``debug``, ``info``, ``warning`` (also called ``warn``), ``error``, and ``critical`` (also called ``fatal``). If you instead wrote ``self.log.warning("Wow!")`` you would see ``2024-01-14T19:36:16.734742000 WARNING Wow! (mydoodad:loop:123)`` in your log file. In fact, you will also see it on the console in the tmux session for ``mydoodad``. (Become xsup with ``xsupify`` and then ``tmux at -t mydoodad``.) Logs with the level ``info`` and above are written to the console.

**What if you want to see debug logs on the console?** There are a few command-line options available when starting an XDevice::

        options:
    -c CONFIG_FILE, --config-file CONFIG_FILE
                            Path to config file, repeat to merge multiple, last one wins for repeated top-
                            level keys
    -h, --help            Print usage information
    -v, --verbose         Enable debug logging
    --dump-config         Dump final configuration state as TOML and exit
    -n NAME, --name NAME  Device name for INDI
    -a, --all-verbose     Set global log level to DEBUG

The ``-v`` option will enable logging your debug messages to the console. (They are always logged to the file.) 

The ``-a`` option will enable debug logging to console and file for your app as well as any other libraries that use the standard Python logging framework. This can be useful to see exactly what PurePyINDI2 is doing, but can be overwhelming for code that uses e.g. matplotlib, or numba.
