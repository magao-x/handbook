# Troubleshooting

### Missing GPUs on RTC

Sometimes the RTC comes up with only one GPU (missing the two on an expansion board). This is due to a weird interaction between the expansion board and the motherboard. To resolve:

1. If RTC is responding, bring it down cleanly (`shutdown -h now`)
1. Power down RTC at PDU0 (e.g. with `pwrGUI`)
2. Wait 10 seconds before attempting to power back on
3. Once it boots (which can take several minutes, with apparent false-starts), run `nvidia-smi` three times. It'll likely die on the second (and lock up).
4. Reset using the switch mounted on the RTC motherboard (or the to-be-installed remote reset switch)
5. Repeatedly run `nvidia-smi` (e.g. `watch nvidia-smi`) to verify it's back up and stable

### OCAM connectivity / bad data

OCAM connects over two CameraLink connections. CameraLink #1 carries serial communication with the detector, so if you're able to command the camera but your data appear bad in `rtimv camwfs`, the culprit is likely the CameraLink #2 cable. Reseat, on ICC do `magaox restart camwfs`, and restart `rtimv`.

### Alpao DM not responding

Make sure it has been initialized. There is an `initialize_alpao` systemd unit that runs at boot and initializes the interface card. Successful execution looks like this in `systemctl status initialize_alpao` output:

```
$ systemctl status initialize_alpao
● initialize_alpao.service - Initialize Alpao interface card
   Loaded: loaded (/opt/MagAOX/config/initialize_alpao.service; enabled; vendor preset: disabled)
   Active: active (exited) since Sun 2019-09-29 11:18:34 MST; 20min ago
  Process: 4449 ExecStart=/opt/MagAOX/config/initialize_alpao.sh (code=exited, status=0/SUCCESS)
 Main PID: 4449 (code=exited, status=0/SUCCESS)
   CGroup: /system.slice/initialize_alpao.service

Sep 29 11:18:34 exao3.as.arizona.edu systemd[1]: Started Initialize Alpao interface card.
Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: ====================================================================
Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: Ref.ID | Model                          | RSW1 |  Type | Device No.
Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: --------------------------------------------------------------------
Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: 1 | PEX-292144                     |    0 |    DI |    17
Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: --------------------------------------------------------------------
Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: 2 | PEX-292144                     |    0 |    DO |    18
Sep 29 11:18:35 exao3.as.arizona.edu initialize_alpao.sh[4449]: ====================================================================
```

The script is saved at `/opt/MagAOX/config/initialize_alpao.sh`, if you want to see what it's doing. Note that executing it again will appear to fail with a message about not finding cards to initialize if the cards have been previously initialized.

### DM Latency and Communication Troubleshooting

There are various ways that the shared memory interprocess communication between the deformable mirrors, loop control(s), and the hardwre control processes can stop functioning properly.

#### Examples with known fixes:

* Inability to set or zero flat or test from the dm control gui

    * This likely points to a bad semaphore.  Simply release DM, then re-initialize, and it usually clears.  If not, go to more general steps below.

    
* Excessive latency, occurs especially for ALPAOs

    * This usually requires a power cycle of the driver itself.  Release the DM, then use the power control GUI to turn off, then on the DM driver.

* Skipped commands

    * This is possibly caused by collisions on a semaphore, meaning more than one process is monitoring a given semaphore.  This can be diagnosed with `streamCTRL`. If this is not the case, a full software shutdown (both cacao and magao-x) and clearing the /milk/shm and /dev/shm directories (rm *), then restarting, should clear the problem. See step 5 below.

#### General Troubleshooting

General troubleshooting steps, in order of severity (try the lower ones first if you don't have a clear idea what the problem is):
1) release, then initialize from the dmCtrl GUI
2) release, then restart the DM controller software
    e.g. for the woofer:
    ```
    [xsup@exao2 ~] $ tmux a -t dmwoofer
     ctrl-c
    [xsup@exao2 ~] $ alpaoCtrl -n dmwoofer
    ```


3) restart the dmcomb process:
    * first stop the DM controller (see above)
    * restart dmcomb using fpsCTRL (to be documented)
    * restart the DM controller (see above)
    * this may cause problems in some other processes due to shmim recreation.

