Coronagraphs
=============================

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
     - scale in telescope pupil [m/pix]
     - scale at coronagraph pupil [mm/pix]
   * - open
     - No mask, just the telescope pupil.  Note: design file includes mask over bump.
     - 100%
     - :static:`magMask.fits.gz <coronagraph/lyot/magMask.fits.gz>`
     - 0.0067528
     - 0.0093501
   * - bump-mask 
     - Undersized pupil, oversized central obscuration, oversized spiders, and mask over bump
     - 86.75%
     - :static:`bumpMask.fits.gz <coronagraph/lyot/bumpMask.fits.gz>`
     - 0.0067528
     - 0.0093501
   * - fat-spider 
     - Same as bump-mask, but one extra-oversized spider.  Intended for kernel-phase type WFS. 
     - 
     -
     -
     - 
     
Focal Plane Masks
+++++++++++++++++++++++++++++    
There are two chrome dots on glass plates. Note: optical densities are estimated from standard chrome.


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
We have experimented with three Lyot stops with different characteristics.  The labels "Large" and "Small" here refer to the clear aperture, i.e. large means a large clear aperture and therefore higher throughput.  In practice we have used only `LyotLg1` for observations. `LyotSm` is
presently removed from the instrument.

.. list-table:: LyotLg1
   :header-rows: 1

   * - parameter
     - value
     - notes
   * - fwlyot Position 
     - LyotLg1 
     -
   * - Throughput
     - 63.8%
     - not incl. FPM 
   * - Image 
     - .. image:: figures/coronagraph_LyotLg1.png
     -
   * - Outer Diam.
     - 7.020 mm 
     - at 9 mm pupil plane 
   * - Inner Diam.
     - 4.620 mm 
     -
   * - Spider Width
     - 0.383 mm 
     -
   * - Bump Diam 
     - 1.149 mm 
     -
   * - FITS file 
     - :static:`lyotMaskLarge1.fits.gz <coronagraph/lyot/lyotMaskLarge1.fits.gz>`
     - 
   * - FITS scale at M1 
     - 0.0067528
     - m/pixel 
   * - FITS scale at fwlyot 
     - 0.0093501
     - 0.0093501
   * - DXF File 
     - :static:`LyotStop_large1.DXF <coronagraph/lyot/LyotStop_large1.DXF>`
     -

.. list-table:: LyotLg2
   :header-rows: 1

   * - parameter
     - value
     - notes
   * - fwlyot Position 
     - LyotLg2
     -
   * - Throughput
     - 57.3%
     - not incl. FPM 
   * - Image 
     - .. image:: figures/coronagraph_LyotLg2.png
     -
   * - Outer Diam.
     - 8.041 mm 
     - at 9 mm pupil plane 
   * - Inner Diam.
     - 3.600 mm 
     -
   * - Spider Width
     - 0.383 mm
     -
   * - Bump Diam 
     - 1.149 mm
     -
   * - FITS file 
     - :static:`lyotMaskLarge2.fits.gz <coronagraph/lyot/lyotMaskLarge2.fits.gz>`
     - 
   * - FITS scale at M1 
     - 0.0067528
     - m/pixel 
   * - FITS scale at fwlyot 
     - 0.0093501
     - 0.0093501
   * - DXF File 
     - :static:`LyotStop_large2.DXF <coronagraph/lyot/LyotStop_large2.DXF>`
     -

