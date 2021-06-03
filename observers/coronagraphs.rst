Coronagraphs
=============================

Vector Apodizing Phase Plate (vAPP)
-----------------------------------

To be documented.


Classical Lyot
-----------------------------

Pupil Masks
+++++++++++++++++++++++++++++
Two pupil masks are currently available, in addition to "open" (no mask).

.. list-table:: Coronagraph Pupil Masks
   :header-rows: 1
  
   * - fwpupil Position
     - Description
     - abs. throughput
     - design file
     - file scale [m/pix]
   * - open
     - No mask, just the telescope pupil.  Note: design file includes mask over bump.
     - 100%
     - :static:`magMask.fits.gz <coronagraph/lyot/magMask.fits.gz>`
     - 0.0067528
   * - bump-mask 
     - Undersized pupil, oversized central obscuration, oversized spiders, and mask over bump
     - 86.75%
     - :static:`bumpMask.fits.gz <coronagraph/lyot/bumpMask.fits.gz>`
     - 0.0067528
   * - fat-spider 
     - Same as bump-mask, but one extra-oversized spider.  Intended for kernel-phase type WFS. 
     - 
     -
     -
     
Focal Plane Masks
+++++++++++++++++++++++++++++    
There are two chrome dots on glass plates. Note: optical densitties are estimated from standard chrome.


Small spot: 272 um diameter.
fwfpm position: `lyotsm`

.. list-table:: lyotsm characteristics
   :header-rows: 1
  
   * - lambda [um]
     - spot size [lam/D]
     - opt. dens.
   * - 0.600
     - 3.285
     - 5.0
   * - 0.656
     - 3.00
     - 4.75
   * - 0.700
     - 2.82
     - 4.56
   * - 0.800
     - 2.46
     - 4.11
   * - 0.900
     - 2.19
     - 3.67
   * - 1.000
     - 1.97
     - 3.22

Large spot: 453 um diameter.
fwfpm position: `lyotlg`

.. list-table:: lyotlg characteristics
   :header-rows: 1
  
   * - lambda [um]
     - spot size [lam/D]
     - opt. dens.
   * - 0.600
     - 5.47
     - 5.0
   * - 0.656
     - 5.00
     - 4.75
   * - 0.700
     - 4.69
     - 4.56
   * - 0.800
     - 4.10
     - 4.11
   * - 0.900
     - 3.65
     - 3.67
   * - 1.000
     - 3.28
     - 3.22
     
     
Lyot Stops
+++++++++++++++++++++++++++++    
     
.. list-table:: Lyot Stops
   :header-rows: 1
  
   * - fwlyot Position
     - Description
     - abs. throughput
     - design file
     - file scale [m/pix]
   * - LyotLg1
     - Lyot Large 1
     - 63.82%
     - :static:`lyotMaskLarge1.fits.gz <coronagraph/lyot/lyotMaskLarge1.fits.gz>`
     - 0.0067528
   * - LyotLg2 
     - Lyot Large 2
     - 57.32
     - :static:`lyotMaskLarge2.fits.gz <coronagraph/lyot/lyotMaskLarge2.fits.gz>`
     - 0.0067528
   * - LyotSm
     - Lyot Small
     - 33.35%
     - :static:`lyotMaskSmall.fits.gz <coronagraph/lyot/lyotMaskSmall.fits.gz>`
     - 0.0067528
     
     
Phase Apodized Pupil Lyot Coronagraph
--------------------------------------

To be documented.
