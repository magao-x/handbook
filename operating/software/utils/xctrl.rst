xctrl
=====

The process control interface for MagAO-X apps.

The ``xctrl`` script is installed on all MagAO-X systems (including VMs
and the test bed) for startup, shutdown, quick status checks, and
inspection of MagAO-X apps.

To use ``xctrl``, open a terminal window on (or SSH in to) the computer
you want to control. (You do not need to ``xsupify`` for ``xctrl``.)
Then, commands take the form of ``xctrl VERB [PROCNAME] ...`` where the
``VERB``\ s are explained below. Most commands can be run without a
``PROCNAME`` and will target all the configured processes by default.

The valid names for ``PROCNAME`` are listed in
``/opt/MagAOX/config/proclist_${MAGAOX_ROLE}.txt``.

``xctrl startup``
-----------------

When called without additional arguments, ``xctrl startup`` will start
any process from the proclist that does *not* have a running tmux
session. (Yes, each process is parented to a tmux session.)

If you list one or more process names,
e.g. ``xctrl startup camtip camsci``, then ``xctrl`` will only consider
the processes named.

``xctrl shutdown``
------------------

When called without additional arguments, ``xctrl shutdown`` will
interrupt all running MagAO-X processes (by sending ``Ctrl+C`` to their
tmux sessions). If they do not cleanly exit after five attempts (~5
seconds), ``xctrl`` will terminate them.

You can list one or more process names, similarly to ``startup``.

``xctrl restart``
-----------------

Effectively ``xctrl shutdown`` followed by ``xctrl startup``.

You can list one or more process names, similarly to ``startup``.

``xctrl inspect PROCNAME``
--------------------------

Requires an argument: the process name to inspect. The ``xctrl inspect``
command attaches to the ``tmux`` session where ``PROCNAME`` is running
(or, if you’re inspecting it, maybe recently crashed). From the prompt
you can use the up arrow key as normal to retrieve the last command
executed (i.e. the process under inspection).

When you’re done inspecting, you can use ``Ctrl+b`` followed by ``d`` to
detach from a running process (or just ``exit`` to end the session).

``xctrl status``
----------------

Displays a short status report for all configured processes. If you
supply one or more PROCNAMEs, it will show only those. Example output:

::

   $ xctrl status
   isAOC: running (pid: 60636)
   pdu0: running (pid: 6181)
   pdu1: running (pid: 16067)
   pdu2: running (pid: 21664)
   pdu3: running (pid: 11874)
   labCool: running (pid: 11956)
   tcsi: running (pid: 11843)
   adctrack: running (pid: 12061)
   aoc_icc_indi: running (pid: 12057)
   aoc_rtc_indi: running (pid: 12054)
   aoc_icc_milkzmq: running (pid: 11883)
   aoc_rtc_milkzmq: running (pid: 12150)
   mzmqClientAOC_ICC: running (pid: 12149)
   mzmqClientAOC_RTC: running (pid: 12045)

The statuses will be color-coded (if your terminal supports it). Green
means it’s all good.

You can also check the status of a single process with
``xctrl status PROCNAME``, e.g.:

::

   $ xctrl status isAOC
   isAOC: running (pid: 60636)

If you shut down a process cleanly (or haven’t yet started it) you will
see ``not started`` in yellow and (usually) log lines indicating the
state transitioned to ``SHUTDOWN``:

::

   isAOC: not started

If the process dies but its parent ``tmux`` session is alive:

::

   isAOC: session exists, but process is not running

You may want to investigate the recent logs with `logdump <logdump>`__
or ``xctrl peek PROCNAME`` to see why it died. To restore it, you can
``xctrl inspect PROCNAME`` to connect to that ``tmux`` session and
attempt to restart the process. You can also ``xctrl restart PROCNAME``
to end and recreate the ``tmux`` session.

It is possible on occasion for a process to die, e.g. after a system
crash and reboot. In those cases, you will see something like this:

::

   isAOC: dead (stale pid)

This is another situation where you may want to check recent logs. To
restore it, you can simply ``xctrl startup`` that process.

``xctrl peek``
--------------

The extended version of ``xctrl status``, which includes both the status
and last ten lines that the process wrote to its log. (For a full log
dump, see `logdump <logdump>`__ docs.) You can also use
``xctrl peek PROCNAME`` to peek at a single process, e.g.:

::

   $ xctrl peek isAOC
   isAOC: running (pid: 60636)
   2020-07-30T16:10:37.150000000 INFO IS: Driver camwfs-dark@localhost:7626 at 127.0.0.1 now connected on socket=91
   2020-07-30T16:10:37.150000000 INFO IS: Driver dmtweeter@localhost:7626 at 127.0.0.1 now connected on socket=92
   2020-07-30T16:10:37.178000000 INFO IS: Driver ttmpupil@localhost:7626 at 127.0.0.1 now connected on socket=93
   2020-07-30T16:10:37.178000000 INFO IS: Driver camwfs-slopes@localhost:7626 at 127.0.0.1 now connected on socket=94
   2020-07-30T16:10:37.211000000 INFO IS: Driver fxngenmodwfs@localhost:7626 at 127.0.0.1 now connected on socket=95
   2020-07-30T16:10:37.218000000 INFO IS: Driver aoloop@localhost:7626 at 127.0.0.1 now connected on socket=96
   2020-07-30T16:10:37.219000000 INFO IS: Driver tweeterModes@localhost:7626 at 127.0.0.1 now connected on socket=97
   2020-07-30T16:10:37.219000000 INFO IS: Driver wooferModes@localhost:7626 at 127.0.0.1 now connected on socket=98
   2020-07-30T16:10:37.220000000 INFO IS: Driver w2tcsOffloader@localhost:7626 at 127.0.0.1 now connected on socket=99
   2020-07-30T16:10:37.259000000 INFO IS: Driver dmtweeter-avg@localhost:7626 at 127.0.0.1 now connected on socket=100
   End isAOC logs

**Tip:** Lines like ``State changed from A to B`` can give you a hint as
to what’s going wrong. See
`stateCodes.hpp <https://github.com/magao-x/MagAOX/blob/master/libMagAOX/app/stateCodes.hpp>`__
for descriptions of the different states.
