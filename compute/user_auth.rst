User accounts and secrets
=========================

MagAO-X / XWCL user accounts are managed centrally for a few reasons.

- Ease of use: users can reset their own passwords
- Ease of administration: admins can update users/groups/SSH keys for all our servers at once
- Ease of revocation: when someone leaves the group, their account should be disabled consistently across all our servers

This document describes how to enroll a new computer in the auth system, the components of the system, and the risks and mitigations that come with this setup.

Components
----------

accounts.xwcl.science
^^^^^^^^^^^^^^^^^^^^^

Powered by LLDAP ("lightweight LDAP", where the L stands for "lightweight" already).

The admin interface lets you add / remove users, add / remove groups, update passwords, and enroll new SSH keys for users (if you are a member of the ``ldap_admin`` LDAP group).

Password reset
~~~~~~~~~~~~~~

Users can reset their own passwords using https://accounts.xwcl.science/. However, if they have previously logged in to an instrument computer, you may need to clear the credentials cache so the new password takes effect. On Rocky/Fedora hosts that looks like this::

    $ sudo sssctl cache-expire -u USERNAME

replacing ``USERNAME`` with the user whose login info you need to refresh.

Adding a new user account
~~~~~~~~~~~~~~~~~~~~~~~~~

Log in to https://accounts.xwcl.science/ and click the "Create a user" button. 

You will need to assign them an available numeric UID (in the ``Uidnumber:`` field), which will probably involve looking at existing user accounts.

Fortunately, the ``list_xwcl_users`` script will tell you which UIDs are in use::
    
    root@exao1:~# list_xwcl_users
                 uid   uidNumber   gidNumber
               admin
        srv_authelia
         srv_grafana
     srv_linux_login
               jlong  2000        2002
             jrmales  2001        2002
          kvangorkom  2002        2001
           syhaffert  2003        2001
               mmars  2004        2001
             perez01  2005        2000
                eden  2006        2001
           jliberman  2007        2001
            rlandman  2008        2001
           twitchell  2009        2001
     parkertjohnson1  2010        2001
            etonucci  2011        2000
              jkueny  2012        2000
            tsnedden  2013        2000
          mileslucas  2014        2001
              ataras  2015        2000
         loganpearce  2016        2000
             rharris  2017        2000
    
The primary group for new accounts should be ``magaox`` (gid: 2000). 

Go to the "Groups" tab. Normal users should be added to the ``magaox`` group, and builders can be added to ``magaox-dev`` (allows deploying software changes) and ``jupyterhub`` (allows using the provided Python notebook server).

.. warning::

    There are ``add_a_user`` and ``add_a_developer`` scripts in ``magao-x-setup`` but they should **only** be used when you specifically need a local account on **only that computer**. If you ever want to make it a cross-computer account, you will need to re-number all the files the user owns.

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

Users whose accounts are removed **may still be able to access the servers** until their credentials expire from that server's cache. To expire all cache entries immediately, use ``sss_cache -E``.

Giving people and computers access to secrets
---------------------------------------------

Software tools
^^^^^^^^^^^^^^

Computers with MagAO-X secrets need these two pieces of software