.. list-table:: LyotSm
   :header-rows: 1

   * - parameter
     - value
     - notes
   * - fwlyot Position 
     - LyotSm
     - removed from instrument
   * - Throughput
     - 33.35%
     - not incl. FPM 
   * - Image 
     - .. image:: figures/coronagraph_LyotSm.png
     -
   * - Outer Diam.
     - 7.800 mm 
     - at 9 mm pupil plane 
   * - Inner Diam.
     - 3.800 mm 
     -
   * - Spider Width
     - 0.383 mm
     -
   * - Bump Diam 
     - 1.149 mm
     -
   * - FITS file 
     - :static:`lyotMaskSmall.fits.gz <coronagraph/lyot/lyotMaskSmall.fits.gz>`
     - 
   * - FITS scale at M1 
     - 0.0067528
     - m/pixel 
   * - FITS scale at fwlyot 
     - 0.0093501
     - 0.0093501
   * - DXF File 
     - :static:`LyotStop_small.DXF <coronagraph/lyot/LyotStop_small.DXF>`
     -


     
PIAA Classical Lyot Coronagraph (PIAACLC)
------------------------------------------
Phase-induced amplitude apodization (PIAA) optics reshape the beam in the pupil and focal planes, enabling more starlight suppression at low angular separations and higher throughput at large angular separations.

Inverse apodization optics after the focal plane mask correct for off-axis field effects to remove comatic distortions on companions. Inverse PIAA optics are identical to forward PIAA optics. Optical path according to naming convention is PIAA0->PIAA1->fpm->iPIAA1->iPIAA0.

The process of pupil remapping before and after the focal plane is illustrated in Guyon et al 2010:

.. image:: figures/coronagraph_Guyon_2010_PIAALC.png
   :alt: Drawing of pupil remapping

.. list-table:: PIAA optics
   :header-rows: 1
  
   * - Optic name
     - Clear aperture diameter (mm)
     - design file
     - scale in pupil [m/pix]
     - Height map (um)
   * - PIAA0
     - 10
     - :static:`piaa0.fits.gz <figures/coronagraph_piaa0.fits.gz>`
     - 0.151e-5
     - .. image:: figures/coronagraph_PIAA0.png
   * - PIAA1
     - 10
     - :static:`piaa0.fits.gz <figures/coronagraph_piaa0.fits.gz>`
     - 0.151e-5
     - .. image:: figures/coronagraph_PIAA1.png
     
     
Coronagraph performance simulations
------------------------------------------

.. list-table:: 
   :header-rows: 1
   
   * - 656nm simulations (λ/D = 20.81marcsec, BW = 651nm-661nm) 
     - 900nm simulations (λ/D = 28.56marcsec, BW = 855nm-945nm)
   * - .. image:: figures/coronagraph_throughput_656.png
            :alt: Throughput for different coronagraph arrangements at 656nm
     - .. image:: figures/coronagraph_throughput_900.png
            :alt: Throughput for different coronagraph arrangements at 900nm
   * - .. image:: figures/coronagraph_contrast_656.png
            :alt: Throughput for different coronagraph arrangements at 656nm
     - .. image:: figures/coronagraph_contrast_900.png
            :alt: Contrast for different coronagraph arrangements at 900nm
   * - .. image:: figures/coronagraph_SNR_poisson_656.png
            :alt: Inverse-Poisson SNR equivalent for different coronagraph arrangements at 656nm
     - .. image:: figures/coronagraph_SNR_poisson_900.png
            :alt: Inverse-Poisson SNR equivalent for different coronagraph arrangements at 900nm 
   * - .. image:: figures/coronagraph_SNR_speckle_656.png
            :alt: Inverse-Speckle SNR equivalent for different coronagraph arrangements at 656nm
     - .. image:: figures/coronagraph_SNR_speckle_900.png
            :alt: Inverse-Speckle SNR equivalent for different coronagraph arrangements at 900nm           
   * - :static:`Simulated throughput data for 656nm <figures/coronagraph_throughput_656.csv>`
     - :static:`Simulated throughput data for 900nm <figures/coronagraph_throughput_900.csv>`
   * - :static:`Simulated contrast data for 656nm <figures/coronagraph_contrast_656.csv>`
     - :static:`Simulated contrast data for 900nm <figures/coronagraph_contrast_900.csv>`


Vector Apodizing Phase Plate (vAPP)
-----------------------------------

To be documented.

