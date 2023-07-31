Tailscale for secure connection tunnels
=======================================

Tailscale automates the setup of secure tunnels between machines in a network. Using it, you can fool your computer into thinking it's on the instrument network, for instance.

Authentication and user access control are managed through GitHub. Your first order of business should be to obtain a GitHub account and get it added to the https://github.com/magao-x organization.

1. Download Tailscale: https://tailscale.com/download/

2. Install following the instructions for your operating system

3. When prompted, choose "Sign in with GitHub". You may be prompted for your GitHub username / password / 2FA code. The default options are fine, so click "allow".

4. After you're authenticated, you will be asked to choose a "tailnet". You want the "magao-x" tailnet.

5. The first time you connect, you will need to be approved by an admin. Send a Slack message in ``#lab-computers`` or directly to an admin so they know you need to be approved.

6. Connect to our lab/instrument machines confidently and securely through the wonders of encryption and overlay networking.

Making use of Tailscale
-----------------------

You will now be able to ssh to the name ``exao1`` or ``exao0`` without a fully-qualified domain (i.e. ``exao1.as.arizona.edu`` or ``exao1.lco.cl``). This name will remain stable even when the instrument is moved. You'll see that it is actually an automatically-generated fully-qualified domain under ``ts.net`` if you ping it::

    % ping exao1
    PING exao1.tailf46fc.ts.net (100.80.124.82): 56 data bytes

The domains exao1.magao-x.org, exao2.magao-x.org, and exao3.magao-x.org point to the tailnet (private) IP addresses. As long as Tailscale is running, you can use them to access lab resources.

SSH
~~~

Deploying Tailscale for our lab was mainly to achieve the joy of never having to worry that your free internet connection in the Santiago airport blocks SSH. Regardless of where and how you and MagAO-X are connected to the Internet, so long as you **are** connected to the Internet, Tailscale will find a path for you.

Jupyter
~~~~~~~

There is an auto-started Jupyter notebook server on each exaoN system on port 9999. You can use, e.g., http://exao1.magao-x.org:9999 to reach the notebook server. The notebook password prompt uses a different password than the operator workstation account, but you can get it from a colleague.

Note that if ``http`` doesn't work---perhaps because of an issue with exao1---many browsers will try upgrading to ``https``, which definitely won't work in this case. Once the issue is resolved, be sure to change the ``https`` back to ``http`` before trying again.

Web UI
~~~~~~

The MagAO-X web GUI lives at https://exao1.magao-x.org/ and is only accessible from the operator workstation and machines on the tailnet.