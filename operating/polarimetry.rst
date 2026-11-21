Polarimetry
===========

Point of contact: Miles Lucas <mileslucas@arizona.edu>

.. WARNING::
    WIP: This document is a work in progress. I recommend emailing me if you plan to do polarimetry.


Procedures
----------

The following procedure the **Polarimetry GUI**, but everything can be ran using INDI properties as well. If the GUI isn't running, launch it from ``exao1`` with

.. code-block:: bash

    nohup polarimetryGUI &


Setup
^^^^^

Align the instrument in the standard way following the :doc:`published procedure <./alignment>`. You will want to leave the ``fwscind`` pupil lens in and the J-test on. 

Prepare Devices
~~~~~~~~~~~~~~~

#. Power on stages (using ``pwrGUI``)

    - ``vpdu1.stagepolrot``
    - ``vpdu1.stageqwprot``
    - In the *ninja* tab: ``vpdu0.stagezaber``


Inserting the HWP
~~~~~~~~~~~~~~~~~

#. Open the AO loop (``holoop``).
#. Open the pupil tracking loop in the **Pupil Alignment GUI**
#. In the **Polarimetry GUI**, set :guilabel:`HWP lin. stage` to ``in``.

Inserting the QWPs
~~~~~~~~~~~~~~~~~~

#. AO loop and pupil tracking loop should be open
#. Set ``stageqwprot1`` and ``stageqwprot2`` to the ``lab`` preset using cursesINDI, if they're not there already. 
#. In the **Polarimetry GUI**, :guilabel:`QWP lin. stage` to ``in``.
#. Realign the system pupil

    .. warning::
        Do **not** use :guilabel:`Auto Alignment` here--there is no autoalignment after a QWP transition.

    #. Use the J-test and the :guilabel:`ttmperi` arrow buttons in the alignment GUI to roughly realign the pupil
    #. Close the high-order loop (``holoop``)
    #. Watch the alignment GUI :guilabel:`Pupil Tracking Loop` offsets and use :guilabel:`ttmperi` until the offsets are less than :math:`|0.05|` in both boxes.

#. Toggle the :guilabel:`QWP pupil tracking` slider in the **Polarimetry GUI** to enable ``ttmperi`` to correct for the pupil shifts as the QWPs move
#. Toggle the :guilabel:`QWP pol. tracking` slider to enable the QWPs to stabilize and optimize the eigenpolarizations of the instrument


Beamsplitter, filters, and cameras
~~~~~~~~~~~~~~~~~~~~~~~~

#. ``stagescibs`` to ``pol``
#. ``fwsci1`` and ``fwsci2`` in the **same filter** (r, i, or z)

    .. important::

        Don't forget to use the same filter for camsci1 and camsci2! We're doing PDI, not SDI.

#. Set :guilabel:`Synchro` on either camsci control GUI and tune exposure time and EM gains for both cameras. 

You can now turn ``stagezaber`` off in the *ninja* tab of ``pwrGUI``.


Sequencing
^^^^^^^^^^

Note: a HWP cycle is one full iteration of imaging at 0°, 45°, 22.5°, and 67.5°. The overheads for single HWP cycle, including the HWP moves and camera triggering, is 10-15 seconds.  

#. Set your sequencing parameters inside the **Polarimetry GUI**

    - The :guilabel:`Num. cycles` can be set to determine the total number of HWP cycles, or 0 to sequence indefinitely
    - The :guilabel:`Frames per pos.` sets the number of frames per HWP position--it is meant for longer exposures, and if the exposure time is less than 1 second it cannot be used. A setting of 0 frames uses a timer instead.
    - The :guilabel:`Time per pos.` can be used if :guilabel:`num. frames` is 0.

#. Prepare observer name, operator name, target name, and observation name in the Observers interface on the MagAO-X Web UI

#. Once ready, click :guilabel:`Start sequencing`
    
    - If you want to stop imaging after the current cycle, click :guilabel:`Last cycle`
    - If you want to stop imaging after the current HWP position, click :guilabel:`Stop sequencing`
    - If you want to stop imaging NOW, click :guilabel:`Abort`

Teardown
^^^^^^^^

Removing the QWPs
~~~~~~~~~~~~~~~~~~

