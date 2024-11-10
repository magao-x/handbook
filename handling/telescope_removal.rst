Removing MagAO-X from the Telescope
===================================

This procedure describes how to remove the MagAO-X instrument on the
Magellan Clay Telescope.

Estimated Time to Complete: 2 hours

This document can be downloaded as a PDF: :static:`Removing MagAO-X from the Telescope <handling/telescope_removal.pdf>`

Initial Conditions
------------------

-  Instrument on Magellan Clay Nasmyth Platform, operating.

.. _tel_remove_shutdown::

Shutdown
------------

-  At the end of the last night, have the TO position the telescope so that the NASE platform faces the elevator.

-  Power down all of MagAO-X

   - Ensure that ``stagepickoff`` is in the ``tel`` position.
   - Place the k-mirror at 0 degrees.
   - Select the Ha-narrow and CH4-875 filters on fwsci1/2
   - turn off power for all devices on MagAO-X following the regular shutdown procedure.
   - use the ``shutdown -h now`` command to halt both RTC and ICC
   - once the computers are off, turn off all things in the rack.

-  Remove blower hose and cover the hole.

-  Remove all cables

   -  See :ref:`detailed procedure <bmc_dm_cabling>` for removing MEMS DM cables

-  Electronics Rack

   -  Ensure that roll-out shelves are restrained
   -  Power off the UPS located in the electronics rack
   -  Close and lock doors
   -  Tape keys down

-  Instrument

   -  Install window cover
   -  Remove eyepiece
   -  Remove bumpers and pusher hardware
   -  Remove air connection
   -  Remove the PEPS II
   -  Tape over any exposed holes (from cables, etc)
   -  Secure any loose cables
   -  Shrink wrap the instrument
   -  Install solar blanket over shrink wrap

-  Cart and Rigging

   -  Verify all cart hardware is in-hand
   -  Verify two wire harnesses are in-hand

Rig Onto Cart
-------------

-  Lower table legs onto the casters by turning the 16 leveling bolts,
   and remove the metal pads

-  Roll the instrument away from the telescope

-  Assemble the cart around the instrument

   -  **CAUTION:** be careful to not bump the legs with the cart

-  The 8 large bolts on the cart should just be touching the washers, but the washers should still spin.

-  Attach the lifting wire-harness to each side of the cart

-  Attach the load spreader with straight extensions to the crane,
   using a crane scale

   .. image:: figures/load_spreader_attach.jpg

   *The load spreader attached to the crane for lifting the cart*

-  Place the load spreader in the center position (the cart is
   symmetric)

-  Lift the load spreader, and position it over the instrument

-  Being careful to not bump the instrument, lower the load spreader
   and attach the lifting harness D rings. Use 4x shackles to extend the
   length to reach the cart on the floor.

   .. image:: figures/cart_lift_extensions.jpg

   *Lifting harnesses attached with shackle extensions*

-  Position a person at each end of the cart

   **CAUTION:** Do not allow the cart to bump the legs or the table
   uncontrolled

-  Slowly lift the cart (**320 lbs**) until it is touching the bottom
   of the table

   .. image:: figures/cart_lift_tofrom_table.jpg

   *The cart being lifted to the bottom of the table.*

-  Install the 4 bolts attaching the cart to the table.  Use only the 4 outboard bolts. Loosen bolts
   on the cart as needed to adjust.

-  Once the cart is bolted to the table bottom, while **320 lbs** is
   still on the crane, tighten all cart bolts. Do not over-tighten: make
   1/4 turn after the washers are no longer free. This is to avoid
   excessive stress on the table.

-  Reposition the load spreader center to the instrument + cart
   position marked on it.

-  Install the triangle stabilizing ropes between the crane hook and 
   the lifting fixture in accordance with the below figure. Tighten, but do not cause
   them to pick the load.

   .. image:: figures/stabilizers.jpg

   *The triangle stabilizing ropes should be tight, but not become the
   lifting point for the load.*

-  Ensure that there is room to move the legs out from under the
   table towards the telescope.

-  Position a person at each end of the cart to stabilize it during
   the lift.

-  Position two people to remove the legs from under the table

-  Lift the table off the legs.

-  Move the legs out from under the table.

   .. image:: figures/cart_lift_legs_ready.jpg

   *The cart and instrument ready to be set down on the wheels, with
   legs out of the way.*

-  Set the cart down on its wheels.

-  Move MagAO-X onto the elevator, and remove from the dome

-  When cart is on concrete outside Clay, move very slowly to avoid
   excessive vibration

Transport MagAO-X To The Clean room
-----------------------------------

-  Ensure that the lift gate at the summit has been adjusted for slow
   smooth operation as is done for the asm

-  Push MagAO-X onto the lift-gate

-  Raise the lift-gate to the height of the flatbed truck

-  Move MagAO-X onto the truck, using the come-along

   .. image:: figures/inst_backed_up.jpg

   *MagAO-X is loaded at the telescope using the lift gate,
   adjusted for slow operation.*

-  Secure the instrument by strapping the cart down at 4 points as
   illustrated in the below figure.

   .. image:: figures/inst_on_truck.jpg

   *MagAO-X will be strapped to the Isuzu.*

-  Slowly drive the truck to the cleanroom

-  Back the flatbed truck up to the lift gate.

-  Next, using the come-along, carefully move MagAO-X onto the lift
   gate.

-  Move MagAO-X into the cleanroom.

-  Return to the top with the flatbed and move
   the legs to the cleanroom.

-  Placed on 2 dollies as in the below image.

   .. image:: figures/legs_dollies.png

   *Legs on 2 dollies placed in the middle of the table under each lower long tie bar (away from basket).*


-  Move the legs to the flatbed and strap them down.

   .. image:: figures/legs_truck.png

   *Legs strapped to the truck.*

Transport Electronics
---------------------

-  remove the earthquake bar

-  Move the rack to the lift gate, and load it on the pickup.

-  place foam between the rack side and the truck to protect cable
   connectors

   .. image:: figures/rack_connectors.jpg

   *The electronics rack has many delicate connectors on the side.*

-  strap the rack securely to the truck

   .. image:: figures/electronics_pickup.jpg

   *The rack on a truck for transport.*


-  drive the truck to the cleanroom

-  unload the rack using the lift gate

Remove AOC from Control Room
----------------------------

-  power down AOC and COC

-  remove monitors and pack

-  move AOC and COC to cleanroom.
