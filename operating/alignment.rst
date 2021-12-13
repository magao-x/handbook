Alignment
===================================

System Pupil Alignment
-----------------------------------

Tweeter Pupil Alignment (F-Test)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To align the pupil on the tweeter, we perform the F-Test.

Prepare the system:

* **fwpupil.filterName** in open

* **fwfpm.filterName** in **flat**

* **stagelosel.presetName** in **pupil**

* **fwlowfs.filterName** in **z** (or whichever filter works the best for conditions)

* configure **camlowfs** so that you can see the pupil without saturating.

* as needed, move **stagelowfs** to focus the pupil image.  You want to be somewhat out of focus to see the test pattern well.

Now put the test pattern on the tweeter with the dmCtrl GUI for dmtweeter.  Press the **load test** button (if not already done) and then **set test**.

Next, use the "Pupil Steering" section of the pupilguideGUI to align the pupil on the tweeter using the arrow keypad .  The following figure demonstrateds what a good alignment looks like.  

.. image:: f-test-good.png
    :width: 500
    :align: center
    
Note that you may need to change the focus by moving **stagelowfs**.

When done, press the **zero test** button on dmCtrl GUI for dmtweeter.

Pyramid Alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Coronagraph Alignment
------------------------------------

Due to their (lack of) intrinsic repeatability, the three wheels holding the coronagraph components must be adjusted every time they are moved.  Aligning the coronagraph should proceed in the following order so that wheels do not need to be moved after adjustment.  The first step "Pupil Mask Alignment" *should be conducted every time the system is started up*.

Also note that the pupil imaging optics are not repeatable, so if the fwscind lens is moved, or the stagelosel position is changed, the pupil will appear to shift.  This does not mean the pupil has actually shifted, but will complicate checking pupil positions.

Pupil Mask Alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Find and mark the pupil position on **camlowfs**:

* **fwpupil.filterName** in **open**

* **fwfpm.filterName** in **flat**

* **stagelosel.presetName** in **pupil**

* **fwlowfs.filterName** in **z** 

* **camlowfs** settings can be adjusted.  Typical settings are
  
  - **exptime** = **0.05**
  
  - **readout_speed** = **emccd_17MHz**
  
  - **vshift_speed** = **3_3us**

* **camlowfs.shutter** to **open**

* adjust **stagelowfs** until features are sharp (spiders and bump).  Being slightly out of focus helps locate the bump effects.

* mark the unobstructed pupil location.  The below figure shows a typical example on **camlowfs**

.. image:: camlowfs_tgt.png
    :width: 500
    :align: center
    
Now align the desired pupil mask.  First select the presets for the mask:

* **fwpupil.filterName** in desired position (e.g. **bump-mask**)

* **picomotors.picopupil** in desired position (matching **fwpupil**)

Now open coronaAlignGUI and use the "Pupil Plane" buttons to move the mask.  The following figure shows a typical exampe of bump-mask alignment

.. image:: bump-mask_aligned.png
    :width: 500
    :align: center
    
Do not move fwpupil anymore.

Lyot Stop Alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Set **fwfpm.filterName**: 

- if you are using the Lyot FPM, or any other transmissive FP optic:

    + select the desired mask
    
    + **stagelosel.presetName** = fpm
    
    + using the coronaAlignGUI "Lyot Plane" left-right buttons, move the spot so it is not obstructing the beam.  You will see two approx equal images (one is a ghost).
    
    + adjust **dmncp** focus using such that the spots are roughly in focus. 
    
    + note that you may need to adjust **camlowfs** due to saturation
 
 - otherwise, select **open**
 
* **fwscind.filterName** = **pupil**

* **stagescibs** = **none** (any position will actually work)

* **fwsci1.filterName** = **CH4-875**

* **fwlyot.filterName** = **open**

* adjust **stagelowfs** until features are well defined.

* mark the unobstructed pupil location.

Now select the desired Lyot mask:

* **fwlyot.filterName** = **LyotLg1** (e.g.)

* **picomotors.picolyot** = **LyotLG1** (e.g.)

and adjust Lyot Plane with coronaAlignGUI until aligned.  See the below figure:

.. image:: fwlyot_lyotlg1_aligned.png
    :width: 500
    :align: center
    
Focal Plane Mask Alignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **fwscind.filterName** = **open**

- **fwfpm.filterName** = **LyotLg** (or desired mask)

- **picomotors.picofpm** = **LyotLg** (or desired mask)

- **stagelosel.presetName** = **fpm**

- center **camlowfs** ROI on lower spot.  32x32 may be necessary to avoid saturation

- center **camsci1** on the image.  Once on the spot it should not be saturating in default parameters.

Now adjust Focal Plane with coronaAlignGUI until aligned.  The post-coronagraph image on **camsci1** is the best indication of good alignment. Note that **dmncpc** also impacts alignment, and until it is also optimized you will probably find a dead band where FPM wheel alignment makes no difference.  The below image illustrates this condition:

.. image:: fpm_aligned_pre_eye-doctor.png
    :width: 500
    :align: center

Now run eye-doctor to optimize the FPM alignment with the following command 

.. code::

   [icc]$ dm_eye_doctor 7624 ncpcModes camlowfs 3 2...10 0.1

The following image illustrates a fairly good alignment of the Lyot coronagraph system:

.. image:: fpm_aligned_post_eye-doctor.png
    :width: 500
    :align: center

