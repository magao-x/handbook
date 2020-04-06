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
     - :static:`atm <magaox_sci1-halpha-cont_bs-halpha-ir_scibs-halpha.dat>`
       :static:`noatm <magaox_sci1-halpha-cont_bs-halpha-ir_scibs-halpha_atm.dat>`
   * - ip
     - 65/35
     - ri
     - 0.764
     - 0.124
     - 0.11
     - :math:`2.1\times10^{10}`
     - :static:`atm <magaox_sci1-ip_bs-65-35_scibs-ri.dat>`
       :static:`noatm <magaox_sci1-ip_bs-65-35_scibs-ri_atm.dat>`
   * - zp
     - 65/35
     - ri
     - 0.910
     - 0.141
     - 0.08
     - :math:`1.3\times10^{10}`
     - :static:`atm <magaox_sci1-zp_bs-65-35_scibs-ri.dat>`
       :static:`noatm <magaox_sci1-zp_bs-65-35_scibs-ri_atm.dat>`
   * - rp
     - 65/35
     - open
     - 0.615
     - 0.111
     - 0.23
     - :math:`6.2\times10^{10}`
     - :static:`atm <magaox_sci1-rp_bs-65-35_scibs-open.dat>`
       :static:`noatm <magaox_sci1-rp_bs-65-35_scibs-open_atm.dat>`
   * - ip
     - 65/35
     - open
     - 0.762
     - 0.130
     - 0.11
     - :math:`2.3\times10^{10}`
     - :static:`atm <magaox_sci1-ip_bs-65-35_scibs-open.dat>`
       :static:`noatm <magaox_sci1-ip_bs-65-35_scibs-open_atm.dat>`
   * - zp
     - 65/35
     - open
     - 0.910
     - 0.141
     - 0.09
     - :math:`1.4\times10^{10}`
     - :static:`atm <magaox_sci1-zp_bs-65-35_scibs-open.dat>`
       :static:`noatm <magaox_sci1-zp_bs-65-35_scibs-open_atm.dat>`
   * - CH4
     - 65/35
     - 50/50
     - 0.875
     - 0.026
     - 0.04
     - :math:`1.3\times10^{9}`
     - :static:`atm <magaox_sci1-ch4_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci1-ch4_bs-65-35_scibs-5050_atm.dat>`
   * - rp
     - 65/35
     - 50/50
     - 0.615
     - 0.112
     - 0.11
     - :math:`2.9\times10^{10}`
     - :static:`atm <magaox_sci1-rp_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci1-rp_bs-65-35_scibs-5050_atm.dat>`
   * - ip
     - 65/35
     - 50/50
     - 0.762
     - 0.129
     - 0.06
     - :math:`1.1\times10^{10}`
     - :static:`atm <magaox_sci1-ip_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci1-ip_bs-65-35_scibs-5050_atm.dat>`
   * - zp
     - 65/35
     - 50/50
     - 0.910
     - 0.140
     - 0.04
     - :math:`6.7\times10^{9}`
     - :static:`atm <magaox_sci1-zp_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci1-zp_bs-65-35_scibs-5050_atm.dat>`
       
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
     - :static:`atm <magaox_sci2-halpha_bs-halpha-ir_scibs-halpha.dat>`
       :static:`noatm <magaox_sci2-halpha_bs-halpha-ir_scibs-halpha_atm.dat>`
   * - gp
     - 65/35
     - ri
     - 0.507
     - 0.061
     - 0.24
     - :math:`5.0\times10^{10}`
     - :static:`atm <magaox_sci2-gp_bs-65-35_scibs-ri.dat>`
       :static:`noatm <magaox_sci2-gp_bs-65-35_scibs-ri_atm.dat>`
   * - rp
     - 65/35
     - ri
     - 0.613
     - 0.106
     - 0.23
     - :math:`5.9\times10^{10}`
     - :static:`atm <magaox_sci2-rp_bs-65-35_scibs-ri.dat>`
       :static:`noatm <magaox_sci2-rp_bs-65-35_scibs-ri_atm.dat>`
   * - CH4 Cont.
     - 65/35
     - 50/50
     - 0.924
     - 0.025
     - 0.04
     - :math:`1.1\times10^{9}`
     - :static:`atm <magaox_sci2-ch4-cont_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci2-ch4-cont_bs-65-35_scibs-5050_atm.dat>`
   * - gp
     - 65/35
     - 50/50
     - 0.497
     - 0.080
     - 0.13
     - :math:`3.8\times10^{10}`
     - :static:`atm <magaox_sci2-gp_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci2-gp_bs-65-35_scibs-5050_atm.dat>`
   * - rp
     - 65/35
     - 50/50
     - 0.614
     - 0.110
     - 0.12
     - :math:`3.3\times10^{10}`
     - :static:`atm <magaox_sci2-rp_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci2-rp_bs-65-35_scibs-5050_atm.dat>`
   * - ip
     - 65/35
     - 50/50
     - 0.762
     - 0.130
     - 0.06
     - :math:`1.2\times10^{10}`
     - :static:`atm <magaox_sci2-ip_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci2-ip_bs-65-35_scibs-5050_atm.dat>`
   * - zp
     - 65/35
     - 50/50
     - 0.911
     - 0.142
     - 0.05
     - :math:`7.3\times10^{9}`
     - :static:`atm <magaox_sci2-zp_bs-65-35_scibs-5050.dat>`
       :static:`noatm <magaox_sci2-zp_bs-65-35_scibs-5050_atm.dat>`
   
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
