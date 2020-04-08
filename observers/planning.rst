******************************
Planning your observations
******************************


Filters and Throughputs
=============================

Calculated filter characteristics and transmission curves are given below.  All are based on standard reflectivity or transmission data for various surfaces, unless a part specific curve was provided by the manufacturer.  No transmissive optics (ADCs, etc) are currently accounted for.

The atmosphere is included in the numbers presented in the table below.  BTRAM was used to calculate the atmospheric transmission for LCO, and the below values assume a zenith distance of 30 degrees and 5.0 mm PWV. A version of each curve is provided without the atmosphere contribution, which can then be combined with the atmosphere of your choice.

None of these values have been validated.  They should be used for planning purposes only.

Visible Science Cameras
=============================
Filters in the visible science cameras.

camsci1
--------------------

.. list-table::
   :header-rows: 1
   
   * - Filter
     - WFS B/S
     - Sci BS
     - :math:`\lambda_0` [\mum]
     - :math:`w_\mathrm{eff}` [\mum]
     - :math:`\mathrm{QE}_\mathrm{max}`
     - :math:`F_0` [photon / sec]
     - Files
   * - H-alpha Cont.
     - H-alpha/IR
     - H-alpha
     - 0.668
     - 0.009
     - 0.22
     - :math:`3.8\times10^{9}`
     - :static:`atm <ref/filters/magaox_sci1-halpha-cont_bs-halpha-ir_scibs-halpha_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-halpha-cont_bs-halpha-ir_scibs-halpha.dat>`
   * - ip
     - 65/35
     - ri
     - 0.764
     - 0.120
     - 0.11
     - :math:`2.1\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-ip_bs-65-35_scibs-ri_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-ip_bs-65-35_scibs-ri.dat>`
   * - zp
     - 65/35
     - ri
     - 0.908
     - 0.130
     - 0.08
     - :math:`1.3\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-zp_bs-65-35_scibs-ri_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-zp_bs-65-35_scibs-ri.dat>`
   * - rp
     - 65/35
     - open
     - 0.615
     - 0.110
     - 0.23
     - :math:`6.1\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-rp_bs-65-35_scibs-open_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-rp_bs-65-35_scibs-open.dat>`
   * - ip
     - 65/35
     - open
     - 0.762
     - 0.126
     - 0.11
     - :math:`2.2\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-ip_bs-65-35_scibs-open_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-ip_bs-65-35_scibs-open.dat>`
   * - zp
     - 65/35
     - open
     - 0.908
     - 0.131
     - 0.09
     - :math:`1.3\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-zp_bs-65-35_scibs-open_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-zp_bs-65-35_scibs-open.dat>`
   * - CH4
     - 65/35
     - 50/50
     - 0.875
     - 0.026
     - 0.04
     - :math:`1.3\times10^{9}`
     - :static:`atm <ref/filters/magaox_sci1-ch4_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-ch4_bs-65-35_scibs-5050.dat>`
   * - rp
     - 65/35
     - 50/50
     - 0.615
     - 0.112
     - 0.11
     - :math:`2.9\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-rp_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-rp_bs-65-35_scibs-5050.dat>`
   * - ip
     - 65/35
     - 50/50
     - 0.762
     - 0.126
     - 0.06
     - :math:`1.1\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci1-ip_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-ip_bs-65-35_scibs-5050.dat>`
   * - zp
     - 65/35
     - 50/50
     - 0.908
     - 0.130
     - 0.04
     - :math:`6.3\times10^{9}`
     - :static:`atm <ref/filters/magaox_sci1-zp_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci1-zp_bs-65-35_scibs-5050.dat>`

       
camsci2
----------------

.. list-table::
   :header-rows: 1

   * - Filter
     - WFS B/S
     - Sci BS
     - :math:`\lambda_0` [\mum]
     - :math:`w_\mathrm{eff}` [\mum]
     - :math:`\mathrm{QE}_\mathrm{max}`
     - :math:`F_0` [photon / sec]
     - Files
   * - H-alpha
     - H-alpha/IR
     - H-alpha
     - 0.656
     - 0.009
     - 0.23
     - :math:`3.5\times10^{9}`
     - :static:`atm <ref/filters/magaox_sci2-halpha_bs-halpha-ir_scibs-halpha_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci2-halpha_bs-halpha-ir_scibs-halpha.dat>`
   * - gp
     - 65/35
     - ri
     - 0.527
     - 0.041
     - 0.24
     - :math:`3.1\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci2-gp_bs-65-35_scibs-ri_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci2-gp_bs-65-35_scibs-ri.dat>`
   * - rp
     - 65/35
     - ri
     - 0.613
     - 0.106
     - 0.23
     - :math:`5.9\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci2-rp_bs-65-35_scibs-ri_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci2-rp_bs-65-35_scibs-ri.dat>`
   * - CH4 Cont.
     - 65/35
     - 50/50
     - 0.923
     - 0.023
     - 0.04
     - :math:`9.6\times10^{8}`
     - :static:`atm <ref/filters/magaox_sci2-ch4-cont_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci2-ch4-cont_bs-65-35_scibs-5050.dat>`
   * - gp
     - 65/35
     - 50/50
     - 0.525
     - 0.044
     - 0.13
     - :math:`1.9\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci2-gp_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci2-gp_bs-65-35_scibs-5050.dat>`
   * - rp
     - 65/35
     - 50/50
     - 0.614
     - 0.109
     - 0.12
     - :math:`3.3\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci2-rp_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci2-rp_bs-65-35_scibs-5050.dat>`
   * - ip
     - 65/35
     - 50/50
     - 0.762
     - 0.126
     - 0.06
     - :math:`1.1\times10^{10}`
     - :static:`atm <ref/filters/magaox_sci2-ip_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci2-ip_bs-65-35_scibs-5050.dat>`
   * - zp
     - 65/35
     - 50/50
     - 0.909
     - 0.132
     - 0.04
     - :math:`6.7\times10^{9}`
     - :static:`atm <ref/filters/magaox_sci2-zp_bs-65-35_scibs-5050_atm.dat>`
       :static:`noatm <ref/filters/magaox_sci2-zp_bs-65-35_scibs-5050.dat>`
   
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
     - :static:`noatm <ref/filters/magaox_wfs_bs-halpha-ir_atm.dat>`
       :static:`atm <ref/filters/filters/magaox_wfs_bs-halpha-ir.dat>`
   * - 65/35
     - open
     - 0.791
     - 0.296
     - 0.08
     - :math:`4.2 \times 10^{10}`
     - :static:`noatm <ref/filters/magaox_wfs-open_bs-65-35.dat>`
       :static:`atm <ref/filters/magaox_wfs-open_bs-65-35_atm.dat>`
       

LOWFS
=================

Filters in the low-order WFS.

Atmosphere
=================

Atmospheric transmission curves.
