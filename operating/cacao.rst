CACAO Setup
===================================

MagAO-X uses the "Compute and Control for Adaptive Optics" software package.
This document describes how to start up CACAO on MagAO-X and use it for normal operations.  It assumes that
software installation and configuration is already complete.

Terminal Interface Setup
-------------------------

1. The basic interface to CACAO is through the terminal.  We normally set up a three-panel terminal.  Open a terminal on AOC,
   and first "split left/right".  Then in the left half, "split up/down".

2. In each of the resultant terminals, ssh to rtc (or to icc) as xsup.

3. Next:

   ::

     [xsup@rtc ~]$ cd /opt/MagAOX/cacao/tweeter-vispyr/tweeter-vispyer-rootdir


   For ICC the path is `/opt/MagAOX/cacao/ncpc/ncpc-rootdir`.  This should be done in the lower left and right hand
   terminals.  It is not required in the upper left.

4. Now that you are in the `rootdir`:

   - in the upper left panel, run the command `milk-procCTRL`
   - in the right-hand panel, run the command `cacao-fpsctrl-TUI`

   The following image shows the state just before the above commands are run

   .. image:: figures/cacao_term_setup.png

   *CACAO terminal preparation*

    The following image shows the state after the above commands are run

   .. image:: figures/cacao_term_inop.png

   *CACAO terminals in operation*

   In the upper left panel where you have run `milk-procCTRL`, you will want to change the font size to fit it all in.  You
   can do this by pressing `ctrl` and using the scroll wheel on the mouse.  `ctrl +` and `ctrl -` also work.

.. note::
     The above steps are ripe for scripting.  Volunteers needed.

Graphical User Interface
-------------------------

To start the GUI for loop control for the high-order loop on AOC:

  ::

    [xsup@aoc ~]$ loopCtrlGUI ho

  .. image:: figures/holoop.png

And for the LOWFS loop:

  ::

    [xsup@aoc ~]$ loopCtrlGUI lo

  .. image:: figures/loloop.png

High-order Loop
-----------------

.. note::
     Almost all CACAO CLI commands must be executed in the `rootdir` of the relevant loop.  On RTC this is
     `/opt/MagAOX/cacao/tweeter-vispyr/tweeter-vispyer-rootdir`, which is in the lower-left terminal after the above setup.

1. First decide which calibration you wish to load.  On RTC this is currently almost certainly `default`.

2. To see a list of calibration available, execute

   ::

      [xsup@rtc tweeter-vispyr-rootdir]$ ls ../tweeter-vispyr-calibs.

.. warning::
     Ensure the loop is open before loading a new calibration, or re-loading the current calibration.

3. To load a calibration, in the lower left terminal run

   ::

    [xsup@rtc tweeter-vispyr-rootdir]$ cacao-calib-apply XXXX

   where `XXXX` is the name of the calibration. You do not include the full path.  For most things, you probably want
   `default`.  So:

   ::

    [xsup@rtc tweeter-vispyr-rootdir]$ cacao-calib-apply default


Low-order T/T Loop
-------------------

.. note::
     Almost all CACAO CLI commands must be executed in the `rootdir` of the relevant loop.  On ICC this is
     `/opt/MagAOX/cacao/ncpc/ncpc-rootdir`, which is in the lower-left terminal after the above setup.

The low-order T/T loop uses light rejected by the coronagraph to control residual vibrations.  The "wavefront sensor"
for this mode is a program running a center-of-light algorithm on either `camflowfs` or `camllowfs`, or the average image
from either camera.

1. First, setup the desired camera.  The ROI size does not really matter, but typically we use 32x32 to make the
   centroiding algorithm efficient.

    - You can run the LOWFS cameras extremely fast.  This can be advantageous to control saturation since roughly 100% of the
      star light is rejected by the coronagraph.  However, you may want to run the loop slower.  So you can use the
      averager for the camera to effectively reduce the exposure time.

.. warning::
     Ensure the loop is open before changing cameras, loading a new calibration, or re-loading the current calibration.

