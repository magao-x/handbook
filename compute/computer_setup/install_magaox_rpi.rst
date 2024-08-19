Installing MagAO-X on a Raspberry Pi
====================================


Configuring the Raspberry Pi
----------------------------

Prepare the MicroSD card
~~~~~~~~~~~~~~~~~~~~~~~~

The first step is to download the Raspberry Pi Imager from the `Raspberry Pi Website <https://www.raspberrypi.com/software/>`__. The MicroSD card can then 
be inserted into your computer. Now open the Raspberry Imager and select the Raspberry Pi Device you have, the operating system (OS) (Ubuntu server 24.04 LTS), 
and the storage (your MicroSD card). To access the OS customization, use ``ctrl+shift+x``. This is where you can set hostname, username password, 
etc. It is crucial that you 'Enable SSH' in the OS customization. Now click 'next' and 'write' to install the OS on the Micro SD card. 

In the MicroSD, update ``cmdline.txt`` by adding the following string to the end: ``ip=192.168.0.5::192.168.0.1:255.255.255.0:rpi:eth0:off``. Note that 
this ip can be changed to match your desired static ip settings.


Boot the Raspberry Pi
~~~~~~~~~~~~~~~~~~~~~

Insert the MicroSD card back into the Raspberry Pi. If you are using your PC, you can use an ethernet cable to connect the Raspberry Pi to your PC 
(you may need an Ethernet to USB C adapter). You can now power up the Raspberry Pi (This may take a couple minutes to boot). While this is booting, 
go to 'Settings', then 'Ethernet'. In here, edit the IP assignment to Manual, the IPv4 address to something similar to 192.168.0.6, and the IPv4 mask 
to something similar to 255.255.255.0. 

After this is complete, go to your terminal and ping the Raspberry Pi's IPv4 address ``ping 192.168.0.5`` to ensure 
it is receiving you. Then SSH into the Raspberry Pi ``ssh 192.168.0.5``.    

Connect the Raspberry Pi to WiFi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The first thing to do is to edit the netplan file ``/etc/netplan/50-cloud-init.yaml`` to:

::

   network:
       version: 2
       ethernets:
           eth0:
               addresses:
               - 192.168.0.5/24
               match:
                   macaddress: dc:a6:32:ef:87:8a
               routes:
               -   to: default
                   via: 192.168.0.1
               set-name: eth0
       wifis:
           wlan0:
               optional: true
               access-points:
                   "summit-data": {}
               dhcp4: true

The part that needs to be added is ``wifis:`` and below, where ``"summit-data"`` is the name of the WiFi. If the WiFi has a password, delete the ``{}`` and 
add ``password: "ENTER_PASSWORD_HERE"``  indented under ``"summit-data"``. Back in the terminal, run the following commands:

::

   $ sudo netplan --debug try
   $ sudo netplan --debug generate
   $ sudo netplan --debug apply

You may then check to see if you are connected to the WiFi using the ``ip ad`` command. The IP address of the WiFi can be found here. This can be used to 
``ssh`` back into the Raspberry Pi. 

Connect automatically to WiFi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a new file called 'interfaces' with ``sudo nano /etc/network/interfaces`` and add the text ``auto wlan0``. Then ``sudo reboot`` and wait a 
couple minutes to ``ssh`` back in using the WiFi's IP address.


Install MagAO-X
---------------

These steps are also outlined :doc:`here <\computer_setup>`, however there are a few that are unnecessary. Provided below is a 
simplified version. 

1. Clone `MagAO-X <https://github.com/magao-x/MagAOX>`__ into your home directory.

::

   $ cd
   $ git clone https://github.com/magao-x/MagAOX.git

2. Switch to the ``setup`` subdirectory in the MagAO-X directory you cloned (``~/MagAOX/setup``) to perform pre-provisioning steps.

::

   $ cd ~/MagAOX/setup
   $ ./pre_provision.sh

This will give you a prompt where you will want to select 'workstation'.

3. Run ``provision.sh``

::

   $ cd ~/MagAOX/setup
   $ bash provision.sh
