Zaber Stages
=======================

Maintenance of the Zaber stages in MagAO-X

   .. image:: figures/zaber_connections.svg

   *The main zaber stage daisy chain*

Configuring
--------------

1. Identify the tty device of the zaber USB adapter.  You can find this in the log for the relevant zaberLowLevel process or using dmesg.  For dmesg you may need to unplug/plugin the adapter.

2. Shutdown the assocated zaberLowLevel process.

3. Open a connection with screen to the tty:

    ::

      [exao3 ~]$ sudo screen /dev/ttyUSBX 115200

    Note that screen does not echo, so when typing you will not see any responses.

4.  To enumerate the devices in the chain

    ::

        / get system.serial

5.  To renumber the devices in the chain

    ::

        /renumber

5.  To get the max position (in counts) of the devices

    ::

        / get limit.max

6. To set the max position of a device:

    ::

       /4 set limit.max 2257638

    This sets the limit of device 4 to 2257638

7. To exit screen, type `ctrl-a` and press the `\\` key.  Then say yes.
