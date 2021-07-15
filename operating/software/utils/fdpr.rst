Focus Diversity Phase Retrieval (and correction)
==================================================

Guide on running focus diversity phase retrieval (FDPR) on MagAO-X. Part of the `magpyx <https://github.com/magao-x/magpyx>`_ Python package.

Description
------------

FDPR estimates the pupil-plane field from a set of measurements of defocused PSFs. This implementation is based on `Thurman et al. (2009) <https://doi.org/10.1364/JOSAA.26.000700>`_.

Setting up the instrument
--------------------------

Follow the usual procedure for :doc:`starting up the instrument <../../startup>` and :doc:`aligning the system pupil <../../alignment>`. We typically run
FDPR in the H\ :math:`\alpha` filter on camsci2. Here's a typical configuration:

==========  ===== 
device      state
==========  =====
fwtelsim    ND1
fwscind     ND1_0
fwsci2      Halpha
stagescibs  Halpha
stagesci2   75mm (center of range)
camsci2     5MHz, 512x512 ROI (centered on PSF at 75mm), ~15 fps (or fastest possible)
==========  =====

Running ``pyindi_send_preset fdpr_camsci2_halpha`` will set all devices to the above configuration, except camsci2 (provided devices that require homing have been homed -- this is a work in progress).

The PSF should be in focus and saturated at the 75 mm position. If it is egregiously out of focus, you can drive it to focus using ``dmncpcModes`` (if it's a large change in focus, this normally introduces astigmatism as well).

We typically make measurements at defocused positions of +/-40 and +/-60mm. To check that the camera is set appropriately, drive stagesci2 to 35 and 115 mm and confirm that the PSF is not saturating. 

When driving the tweeter on the RTC, you will need to set up a TCP shmim stream of camsci2 from the ICC to RTC.

Quick start
-------------------

A typical session of FDPR-driven optimization will start by driving the NCPC DM on camsci2 measurements, followed by driving the tweeter on camsci2. Here are some commands to selectively copy & paste as needed.

On the ICC with the NCPC DM::

    pyindi_send_preset fdpr_camsci2_halpha # configure the instrument. make sure you've set camsci2 separately
    fdpr_measure_response fdpr_dmncpc_camsci2_stage # measure a new response matrix
    fdpr_estimate_response fdpr_dmncpc_camsci2_stage # estimate the phase from the latest measured response matrix (this will take a few minutes)
    fdpr_compute_control_matrix fdpr_dmncpc_camsci2_stage # compute a control matrix
    fdpr_close_loop fdpr_dmncpc_camsci2_stage # close the loop
    dm_eye_doctor_update_flat ncpc # collapse all DM channels into a new flat

On the RTC with the tweeter DM::

    pyindi_send_preset fdpr_camsci2_halpha # configure the instrument. make sure you've set camsci2 separately
    fdpr_measure_response fdpr_dmtweeter_camsci2_stage # measure a new response matrix
    fdpr_estimate_response fdpr_dmtweeter_camsci2_stage # estimate the phase from the latest measured response matrix (this will take a ~ 1 hr, 15 min)
    fdpr_compute_control_matrix fdpr_dmtweeter_camsci2_stage # compute a control matrix
    fdpr_close_loop fdpr_dmtweeter_camsci2_stage # close the loop
    dm_eye_doctor_update_flat tweeter # collapse all DM channels into a new flat

Overview
-------------------------------------------------------

First, get the instrument into the expected configuration (not quite implemented yet)::

    pyindi_send_preset <fdpr preset name>

If you've already got a calibration and only need to close the loop::

    fdpr_close_loop <name of config file (always without the path and .conf extension)>

If you just want to estimate the current wavefront state (this will update a set of shmims specified in the config file)::

    fdpr_one_shot <name of config file>

To run the calibration from scratch:

1. Measure a response matrix (Hadamard modes)::

    fdpr_measure_response <name of config file>

2. Run the estimator on the last measured response matrix::

    fdpr_estimate_response <name of config file>

3. Compute the control matrix::

    fdpr_compute_control_matrix <name of config file>

4. Close the loop (see above)

Calibration and configuration
--------------------------------

All calibration products associated with a particular loop (unique config file) are stored in ``\opt\MagAOX\calib\fdpr\<loop name>`` (where the final directory is specified in the config file).

The latest calibration products are symlinked in the parent directory and are used as the defaults when running the scripts (unless an override argument is provided).

The directory is structured following

::

    loop name
    ├── ctrlmat.fits
    ├── ctrlmat
    │   ├── ctrlmat_<datetime1>.fits
    |   ...
    |   └── ctrlmat_<datetimeN>.fits
    ├── measrespM.fits
    ├── measrespM          
    │   ├── measrespM_<datetime1>.fits
    |   ...
    |   └── measrespM_<datetimeN>.fits
    ├── dmmap.fits
    ├── dmmap          
    │   ├── dmmap_<datetime1>.fits
    |   ...
    |   └── dmmap_<datetimeN>.fits
    ├── dmask.fits
    ├── dmask
    │   ├── dmmask_<datetime1>.fits
    |   ...
    |   └── dmmask_<datetimeN>.fits
    └── etc. 

The configuration files are stored at ``\opt\MagAOX\config``. A typical example looks like::

    [camera]
    name=camsci2

    [diversity]
    wfilter=Halpha
    type=stage
    camstage=stagesci2
    stage_focus=75
    dmModes=wooferModes
    dmdelay=0.13
    indidelay=1
    values =-60,-40,40,60
    navg=1
    ndark=10
    dmdivchannel=dm01disp05
    port=7625

    [estimation]
    N=512
    nzernike=45
    npad=10
    pupil=bump_mask
    phase_shmim=fdpr_camsci2_phase
    amp_shmim=fdpr_camsci2_amp
    nproc=3
    gpus=0,1,2

    [calibration]
    path=/opt/MagAOX/calib/fdpr/dmtweeter_camsci2_stage

    [interaction]
    hval = 0.05
    Nact = 2040
    dm_map=/opt/MagAOX/calib/dm/bmc_2k/bmc_2k_actuator_mapping.fits
    dm_mask=/opt/MagAOX/calib/dm/bmc_2k/bmc_2k_actuator_mask.fits
    fix_xy_to_first=True

    [control]
    dmctrlchannel=dm01disp05
    nmodes=1500
    ampthreshold=0.
    dmthreshold=1.1
    wfsthreshold=0.5
    ninterp=3
    gain=0.5
    leak=0.
    niter=10
    delay=0.5

A few parameters of note:

* `diversity.type` can be either `stage` or `dm` and specifies whether the focus diversity is achieved by moving the camera stage or the DM specified by the `dmModes` parameter
* `diversity.values` is a comma-separated list of diversity values: axial stage movement in mm if `diversity.type=stage` or microns RMS if `diversity.type=dm`
* `diversity.stage_focus` sets the nominal focused position about which the stage will move if `diversity.type=stage`

There are a large number of other parameters (particularly those used in the estimation process) that are only exposed through interactive usage in a python session.

Command line usage
-------------------

When calling FDPR from the command line, the configuration parameters can be overriden with the following syntax::

    <fdpr_console_script> <conf file> -o section1.parameter1=value1 section2.parameter2=value2

For example, to run a closed loop with a different number of modes and a different gain::

    fdpr_close_loop <conf file> -c -o control.nmodes=1000 control.gain=0.6

(the `-c` flag above forces the control matrix to be recomputed with the new parameters.)

The `-o` flag is valid for any FDPR script. Individual scripts have unique flags that you can find by calling the help on a given function (`-h`).

Interactive usage
------------------

More advanced/configurable usage can be done interactively. An example Jupyter notebook is linked to here (or will be in the future).