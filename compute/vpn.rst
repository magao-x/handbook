Instrument Virtual Private Network
==================================

The MagAO-X instrument uses a secure self-hosted virtual private network (VPN) to allow authorized users to access the instrument. Since this is an "overlay network" VPN, traffic between your computer and the instrument computer travels by the most direct route possible. All traffic is encrypted in transit.

On first connection
-------------------

The first time you connect your computer to the MagAO-X VPN, you will need to register its encryption key with the coordinating server at https://inst.magao-x.org/.

1. `Download <https://tailscale.com/download/>`_ the VPN client

2. Install, following the instructions for your operating system. Skip any prompts to log in, as we will need to set the MagAO-X login server later.

3. Depending on your operating system:

    a. **Linux**: In a terminal, run ``sudo tailscale up --hostname=YOURHOSTNAMEHERE --login-server=https://inst.magao-x.org/ --force-reauth``. (If you don't know / care what your hostname is, you can leave off the whole ``--hostname=YOURHOSTNAMEHERE`` segment.)

    b. **macOS (terminal)**: Use Tailscale's login command to add your profile: ``tailscale login --login-server https://inst.magao-x.org``
    c. **macOS (GUI)**: 
    
        1. Hold the alt/option key and click the Tailscale icon in the menu, go down to the "Debug" menu
        2. Under "Custom Login Server", select "Add Account..."
        3. Enter the address of the headscale instance  "https://inst.magao-x.org" and press "Add Account"
        4. Follow the login procedure in the browser
    d. **Windows**: Open a command prompt (hold the Windows key + R, type ``cmd``, hit enter). In the command prompt, type ``tailscale login --login-server https://inst.magao-x.org`` and hit enter.

4. You will get a message of the form::

        To authenticate, visit:

        https://inst.magao-x.org/register/nodekey:...

    (Or, the link might be opened for you automatically on macOS or Windows.)

5. After loading the page, it will contain a command like ``headscale nodes register --user USERNAME --key nodekey:...``. Copy the entire line and send it to an admin (e.g. by Slack direct message). For reference, ``--user`` is the name of the private network, ``xnet`` in this case.

6. Once they confirm your machine has been registered, you will have network access to the MagAO-X computers over a virtual private network.

Making use of the VPN
---------------------

You will now be able to ssh to the name ``exao1`` or ``exao0`` without a fully-qualified domain (i.e. ``exao1.as.arizona.edu`` or ``exao1.lco.cl``). This name will remain stable even when the instrument is moved. You'll see that it is actually an automatically-generated fully-qualified domain under ``xnet.magao-x.org`` if you ping it::

    % ping exao1
    PING exao1.xnet.magao-x.org (100.64.0.4): 56 data bytes

The domains exao1.magao-x.org, exao2.magao-x.org, and exao3.magao-x.org point to the VPN (private) IP addresses. As long as you have the VPN running, you can use them to access lab resources.

SSH
~~~

The first time you use ``ssh`` to connect over the VPN, you will probably have to authorize the host key again by typing ``yes`` (and may get notified that the key is already known by other names). You may use the full name ``exao1.magao-x.org`` or just ``exao1`` to connect.

Jupyter
~~~~~~~

There is an auto-started Jupyter notebook server on each exaoN system on port 9999. You can use, e.g., http://exao1.magao-x.org:9999 to reach the notebook server. The notebook password prompt uses a different password than the operator workstation account, but you can get it from a colleague.

Note that if ``http`` doesn't work---perhaps because of an issue with exao1---many browsers will try upgrading to ``https``, which definitely won't work in this case. Once the issue is resolved, be sure to change the ``https`` back to ``http`` before trying again.

Web UI
~~~~~~

The MagAO-X web GUI lives at https://exao1.magao-x.org/ and is only accessible from the operator workstation and machines on the VPN.
