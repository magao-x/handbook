Networking
==========

This document uses the hostnames of the machines interchangeably with
their roles. For reference:

-  ``exao1`` — AOC
-  ``exao2`` — RTC
-  ``exao3`` — ICC

Topology
--------

**University of Arizona**

.. figure:: ua_network.drawio.svg
   :alt: Schematic representation of the connections between our lab computers when at home at University of Arizona

   Schematic representation of the connections between our lab computers when at home at University of Arizona


**Las Campanas Observatory**

.. figure:: lco_network.drawio.svg
   :alt: Schematic representation of the connections between our computers when at the telescope at Las Campanas Observatory

   Schematic representation of the connections between our computers when at the telescope at Las Campanas Observatory


Ubuntu and NetworkManager and ufw and firewalld
-----------------------------------------------

Ubuntu does not use NetworkManager, so you have to change to NetworkManager. This is done in `switch_ubuntu_networkmanager.sh <https://github.com/magao-x/MagAOX/blob/dev/setup/switch_ubuntu_networkmanager.sh>`_ when setting up the system, and again as updates break it.

The firewall of choice in Ubuntu is UFW, but firewalld integrates with NetworkManager so we can tag connections as trusted rather than interfaces. Install::

   sudo apt install firewalld
   sudo systemctl enable firewalld
   sudo systemctl start firewalld
   ufw disable

Firewall zones
--------------

Certain interfaces are instrument internal: rack LAN, cameras, and
direct NIC-to-NIC links. To ensure traffic is unrestricted on them,
configure as follows:

-  ``exao1``, ``exao2``, and ``exao3``

   -  ``sudo nmcli con modify instrument connection.zone trusted``

-  ``exao2`` only

   -  ``sudo nmcli con modify rtc-to-icc connection.zone trusted``

-  ``exao3`` only

   -  ``sudo nmcli con modify icc-to-rtc connection.zone trusted``
   -  ``sudo nmcli con modify camsci1 connection.zone trusted``
   -  ``sudo nmcli con modify camsci2 connection.zone trusted``

Network Connections
-------------------

exao1
~~~~~

+------------------+-------------------+------------------+----------------+--------------------------+----------------------+-----------------+
| connection name  | device            | IPv4 address     | subnet mask    | default route / gateway  | DNS servers          | search domains  |
+==================+==================+==================+================+==========================+======================+==================+
| instrument-10g   | 98:B7:85:01:AD:66 | 192.168.0.10     | 255.255.255.0  | 192.168.0.1              | n/a                  | n/a             |
+------------------+-------------------+------------------+----------------+--------------------------+----------------------+-----------------+
| www-ua           | 2C:FD:A1:C6:1F:09 |                                                                                            (DHCP)     |
+------------------+-------------------+------------------+----------------+--------------------------+----------------------+-----------------+
| lco-telescope    | 2C:FD:A1:C6:1F:09 | 200.28.147.221   | 255.255.255.0  | 200.28.147.1             | 10.8.8.11 10.8.8.12  | lco.cl          |
+------------------+-------------------+------------------+----------------+--------------------------+----------------------+-----------------+


**For reference:** At last setup, the automatic DHCP-assigned
configuration for ``www-ua`` was:

-  IP Address: ``128.196.208.35``
-  Subnet Mask: ``255.255.252.0``
-  Default Route: ``128.196.208.1``
-  DNS: ``128.196.208.2 128.196.211.3 128.196.11.233 128.196.11.234``

exao2
~~~~~

+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| connection name  | device           | IPv4 address     | subnet mask    | default route / gateway  | DNS servers                                | search domains  |
+==================+==================+==================+================+==========================+============================================+=================+
| instrument-10g   | enx98b78501aebd  | 192.168.0.11     | 255.255.255.0  | 192.168.0.1              | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| www-ua           | enx50ebf6b783bb  | 10.130.133.207   | 255.255.254.0  | 10.130.132.1             | 128.196.208.2 128.196.209.2 128.196.11.233 | as.arizona.edu  |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| lco-telescope    | enx50ebf6b783bb  | 200.28.147.222   | 255.255.255.0  | 200.28.147.1             | 10.8.8.11 10.8.8.12                        | lco.cl          |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| rtc_icc          | enx98b78501aebc  | 192.168.2.2      | 255.255.255.0  | n/a                      | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+

``instrument-10g`` is a routerless network within the rack (and to AOC) using a switch.
``rtc-to-icc`` is a direct NIC-to-NIC link between RTC and ICC.

exao3
~~~~~