- `sops` - for `Secrets OPerationS <https://github.com/getsops/sops>`_ (It's pretty clever; you can read about it `here <https://github.com/getsops/sops/blob/main/README.rst>`_.)
- `age` - https://github.com/FiloSottile/age

To add/remove computers or update secrets you will need these tools installed on your own computer as well.

Secret data
^^^^^^^^^^^

The secrets live in https://github.com/xwcl/hush-hush in an encrypted form, as described below. You'll want to clone a copy to your computer to follow along::

    git clone https://github.com/xwcl/hush-hush.git

Getting set up as an administrator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The `.sops.yaml <https://github.com/xwcl/hush-hush/blob/main/.sops.yaml>`_ file in ``xwcl/hush-hush`` lists all the target keys for which secrets get encrypted. Every secret (file/value) gets encrypted once for each possible editor and each possible consumer, using their public keys. Since anyone can encrypt with a public key, editing the secret just involves decrypting it for yourself and re-encrypting the edited version N different times to update the file.

This process is what the ``sops`` command automates.

SOPS can use your SSH key pair. If you have a key called ``~/.ssh/id_ed25519`` with public key ``~/.ssh/id_ed25519.pub``, you'll want to copy the **public** part and send it to one of the existing administrators.

That will look like this::

    ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOumkkhMI1bIO3Pzkm8lW9Pwz+68G7fbXU1/Ho3X+LA0 josephlong@kestrel

**Steps to be done by an existing administrator:**

1. In `.sops.yaml <https://github.com/xwcl/hush-hush/blob/main/.sops.yaml>`_ there is a ``keys:`` block. By convention, administrator keys are named ``admin-<username>-<provenance>``. (So, for my key above, that would be ``admin-jlong-kestrel`` because the key was generated on the machine ``kestrel``.)

2. Add the key, noting the ``-`` to make it a list item and the ``&`` prefix. (Any extra comment text like the ``josephlong@kestrel`` at the end of my ``id_ed25519.pub`` above is optional, but ignored if present.) ::

    keys:
    - &admin-jlong-kestrel ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOumkkhMI1bIO3Pzkm8lW9Pwz+68G7fbXU1/Ho3X+LA0
    # ... rest of file omitted ...

3. Next, add a reference to the key (i.e. ``*`` prefixed name) to any ``key_groups`` they should be able to access. For example::

        # ...
        creation_rules:
        - path_regex: 'secrets/common/.+'
            key_groups:
            - age:
            - *admin-jlong-kestrel
        # ...

4. Save ``.sops.yml``. Regenerate the ciphertexts using the newly added key with ``./updatekeys-all.sh`` (or just run ``sops updatekeys $filename`` for every file affected).

5. Commit and push your changes to GitHub.

.. _add_a_server:

Updating secrets repository to add a server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. The computer must be configured for SSH, with a host key in (most likely) ``/etc/ssh/ssh_host_ed25519_key.pub``. Copy the host key and proceed as above, except that it should be named ``server-<hostname>`` (instead of ``admin-``).

2. Add the host to the minimal set of secrets. (At least the group under ``secrets/common/``, though, for network login to work.)

3. Regenerate the ciphertexts using the newly added key with ``./updatekeys-all.sh``.

4. Commit and push your changes to GitHub.

Enrolling a new computer
^^^^^^^^^^^^^^^^^^^^^^^^

After the secret files have been updated, you still need to deploy them to the new computer.

1. Make (or symlink) a script in ``deploy-local.d`` with the hostname of the new computer (e.g. ``ln -s ./rocky_ldap_certs.sh ./exao10.sh`` from inside ``./deploy-local.d``)

2. Install SSSD on the new computer to enable user authentication against LDAP (for Rocky or Fedora, use ``install_sssd.sh`` from `magao-x/magao-x-setup <https://github.com/magao-x/magao-x-setup/blob/main/steps/install_sssd.sh>`_)

3. Deploy to the new computer from your own with ``bash deploy.sh my-host-name`` (replacing ``my-host-name`` with an SSH-able hostname or alias to the server)

4. Add the new computer's hostname to the list in ``deploy-all.sh``.

5. Commit and push your changes to GitHub.

.. _new_computer_setup:

New computer setup
------------------

When you have just finished the mostly-automated provisioning, you have a computer with two user accounts: ``xdev`` and ``xsup``. To enable login with MagAO-X accounts, you will need to:

1. Get the newly-generated public key from ``/etc/ssh/ssh_host_ed25519_key.pub`` and follow :ref:`add_a_server`
2. Run the ``install_sssd.sh`` script from https://github.com/magao-x/magao-x-setup/blob/main/steps/install_sssd.sh
3. Open up a root terminal (``sudo -i``) and keep it around in case something breaks in the next step
4. Add the necessary symlink to ``hush-hush/deploy-local.d/`` and run ``deploy.sh xdev@$NEW_COMPUTER_HOSTNAME``
5. Verify you can now log in with your MagAO-X account and the appropriate groups are applied and SSH authorized keys are accepted
