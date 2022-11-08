Data reduction and calibration
==============================

Sky orientation & pixel scale
-----------------------------

The as-designed pixel scale is 6 milliarcseconds per pixel in camsci1 and camsci2. The exact plate scale and distortion solution can potentially change by a small amount each time MagAO-X is (re-)installed at the telescope. We perform calibration observations to determine these values, and the detailed values for each run are (or will be) listed below.

2022B
^^^^^

To place north-up-east-left, rotate them CCW by ``PARANG``.
For data taken after October 2022, it is not necessary to flip either ``camsci1`` or ``camsci2`` image orientation .

*Astrometric solution TBD.*

2022A
^^^^^

For data taken in 2022A: both ``camsci1`` and ``camsci2`` images should be flipped left-to-right (i.e. in X) before analysis.
To get north-up-east-left, you should rotate counter-clockwise by the angle given in ``PARANG`` in the headers after any necessary flips.

*Astrometric solution TBD.*

2019B
^^^^^

For data taken in 2019B: ``camsci1`` frames should be flipped left-to-right. (i.e. in X). ``camsci2`` images do not need to be flipped.
To get north-up-east-left, you should rotate counter-clockwise by the angle given in ``PARANG`` in the headers after any necessary flips.

*Astrometric solution TBD.*