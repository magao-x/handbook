Alignment
===================================

These procedures assume that you have completed the :doc:`startup` and :doc:`daily_startup`, have a PSF
on `camtip`, and are modulating.

System Pupil Alignment
-----------------------------------

Decide on your beam splitter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All of the alignment takes place downstream of the ``stagebs`` science/WFS beamsplitter, so a change of beamsplitter will invalidate your alignment and require you to repeat these steps.

Decide whether you're using H-alpha / IR or 65-35 first, and configure ``stagebs``.

Pupil Alignment
~~~~~~~~~~~~~~~~

1. hit `t` in the `camtip` `rtimv` display to show the target cross

2. use the keypad on Pupil Alignment GUI to **move woofer** so the PSF is on the cross

3. check that camwfs EM gain is 1, then open shutter

4. make sure synchro is on

5. put `fwpm`` in flat

6. put `camflowfs`` in `default` ROI, and press `t` to show the target cross on its display

7. On *Pupil Alignment Gui* us the `pico sci-x` buttons to move the PSF left and right to center on the target

 - If switching beamsplitters, use the drop-down box to select the new beamsplitter.
 - Use the arrow buttons to make smaller moves
 - The PSF should be centered on the target int he

8. Next set woofer offloading to 2 modes

9. Close the loop on tip/tilt only

 - low gain is fine.  Multiplication Coefficient should be 1.0

10. Now select `move TTM`` on lower left of pupil guide gui

11. With the loop closed move up and down with the arrows to center on the target on `camflowfs` in y. Also clean up any remaining x with pico-sci-x.

12. Keeping the loop closed, you can now start `Auto Alignment`

 - Monitor the `camwfs` pupil position to ensure it does not run away
 - Monitor "Pupil Tracking Loop" and "Actuator Alignment Loop" deltas.

13. Once the loops have converged ("Pupil Tracking Loop" and "Actuator Alignment Loop" deltas less than 0.05 in the lab) stop the `Auto Alignment` loop.

 - In the lab the `Pupil Tracking Loop` should turn off when you stop the `Auto Alignment` loop.
 - On sky the `Pupil Tracking Loop` should remain on when you stop the `Auto Alignment` loop.

14. Adjust flux on `camwfs` using `flipwfsf` and `fwtelsim`, and set `camwfs` emgain

 - you may need to reset protection

15. take a camwfs dark

16. now close the loop, up to ~200 modes

 - bring up t/t, then focus, then higher order modes block by block
 - Once 10 modes are closed, increase Woofer Offloading to 10 modes

17. Now repeat the `Auto Alignment` steps above with the loop closed

18. Once the `Auto Alignment` has converged again, stop it.

19. Now perform the J test (see below).  Once the J test is complete, you need to re-align the `camwfs` pupils using the camera lens by hand.  Do not run `Auto Alignment` at this step.

20. You should now be able to close all modes.

Tweeter Pupil Alignment (F-Test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This does not need to be done if you have performed the `Auto Alignment`.

To manually align the pupil on the tweeter, we perform the F-Test (which is actually an R).

* **fwpupil** to **open** (in Coronagraph Alignment GUI)

* **fwfpm** to **open**

* **fwlyot** to **open**

* **fwscind** to **pupil** (in camsci1Ctrl)

* **fwsci1** to **z**

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

* Clear the J-test with the "zero test" button on the **Pupil Alignment GUI**

* Return ``stagesci1`` to the ``fpm`` position

Pyramid Pupil Alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have performed the `Auto Alignment` this only needs to be done after performaing the J-test.

* Using the directional buttons under the "Camera Lens" section to move the pupil images on camwfs until the "Avg:" x and y displacements are less than 0.05 pixels in the lab (0.1 pixels on-sky).

.. warning::

    The "pupil tracking loop" is not used in lab mode, only on-sky.

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

There are multiple ways to configure the algorithm (see :doc:`./software/utils/fdpr`), but we most commonly use the ``CH4-875`` filter in camsci1 to compute a correction applied to ``dmncpc``.

1. Configure fwsci1 with the narrowband methane filter ``CH4-875``
2. Place stagesci1 at preset ``fpm``
3. Define a :term:`ROI` centered on the core of the PSF
4. Adjust exposure times as needed to have plenty (25000--30000) of counts in the peak of the PSF
5. Close the shutter and take new darks. (Then open the shutter.)
6. Open a terminal on ICC
7. ``export OPENBLAS_NUM_THREADS=1`` to avoid bogging down ICC with the process (TODO: make this automatic)
8. Run the FDPR process with: ``fdpr2_close_loop fdpr2_dmncpc_camsci1_CH4``
9. Save the flat with ``dm_save_flat ncpc -d fdpr``
