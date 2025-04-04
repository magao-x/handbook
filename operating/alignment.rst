Alignment
===================================

System Pupil Alignment
-----------------------------------
The following procedures make use of the **Pupil Alignment GUI** shown below:

.. image:: figures/alignment_gui.png
    :width: 750
    :align: center

| 
Tweeter Pupil Alignment (F-Test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To align the pupil on the tweeter, we perform the F-Test (which is actually an R).

Prepare the system as in :doc:`daily_startup`, then in **Coronagraph Alignment GUI**, configure:

* **fwpupil** to **open**

* **fwfpm** to **open**

* **fwlyot** to **open**

The figure below shows the **Coronagraph Alignment GUI**:

.. image:: figures/coro_alignment_gui.png
    :width: 750
    :align: center

| 
In camsci1Ctrl:

* **fwscind** to **pupil**

* **fwsci1** to **z** (in almost all cases you should align in ``z`` for repeatability)

* configure **camsci1** so that you can see the pupil without saturating.

* Move **stagesci1** to preset **fpm**.

The camsci1Ctrl GUI is shown below:

.. image:: figures/camsci1_gui.png
    :width: 500
    :align: center
|
Now put the test pattern on the tweeter with **Pupil Alignment GUI** for dmtweeter.  Press the **set test** under **Tweeter**

Next, use the "TTM Pupil" section to align the pupil on the tweeter using the arrow keypad .  The following figure demonstrates what a good alignment looks like.

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

* In the **Pupil Alignment GUI**, Tip Alignment should show "move woofer" above the directional buttons. Use the directional buttons to try and get all four pyramid pupils uniformly illuminated.

* Use the directional buttons under the "TTM Pupil" section to move the pupil images on camwfs until the "Avg:" x and y displacements are less than 0.1 pixel.

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

Bump Mask Alignment
-------------------

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

**Continue improving PSF quality with `FDPR <./software/utils/fdpr>`__**

Following FDPR, you should end up with a near diffraction-limited PSF that looks like this:

.. image:: figures/fdpr_psf.png
   :width: 500
   :align: center

|
Coronagraph Alignment
---------------------

Knife Edge Alignment
~~~~~~~~~~~~~~~~~~~~~

From the **Coronagraph Alignment GUI**: set **fwfpm** to **knifemask**.

In **camsci1Ctrl**, change: 

* **ROI** to **512x512** and take a closed-shutter dark
* **fwscind** to **ND1** 
 
This will make the knife edge easier to align.

Use the "Focal Plane" directional buttons on the coronagraph alignment GUI to bring the knife edge into view.

Once the knife edge is relatively close to the PSF, click the camsci1 display and press **s** to monitor the PSF pixel counts.

Once the pixel counts drop to about 3-4000, the knife edge is sufficiently aligned as shown below:

.. image:: figures/knife_edge_img.png
   :width: 500
   :align: center

|
Lyot Stop Alignment
~~~~~~~~~~~~~~~~~~~~~
In **camsci1Ctrl**, change:

* **fwscind** to **pupil**
* **stagesci1** to **lyotlG-50/50**

Now take an **open-shutter** dark frame.

In the coronagraph alignment GUI, change **fwlyot** to your stop of choice (typically **LyotLg1**).

Use the "Lyot Plane" directional buttons to center the Lyot stop on the pupil. 

Below is an image of the **LyotLg1** stop after it has been aligned:

.. image:: figures/lyot_stop_img.png
   :width: 500
   :align: center

Congrats! You now have an aligned knife edge coronagraph!