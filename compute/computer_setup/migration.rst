Migrating data from an existing installation
============================================

There are several very important files to retain when reinstalling the operating system.

  - ``/var/lib/tailscale/tailscaled.state`` -- this file allows the machine to keep its name and IP address on the VPN
  - ``/etc/ssh/ssh_host_*_key*`` -- these files allow clients to connect over SSH without triggering a scary warning and requiring manual intervention
  - ``/home/xsup/.ssh/{authorized_keys,id_ed25519,id_ed25519.pub,known_hosts}`` -- these files allow ``xsup`` to connect to other MagAO-X machines without prompting for host key verification
  - ``/etc/{passwd,group,shadow}`` -- these files contain the UID and GID mappings and user passwords to restore. Manual surgery will be required because new installs come with new system accounts. Generally, we only want to migrate user accounts (UID ≥ 1000).
  - ``/etc/systemd/system/renew_certificates.service.d/override.conf`` -- API credentials used by the ``lego`` command to renew HTTPS certificates used by the web UI (only on AOC)

You may additionally want to back up the user home directories to retain their configuration files, though they should store data on the `/data` partition.
