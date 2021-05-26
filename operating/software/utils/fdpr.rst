Focus Diversity Phase Retrieval (and correction)
==================================================

Guide on how to run focus diversity phase retrieval (FDPR) on MagAO-X. Part of the `magpyx <https://github.com/magao-x/magpyx>`_ Python package.

Description
------------

FDPR estimates the pupil-plane field from a set of measurements of defocused PSFs. This implementation is based on `Thurman et al. (2009) <https://doi.org/10.1364/JOSAA.26.000700>`_.

Quick start (for when you just want to copy and paste)
-------------------------------------------------------

First, get the instrument into the expected configuration::

    send_to_preset <fdpr preset name>

If you've already got a calibration and only need to close the loop::

    fdpr_close_loop <name of config file (always without the path or .conf extension)>

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

Setting up the instrument
--------------------------

Required devices, alignment, configuration... 

.. Notes to myself: ND1 / ND1, 5Mhz, 50fps, Halpha 256x256 ROI at (708,248)


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
    region_roi_x=256

    [instrument]
    fwpupil=bump_mask
    fwsci2=Halpha

    [diversity]
    wfilter=Halpha
    type=stage
    camstage=stagesci2
    stage_focus=75
    dmModes=wooferModes
    dmdelay=0.063
    indidelay=1
    values =-60,-40,40,60
    navg=1
    ndark=10
    dmdivchannel=dm01disp05
    port=7624

    [estimation]
    N=256
    nzernike=45
    npad=10
    pupil=bump_mask
    phase_shmim=fdpr_camsci2_phase
    amp_shmim=fdpr_camsci2_amp
    nproc=3

    [calibration]
    path=/opt/MagAOX/calib/fdpr/dmtweeter_camsci2_stage

    [interaction]
    hval = 0.05
    Nact = 2040
    dm_map=/opt/MagAOX/calib/dm/bmc_2k/bmc_2k_actuator_mapping.fits
    dm_mask=/opt/MagAOX/calib/dm/bmc_2k/bmc_2k_actuator_mask.fits

    [control]
    dmctrlchannel=dm01disp06
    nmodes=1500
    ampthreshold=0.
    dmthreshold=0.5
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

Command line usage
-------------------

A general note about arguments 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

overriding the configuration file

One-shot estimation
^^^^^^^^^^^^^^^^^^^^^

Response matrix measurement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Response matrix estimation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Computing the control matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Closing the loop
^^^^^^^^^^^^^^^^^

Interactive usage
------------------

More advanced/configurable usage can be done interactively. An example Jupyter notebook is linked to here (or will be in the future).