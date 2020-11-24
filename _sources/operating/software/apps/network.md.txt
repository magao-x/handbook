# Networking

Networking apps manage communication internal to the instrument. (They are distinct from utilities in that they run until killed.)

## sshDigger

`sshDigger` uses the `autossh` utility to form a robust `SSH` tunnel or port forward to a remote host.  In addition, the forked `autossh` process is monitored, and if it dies a new one is created.

The base configuration is normally located at `/opt/MagAOX/config/sshTunnels.conf` ([view in magao-x/config](https://github.com/magao-x/config/blob/master/sshTunnels.conf)).  It should contain options applicable to all tunnels, as well as the tunnel definitions themselves.

The tunnel name must be specified with the `-n` command line option. The `tunnel_name` denotes the section in the configuration file(s) which contains the specification of the tunnel. `sshDigger` is normally configured via a base configuration file, hence all other command-line arguments are optional.

This app does not require that an instance specific configuration `tunnel_name.conf` be available.  If one is available matching the name given with the `-n tunnel_name` option, then any settings contained therein will override those given in the base config file.

### Tunnel Specification

Tunnels are specified by a section in the configuration files, normally the base `sshTunnels.conf` file.  The section must have the following members

```
[tunnel_name]
remoteHost=resolvable_name
localPort=X
remotePort=Y
```

Where
- `resolvable_name` is an ip address or host name.  This can include a user name `user@` at the beginning if needed.
- `X` denotes the integer local port number.
- `Y` denotes the integer remote port number

This results in `ssh` being started with

```
$ ssh -nNTL X:localhost:Y resolvable_name
```

by the `autossh` utility.

For example, to create an SSH tunnel for `magaox_aoc_to_rtc_indi`:
```
$ /opt/MagAOX/bin/sshDigger -n magaox_aoc_to_rtc_indi
```

Which expects a configuration entry of the form:
```
[magaox_aoc_to_rtc_indi]
remoteHost=rtc
localPort=7630
remotePort=7624
```

This then securely forwards traffic from `localhost:7630` to the INDI server on `rtc:7624`.

## xindiserver

`xindiserver` wraps the standard `indiserver` program in a MagAO-X interface.  This includes exposing configuration options, and capturing logs which are reformatted in the `flatlogs` binary logging system.

### Options

| Short | Long              | Config-File *        | Type              | Description |
|-------|-------------------|----------------------|-------------------|-------|
| `-m`  |                   | indiserver.m         | int               | indiserver kills client if it gets more than this many MB behind, default 50 |
| `-N`  |                   | indiserver.N         | bool              | indiserver: ignore /tmp/noindi. Capitalized to avoid conflict with `--name` |
| `-p`  |                   | indiserver.p         | int               | indiserver: alternate IP port, default 7624 |
| `-v`  |                   | indiserver.v         | int               | indiserver: log verbosity, -v, -vv or -vvv |
| `-x`  |                   | indiserver.x         | bool              | exit after last client disconnects -- FOR PROFILING ONLY |
| `-L`  | `--local`         | local.drivers        | vector of strings | List of local drivers to start. |
| `-R`  | `--remote`        | remote.drivers       | vector of string  | List of remote drivers to start, in the form of name\@hostname without the port.  Hostname needs an entry in remote.hosts |
| `-H`  | `--hosts`         | remote.hosts         | vector of string  | List of remote hosts, in the form of `hostname[:remote_port]:local_port`.  `remote_port` is optional if it is the INDI default. |

### Driver Specifications

Lists of driver names are passed to `xindiserver` via the configuration system.  Drivers can be either local or remote.

Driver names can not be repeated, whether local or remote.

#### Local Drivers

Drivers running on the same machine are specified by their names only.  On the command line this would be
```
--local=driverX,driverY,driverZ
```
and in the configuration file this would be
```
[local]
drivers=driverX,driverY,driverZ
```

#### Remote Drivers

Drivers running a remote machine are specified by their names and the name of the SSH tunnel to that machine.  `xindiserver` parses the `sshTunnels.conf` config file as part of configuration.

NOTE: the tunnel specification is by the tunnel name (the section in the config file), not the host name.

On the command line this would be
```
--remote=driverR@tunnel_name_1,driverS@tunnel_name_2,driverT@tunnel_name_1
```
and in the configuration file this would be
```
[remote]
drivers=driverR@tunnel_name_1,driverS@tunnel_name_2,driverT@tunnel_name_1
```

In both cases it must be true that `sshTunnels.conf` contains a valid tunnel specification for `tunnel_name_1` and `tunnel_name_2`.

### Exit Status

If there are no errors `xindiserver` runs until killed.

If the specified port is already in use, i.e. due to a previously running `indiserver`, then `xindiserver` will produce a log entry, change to state FAILURE, and exit.

If the `indiserver` process exits for any reason, then `xindiserver` will produce a log entry, change to state FAILURE, and exit.

If the `xindidriver` program for a driver reports that it can not get a lock, which indicates that another instance of `xindidriver` already has the FIFO open, then `xindiserver` will produce a log entry, change to state FAILURE, and exit.


### Troubleshooting

If `indiserver` exits abnormally (this is extremly rare, and is not expected except due to operator error!), it can leave the `xindidriver` processes running.  A subsequent attempt to restart will fail when new instances of `xindidriver` can not lock the FIFOs.  The solution is manually kill each of the `xindidriver` processes, which will have the symlinked names of the `MagAOXApp` they are communicating with.
