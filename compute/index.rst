Compute System
==============

The MagAO-X computing system.

.. toctree::
   :maxdepth: 1

   remote_operation
   python
   administration
   networking
   data_storage_management
   computer_setup/computer_setup
   ssl_certs
   nas
   tailscale

Computer Architecture
---------------------

The computers that run MagAO-X are:

-  The Instrument Control Computer (ICC)
-  The Real Time control Computer (RTC)
-  The Adaptive optics Operator Computer (AOC) *TODO*

While on the University of Arizona network, the RTC is known as
``exao2.as.arizona.edu``and the ICC as
``exao3.as.arizona.edu``. (At Las Campanas, they are ``.lco.cl``.)

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