2. Now to setup CACAO to use the desired camera, run the command

    ::

      [xsup@icc ncpc-rootdir]$ lowfs_switch camflowfs_fit

   In addition to `camflowfs_fit` you can select `camflowfs_avg_fit`, `camllowfs_fit`, or `camllowfs_avg_fit`.

3. Now load the desired calibration.  Note that this only depends on the camera, not whether you are using the averager
   for that camera.  For `camflowfs` run:

    ::

      [xsup@icc ncpc-rootdir]$ cacao-calib-apply flowfsTT

   and for `camllowfs` run:

    ::

      [xsup@icc ncpc-rootdir]$ cacao-calib-apply llowfsTT

   Now the following processes should be running in `cacao-fpsctrl-TUI` (the right hand CACAO terminal).
   These should all be green:

     - wfs2cmodeval-2
     - mvalC2dm-2
     - mfilt-2
     - DMch2disp-02
     - acquWFS-2

   It is ok if other processes are green.

4. To record the current star location (or rather its average) you need to take a reference with:

    ::

       [xsup@icc ncpc-rootdir]$ cacao-aorun-026-takeref -n 20000

    You can change the number of measurements averaged to suit based on the exposure time of the camera in use.  This
    sets the convergence point of the loop.  Now Check that the `acquWFS-2` processes is updating `aol2_imWFS2` with:

    ::

      [xsup@icc ~]$ milk-shmimmon aol2_imWFS2

Troubleshooting
~~~~~~~~~~~~~~~~~
If the loop isn't working or is behaving erratically, for instance you close the loop and it runs away immediately, try the following:

0. In cursesINDI, there are a variety of parameters that can be adjusted to fix or optimize the behavior of the FLOWFS loop.

::

`camflowfs-fit.deltaPixThresh` [pixels]

This regularizes magnitude of the Tip/Tilt commands sent to the NCPC DM via CACAO. E.g., for a value of 2 pixels, if the pixel coordinates for the center-of-light is more than 2 pixels away from the max value pixel coordinates on camflowfs (or camllowfs), no command will be sent. This is useful for, e.g., a hot pixel in a corner of the current ROI.

:: 

`camflowfs-fit.sigmaMaxThreshDown` and `camflowfs-fit.sigmaMaxThreshDown`

This sets upper/lower sigma clipping thresholds for RMS pixel values of the max pixel value in the current ROI, frame-by-frame. This has a 5 seconds circular buffer (can be modified using `camflowfs-fit.statstime`). If the max pixel value falls outside these thresholds, no command will be sent to the NCPC DM. This is useful for, e.g., intermittent clouds or seeing bursts.

:: 

`camflowfs-fit.sigmapixthresh`

This sets a sigma clipping threshold for the center-of-light pixel coordinate, frame-by-frame. This has a 5 seconds circular buffer (can be modified using `camflowfs-fit.statstime`).

:: 

`camflowfs-fit.dx` and `camflowfs-fit.dy` [pixels]

This sets an additive value to the tip/tilt commands sent to the NCPC DM via CACAO. This is useful for, e.g., moving the PSF on camflowfs as an alternative to nudging the focal plane mask using coronAlignGUI.

1. Restart the fitter process:

In cursesINDI, use:

:: 

`camflowfs-fit.reset`

Toggle this to do a soft reset of the camflowfs-fit process. This should avoid needing to rerun steps 2 through 5.

If the loop is *still* not behaving:

   ::

      [xsup@icc ~]$ xctrl restart camflowfs-fit / camflowfs-avg-fit / camllowfs-fit / camllowfs-avg-fit

   selecting the process accordingly

2. Verify in `cacao-fpsctrl-TUI` (the right hand CACAO terminal) that:

   - `wfs2cmodeval-2.option.MODENORM=OFF`
   - `acquWFS-2.comp.WFSrefsub=ON`
   - `acquWFS-2.comp.****=OFF` (all other things but WFSrefsub off)

3. Re-run steps 2,3,and 4 under "Low Order T/T Loop" above.  Note especially that you need to run step 4 if you run step 3.




