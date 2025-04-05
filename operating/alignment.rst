Alignment
===================================

System Pupil Alignment
-----------------------------------

Tweeter Pupil Alignment (F-Test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To align the pupil on the tweeter, we perform the F-Test (which is actually an R).

Prepare the system as in :doc:`daily_startup`, then configure:

* **fwpupil** to **open** (in Coronagraph Alignment GUI)

* **fwfpm** to **open**

* **fwlyot** to **open**

* **fwscind** to **pupil** (in camsci1Ctrl)

* **fwsci1** to **z** (in almost all cases you should align in ``z`` for repeatability)

* configure **camsci1** so that you can see the pupil without saturating.

* Move **stagesci1** to preset **fpm**.

Now put the test pattern on the tweeter with **Pupil Alignment GUI** for dmtweeter.  Press the **set test** under **Tweeter**

Next, use the "TTM Pupil" section to align the pupil on the tweeter using the arrow keypad.
The following figure demonstrates what a good alignment looks like.

.. image:: f-test-good.png
    :width: 500
    :align: center


When done, use the Tweeter **zero test** button on the Alignment GUI.

NCPC Pupil Alignment (J-Test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To align the pupil on the NCPC DM, we perform the J-Test.

The system should be configured for the F-test above. Next,

* Move **stagesci1** to preset **jtest**.

* Put the test pattern on the NCPC with the "Set Test" button next to "NCPC" on the **Pupil Alignment GUI**.

* Press the **set test** under **NCPC**

Next, use the "TTM Peri" section to align the pupil on the tweeter using the arrow keypad.
The following figure demonstrates what a good alignment looks like.

.. image::j-test_align.png

    :width: 500
    :align: center

* Clear the J-test with the "clear test" button on the **Pupil Alignment GUI**

* Return ``stagesci1`` to the ``fpm`` position

Pyramid Alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* In the Alignment GUI, Tip Alignment should show "move woofer" above the directional buttons. Use the directional buttons to try and get all four pyramid pupils uniformly illuminated.

* Using the directional buttons under the "Pupil Fitting" section to move the pupil images on camwfs until the "Avg:" x and y displacements are less than 0.1 pixel.

.. warning::

    The "pupil tracking loop" is not used in lab mode, only on-sky.

Close loop and refine pupil alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If CACAO is not yet started, consult the :doc:`CACAO startup guide <cacao>`.

In the ``holoop`` control GUI:

1. zero all gains
2. set global gain to 1
3. apply a small nonzero gain to tip and tilt
4. close the loop

Close a number of tweeter modes > number of offloaded modes, then turn on t2w offload in the offloading GUI.

Work your way up the mode blocks in the loop control GUI. As you close more modes, return to the directional buttons under the "Pupil Fitting" section of the Alignment GUI and try to keep the displacements under 0.1 pixel.

Coronagraph Alignment
---------------------

From the **camsci1** gui, set

    * **fwscind** to **pupil**
    * **stagesci1** to **telsim**
    
With the camsci1 shutter **open**, take a new dark. This will serve as the reference for alignment.

In the coronagraph alignment GUI: set **fwpupil** to **bump-mask**.

The camsci1 viewer will show the difference image, making it easier to align with the (now obscured) spider arms of the pupil.

Use the "Pupil Plane" directional buttons on the coronagraph alignment GUI to align the mask to the pupil.

.. image:: figures/bump_mask_alignment.png
   :width: 500
   :align: center

Once the bump mask is aligned, remember to close the shutter on camsci1 and **take a new dark**.

.. _fdpr2:

Focus Diversity Phase Retrieval (FDPR)
--------------------------------------

To further improve PSF quality, run focus diversity phase retrieval (FDPR) on camsci1 to derive a new non-common-path correction DM shape.

There are multiple ways to configure the algorithm (see :doc:`../software/fdpr`), but we most commonly use the ``CH4-875`` filter in camsci1 to compute a correction applied to ``dmncpc``.

1. Configure fwsci1 with the narrowband methane filter ``CH4-875``
2. Place stagesci1 at preset ``fpm``
3. Define a :term:`ROI` centered on the core of the PSF
4. Adjust exposure times as needed to have plenty (25000--30000) of counts in the peak of the PSF
5. Close the shutter and take new darks. (Then open the shutter.)
6. Open a terminal on ICC
7. ``export OPENBLAS_NUM_THREADS=1`` to avoid bogging down ICC with the process (TODO: make this automatic)
8. Run the FDPR process with: ``fdpr2_close_loop fdpr2_dmncpc_camsci1_CH4``
9. Save the flat with ``dm_save_flat ncpc -d fdpr``
