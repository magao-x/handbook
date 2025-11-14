User accounts and secrets
=========================

MagAO-X / XWCL user accounts are managed centrally for a few reasons.

- Ease of use: users can reset their own passwords
- Ease of administration: admins can update users/groups/SSH keys for all our servers at once
- Ease of revocation: when someone leaves the group, their account should be disabled consistently across all our servers

This document describes how to enroll a new computer in the auth system, the components of the system, and the risks and mitigations that come with this setup.

Enrolling a new computer
------------------------

1. Set up the computer to the point where it has an ``xdev`` and ``xsup`` account and SSH access
2. Grab the computer's SSH public key at ``/etc/ssh/ssh_host_ed25519_key.pub``
3. Follow the instructions at `xwcl/hush-hush <https://github.com/xwcl/hush-hush>`_ to add a new key to ``.sops.yaml`` (from a computer that's already enrolled)
4. Update the ciphertexts (e.g. ``sops updatekeys common.yaml``)
5. Make (or symlink) a script in ``deploy-local.d`` with the hostname of the new computer
5. Deploy

Adding a new user
-----------------

TODO automate identifying the next unused uid, updating ``add_a_user``/``add_a_developer`` scripts.

Components
----------

accounts.xwcl.science
^^^^^^^^^^^^^^^^^^^^^

Powered by LLDAP ("lightweight LDAP", when the L stands for "lightweight" already).

Users can only reset their passwords.

The admin interface lets you add / remove users, add / remove groups, update passwords, and enroll new SSH keys for users (if you are a member of the ``ldap_admin`` LDAP group).

SOPS (hush-hush)
^^^^^^^^^^^^^^^^

Secret management uses a relatively simple scheme (no need for yet another internet-accessible service) called SOPS. By storing every user and every server's public keys alongside them, the secrets can be encrypted separately for every reader and preserve editability.

It's pretty clever; you can read about it `here <https://github.com/getsops/sops/blob/main/README.rst>`_.

The secrets are stored in `xwcl/hush-hush <https://github.com/xwcl/hush-hush>`_.

SSSD
^^^^

The LDAP server is hosted at Vultr (same server as xwcl.science and magao-x.org). In case of a sudden loss of ~~cabin pressure~~ internet access, it should still be possible for users to log in.

Risks and mitigations
---------------------

All servers may become disconnected from the Internet (or, equivalently, the magao-x.org server may go down). Any credentials added or revoked on the accounts.xwcl.science interface will take effect when network access is restored.

Any users who have previously logged in will be able to log in with their cached credentials. The ``xdev`` and ``xsup`` accounts, as well as the ``magaox`` and ``magaox-dev`` groups, are defined in the ``/etc/passwd`` and ``/etc/group`` files on the instrument computers, so they will continue working when nothing else is. (At least one administrator should have their public key in the ``xdev`` account's ``~/.ssh/authorized_keys`` to bootstrap access in an outage.)

Users whose accounts are removed may still be able to access the servers until their credentials expire from that server's cache. To expire all cache entries immediately, use ``sss_cache -E``.

