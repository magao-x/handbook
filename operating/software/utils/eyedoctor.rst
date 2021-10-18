The Eye Doctor
==============

Part of the `magpyx <https://github.com/magao-x/magpyx>`__ Python
package.

Quick Start
-----------

If the wavefront is in sorry shape, you’ll probably want to do the
optimization in 3 steps (shown here for the woofer and camtip):

**Step 1**: dial in defocus by hand. Don’t worry about getting it
perfect—just get it close. You could also optimize defocus by itself if
you want. Example:

::

   dm_eye_doctor 7626 wooferModes camtip 10 2 0.5

**Step 2**: optimize low order modes over a large range of amplitudes.
Example:

::

   dm_eye_doctor 7626 wooferModes camtip 10 2...10 0.25

**Step 3**: optimize all modes over a smaller range. Example:

::

   dm_eye_doctor 7626 wooferModes camtip 10 2...35 0.05

And for the NCPC DM and camsci2, this is the equivalent sequence of
commands:

::

   dm_eye_doctor 7624 ncpcModes camsci2 5 2 0.5
   dm_eye_doctor 7624 ncpcModes camsci2 5 2...10 0.25
   dm_eye_doctor 7624 ncpcModes camsci2 5 2...35 0.05

Command-line Operation
----------------------

The eye doctor can be run from the command line:

::

   dm_eye_doctor [portINDI] [dmModes] [shmim] [psf_core_radius_pixels] [modes_to_optimize] [search_range]

For example, to optimize the woofer on the pyramid tip camera, you’ll
run something like:

::

   dm_eye_doctor 7626 wooferModes camtip 10 2...10 0.1

This performs a grid search over modes 2-10 over amplitudes of -0.05 to
0.05 microns RMS. A 10 pixels core radius is a good choice for the
pyramid tip camera.

**NB: the eye doctor must be run on the computer where the shared memory
camera image lives. This is almost always the ICC.** The INDI port
should be 7626 for wooferModes on the ICC and 7624 for ncpcModes.

To fully optimize the ncpc DM on camsci1, a good template is:

::

   dm_eye_doctor 7624 ncpcModes camsci1 5 2...35 0.1

Note that a 5-pixel core radius is generally a good choice on the
science cameras.

When you’re happy with the results, you can update the flat file and
clear the optimization DM channel:

::

   dm_eye_doctor_update_flat [dm: woofer, ncpc, or tweeter]

**NB: The update flat command must be run on the computer where the DM
shared memory image and calibration files live.** For the woofer and
tweeter, this is the RTC. For the NCPC, this is the ICC.

Options
-------

Mode selection
~~~~~~~~~~~~~~

The modes argument can be specified by comma-separated integers, ranges
(…), or a combination thereof. Examples:

::

   2 -> 2
   3...5 -> 3,4,5
   2,6,10...15,18 -> 2,6,10,11,12,13,14,15,18

Baselines
~~~~~~~~~

By default, the eye doctor performs the grid search over the mode values
already set in the dmModes app. So if you dial in modes manually, the
grid search is centered on those points. To ignore these, add a
``--reset`` flag.

Focus
~~~~~

When optimizing > 1 mode, focus is always performed first (even if it’s
repeated later). To disable this, use the ``--ignorefocus`` flag.

Image Averaging
~~~~~~~~~~~~~~~

To average multiple frames from the camera, set
``--nimages [# of images]``

Sampling
~~~~~~~~

By default, the eye doctor makes 3 sweeps through each mode, sampling at
20 points between -``search_range``/2 to +\ ``search_range``/2. (All
data points from the sweeps are combined, and a quadratic is fit to
these points to find the optimal mode amplitude.) You can change the
number of sweeps by setting ``--nrepeats [# of sweeps]``. Change the
sampling by setting ``--nsteps [# of steps]``.

Sequences
~~~~~~~~~

The eye doctor splits the modes-to-be-optimized into clusters of 5,
shuffles them around, and optimizes them. If you’re fighting creep or
otherwise struggling to keep the PSF optimized, you can automate more
sophisticated sequences:

``--nclusterrepeats [# of repeats]`` will repeat each cluster the
requested number of times, each time in a new, randomized order.

``--nseqrepeat [# of repeats]`` will repeat the *entire* optimization
(all modes) the requested number of times.

From Python
-----------

Examples of Python notebook usage are
`here <https://github.com/magao-x/magpyx/blob/master/notebooks/dm_interaction.ipynb>`__.
