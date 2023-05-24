Tailscale for secure connection tunnels
=======================================

Tailscale automates the setup of secure tunnels between machines in a network. Using it, you can fool your computer into thinking it's on the instrument network, for instance.

Authentication and user access control are managed through GitHub. Your first order of business should be to obtain a GitHub account and get it added to the https://github.com/magao-x organization.

1. Download Tailscale: https://tailscale.com/download/

2. Install following the instructions for your operating system

3. When prompted, choose "Sign in with GitHub". You may be prompted for your GitHub username / password / 2FA code. The default options are fine, so click "allow".

4. After you're authenticated, you will be asked to choose a "tailnet". You want the "magao-x" tailnet.

5. Connect to our lab/instrument machines confidently and securely through the wonders of encryption and overlay networking.

Making use of Tailscale
-----------------------

You will now be able to ssh to the name ``exao1`` or ``exao0`` without a fully-qualified domain (i.e. ``exao1.as.arizona.edu`` or ``exao1.lco.cl``). This name will remain stable even when the instrument is moved. You'll see that it is actually an automatically-generated fully-qualified domain under ``ts.net`` if you ping it::

    % ping exao1
    PING exao1.tailf46fc.ts.net (100.80.124.82): 56 data bytes

**TODO** Web interface access over tailnet