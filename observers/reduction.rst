Data reduction and calibration
==============================

Sky Orientation
---------------

For data taken in Oct 2022 or later, the ``camsci1`` and ``camsci2`` images no longer need to be flipped left-to-right.  For north-up-east-left rotate CCW by ``PARANG``.

For data taken in 2022A: both ``camsci1`` and ``camsci2`` images are flipped
left-to-right (i.e. in X). To get north-up-east-left, flip the images
left-to-right, then rotate counter-clockwise by the angle given in
``PARANG`` in the headers.


*Additional information TODO*
