Operation of the MagAO-X instrument
===================================

The MagAO-X instrument has (at last count) several thousand controllable 
degrees of freedom, three computers, and dozens of processes. To manage 
that complexity, we have the guides and tools detailed herein.

Good starting points include the :doc:`startup <startup>` guide and the
:doc:`troubleshooting <../troubleshooting>` guide. Useful tools include 
:doc:`software/utils/xctrl`, :doc:`software/utils/cursesINDI`, and 
:doc:`software/utils/logdump`.

Viewing camera output and DM input (really, any shared memory image) uses
`rtimv`, which is documented in its own 
`User Guide <https://github.com/jaredmales/rtimv/blob/master/doc/UserGuide.md#rtimv>`_.

.. toctree::
   :maxdepth: 2

   startup
   shutdown
   alignment
   software/python_indi_device
   software/guis/index
   software/utils/index
   software/apps/index
   abeginnersguidetomagaox   
   