+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| connection name  | device           | IPv4 address     | subnet mask    | default route / gateway  | DNS servers                                | search domains  |
+==================+==================+==================+================+==========================+============================================+=================+
| instrument       | enx2cfda1c6db1a  | 192.168.0.192    | 255.255.255.0  | 192.168.0.1              | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| instrument-10g   | enx98b78501ae65  | 192.168.0.12     | 255.255.255.0  | 192.168.0.1              | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| www-ua           | enx2cfda1c6db1b  | 10.130.133.208   | 255.255.254.0  | 10.130.132.1             | 128.196.208.2 128.196.209.2 128.196.11.233 | as.arizona.edu  |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| lco-telescope    | enx2cfda1c6db1b  | 200.28.147.223   | 255.255.255.0  | 200.28.147.1             | 10.8.8.11 10.8.8.12                        | lco.cl          |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| rtc_icc          | enx98b78501ae64  | 192.168.2.3      | 255.255.255.0  | n/a                      | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| camsci1          | enx503eaa0ceeff  | 192.168.101.2    | 255.255.255.0  | 192.168.101.1            | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| camsci2          | enx503eaa0cf4cd  | 192.168.102.2    | 255.255.255.0  | 192.168.102.1            | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+

``instrument`` is a routerless network within the rack using a switch.
``rtc_icc`` is a direct NIC-to-NIC link between RTC and ICC. The
``camsci1`` and ``camsci2`` networks are just direct connections from
the Princeton Instruments cameras to their NICs.

MagAOX-RPI's 
~~~~~~~~~~~~

+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| connection name  | device           | IPv4 address     | subnet mask    | default route / gateway  | DNS servers                                | search domains  |
+==================+==================+==================+================+==========================+============================================+=================+
| MagAOX-RPI       |                  | 10.8.10.190      | 255.255.255.0  | 10.8.10.1                | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+
| MagAOX-RPI2      |                  | 10.8.22.97       | 255.255.255.0  | 10.8.10.1                | n/a                                        | n/a             |
+------------------+------------------+------------------+----------------+--------------------------+--------------------------------------------+-----------------+

Hostnames
---------

Each instrument computer has a ``/etc/hosts`` file installed with names
and aliases for devices internal to MagAO-X. Changes to this file are
made in
`setup/steps/configure_etc_hosts.sh <https://github.com/magao-x/MagAOX/blob/master/setup/steps/configure_etc_hosts.sh>`__,
and applied with ``provision.sh``.

University of Arizona
~~~~~~~~~~~~~~~~~~~~~

While at the University of Arizona, the FQDN is
``<hostname>.as.arizona.edu``. Only ``exao1`` has a publicly-routable IP
address, while ``exao2`` and ``exao3`` live behind the NAT.

Las Campanas Observatory
~~~~~~~~~~~~~~~~~~~~~~~~

While at LCO, the FQDN is ``<hostname>.lco.cl``. All three instruments
are accessible from the LCO-VISITORS wireless network and other usual
places, but not from the outside internet.

Time synchronization
--------------------

Time synchronization depends on
`chrony <https://chrony.tuxfamily.org/index.html>`__, configured at
``/etc/chrony/chrony.conf`` (Debian/Ubuntu) or ``/etc/chrony.conf``
(Red-Hat-like). Those files are updated by ``provision.sh`` according to the
script in
`setup/steps/configure_chrony.sh <https://github.com/magao-x/MagAOX/blob/master/setup/steps/configure_chrony.sh>`__.

The AOC and ICC take their time from RTC, which is configured to allow
NTP queries from these addresses:

* the ``192.168.0.0/24`` subnet
* the ``200.28.147.0/24`` subnet (i.e. LCO telescopes LAN)
* the ``10.8.10.0/24`` subnet (i.e. LCO-SCIENCE WiFi)
* ``192.168.2.3`` (the IP of ICC as seen from RTC over the point-to-point direct link)

AOC, in turn gets its time from a combination of

-  ``lbtntp.as.arizona.edu`` - LBT / Steward Observatory NTP server
   (when in the lab)
-  ``ntp1.lco.cl`` - Las Campanas NTP server (when at the telescope)
-  ``ntp2.lco.cl`` - Backup Las Campanas NTP server (when at the
   telescope)
-  ``0.rocky.pool.ntp.org`` — Alias for a pool of hosts that contribute
   to pool.ntp.org (whenever reachable)

Troubleshooting
~~~~~~~~~~~~~~~

