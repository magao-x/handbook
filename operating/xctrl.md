# xctrl

The process control interface for MagAO-X apps.

The `xctrl` script is installed on all MagAO-X systems (including VMs and the test bed) for startup, shutdown, quick status checks, and inspection of MagAO-X apps.

To use `xctrl`, open a terminal window on (or SSH in to) the computer you want to control. (You do not need to `su xsup` for `xctrl`.) Then, commands take the form of `xctrl VERB [PROCNAME] ...` where the `VERB`s are explained below. Most commands can be run without a `PROCNAME` and will target all the configured processes by default. 

The valid names for `PROCNAME` are listed in `/opt/MagAOX/config/proclist_${MAGAOX_ROLE}.txt`.

## `xctrl startup`

When called without additional arguments, `xctrl startup` will start any process from the proclist that does *not* have a running tmux session. (Yes, each process is parented to a tmux session.)

If you list one or more process names, e.g. `xctrl startup camtip camsci`, then `xctrl` will only consider the processes named.

## `xctrl shutdown`

When called without additional arguments, `xctrl shutdown` will interrupt all running MagAO-X processes (by sending `Ctrl+C` to their tmux sessions). If they do not cleanly exit after five attempts (~5 seconds), `xctrl` will terminate them.

You can list one or more process names, similarly to `startup`.

## `xctrl restart`

Effectively `xctrl shutdown` followed by `xctrl startup`.

You can list one or more process names, similarly to `startup`.

## `xctrl inspect PROCNAME`

Requires an argument: the process name to inspect. The `xctrl inspect` command attaches to the `tmux` session where `PROCNAME` is running (or, if you're inspecting it, maybe recently crashed). From the prompt you can use the up arrow key as normal to retrieve the last command executed (i.e. the process under inspection).

When you're done inspecting, you can use `Ctrl+b` followed by `d` to detach from a running process (or just `exit` to end the session).

## `xctrl status`

Displays a short status report for all configured processes. If you supply one or more PROCNAMEs, it will show only those. Example output:

```
$ xctrl status aoloop
aoloop: running (pid: 62852)
2020-07-28T21:01:52.855798452 INFO PID (62852) locked.
2020-07-28T21:01:52.856423980 INFO State changed from UNINITIALIZED to INITIALIZED
2020-07-28T21:01:52.856568207 INFO offload thread scheduler priority set to 0
2020-07-28T21:01:52.856707653 INFO INDI driver communications started
2020-07-28T21:01:52.856712784 INFO State changed from INITIALIZED to READY
End aoloop logs
```

The first line shows the state, and color-codes it if your terminal supports it. Green means it's all good. Below that, you see the last five lines that the process wrote to its log. (For a full log dump, see [logdump](software/utils/logdump.md) docs.)

**Tip:** Lines like `State changed from A to B` can give you a hint as to what's going wrong. See [stateCodes.hpp](https://github.com/magao-x/MagAOX/blob/master/libMagAOX/app/stateCodes.hpp) for descriptions of the different states.

If the process didn't exit cleanly, i.e. crashed, `xctrl` will report `dead (stale pid)` in red. In those cases, the log output may say the process is `READY`, but that's just the last thing that it logged before it died.

```
$ xctrl status aoloop
aoloop: dead (stale pid)
2020-07-28T21:01:52.855798452 INFO PID (62852) locked.
2020-07-28T21:01:52.856423980 INFO State changed from UNINITIALIZED to INITIALIZED
2020-07-28T21:01:52.856568207 INFO offload thread scheduler priority set to 0
2020-07-28T21:01:52.856707653 INFO INDI driver communications started
2020-07-28T21:01:52.856712784 INFO State changed from INITIALIZED to READY
End aoloop logs
```

If you shut down a process cleanly (or haven't yet started it) you will see `not started` in yellow and log lines indicating the state transitioned to `SHUTDOWN`:

```
$ xctrl status aoloop
aoloop: not started
2020-07-28T21:01:30.373659212 INFO State changed from INITIALIZED to READY
2020-07-28T21:01:38.124834593 INFO Caught signal SIGTERM. Shutting down.
2020-07-28T21:01:38.374862137 INFO State changed from READY to SHUTDOWN
2020-07-28T21:01:38.374991913 INFO INDI driver communications stopped
2020-07-28T21:01:38.375123905 INFO PID (62578) unlocked.
End aoloop logs
```

If the process has exited but the tmux session exists, you will also see `not started` and will have to `xctrl inspect PROCNAME` to go start it again (or `xctrl shutdown PROCNAME` to end the tmux session). (TODO: make this better.)