#. Open the AO loop (``holoop``).
#. Toggle the :guilabel:`QWP pol. tracking` slider off
#. Toggle the :guilabel:`QWP pupil tracking` slider in the **Polarimetry GUI** off
#. Open the pupil tracking loop in the **Pupil Alignment GUI**
#. In the **Polarimetry GUI**, :guilabel:`QWP lin. stage` to ``out``.


Removing the HWP
~~~~~~~~~~~~~~~~~

#. AO loop and pupil tracking loop should be open
#. In the **Polarimetry GUI**, set :guilabel:`HWP lin. stage` to ``out``.
#. Start with :guilabel:`ttmperi` to roughly realign the pupil using the J-test
#. Close the AO loop (``holoop``)
#. Run :guilabel:`Auto Alignment` in the **Pupil Alignment GUI** until the pupil offsets are less than :math:`|0.05|`, then turn it off.
#. Close the pupil tracking loop in the **Pupil Alignment GUI**


Details
------------

Polarizing beamsplitter (PBS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The polarizing beamsplitter cube (PBS) splits incident light into orthogonal polarization states for each science camera. The orientation of the PBS is such that camsci1 measures horizontally polarized light while camsci2 measures vertically polarized light. Polarimetric observables are obtained from differencing the two cameras' images or fluxes

.. math::

    X = I_{cam2} - I_{cam1}

to normalize the observable, divide by the single sum

.. math::

    I = I_{cam2} + I_{cam1}

    x = X / I

To use the PBS, it must be inserted in ``stagescibs`` ('pol'). This can be done through INDI or from either camsciCtrl GUI. In data analysis, the beamsplitter option can be confirmed in the ``STAGESCIBS PRESET NAME`` FITS header (should be 'pol').


Half-wave plate (HWP)
~~~~~~~~~~~~~~~~~~~~~

Because the PBS has a fixed orientation, each camera can only measure the horizontal and vertical polarized light (Stokes Q). Therefore, to measure +45° and -45° polarized light (Stokes U) a half-wave plate (HWP) modulates input polarized light such that incident Stokes U light can be measured as horizontal and vertically polarized light.

Additionally, the HWP is a critical component for cancelling instrumental polarization effects. In the same way it modulates incident Stokes U light into horizontal/vertical, it can modulate incident Stokes Q light into the -Q orientation. By making two measurements with different HWP orientations, one for Stokes +Q and one for Stokes -Q, we can differentially cancel instrumental effects:

.. math::

    I_{HWP0} = +Q + inst

    I_{HWP45} = -Q + inst
    
    0.5 * (I_{HWP0} - I_{HWP45}) = 0.5 * (+Q + inst - -Q - inst) = Q

In order to use the HWP, it must be inserted into the beam using ``stagepollin``. Once it is in, the key MagAO-X application to use is ``hwptrack``. To move the HWP to a given angle, set ``hwptrack.hwp_position.target``. The standard sequence for linear Stokes polarimetry steps through 0°, 45°, 22.5°, and 67.5°. These correspond to measuring Stokes +Q, -Q, +U, and -U in sequence. These names are shown in the ``hwptrack.hwp_position_name.value`` and can be used for grouping frames for data analysis.

For data analysis, the following FITS headers are provided--

.. code-block:: bash

    HWPTRACK SET ANGLE / [deg] The fast-axis angle of the HWP, typically 0, 45, 22.5, and 67.5
    HWPTRACK ACTUAL ANGLE / [deg] The actual orientation of the HWP, only differs from the SET ANGLE when tracking is on
    HWPTRACK POS NAME / The named HWP position, one of 'Qplus', 'Qminus', 'Uplus', 'Uminus', or 'unknown'
    HWPTRACK TRACKING / [int] 0 if synchro_adi tracking is off, 1 if tracking is on



Dual rotating quarter-wave plate compensator (DQWP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The DQWP is used to arbitrarily reorient the eigenpolarizations of the instrument. In other words, it will ensure that horizontal and vertically polarized light remains horizontal or vertically polarized when measured. The main usage for the DQWP is to compensate for cross-talk between polarization states induced by the k-mirror image rotator.


For data analysis, the following FITS headers are provided--

.. code-block:: bash

    QWPTRACK QWP1 SET ANGLE / [deg] The fast-axis angle of QWP1
    QWPTRACK QWP2 SET ANGLE / [deg] The fast-axis angle of QWP2
    QWPTRACK TRACKING / [int] 0 if QWP pol. tracking is off, 1 if tracking is on

