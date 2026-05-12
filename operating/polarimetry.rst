Polarimetry
===========

Point of contact: Miles Lucas <mileslucas@arizona.edu>

.. WARNING:: 
    WIP: This document is a work in progress. I recommend emailing me if you plan to do polarimetry.

Introduction
------------


Devices and Stages
------------------

Polarizing beamsplitter (PBS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The polarizing beamsplitter cube (PBS) splits incident light into orthogonal polarization states for each science camera. The orientation of the PBS is such that camsci1 measures horizontally polarized light while camsci2 measures vertically polarized light. Polarimetric observables are obtained from differencing the two cameras' images or fluxes

.. code-block:: math

    X = I_cam2 - I_cam1

to normalize the observable, divide by the single sum

.. code-block:: math

    I = I_cam2 + I_cam1
    x = X / I

To use the PBS, it must be inserted in ``stagescibs`` ('pol'). This can be done through INDI or from either camsciCtrl GUI. In data analysis, the beamsplitter option can be confirmed in the ``STAGESCIBS PRESET NAME`` FITS header (should be 'pol').

.. important::

    Don't forget to use the same filter for camsci1 and camsci2! We're doing PDI, not SDI.


Half-wave plate (HWP)
~~~~~~~~~~~~~~~~~~~~~

Because the PBS has a fixed orientation, each camera can only measure the horizontal and vertical polarized light (Stokes Q). Therefore, to measure +45° and -45° polarized light (Stokes U) a half-wave plate (HWP) modulates input polarized light such that incident Stokes U light can be measured as horizontal and vertically polarized light.

Additionally, the HWP is a critical component for cancelling instrumental polarization effects. In the same way it modulates incident Stokes U light into horizontal/vertical, it can modulate incident Stokes Q light into the -Q orientation. By making two measurements with different HWP orientations, one for Stokes +Q and one for Stokes -Q, we can differentially cancel instrumental effects:

.. code-block:: math

    I_HWP0 = +Q + inst
    I_HWP45 = -Q + inst
    0.5 * (I_HWP0 - I_HWP45) = 0.5 * (+Q + inst - -Q - inst) = Q

In order to use the HWP, it must be inserted into the beam using ``stagepollin``. Once it is in, the key MagAO-X application to use is ``hwptrack``. To move the HWP to a given angle, set ``hwptrack.hwp_position.target``. The standard sequence for linear Stokes polarimetry steps through 0°, 45°, 22.5°, and 67.5°. These correspond to measuring Stokes +Q, -Q, +U, and -U in sequence. These names are shown in the ``hwptrack.hwp_position_name.value`` and can be used for grouping frames for data analysis.

The last feature is the ADI synchronization tracking mode for the HWP, set by ``hwptrack.tracking.toggle``. This synchronizes the HWP with the image rotator, adding an offset on top of the desired HWP angle (shown with ``hwptrack.hwp_tracking_offset.value``). This keeps the eigenpolarizations of the instrument coincident with the sky even while the field is rotating due to pupil tracking. This also simplifies the data analysis--when each frame is derotated to orient north up and east left, the additional HWP offset will perfectly align the Stokes Q and U axes to the sky axes.

For data analysis, the following FITS headers are provided--

.. code-block:: bash

    HWPTRACK SET ANGLE / [deg] The polarization angle of the HWP, typically 0, 45, 22.5, and 67.5
    HWPTRACK ACTUAL ANGLE / [deg] The actual orientation of the HWP, only differs from the SET ANGLE when tracking is on
    HWPTRACK POS NAME / The named HWP position, one of 'Qplus', 'Qminus', 'Uplus', 'Uminus', or 'unknown'
    HWPTRACK TRACKING / [int] 0 if synchro_adi tracking is off, 1 if tracking is on



Dual rotating quarter-wave plate compensator (DQWP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The DQWP is used to arbitrarily reorient the eigenpolarizations of the instrument. In other words, it will ensure that horizontal and vertically polarized light remains horizontal or vertically polarized when measured. The main usage for the DQWP is to compensate for cross-talk between polarization states induced by the k-mirror image rotator.

.. important::

    Inserting or removing the QWP shifts both the PSF and the pupil. There is no auto-alignment for this configuration, so a :ref:`J-test <jtest>` must be performed **every time** the QWP is inserted or removed, and the ``camwfs`` pupils must be re-aligned by hand with the camera lens.

Before any QWP transition, configure ``camsci1`` for alignment work:

* ``camsci1`` ROI to ``full``
* ``stagesci1`` to focus, then to ``test`` for the J-test

Inserting the QWP
^^^^^^^^^^^^^^^^^

#. Open the AO loop (``holoop``).
#. In ``cursesINDI``, toggle ``stageqwplin`` to ``in``.
#. From the **Pupil Alignment GUI**, **move woofer** to bring the PSF back onto the target cross.
#. Adjust ``holoop`` gains to tip and tilt only and close the loop. Start increasing gains on higher order blocks up to block 5 (or fewer if the loop diverges).
#. Manually move the pupils on ``camwfs`` with the **camera lens**. Target x and y displacements <0.01.
#. Adjust ``holoop`` gains to include all blocks.
#. Perform the :ref:`J-test <jtest>`.

    .. warning::
        Do **not** use :guilabel:`Auto Alignment` here--there is no autoalignment after a QWP transition. If tip/tilt is large enough, you may close the loop while still nudging the camera lens.


Removing the QWP
^^^^^^^^^^^^^^^^

#. Open the AO loop (``holoop``).
#. In ``cursesINDI``, toggle ``stageqwplin`` to ``out``.
#. From the **Pupil Alignment GUI**, **move woofer** to bring the PSF back onto the target cross.
#. Adjust ``holoop`` gains to tip and tilt only and close the loop. Start increasing gains on higher order blocks up to block 5 (or fewer if the loop diverges).
#. Manually move the pupils on ``camwfs`` with the **camera lens**. Target x and y displacements <0.01.
#. Adjust ``holoop`` gains to include all blocks.
#. Perform the :ref:`J-test <jtest>`.


Operation
---------

#. Make sure the PBS is selected in ``stagescibs``
#. Make sure both science cameras are in the same filter, ``r``, ``i``, or ``z``.
#. (Optional) Insert the DQWP following the `Inserting the QWP`_ procedure above. Note that the J-test must be redone after inserting, since there is no auto-alignment for the QWP-in configuration.

    #. (TODO; code doesn't exist yet) ``qwptrack`` start tracking
#. Ensure the science cameras are synchronized via the ``synchro`` property
#. Insert the HWP
    #. Make sure ``stagezaber`` power is on and ``stagepollin`` USB is on in the ninja tab of ``pwrGui``
    #. Move ``stagepollin`` to preset ``in``
    #. Turn ``stagezaber`` power off and ``stagepollin`` USB off
#. Prepare the HWP
    #. Make sure ``stagepolrot`` power and USB are on in ``pwrGui``

At this point, all optics are ready for polarimetry. Polarimetry is run via the ``hwpSequencer`` app or inside the ``hwpSequencerGUI``.

