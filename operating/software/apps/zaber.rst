Zaber Stages
========================


homing
---------------

The zaber stages should normally be powered off to avoid heating the instrument.  The software remembers the state of
stages between power cycles.

If you need to move a zaber stage, the first thing you need to do is power-on the stages.  These are controlled from the
"ninja" tab of `pwrGUI`.  Most zaber stages are powered from `stagezaber`, remember that you need to power-on both
`pdu2.stagezaber` and `usbdu1.stagezaber`.  Once the stages are powered on, the software will connect automatically.  You
do not need to home every time they are powered on.  Simply move the stage to where you want it and then power off.

It is best to power off a stage system from the `pdu` before powering off from the associated `usbdu`.

The stages do need to be homed periodically to acquire a reference position to ensure that positions are accurate.  Currently
we want to do this once per day.  The `labrules` will issue a `caution`` when it has been more than 22 hours since the stages were
last homed.  To home the stages, first power them off.  While you can home the individual stages one-by-one, there is a `home_all`
request switch in the low-level process that will issue a home command to all the stages at once.  For instance, for the main zaber
system use `cursesINDI` to toggle `zaberLowLevel.home_all.request`.  Once homing is complete, power-off.

Always power off as soon as you are done using the stages.
If the zaber stages are powered-on for more than 10 minutes `labrules` will warn you.



control system
------------------

Zaber Stages are controlled by apps derived from the
`stdMotionStage <https://github.com/magao-x/MagAOX/blob/master/libMagAOX/app/dev/stdMotionStage.hpp>`__
implementation, meaning they share some common properties and options.
