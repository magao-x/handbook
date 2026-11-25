Polarimetry
===========

Point of contact: Miles Lucas <mileslucas@arizona.edu>

.. warning::

   This document is a work in progress. If you plan to do polarimetry, please email me beforehand.

The procedures below use the **Polarimetry GUI**, but every step can also be done with INDI properties directly. If the GUI isn't running, launch it from ``exao1`` with

.. code-block:: bash

   nohup polarimetryGUI &


Setup
^^^^^

Align the instrument following the standard :doc:`alignment procedure <./alignment>`. Leave the ``fwscind`` pupil lens in and the J-test on; you will need them to realign the pupil after inserting the QWPs.

Prepare devices
~~~~~~~~~~~~~~~

#. Power on the following stages using ``pwrGUI``:

   - ``vpdu1.stagepolrot``
   - ``vpdu1.stageqwprot``
   - ``vpdu0.stagezaber`` (in the *ninja* tab)

Insert the HWP
~~~~~~~~~~~~~~

#. Open the AO loop (``holoop``).
#. Open the pupil tracking loop in the **Pupil Alignment GUI**.
#. In the **Polarimetry GUI**, set :guilabel:`HWP lin. stage` to ``in``.

Insert the QWPs
~~~~~~~~~~~~~~~

#. Make sure the AO loop and the pupil tracking loop are both open.
#. If they aren't there already, set ``stageqwprot1`` and ``stageqwprot2`` to the ``lab`` preset using ``cursesINDI``.
#. In the **Polarimetry GUI**, set :guilabel:`QWP lin. stage` to ``in``.
#. Realign the system pupil:

   .. danger::

      Do **not** use :guilabel:`Auto Alignment` here. It is not calibrated for the pupil position after a QWP insertion.

   #. Roughly realign the pupil using the J-test and the :guilabel:`ttmperi` arrow buttons in the **Pupil Alignment GUI**.
   #. Close the AO loop (``holoop``).
   #. Watch the :guilabel:`Pupil Tracking Loop` offsets and adjust :guilabel:`ttmperi` until both are within :math:`\pm 0.05`.

   .. figure:: figures/pupil_alignment_loop.png
        :align: center

        The pupil alignment loop offsets in the **Alignment** GUI

#. In the **Polarimetry GUI**, enable :guilabel:`QWP pupil tracking`. This lets ``ttmperi`` correct the pupil shifts as the QWPs rotate.
#. Enable :guilabel:`QWP pol. tracking`. This lets the QWPs stabilize and optimize the eigenpolarizations of the instrument.

Beamsplitter, filters, and cameras
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Set ``stagescibs`` to ``pol``.
#. Put ``fwsci1`` and ``fwsci2`` in the **same filter** (r, i, or z).

   .. important::

      camsci1 and camsci2 must use the same filter. This is PDI, not SDI.

#. Enable :guilabel:`Synchro` in either camsci control GUI, then tune the exposure time and EM gain for both cameras.

Setup is complete. You can now power off ``stagezaber`` in the *ninja* tab of ``pwrGUI``.


Sequencing
^^^^^^^^^^

#. Set the sequencing parameters in the **Polarimetry GUI**:

   - :guilabel:`Num. cycles`: the number of HWP cycles to run. Set to 0 to run until stopped.
   - :guilabel:`Frames per pos.`: the number of camera frames at each HWP position. This is meant for long exposures and requires an exposure time of at least 1 s. Set to 0 to use a timer instead (the default).
   - :guilabel:`Time per pos.`: the time spent at each HWP position, in seconds. Only used when :guilabel:`Frames per pos.` is 0.

#. In the Observers interface of the MagAO-X Web UI, fill in the observer, operator, target, and observation names.
#. Click :guilabel:`Start sequencing`. To stop:

   - :guilabel:`Last cycle`: finish the current HWP cycle, then stop.
   - :guilabel:`Stop sequencing`: finish the current HWP position, then stop.
   - :guilabel:`Abort`: stop immediately.

Timing and efficiency
~~~~~~~~~~~~~~~~~~~~~

A HWP cycle is one full pass of imaging at 0°, 45°, 22.5°, and 67.5°. Each cycle carries 19 ± 2 s of overhead from the HWP moves and camera triggering, regardless of the time per position.

.. table:: HWP cycle overheads and observing efficiency
   :widths: auto

   =================  =========  =========  ====================
   Time per pos. (s)  Cycle (s)  Overheads  Observing efficiency
   =================  =========  =========  ====================
   5                  39         49%        51%
   10                 59         33%        67%
   15                 79         24%        76%
   30                 139        14%        86%
   60                 259        7%         93%
   =================  =========  =========  ====================

The total time for a sequence can be estimated as

