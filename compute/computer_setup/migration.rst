Migrating data from an existing installation
============================================

There are several very important files to retain when reinstalling the operating system.

  - ``/var/lib/tailscale/tailscaled.state`` -- this file allows the machine to keep its name and IP address on the VPN
  - ``/etc/ssh/ssh_host_*_key*`` -- these files allow clients to connect over SSH without triggering a scary warning and requiring manual intervention
  - ``/home/xsup/.ssh/{authorized_keys,id_ed25519,id_ed25519.pub,known_hosts}`` -- these files allow ``xsup`` to connect to other MagAO-X machines without prompting for host key verification
  - ``/home/xsup/.lego/*`` -- these files store the identity used for TLS certificate renewal
  - ``/etc/systemd/system/renew_certificates.service.d/override.conf`` -- API credentials used by the ``lego`` command to renew HTTPS certificates used by the web UI (only on **AOC**)

.. note::

  UID and GID maps are handled primarily by the :doc:`../user_auth` system. If you need particular accounts or groups, copy them from ``/etc/{passwd,group,shadow}`` on the old machine.

You may additionally want to back up the user home directories to retain their configuration files. If you're trying to encourage judicious use of disk space by giving a fresh start, make sure to at least grab key material (i.e. ``~/.ssh/id_*``) for each user (and preserve permissions on the keys).

Tailscale doesn't want to have two computers with the same state data, so make sure to

- ``tailscale down && systemctl stop tailscaled`` on the old machine before you make the archive
- ``systemctl stop tailscaled`` on the new machine (if Tailscale is already installed)

before copying the ``/var/lib/tailscale/tailscaled.state`` to the new install and removing the original file.

For an example of how that might work in order::

  # On the old machine...
  xdev@exao1old:~$ sudo tar cvf /root/secrets.tar /var/lib/tailscale/tailscaled.state /etc/ssh/ssh_host_*_key* /home/xsup/.ssh/{authorized_keys,id_ed25519,id_ed25519.pub,known_hosts} /etc/systemd/system/renew_certificates.service.d/override.conf
  xdev@exao1old:~$ sudo chmod u=r,g=,o= /root/secrets.tar
  xdev@exao1old:~$ sudo cp /root/secrets.tar ~/
  xdev@exao1old:~$ sudo chown $USER ~/secrets.tar

  # Switching to the new machine...
  xdev@exao1:~$ scp jlong@200.28.147.179:secrets.tar ~/
  xdev@exao1:~$ sudo mv ~/secrets.tar /root/secrets.tar
  xdev@exao1:~$ sudo su
  # Now extract and fix permissions as root
  root@exao1:~# systemctl stop tailscaled
  root@exao1:~# cd /
  root@exao1:/# tar xvf /root/secrets.tar
  root@exao1:/# chmod u=r,g=,o= /etc/ssh/*_key
  root@exao1:~# systemctl restart sshd
  root@exao1:~# systemctl start tail