4) Power cycle the DM
    * release from the dmCtrl GUI
    * turn off the power with the pwrCtrl GUI, then turn it back on
    * if it doesn't happen automatically, initialize the DM from the GUI when it has power
    * if this does not fix the problem, try steps 1-3 again.

5) Full Software Restart 
    * Place all hardware controlled from this computer in a safe condition
         * rest modttm and ttmpupil
         * start camera warmup (in case you can't get software back up)
         * release all DMs controlled from this computer
    * Shutdown all software with:
      ```
       [xsup@exao2 ~] tmux kill-server
      ```
    * Clear all shared memory:
      ```
       [xsup@exao2 ~] cd /milk/shm 
       [xsup@exao2 ~] sudo rm *
       [xsup@exao2 ~] cd /dev/shm 
       [xsup@exao2 ~] sudo rm *
      ```
    * Now restart software and restore hardware to operating condition

6) Reboot
    * This is a last resort.  This may be necessary if a problem has developed in the device driver for instance.
    * Follow procedure for computer reboot.  Ensure all hardware is in a safe condition, including powered-off if needed, before rebooting.

    
    
### Troubleshooting a MagAO-X app that won't start

The typical MagAO-X app is started by `magaox startup` based on a line in a config file in `/opt/MagAOX/config/proclist_$MAGAOX_ROLE.txt`. This proclist determines which application to start and which config file from `/opt/MagAOX/config` should be supplied as the `-n` option (see [Standard options](#standard-options)). It also uses `sudo` to run the process as user `xsup`, regardless of which user called `magaox startup`.

Many, if not all, MagAO-X apps are intended to run "forever" (i.e until shutdown). Obviously, if the process exits early, that's cause for concern. To interrogate the list of running processes, use `magaox status`. To attempt a restart, you can attach to the `tmux` session that's the parent of the process in question with `magaox inspect PROCNAME` (where `PROCNAME` is the name of the failed process).

For example, if `trippLitePDU` is started by `magaox startup` with config specified by `-n pdu0` and there's a syntax error in `/opt/MagAOX/config/pdu0.conf` preventing startup, you can attach to the tmux session with

```
yourlogin$ magaox inspect pdu0
```

The errors before exit, if any, will be in the log. The last few lines of the log are shown in `magaox status` output, or you can do `logdump -f pdu0`.

The command that started the app will be of the form `/opt/MagAOX/bin/$appName -n $configName`. You can use the up-arrow key in the tmux session to retrieve it from the shell history and try to relaunch once you've corrected whatever error was preventing startup.

### EDT Framegrabber Problems (camwfs and camlowfs)

The EDT PCIe framegrabber occassionally stops responding.  The main symptom of this is no data from `camwfs`, and no response on the serial over camera link.  This has not yet been observed on `camlowfs` (which does not use serial over C.L.).

If `camwfs` (or any EDT camera) stops responding on serial, first shutdown the controlling application.

```
$ magaox inspect camwfs
<Ctrl-C>
```

then do these steps as root:

```
$ modprobe -r edt
$ cd /opt/EDTpdv
$ ./edt_load
```

This will reset the kernel module and restore operation.  Now restart the controlling application by returning to the tmux session, up-arrow to find the command, and press enter.

### killing indi zombies

If the `indiserver` crashes uncleanly (itself a subprocess of `xindiserver`), the associated `xindidriver` processes may become orphans.  This will prevent `xindiserver` from starting gain until these processes have been killed.  The following shell command will kill them:
```
$ kill $(ps -elf | awk '{if ($5 == 1){print $4" "$5" "$15}}' | grep MagAOX/drivers | awk '{print $1}')
```
To check if any remain use
```
$ ps -elf | awk '{if ($5 == 1){print $4" "$5" "$15}}' | grep MagAOX/drivers
```

### Difficulties with NVIDIA proprietary drivers

1. When installing, ensure you have `systemctl set-default multi-user.target` and a display is connected **only** to the VGA header provided by the motherboard
2. If NVIDIA graphical output did work, and now doesn't: Your kernel may have been updated, requiring a rebuild of the NVIDIA driver. Having `dkms` installed *should* prevent needing to do this, but an uninstall and reinstall over SSH will also remedy it.
2. Runfile installs can be uninstalled with `/usr/local/cuda/bin/cuda-uninstaller`