.. math::

   T_\mathrm{seq} \approx 5~\mathrm{s} + N_\mathrm{cycles} \times \left(4\,t_\mathrm{pos} + 19.3~\mathrm{s}\right)


Teardown
^^^^^^^^

Remove the QWPs
~~~~~~~~~~~~~~~

#. Open the AO loop (``holoop``).
#. In the **Polarimetry GUI**, disable :guilabel:`QWP pol. tracking`.
#. Disable :guilabel:`QWP pupil tracking`.
#. Open the pupil tracking loop in the **Pupil Alignment GUI**.
#. In the **Polarimetry GUI**, set :guilabel:`QWP lin. stage` to ``out``.

Remove the HWP
~~~~~~~~~~~~~~

#. Make sure the AO loop and the pupil tracking loop are both open.
#. In the **Polarimetry GUI**, set :guilabel:`HWP lin. stage` to ``out``.
#. Roughly realign the pupil using the J-test and :guilabel:`ttmperi`.
#. Close the AO loop (``holoop``).
#. In the **Pupil Alignment GUI**, run :guilabel:`Auto Alignment` until both pupil offsets are within :math:`\pm 0.05`, then turn it off.
#. Close the pupil tracking loop.


Details
^^^^^^^

Polarizing beamsplitter (PBS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The polarizing beamsplitter cube (PBS) splits the incident light into orthogonal linear polarizations, one for each science camera: camsci1 measures horizontally polarized light and camsci2 measures vertically polarized light. Polarimetric observables come from differencing the two cameras' images or fluxes,

.. math::

   X = I_\mathrm{cam2} - I_\mathrm{cam1},

and they are normalized by the sum,

.. math::

   I = I_\mathrm{cam2} + I_\mathrm{cam1}, \qquad x = X / I.

To use the PBS, set ``stagescibs`` to ``pol``, either through INDI or from either camsciCtrl GUI. In the data, check the ``STAGESCIBS PRESET NAME`` FITS header; it should read ``pol``.

Half-wave plate (HWP)
~~~~~~~~~~~~~~~~~~~~~

Because the PBS has a fixed orientation, the cameras alone can only measure horizontal and vertical polarization (Stokes Q). To measure +45° and −45° polarization (Stokes U), the half-wave plate (HWP) rotates the incoming polarization so that Stokes U lands on the horizontal/vertical axes of the PBS.

The HWP is also critical for cancelling instrumental polarization. In the same way it rotates Stokes U onto Q, it can flip incident +Q to −Q. Two measurements at different HWP angles, one measuring +Q and one measuring −Q, let us cancel the instrumental term differentially:

.. math::

   X_\mathrm{HWP\,0^\circ} &= +Q + X_\mathrm{inst}

   X_\mathrm{HWP\,45^\circ} &= -Q + X_\mathrm{inst}

   \tfrac{1}{2}\left(X_\mathrm{HWP\,0^\circ} - X_\mathrm{HWP\,45^\circ}\right) &= Q

To use the HWP, insert it into the beam with ``stagepollin``. The HWP is controlled by the ``hwptrack`` application. To move it to a given angle, set ``hwptrack.hwp_position.target``. The standard sequence for linear Stokes polarimetry steps through 0°, 45°, 22.5°, and 67.5°, which measure Stokes +Q, −Q, +U, and −U, respectively. The current position name is reported in ``hwptrack.hwp_position_name.value`` and can be used to group frames during data analysis.

The following FITS headers are provided for data analysis:

.. code-block:: text

   HWPTRACK SET ANGLE    / [deg] Commanded fast-axis angle of the HWP, typically 0, 45, 22.5, or 67.5
   HWPTRACK ACTUAL ANGLE / [deg] Actual fast-axis angle of the HWP; differs from SET ANGLE only when tracking is on
   HWPTRACK POS NAME     / Named HWP position: 'Qplus', 'Qminus', 'Uplus', 'Uminus', or 'unknown'
   HWPTRACK TRACKING     / [int] 1 if synchro_adi tracking is on, 0 if off

Dual rotating quarter-wave plate compensator (DQWP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The DQWP can reorient the eigenpolarizations of the instrument. In practice, this means it keeps light that enters horizontally or vertically polarized horizontally or vertically polarized when it is measured. Its main use is to compensate for the cross-talk between polarization states caused by the k-mirror image rotator.

The following FITS headers are provided for data analysis:

.. code-block:: text

   QWPTRACK QWP1 ANGLE / [deg] Fast-axis angle of QWP1
   QWPTRACK QWP2 ANGLE / [deg] Fast-axis angle of QWP2
   QWPTRACK TRACKING   / [int] 1 if QWP pol. tracking is on, 0 if off