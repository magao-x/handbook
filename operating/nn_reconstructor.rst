Neural Network Reconstructor and Predictive Control
===================================================

You can use the neural network reconstructor (CNN) to run the high-order (HO)
loop with the pyramid unmodulated. Predictive control (PO4AO) can be used with
either the CNN or the CACAO reconstructor. To open the GUI, run::

   $ po4aoGUI

Switching reconstructors
------------------------

1. Check :guilabel:`Link modulation` if you want the pyramid modulation to follow
   the reconstructor switch.
2. To use the currently loaded model, click :guilabel:`Switch to CNN`. To select
   a model, choose it from the :guilabel:`CNN Reconstructor` dropdown and click
   :guilabel:`Set reconstructor` to activate it.
3. Click :guilabel:`Switch to CACAO` to switch back.

Predictive control
------------------

1. With the HO loop closed, click :guilabel:`Enable policy`.
2. To train a policy, click :guilabel:`Start learning` once warmup shows ``Ready``.
   Keep the HO loop gains fixed while PO4AO is training.

**Optional controls**

- Click :guilabel:`Recollect warmup` if you want fresh data.
- Click :guilabel:`Pause learning` to keep using the current policy without updating
  it. Click :guilabel:`Resume learning` to continue training.
- Click :guilabel:`Disable policy` to return to the integrator and pause learning.
- To save the current policy, click :guilabel:`Save policy`. To use a saved one, select
  it under :guilabel:`Policy`, click :guilabel:`Set policy`, then :guilabel:`Enable policy` if needed.

If predictive control becomes unstable, click :guilabel:`Reset PO4AO` to return to the
integrator and discard the current policy. Increase :guilabel:`Command regularization`
to penalize large commands, increase :guilabel:`Delta policy regularization` to limit
changes between policies, or decrease :guilabel:`Learning rate` to take smaller training
steps. Press :kbd:`Enter` after each edit. Once the loop is stable, click :guilabel:`Enable policy`, then :guilabel:`Start learning` when warmup shows ``Ready``.
