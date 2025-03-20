Alignment
===================================

System Pupil Alignment
-----------------------------------

Tweeter Pupil Alignment (F-Test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To align the pupil on the tweeter, we perform the F-Test (which is actually an R).

Prepare the system as in :doc:`daily_startup`, then configure:

* **fwpupil** to **open**

* **fwfpm** to **open**

* **fwlyot** to **open**

* **fwscind** to **pupil**

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

Pyramid Alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Alignment GUI, Tip Alignment should show "move woofer" above the directional buttons. Use the directional buttons to try and get all four pyramid pupils uniformly illuminated.

Using the directional buttons under the "Pupil Fitting" section to move the pupil images on camwfs until the "Avg:" x and y displacements are less than 0.1 pixel.

.. warning::

    The "pupil tracking loop" is not used in lab mode, only on-sky.

Close loop and refine pupil alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In a terminal on RTC/exao2, change directories to the CACAO "rootdir" in ``/opt/MagAOX/cacao/tweeter-vispyr/tweeter-vispyr-rootdir``.

If CACAO is not yet started, the command ``/opt/MagAOX/cacao/startup`` will start it. The command ``cacao-calib-apply default`` makes symlinks expected by CACAO and loads appropriate references, and may be needed as well.

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

**Continue improving PSF quality with :doc:`software/fdpr`**