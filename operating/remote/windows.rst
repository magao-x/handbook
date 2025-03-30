Running MagAO-X from Windows
============================

Windows users can use WSL2 or multipass to set up.

Multipass
---------

You should run ``multipass set local.privileged-mounts=true`` to enable file transfers. `Read here <https://multipass.run/docs/privileged-mounts>`_ about the security implications this setting has for Windows.

In a new terminal window, to create a VM with Ubuntu version 24.04::

   $ multipass launch -n magao-x-vm 24.04
   Launched: magao-x-vm

You should mount your home directory into the VM::

   $ multipass mount $HOME magao-x-vm:/home/ubuntu/Home

(TODO: what is $HOME equivalent in Windows?)

Next, verify you can connect to the VM and get a shell prompt::

   $ multipass shell magao-x-vm
   [... some lines omitted ...]
   ubuntu@magao-x-vm:~$

Notice that the shell prompt has changed to ``ubuntu@magao-x-vm:~$``. Commands within the VM will be prefixed with ``ubuntu@magao-x-vm:~$`` (though ``~`` may change), and "host" commands will continue to be prefixed with ``$``. Your home directory will be available inside the VM under ``~/Home``. This is one way to get files into and out of the VM. ::

   $ ls ~/Home
   [... list of all your files ...]

Now, exit the VM shell::

   ubuntu@magao-x-vm:~$ exit
   $

The first thing to do after creating the VM is to stop it (which is just like shutting down a "real" physical computer) and adjust some settings::

   $ multipass stop magao-x-vm
   $ multipass set local.magao-x-vm.disk=20GiB
   $ multipass set local.magao-x-vm.cpus=4
   $ multipass set local.magao-x-vm.memory=8G

This ensures you have enough space in the VM to install the MagAO-X software. (You can change the number of CPUs allocated to the VM to a number other than four if you want.)

Now, boot the virtual machine::

   $ multipass start magao-x-vm

You will see the message "Starting magao-x-vm" and a loading spinner. When the VM has started, you will be back at your host shell prompt. Wait a minute for the VM to start, then connect your terminal to the VM with::

   $ multipass shell magao-x-vm
   ubuntu@magao-x-vm:~$

Authentication Error
~~~~~~~~~~~~~~~~~~~~
Also, in the unlikely event you encounter this error (maybe upon reinstalling multipass)::

   The client is not authenticated with the Multipass service.
   Please use 'multipass authenticate' before proceeding.

this `forum post <https://discourse.ubuntu.com/t/unable-to-authorize-the-client-and-cannot-set-a-passphrase-workaround/28321>`_ explains recovery steps.


Resetting the VM
----------------

If you need to reset the VM, start by copying any data you need out of it (e.g. to ``~/Home``). Then, to **delete it forever**, use these commands::

   $ multipass stop magao-x-vm
   $ multipass delete magao-x-vm
   $ multipass purge

To recreate the VM, follow the instructions from the top of the page again.

Manually Install MagAO-X Software
-----------------------------------

Note: you do not need to do this if the automated creation script worked above.

Next, within the VM, obtain a copy of the MagAO-X software and install scripts. Using ``git`` we clone the MagAOX repository::

   ubuntu@magao-x-vm:~$ git clone --depth=1 https://github.com/magao-x/MagAOX.git
   Cloning into 'MagAOX'...
   remote: Enumerating objects: 1040, done.
   remote: Counting objects: 100% (1040/1040), done.
   remote: Compressing objects: 100% (907/907), done.
   remote: Total 1040 (delta 166), reused 642 (delta 100), pack-reused 0
   Receiving objects: 100% (1040/1040), 2.13 MiB | 1.04 MiB/s, done.
   Resolving deltas: 100% (166/166), done.

Go to the ``setup`` subdirectory::

   ubuntu@magao-x-vm:~$ cd MagAOX/setup/

Run the pre-provisioning script to establish the workstation role::

   ubuntu@magao-x-vm:~/MagAOX/setup$ MAGAOX_ROLE=workstation ./pre_provision.sh

You need to reload the ubuntu user's groups, so now logout::

   ubuntu@magao-x-vm:~/MagAOX/setup$ exit

And log back in::

   $ multipass shell magao-x-vm

You can now run the provisioning script::

   ubuntu@magao-x-vm:~/MagAOX/setup$ bash provision.sh

Now, wait a while. Don't be alarmed by the amount of output! Provisioning is very
noisy, and messages in red aren't necessarily errors. Successful
provisioning will end with the message

::

   Provisioning complete
   You now need to log out and back in for group changes to take effect

As the message says, you should exit the VM with ``exit``, and return to your host command prompt.

What to do if you don't see ``Provisioning complete``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most likely that means an error occurred running the provisioning
scripts and they did not finish. That can happen if a big download gets
interrupted, for example. It's always safe to run ``bash provision.sh``
again. It'll re-run only necessary steps, which may be enough to get you to
``Provisioning complete``.

If that doesn't resolve the issue, you'll need the complete provisioning
output to get help. The following command will save it to a file
``provision.log`` in your home folder on the host machine, which you can then email or Slack to someone who can help. ::

   ubuntu@magao-x-vm:~/MagAOX/setup$ bash provision.sh | tee ~/Home/provision.log

Configuring the VM to connect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before you can remotely control MagAO-X, a little post-provisioning
configuration is required. You must have a user account on MagAO-X with
an SSH key file configured. For the preconfigured tunnels to work, that key must not have a passphrase.

(TODO: where does Windows keep its key files?)

If you have a key pair in your computer's ``~/.ssh/`` folder, this appears at ``~/Home/.ssh/`` in the VM. (Note: RSA keys are not allowed.) Copy it into place::


   $ multipass shell magao-x-vm
   ubuntu@magao-x-vm:~$ cp ~/Home/.ssh/id_* ~/.ssh/
   ubuntu@magao-x-vm:~$ chmod u=r,g=,o= ~/.ssh/id_*

Next, you will need to edit the VM's ``~/.ssh/config`` file to add your username. Still within the VM, open a text editor::

   ubuntu@magao-x-vm:~$ nano ~/.ssh/config

At the end of the file, the line ``User YOURUSERNAME`` should be changed to reflect your MagAO-X username. Save and exit.

Next steps
----------

Usage of the multipass VM is described in the Linux guide under :ref:`multipass_usage`.