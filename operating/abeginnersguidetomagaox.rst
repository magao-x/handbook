.. raw:: html

    <style> .red {color:red} </style>

.. role:: red



.. raw:: html

    <style> .blue {color:blue} </style>

.. role:: blue


.. raw:: html

    <style> .green {color:green} </style>

.. role:: green


.. raw:: html

    <style> .orange {color:orange} </style>

.. role:: orange


**********************************
A Beginner's Guide to Using MagAOX
**********************************

A Bit of Book-Keeping
=====================

To ssh on to rtc and icc from our local machine rather than the VM, we need to set up a proxy jump through aoc:

.. code-block:: bash

    cd ~/.ssh

make or edit a file named config to include:

Host aoc
  HostName exao1.magao-x.org
Host rtc
  HostName rtc
  ProxyJump aoc
Host icc
  HostName icc
  ProxyJump aoc
Host *
  User <your-username>

With this set up, you should now be able to jump to rtc and icc just by typing:
``ssh rtc`` or ``ssh icc`` in a terminal without logging in to the VM. This is especially useful for using scp to copy files to local.


Getting Started
===============

First, open a terminal window (henceforth terminal #1), navigate to the VM, start it up, and start the tunnels:

.. code-block:: bash

   cd dir/to/MagAOX/
   vagrant up       # if not done already
   vagrant ssh
   xctrl startup

Now, open up Terminator (or any terminal emmulator like Konsole in kde), and split in half such that it has an upper window and a lower window.

Log in to the VM in both windows and then:

top window:

.. code-block:: bash

   cursesINDI


bottom window:

.. code-block:: bash

   tail -f /tmp/cursesINDI_logs.txt

The cursesINDI_logs.txt file will print updates to let you know that the connection to the INDI server, and thus to the hardware, is active and working the way it should be.

:blue:`Note`:
When using cursesINDI, you can type the name of the device you want to scroll to it faster. For target properties that are toggle-able, press "t" for toggle, then "y" to confirm.

| :green:`================================================================================`
| :green:`In case this goes wrong`:


If cursesINDI or getINDI fails with a connection error, we might need to run the system startups as the INDI server is probably down:

Check rtc:

.. code-block:: bash

    ssh rtc
    su xsup
    cd
    bash ./cacao_startup_woofer.sh
    bash ./cacao_startup_tweeter.sh
    fpsCTRL     #to check if DMCOMB has started
    xctrl startup
    xctrl status        #to check that processes have started
    
If everything is green, logout of the ssh

Now check icc:

.. code-block:: bash    

    ssh icc
    su xsup
    cd
    bash ./cacao_startup_dmncpc.sh
    xctrl startup
    xctrl status        #to check that processes have started
    fpsCTRL         #to check if DMCOMB has started
    
If everything looks good, logout of the ssh

Now check aoc:

.. code-block:: bash

    ssh aoc
    su xsup
    cd
    xctrl startup
    xctrl status


All processes should be green, but if isAOC is red:
``xctrl startup``

If this doesn't fix the process:
``xctrl restart isAOC``


Now we need to check isICC and isRTC to make sure the INDI servers are connected

.. code-block:: bash

    ssh icc
    su xsup
    getINDI

If there is no response, ie:

.. code-block:: bash

    [xsup@exao3] $ getINDI 
    No *.*.* from localhost:7624

Do:

.. code-block:: bash

    xctrl restart isICC
    getINDI

If still no response:

.. code-block:: bash

    xctrl shutdown
    xctrl startup
    xctrl status
    getINDI

Now repeat the same process on rtc until getINDI gives a response. With this done, everything should be good to go to continue on as normal

:green:`================================================================================`


In terminal #1, type:

.. code-block:: bash

   getINDI

If a bunch of information is printed, it means you are connected to the INDI server.



Now power up the Power GUI in terminal #1:

.. code-block:: bash

   pwrGUI &

A window with a bunch of sliders will pop open.


:red:`Important`:
(the following sliders should all be on when pwrGUI comes up, and left on when shutting down!)
**NEVER TURN OFF**:

| :orange:`pdu0`:
| compicc
| comprtc
| dcpwr
| swinst

| :orange:`pdu3`:
| blower
| fan1
| fan2
| instcool


Set up the milkzmqClient with everything we (may) need, again in terminal #1:

.. code-block:: bash

   milkzmqClient -p 9000 localhost camwfs camwfs_dark camtip camtip_dark camlowfs camlowfs_dark camsci1 camsci1_dark camsci2 camsci2_dark dm00disp00 dm00disp dm00dispST  dm01disp00 dm01disp dm01dispST dm02disp00 dm02disp dm02dispST &


Now the real time image viewers can be turned on. Let's start with camtip, the camera viewing light picked off of the Pyramid WFS tip.

1. now can power on camtip using the slider in :orange:`pwrGUI:usbdu0`

2. Turn on the real time viewer for camtip by typing the command:

.. code-block:: bash

    rtimv -c rtimv_camtip.conf &

:green:`================================================================================`
:green:`Note for if camtip has an error`:

if camtip-sw has an error appear in the INDI log that lead it to shutdown, the process needs to be restarted:

.. code-block:: bash

    ssh icc
    su xsup
    xctrl status        # to verify the process is dead
    xctrl restart camtip-sw

:green:`================================================================================`


The DMs
=======

:blue:`Note`:
dm00 is the woofer, dm01 is the tweeter, and dm02 is the ncpc


The safety check for turning on the DMs is the tweeter humidity. The easiest way to check the humidity is to open the real time viewers for the DMs, and check the RH value printed for dm01:

.. code-block:: bash 

    rtimv -c rtimv_dm00disp.conf &
    rtimv -c rtimv_dm01disp.conf &
    rtimv -c rtimv_dm02disp.conf &

Looking at the viewer for dm01, the upper right corner should have "RH: #.#%" printed. This is a readout of rhtweeter.humidity.current in cursesINDI.

This means it you can also use:

.. code-block:: bash

    getINDI rhtweeter.*.* 

Read the number next to humidity.current

:red:`Important`: 
Anything higher than **18%** for the current humidity, **do NOT** power the DMs on, and post about it on Slack.

If humidity.current < 18, it is safe to turn on the 3 DMs in :orange:`pwrGUI:pdu1`, and post in Slack that MagAOX is in use.

| If the real time viewer for dm01 does not have the humidity printed, the cameraGUI isn't building:
| 1. post in Slack software channel, then when notified of fix:
| 2. ``cd /opt/MagAOX/source/MagAOX``
| 3. ``git pull``
| 4. ``make guis_install``
| This should fix the problem.


Although we are checking the humidity of dm01, the tweeter, to ensure the safety powering it up, we also start the other two DMs first in part to get the ALPAO DMs over their creep.

.. code-block:: bash

    dmCtrlGUI dmwoofer &
    dmCtrlGUI dmtweeter &
    dmCtrlGUI dmncpc &


Once all 3 GUIs are open, press the "set flat" button on all 3 GUIs



| :blue:`Note`:
| "[" on the keyboard to square rtimv viewers as big as possible (scaled to the data)
| "]" makes square as small as possible




Now the Tip/Tilt mirrors
========================

Turn on the Pupil Alignment GUI:

.. code-block:: bash

    pupilGuideGUI &

now in :orange:`pwrGUI:pdu1`, turn on ttmmod, ttmpupil, and in :orange:`pwrGUI:pdu2`, turn on stagecamlens.

:blue:`Note`: the ttmmod slider automatically goes halfway and stays for a bit, and then all the way to the right after some time for safety


Now in the Pupil Alignment GUI, press the "set" button for the Modulation & Centering and the Pupil Steering sections. The Camera Lens section largely takes care of itself.


Now power up camwfs using the :orange:`pwrGUI:pdu1` camwfs and run:

.. code-block:: bash

    rtimv -c rtimv_camwfs.conf &


open the camera GUI for camwfs:

.. code-block:: bash

    cameraGUI camwfs &

:green:`================================================================================`
:green:`Note for if this doesn't go right`:

If the rtimv viewer for camwfs appears all white, and the cameraGUI for it is blank, the process for camwfs has failed. To check this, open a terminal and:

.. code-block:: bash

    ssh rtc
    su xsup
    tmux a -t camwfs

This should give a log. If it has an error in it that has stopped the funtion (e.g. "no serial response"), you need to restart the driver. This is most easily done by doing **ctrl-c** to stop the process, and then the up-arrow key to get the correct command. Press enter. The rtimv image should look right, and the cameraGUI should no longer be blank. Detach the tmux shell with **ctrl-b + d**, and then you can close the connection to rtc and the terminal.

:green:`================================================================================`


In the camwfs cameraGUI, the Mode should be bin2 (use the "..." button and pulldown bar to select bin2).
Cool down **camwfs** by editing the **Detector Temp** to **-40**
Set **camwfs** FPS to **200**


Now turn on shwfs in :orange:`pwrGUI:dcdu1` (shwfs stands for wfs shutter).
"(off)" should disapper at the camwfs cameraGUI shutter.

:blue:`Note`: The shutter is open with the slider to the left, closed with the slider to the right.


Now repeat the process for the science cameras, camsci1 and camsci2:

Power up camsci1 and camsci2 using the pwrGUI sliders for them.

.. code-block:: bash

    rtimv -c rtimv_camsci1.conf &
    rtimv -c rtimv_camsci2.conf &


open the camera GUI for camwfs:

.. code-block:: bash

    cameraGUI camsci1 &
    cameraGUI camsci2 &


Open the shutters for both cameras by sliding the shutter slider in their respective cameraGUI window.



Finally, turn source on in :orange:`pwrGUI:pdu0` using source slider.


:blue:`Note`: At this point, the DMs are flat, the TT mirros are set, the shutter is open:
check if there is light in camtip and camwfs


Filter Wheels, Final Power ups, and Final Checks
================================================


:red:`IMPORTANT`: The proper order for powering on the filter wheels fwscind and fwtelsim is to turn on the DC power first in pwrGUI before the USB power:

1. Slide the sliders for fwscind fwtelsim in :orange:`pwrGUI:dcdu1`.

2. Now all sliders in :orange:`dcdu0` and :orange:`dcdu1` categories.

3. Now can turn on everything in :orange:`usbdu0` except for camacq.

:red:`REMINDER`: fwscind and fwtelsim in :orusbdu0 must be done after the dcdu1 ones!

4. Turn on sliders in :orange:`usbdu1` except for flipacq and flipeye

5. now in :orange:`pdu3`, turn on fliptip and tableair

6. now in :orange:`pdu2`, turn everything on

:blue:`Note`: stagerot and stagezaber take a couple minutes to home; the INDI log in the split window terminal bottom will print when they are ready. Wait for that message.

| :blue:`Note`: Now in pwrGUI, everything is on except:
| evncontweeter and flipacq (in :orange:`pdu3`)
| camacq and flipacq (in :orange:`usbdu1`)
| flipeye


Now perform the final checks:

1. In cursesINDI (the top window of the split window terminal), go to fwtelsim
we want to be in ND1, so go to ND1 filterName and toggle it on.

2. Double check that fliptip is "in" (also in cursesINDI)

3. Check that flipwfsf is also "in" (also in cursesINDI)

4. Make sure that stagepickoff is "in" (also in cursesINDI)


Now Align the System
====================


**Follow steps in the Handbook for:**
:doc:`System Pupil Alignment <./alignment>`



:green:`Pointers for going through this procedure`:

1. Make sure to check the list at the top of the linked page vs. your curseINDI. It is **important** for getting light on camtip, camlowfs, and camwfs, at the correct light level.

2. If you need to open the camlowfs shutter (e.g. the rtimv viewer for camlowfs has "SHUT" written in it):

.. code-block:: bash

    cameraGUI camlowfs &
    rtimv -c rtimv_camlowfs.conf &

Just toggle the shutter slider as you did on camwfs.

3. In the real time viewer for camlowfs, press z to get the yellow box. Move it over the pupil image to set viewer scales appropriately.

4. set Rtest_03um on dmtweeter:
using the pulldown at the bottom of the dmtweeter GUI, select 'Rtest_0p3um', then click the "set test" button.

5. Use the Pupil Steering section of the Pupil Alignment GUI to center the pupil using the diagonal arrows at the bottom middle. Make the the edge actuators evenly illuminated. If needed, you can switch to "ND2" on fwtelsim (to reduce saturation).

6. Press the "zero test" button on the dmtweeter control GUI when done.


Now align the WFS
=================

You need camwfs and the Camera Lens section in the Pupil Alignment GUI to do this

1. In the camwfs viewer, press "t" to get the target quadrants to show

2. Using the **Camera Lens** section in Pupil Alignment GUI, use the arrows at the bottom to move pupils to roughly be even in the 4 quadrants in the real time viewer.

3. press "t" again to turn off the quadrant targets.


Now go to **Modulation & Centering**:

1. click the box for delta from mean

2. Use the arrows at the bottom to make the light in each pupil close to equal. you want to move from the largest positive toward the negative (mainly will be on the diagonal motions)

3. When they are pretty even, modulate:
    - type 1000 in Frequency taret and hit enter
    - type 3 in Radius and hit enter
    - now click the modulate button (watch camtip real time viewer to see it working)

4. Go back to camwfs viewer and press "r", then "P" (shift+p) to fit circles to the pupils
    - if the Red circles overlap or look funky, you aren't getting enough signal
    - go to the camera gui for camwfs, and edit the FPS to be slower (should be at 200Hz)

5. Go back to **Camera Lens** in the Pupil Alignment GUI
    - try to match the red circles to the green ones
    - click the delta from set pt box, and look at the avg. try to get them to be ~0.1 or less
    - do "P" (shift+p) again in the viewer to turn off the fitting lines

:blue:`The system is now aligned!`



Now for Cacao-ing
=================

Open another terminal (henceforth terminal #2):

.. code-block:: bash

    ssh rtc
    su xsup
    cd /opt/MagAOX/cacao/tweeter
    ./aolconf

:blue:`Note`: If you close this loop on accident, start again with ``./aolconf -n``. This doesn't load the shared memory stuff, so it will connect faster. This is likely not dangerous to do, but only if you have run ``./aolconf`` already.


Now, open another terminal (terminal #3) and ssh to rtc:

.. code-block:: bash

    su xsup
    cd
    procCTRL

Now change font size (by zooming out or otherwise, depending on your default terminal) until all the text fits.
Press X (shift+x) to quit, and then restart the program so it can all be seen (will help detect crashes in CACAO, and let you know when processes have completed)

.. code-block:: bash

    procCTRL


:blue:`Note`: To reset procCTRL, press "R" (shift+r) on the keyboard

1. Get the dm01disp and camwfs real time viewers up.

In terminal #2, the left and right arrow keys move between "select" and "exit" on the bottom; up and down arrow keys move in the menu.

2. Scroll down (via down arrow presses) to **Configure/link AO loop**.

3. Go to the **camwfs cameraGUI** and make sure it is running at 1kHz, as it is probably not due to the alignment steps (click in Frame Rate box, type 1000, hit enter, box will be blue when it reaches it. Then restretch the camwfs viewer with "r")

:blue:`Note`: The 1000 Hz here is actually whatever speed the loop is being run at. It must be the same as the **Modulation & Centering** modulation frequency! If you change the loop frequency (say to 2kHz), you must change the modulation frequncy. To do that, go to the **Pupil Alignment GUI**, **Modulation & Centering**, enter the desired frequency, 2000, in the Frequency target box, hit enter, 3 in the Radius target box, hit enter, then press the modulate button.

4. Return to the Cacao GUI, scroll down to **Acquire WFS Dark** and hit enter. This will take dark frames. "D" (shift+D) in the viewer for cameras will show with/out dark subtraction.

5. Scroll down in Cacao now to **Measure Hardware Latency** and hit enter. Hit enter again on 100. It will run. procCTRL will list "lat aol1_dmC aol1_wfsim", when complete, the message will say "Loop exit <time_stamp>".
Scroll up in the GUI to read **Hardware Latency** and hope to see < 2 frames.
If it's near 2 frames or larger, message the PI / Slack.

6. Go back to the Pupil Alignment GUI and check the centering using **Modulation & Centering** only (no need for other two again!)

7. Adjust to try to get the median fluxes deltas close to 0 using the arrows and small movements

:green:`Protip`: Have No. Avgs set to 200 still


Getting a Response Matrix:
==========================

To begin, set up rtc in the mode to have the lowest latency:

.. code-block:: bash

    ssh rtc
    cat /proc/cpuinfo | grep MHz | wc -l

If this is 72:

.. code-block:: bash

    sudo /opt/MagAOX/source/MagAOX/script/rtc_cpuset
    sudo /opt/MagAOX/source/MagAOX/script/rtc_procset
    cat /proc/cpuinfo | grep MHz | wc -l


| It should now be 54. Now we are ready to set rtc into lowest latency mode:
| go to cursesINDI
| search sysMonRTC
| go to sysMonRTC.set_latency and toggle it on


1. Now, in the Cacao GUI terminal (terminal #2), scroll to **START AUTO SYSTEM CALIBRATION (new modes)**

2. Press enter
    - procCTRL will say loop exit on far right for two processes (dmpokeC2b both times, one for hadamard modes and one for low order zernike modes) with STOPPED as the status. If it crashed, it will say so with a red box.

3. Scroll up in Cacao to the line with **AUTOMATIC SYSTEM CALIBRATION** and hit enter to refresh the GUI

To save the Response Matrix:

1. Open a new terminal:

.. code-block:: bash

    ssh rtc
    su xsup
    cd /opt/MagAOX/cacao/tweeter
    ls -l zrespM.fits

2. If it's there we can copy it to local. Open a terminal without any ssh'ing:
``scp rtc:/opt/MagAOX/cacao/tweeter/zrespM.fits /home/.../``

3. It is also useful (and pretty much necessary) to copy some other files from this location as well in order to do reconstructions. These include:
    - dmmask.fits
    - wfsmask.fits
    - wfsref0.fits
    - wfsdark/wfsdark_<date>.fits 


To do stuff in Python
=====================

1. open a terminal:
2. ``ssh rtc -L 9999:localhost:9999``
3. navigate to localhost:9999 in a browser

Useful Python stuff to know to build around:

.. code-block:: python

    from magpyx.utils import ImageStream

    # getting camera images
    cam = ImageStream('camwfs')
    image = cam.grab_latest() # simplest way to grab an image
    cam.close() # when you're done

    # commanding DMs
    dm = ImageStream('dm01disp04')
    cmd = np.zeros_like(dm.buffer)
    cmd[20,23] = 0.1 # a poke
    dm.write(cmd) # send the command
    dm.close() # when finished

    # Magic recipe for matching how Cacao does its reconstructions
    # subtract the wfsdark from the measurement
    # Multiply by wfsmask
    # normalize by the sum [ e.g. var /= var.sum() ]
    # Subtract wfsref0


Safe Shutdown!
==============

:red:`IMPORTANT`: First is warm up the 4 EMCCDs! These are camwfs, camlowfs, camsci1, and camsci2 (the camsci's cool automatically, even if you don't use them)

| 1. Edit in their camera GUI temp box, or through cursesINDI:
| In cursesINDI, go to the device and edit the <device>.temp_ccd target to 20.
| For example:
| type "camsci1" in cursesINDI, go to target for temp_ccd, press "e", type 20, then press enter, then press "y"

2. Close the shutter on camwfs in its cameraGUI (slide slider to the right)

3. Close the shutter on camlowfs in its cameraGUI

4. Close the shutter on camsci1 in its cameraGUI

5. Close the shutter on camsci2 in its cameraGUI

| 5. **For the 3 DMs and 2 Tip/Tilt mirrors:**
| For DMs, press the "zero flat" button and then "release" button
| It is now safe to slide the DMs off in :orange:`pwrGUI` (dmtweeter, dmwoofer, and dmncpc)

| 6. **For ttmmod and ttmpupil:**
| go to the Pupil Alignment GUI and hit the "set" button under **Modulation & Centering**
| once it is in SET state, it is safe to hit "rest" for **Modulation & Centering** and **Pupil Steering**
| Both will have state set to RIP
| It is now safe to slide off ttmmod and ttmpupil in :orange:`pwrGUI`


:red:`IMPORTANT!` You must turn off fwtelsim and fwscind in :orange:`usbdu0`  next (must be done before the dc power ones!!)

| 7. Now everything in pwrGUI except the following can be off:
| :orange:`cameras`:
| camwfs
| camlowfs
| camsci1
| camsci2

| :orange:`pdu0`:
| compicc
| comprtc
| dcpwr
| swinst

| :orange:`pdu3`:
| blower
| fan1
| fan2
| instcool


If the temperature is 20C, the cameras can be slid off. 19C is okay, <19C is not. Check cursesINDI or camera GUIs for the current temps. 


:red:`IMPORTANT`: Before being done, double check that "instcool" is still powered on in pwrGUI (this is important as it keeps the CPUs and such from overheating)

Now close all the windows and post in Slack that MagAOX is off.

:green:`================================================================================`
:green:`Note if things go wrong:`


If sliders in pwrGUI stop sliding off, it is possible that fwtelsim in usbdu0 has rebooted ICC. If this happens, we need to go ensure that the processes are all running, and that the INDI server is connected.

open a terminal:

.. code-block:: bash

    ssh icc
    su xsup
    xctrl status # everything should be dead if ICC rebooted
    xctrl startup
    xctrl status # everything should be green again
    getINDI


| getINDI probably still won't connect. Symptoms of this include:
| 1. ``getINDI`` on ICC returns nothing
| 2. Inspecting the log of one of the processes (e.g. logdump -f camlowfs) will show "waiting for power state"
| 3. pwrGUI from the VM or AOC will only have pdu0-3 (and nothing else)

In order to reconnect, run

.. code-block:: bash

    xctrl restart isICC


Once this completes, cursesINDI and the INDI log should reconnect, and running ``getINDI`` on ICC should return stuff.
You should now notice all of the options back in pwrGUI. Continue to shut off where you left off (likely at fwtelsim or fwscind)
:green:`================================================================================`


