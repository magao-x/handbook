Compute System
==============

The MagAO-X computing system.

.. toctree::
   :maxdepth: 1

   remote_operation
   python
   database
   administration
   networking
   data_storage_management
   computer_setup/computer_setup
   ssl_certs
   nas
   vpn

Computer Architecture
---------------------

The computers that run MagAO-X are:

-  The Instrument Control Computer (ICC)
-  The Real Time control Computer (RTC)
-  The Adaptive optics Operator Computer (AOC)

We use Rocky Linux 9 because it is based on Red Hat Enterprise Linux, which our vendors sort-of support. However, Red Hat no longer supports the KDE graphical desktop environment we use, which leaves us in a bit of a pickle.

For consistency, we use Rocky Linux 9 with KDE on our operator workstation (AOC), and Rocky Linux 9 server on ICC and RTC, which are used headless.

Real Time Controller
~~~~~~~~~~~~~~~~~~~~

Responsible for wavefront sensing and control, and directly connected to
the HOWFS detector and deformable mirrors. The operation of the control
loop depends on `CACAO: Compute And Control for Adaptive
Optics <https://github.com/cacao-org/cacao>`__ authored by `Olivier
Guyon and
collaborators <https://github.com/cacao-org/cacao/graphs/contributors>`__.

Instrument Control Computer
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Responsible for functions that do not depend on strong realtime
constraints, including LOWFS, configuring and reading out science
cameras, etc.