The RTC (``exao2``) is the time source for the rest of the instrument. It, in turn, gets its time over the network. Inspect its time sources and offsets with ``chronyc sources``::

   [jlong@exao2 ~]$ chronyc tracking
   Reference ID    : C81C933B (vicuna.lco.cl)
   Stratum         : 2
   Ref time (UTC)  : Wed Apr 09 01:38:13 2025
   System time     : 0.000009261 seconds slow of NTP time
   Last offset     : -0.000014544 seconds
   RMS offset      : 0.000013495 seconds
   Frequency       : 11.212 ppm slow
   Residual freq   : -0.013 ppm
   Skew            : 0.116 ppm
   Root delay      : 0.000255977 seconds
   Root dispersion : 0.001222735 seconds
   Update interval : 64.4 seconds
   Leap status     : Normal
   [jlong@exao2 ~]$ chronyc sources
   MS Name/IP address         Stratum Poll Reach LastRx Last sample
   ===============================================================================
   ^? lbtntp.as.arizona.edu         0  10     0     -     +0ns[   +0ns] +/-    0ns
   ^+ alpaca.lco.cl                 1   6   377    50  -5031ns[-3877ns] +/- 1276us
   ^* vicuna.lco.cl                 1   6   377    20   +144ns[+1087ns] +/- 1352us
   ^- any.time.nl                   2   7   377    78  +3336us[+3337us] +/-   71ms
   ^- time.cloudflare.com           3   9   377   423   -430us[ -429us] +/-   68ms
   ^- slot.inf.utfsm.cl             2   9   377   281   +371us[ +357us] +/-   55ms
   ^- time.cloudflare.com           3   9   377   332   -372us[ -382us] +/-   68ms
   [jlong@exao2 ~]$ chronyc sourcestats
   Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
   ==============================================================================
   lbtntp.as.arizona.edu       0   0     0     +0.000   2000.000     +0ns  4000ms
   alpaca.lco.cl               7   4   583     -0.013      0.112  +5592ns  8661ns
   vicuna.lco.cl               7   4   389     +0.023      0.159  -5860ns  6630ns
   any.time.nl                10   3  1164     +0.007      0.221  +3369us    59us
   time.cloudflare.com        17  12   73m     -0.070      0.046   -533us    59us
   slot.inf.utfsm.cl           9   4   68m     -0.069      0.149   +361us   103us
   time.cloudflare.com        22  13   75m     -0.051      0.032   -409us    46us

Alternatively, you can compare one of the instrument computers to the RTC::

   exao3# chronyc tracking
   Reference ID    : C0A80202 (rtc-from-icc)
   Stratum         : 3
   Ref time (UTC)  : Wed Apr 09 01:42:37 2025
   System time     : 0.000000138 seconds fast of NTP time
   Last offset     : +0.000000387 seconds
   RMS offset      : 0.000001489 seconds
   Frequency       : 4.327 ppm slow
   Residual freq   : +0.023 ppm
   Skew            : 2.187 ppm
   Root delay      : 0.000305708 seconds
   Root dispersion : 0.001010077 seconds
   Update interval : 0.1 seconds
   Leap status     : Normal

   exao3# chronyc sources
   MS Name/IP address         Stratum Poll Reach LastRx Last sample
   ===============================================================================
   ^* rtc-from-icc                  2  -4   377     0  -1178ns[-1152ns] +/- 1160us

   exao3# chronyc sourcestats
   Name/IP Address            NP  NR  Span  Frequency  Freq Skew  Offset  Std Dev
   ==============================================================================
   rtc-from-icc               49  22    12     -0.001      0.097     -2ns   712ns


If the source is shown with a ``?`` in the second column or ``0`` in the
``Reach`` column, you may have firewalled traffic on the internal
“instrument” interface. You should ensure that the interface
corresponding to ``instrument`` or ``instrument-10g`` in ``nmtui``/``nmcli`` has
``ZONE=trusted``.

If it's not any of that, consult the `chrony FAQ <https://chrony.tuxfamily.org/faq.html>`__.

To force a (potentially discontinuous) time sync, ``sudo chronyc -a makestep``.

To verify correct operation from the time source end, ``sudo chronyc clients``:

::

   $ sudo chronyc clients
   [sudo] password for jlong:
   Hostname                      NTP   Drop Int IntL Last     Cmd   Drop Int  Last
   ===============================================================================
   localhost                       0      0   -   -     -      49      0  11    16
   exao2                          92      0   6   -    21       0      0   -     -
   exao3                          27      0   6   -    16       0      0   -     -

If either exao1 or exao2 does not appear, ssh into them and verify
``chronyd`` has started...

::

   $ systemctl is-active chronyd
   active

...and ensure ``exao2`` is reachable via that name…

::

   $ ping exao1
   PING exao1 (192.168.0.10) 56(84) bytes of data.
   64 bytes from exao1 (192.168.0.10): icmp_seq=1 ttl=64 time=0.196 ms
   ...

...and finally, consult the `chrony FAQ <https://chrony.tuxfamily.org/faq.html>`__.
