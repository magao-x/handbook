.. raw:: html

    <style> .red {color:red} </style>

.. role:: red


Installing MagAO-X on a Raspberry Pi
====================================

Image MicroSD card
~~~~~~~~~~~~~~~~~~~~~~~~
1. Go to raspberry pi imager on your computer.
2. Insert microSD card to your computer.
3. Select R-Pi device you are using (R-Pi 5), OS (Ubuntu Desktop 24.04.3 LTS for R-Pi 5), and storage (SD card). Do ctrl+shift+X to customize and make sure to enable ssh, and set the pis name and password. Then write.
4. After it successfully writes, add a blank text file titled "ssh" in "system-boot" drive. 

Connect the Raspberry Pi to WiFi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. If you are using Ubuntu OS, you will want to edit /etc/netplan/50-cloud-init-yaml
2. Add another section called "wifis:":

::

    network:
      version: 2
      ethernets:
        eth0:
          match:
            macaddress: ""
          addresses: 
            -  ???.???.??.?/?? # Set your desired static IP
          dhcp4: false  #true
          #dhcp6: true
          set-name: "eth0"
      wifis:
        wlan0:
          dhcp4: true
          access-points:
            "WIFI NAME HERE":
              password: "WIFI PASS HERE"

::

3. Once saved, run "sudo netplan apply" 
4. To confirm connection run "ip a show wlan0", and run "ping -c 3 8.8.8.8"
5. If this still does not work, you may need to go to settings to type username and password under the wifi you are trying to connect to.
6. Once connected to WiFi, you should be able to run "ssh username@wifi_ip_address" to connect to the Raspberry Pi. 

Install MagAO-X
~~~~~~~~~~~~~~~

1. Install git with "sudo apt install git".
2. To get ssh working properly, run "sudo apt update", then "sudo apt install openssh-server". 
3. To avoid "Failed to restart sshd.service: Unit sshd.service not found." error when provisioning, run "sudo systemctl status ssh" (which should have something that says disabled) then run "sudo systemctl enable ssh" (this should change that to enabled).
4. Clone MagAO-X repo with "git clone https://github.com/magao-x/MagAOX.git".
5. Change to the setup directory to run preprovisioning. run "cd ~/MagAOX/setup" and "./pre_provision.sh".
6. When prompted for Role, select "workstation".

    * For the accelerometer application, you may want to switch role permanently by editing "/etc/profile.d/magaox_role.sh" and adding "export MAGAOX_ROLE=ACC001"

7. Now you need to logout and login again. This means exit and run "reboot" in terminal. 
8. Open a new terminal, go to the setup directory and run "bash provision.sh". This should run for ~30 minutes. 

Troubleshooting Common Provsioning Errors
-----------------------------------------

1. Error: "curl: (56) Recv failure: Connection reset by peer"
    * You can run "bash -x provision.sh" to see exactly what script caused the error
    * Go to where the error occured "nano /home/user/MagAOX/setup/steps/install_cfitsio.sh"
    * In here, you will find a link to a .tar file "https://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.47.tar.gz" 
    * Download the .tar file and put it in "cd /opt/MagAOX/vendor"
    * Re-run "bash provision.sh" in "~/MagAOX/setup" 

Setting up SSH
~~~~~~~~~~~~~~

Follow the procedure in the handbook under 'Compute System -> Instrument computer setup guide -> Setup ssh

Adding a Static IP Address
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Ensure you have edited /etc/netplan/50-cloud-init-yaml to:

::

    eth0:
      addresses: 
      -  ???.???.??.?/?? # Set your desired static IP
      dhcp4: false

:: 

2. Also edit /etc/dhcpcd.conf to set your static ip address there to:

::

    interface eth0
    static ip_address=???.???.??.?/??
    static routers=???.???.??.?

::
