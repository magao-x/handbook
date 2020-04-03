******************************
Planning your observations
******************************

Filters and Throughputs
=============================

Calculated filter characteristics and transmission curves are given below.  All are based on standard reflectivity or transmission data for various surfaces, unless a part specific curve was provided by the manufacturer.  No transmissive optics (ADCs, etc) are currently accounted for.

The atmosphere is included in the numbers presented in the table below.  BTRAM was used to calculate the atmospheric transmission for LCO, and the below values assume a zenith distance of 30 degrees and 5.0 mm PWV. A version of each curve is provided without the atmosphere contribution, which can then be combined with the atmosphere of your choice.

None of these values have been validated.  They should be used for planning purposes only.

Science
=============================
Filters in the science cameras.

camsci1
--------------------

.. list-table::
   :header-rows: 1

   * - WFS B/S
     - Pupil
     - Sci-BS
     - Filter
     - :math:`\lambda_0` [µm]
     - :math:`w_\mathrm{eff}` [µm]
     - :math:`\mathrm{QE}_\mathrm{max}`
     - :math:`F_0` [photon / sec]
     - Files
   * - H-alpha/IR
     - open
     - H-alpha
     - Ha-cont
     - 0.668
     - 0.0086
     - 0.22
     - :math:`3.8 \times 10^9`
     - :static:`atm <ref/filters/magaox_sci-halpha-cont_bs-halpha-ir_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci-halpha-cont_bs-halpha-ir.dat>`
   * - 65/35
     - open
     - 50/50
     - CH4
     - 0.875
     - 0.025
     - 0.043
     - :math:`1.3 \times 10^9`
     - :static:`atm <ref/filters/magaox_sci-ch4_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci-ch4_bs-65-35_atm.dat>`
   * - 65/35
     - open
     - 50/50
     - r'
     - 0.614
     - 0.104
     - 0.12
     - :math:`3.0 \times 10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-rp_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci1-rp_bs-65-35_atm.dat>`
   * - 65/35
     - open
     - 50/50
     - i'
     - 0.762
     - 0.129
     - 0.055
     - :math:`1.1 \times 10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-ip_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci1-ip_bs-65-35_atm.dat>`
   * - 65/35
     - open
     - 50/50
     - z'
     - 0.910
     - 0.140
     - 0.042
     - :math:`6.7 \times 10^{9}`
     - :static:`atm <ref/filters/magaox_sci1-zp_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci1-zp_bs-65-35_atm.dat>`
       
camsci2
----------------

.. list-table::
   :header-rows: 1
   
   * - WFS B/S
     - Pupil
     - Sci-BS
     - Filter
     - :math:`\lambda_0` [µm]
     - :math:`w_\mathrm{eff}` [µm]
     - :math:`\mathrm{QE}_\mathrm{max}`
     - :math:`F_0` [photon / sec]
     - Files
   * - H-alpha/IR
     - open
     - H-alpha
     - H-alpha
     - 0.656
     - 0.0085
     - 0.23
     - :math:`3.5 \times 10^9`
     - :static:`atm <ref/filters/magaox_sci-halpha_bs-halpha-ir_atm.dat>`
       :static:`noatm <ref/filters/filters/magaox_sci-halpha_bs-halpha-ir.dat>`
   * - 65/35
     - open
     - 50/50
     - CH4-cont
     - 0.923
     - 0.023
     - 0.037
     - :math:`9.6 \times 10^8`
     - :static:`atm <ref/filters/magaox_sci-ch4-cont_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci-ch4-cont_bs-65-35_atm.dat>`
   * - 65/35
     - open
     - 50/50
     - g'
     - 0.524
     - 0.044
     - 0.14
     - :math:`1.9 \times 10^{10}`
     - :static:`atm <ref/filters/magaox_sci2-gp_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci2-gp_bs-65-35_atm.dat>`
   * - 65/35
     - open
     - 50/50
     - r'
     - 0.613
     - 0.103
     - 0.14
     - :math:`3.4 \times 10^{10}`
     - :static:`atm <ref/filters/magaox_sci2-rp_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci2-rp_bs-65-35_atm.dat>`
   * - 65/35
     - open
     - 50/50
     - i'
     - 0.762
     - 0.130
     - 0.058
     - :math:`1.2 \times 10^{10}`
     - :static:`atm <ref/filters/magaox_sci2-ip_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci2-ip_bs-65-35_atm.dat>`
   * - 65/35
     - open
     - 50/50
     - z'
     - 0.911
     - 0.142
     - 0.045
     - :math:`7.3 \times 10^{9}`
     - :static:`atm <ref/filters/magaox_sci2-zp_bs-65-35.dat>`
       :static:`noatm <ref/filters/magaox_sci2-zp_bs-65-35_atm.dat>`       
   
WFS
=================

Filters in the main WFS.

.. list-table::
   :header-rows: 1
   
   * - WFS B/S
     - Filter
     - :math:`\lambda_0` [µm]
     - :math:`w_\mathrm{eff}` [µm]
     - :math:`\mathrm{QE}_\mathrm{max}`
     - :math:`F_0` [photon / sec]
     - Files
   * - H-alpha/IR
     - open
     - 0.837
     - 0.205
     - 0.20
     - :math:`5.3 \times 10^{10}`
     - :static:`atm <ref/filters/magaox_wfs_bs-halpha-ir_atm.dat>`
       :static:`noatm <ref/filters/filters/magaox_wfs_bs-halpha-ir.dat>`
   * - 65/35
     - open
     - 0.791
     - 0.296
     - 0.08
     - :math:`4.2 \times 10^{10}`
     - :static:`atm <ref/filters/magaox_wfs-open_bs-65-35.dat>`
       :static:`noatm <ref/filters/filters/magaox_wfs-open_bs-65-35_atm.dat>`
       

LOWFS
=================

Filters in the low-order WFS.

Atmosphere
=================

Atmospheric transmission curves.
