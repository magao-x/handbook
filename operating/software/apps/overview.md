# Overview

MagAO-X applications are individual programs which control some aspect of the instrument, e.g. a hardware device or a software process.  When an application starts, it is assigned an INDI device name, which is usually different from the executable file name.  For instance, the pyramid WFS camera is controlled by the ocam2KCtrl process with device name `camwfs`.  The command line to start this program is 
```
[xsup@exao2 ~]$ /opt/MagAOX/bin/ocam2KCtrl -n camwfs
```
Note that MagAO-X apps normally need to be run as user `xsup`.

Each application runs in its own tmux session.  This can be accessed (as xsup) using either tmux (`tmux a -t camwfs`) or using the [xctrl](../utils/xctrl) utility:
```
[xsup@exao2 ~]$ xctrl inspect camwfs
```
See [xctrl](../utils/xctrl) for additional tools to control and monitor MagAO-X applications.  To follow the log use the [logdump](../utils/logdump) utility:
```
[any-user@exao2 ~]$ logdump -f camwfs
```

## Configuring instrument applications

All MagAO-X applications use a common configuration system.  In normal operations, the app configuration is read from a file located in `/opt/MagAOX/config/` with the INDI device name and the `.conf` extension. E.g. `camwfs.conf`.  The configuration files are basic TOML files, with key=value pairs, organized in sections:
```
key1=value1
key2=value2
# this is a comment

[section1]
key1=value1 #this key1 is distinct from the key1 above, since it's in a section

[section2]
key3=1,2,3,4,5 #this is a vector or list
```

To see what the options for a particular application are use the `-h` options:
```
[xsup@exao2 ~]$ /opt/MagAOX/bin/ocam2KCtrl -h`.
```
An example from the output of that command is
```
-L --logDir                  logger.logDir             <string>        The directory for log files 
```
which tells you that the short command-line option is `-L`, the long command-line option is `--logDir`, and the configuration file section is `[logger]` with keyword `logDir`.  The value expected is a string.  Finally, the description of this option is provided.

Though the configuration file specified by the `-n` option is the normal method to configure an app, additional settings can be made using the command line for troubleshooting and development.  Use the `-c` option to specify an additional configuration file -- any settings in this file will override the defaults (but anything not overridden will still be set by the default).  Any options passed as command-line arguments will override any settings in the configuration files.

## Standard Options

All MagAO-X applications accept the following options:

| Short | Long                   | Config-File *         | Type            | Description |
| ---   | ---                    | ---                   | ---             | --- |
| `-c`  | `--config`             | config                | string          | A local config file |
| `-h`  | `--help`               |                       | none            | Print this message and exit |
| `-p`  | `--loopPause`          | loopPause             | unsigned long   | The main loop pause time in ns |
| `-P`  | `--RTPriority`         | RTPriority            | unsigned        | The real-time priority (0-99) |
| `-L`  | `--logDir`             | logger.logDir         | string          | The directory for log files |
|       | `--logExt`             | logger.logExt         | string          | The extension for log files |
|       | `--maxLogSize`         | logger.maxLogSize     | string          | The maximum size of log files |
|       | `--writePause`         | logger.writePause     | unsigned long   | The log thread pause time in ns |
|       | `--logThreadPrio`      | logger.logThreadPrio  | int             | The log thread priority |
| `-l`  | `--logLevel`           | logger.logLevel       | string          | The log level |
| `-n`  | `--name`               | name                  | string          | The name of the application, specifies config. |

\* In the "Config-File" column, the syntax `section.keyword` means that in the config file this option is set as follows:
```
[section]
keyword=value
```
