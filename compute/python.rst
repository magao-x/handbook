Python environments
===================

Plenty of MagAO-X software is written in Python, so we need a consistent
environment.

There are two config files in magao-x/MagAOX that control conda
environments on AOC/RTC/ICC:

-  ``setup/conda_env_base.yml``
-  ``setup/conda_env_pinned.yml``

The first, ``conda_env_base.yml``, stores just the top-level
dependencies (i.e. not everything they depend on) without versions. This
makes it easier to track what we *really* depend on in case we need to
help conda along with failing dependency resolution.

The second, ``conda_env_pinned.yml``, reflects the actual set of
packages installed in the environment. This lets us recreate/update
(nearly) identical environments on AOC/RTC/ICC.

Adding a package
----------------

If there’s a package you need for your work on the instrument machines,
it’s a good idea to make it part of the environment so a rebuild is sure
to install it.

Installation
~~~~~~~~~~~~

Install as normal, preferring ``conda`` packages if possible:

::

   $ conda install foopkg

   # *only* if it's not found:
   $ pip install foopkg

Verify that it imports, works, etc.

Now when you do ``conda env export``, you should see an entry for your
new package. Example:

::

   $ conda env export
   name: base
   channels:
     - conda-forge
     - defaults
   dependencies:
   [...]
     - foopkg=0.1
   [...]

If it was installed via pip, the package will be in a sub-list under the
``pip:`` heading.

Updating the environment template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add it to the template, first pull any changes:

::

   cd /opt/MagAOX/source/MagAOX
   git pull
   # resolve any conflicts

Then open ``/opt/MagAOX/source/MagAOX/setup/conda_env_base.yml``. You’ll
see something like ``conda env export``, but without the version
numbers. Add your package name (but not version, unless you know what
you’re doing) to the list, being careful to put it under the ``pip:``
heading if that’s how it was installed.

Updating the list of pinned packages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, you need to update the list of pinned packages and versions
in ``/opt/MagAOX/source/MagAOX/setup/conda_env_pinned.yml`` by
exporting the current packages and versions from the system where
you just installed a new package.

::

   $ conda env export > /opt/MagAOX/source/MagAOX/setup/conda_env_pinned.yml

This updates the versioned file in the MagAO-X source, and you can
use ``git diff`` to see what has changed.

Storing in version control
~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to commit the updates to these files to version control
and push them to the central copy.

::

   $ cd /opt/MagAOX/source/MagAOX/setup
   $ git add conda_env_pinned.yml conda_env_base.yml
   $ git commit -m "Added Python package foopkg to conda envs"
   $ git push

Replicating across all the machines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you just performed these steps on AOC, now you need to connect to ICC
and RTC and run the following steps:

::

   $ cd /opt/MagAOX/source/MagAOX/setup
   $ git pull
   $ conda env update -f /opt/MagAOX/source/MagAOX/setup/conda_env_pinned.yml

(Or, if you made the change another one of the machines, just run the above
steps on the two **other** ones.)

Updating ``conda``
------------------

If there are updates to ``conda`` itself, it’ll probably tell you. You
can run ``conda update -n base -c defaults conda`` to update it, but be
sure to follow the steps beginning at `Updating the pinned
packages <#Updating-the-pinned-packages>`__ to record the upgrade.

Performing a fresh conda install/upgrade
----------------------------------------

Generally only something to do if things are totally messed up, there’s
a new version of the Python interpreter itself, or both.

1. Move ``/opt/miniconda3`` out of the way
   (i.e. ``mv /opt/miniconda3 /opt/miniconda3.bak``)
2. Edit ``/opt/MagAOX/source/MagAOX/setup/install_python.sh`` and change
   ``MINICONDA_VERSION="X-pyXX_X.Y.Z"`` appropriately, and commit/push
   to version control.
3. Run ``bash /opt/MagAOX/source/MagAOX/setup/install_python.sh`` to
   download and install the new ``conda`` to ``/opt/miniconda3`` with
   appropriate permissions

At this point you should log out and back in to reset any environment
variables that were set by the old ``conda``.

If the Python version hasn’t increased
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In most cases, the version of Python shipped with Miniconda hasn’t
changed.

4. Run ``bash /opt/MagAOX/source/MagAOX/setup/configure_python.sh``

If the Python version has changed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default ``configure_python.sh`` would try to restore the pinned
versions from ``conda_env_pinned.yml``, but would fail because of the
Python version mismatch. Instead, you need to create the environment
from ``conda_env_base.yml`` and update ``conda_env_pinned.yml`` yourself

4. ``conda env update -f /opt/MagAOX/source/MagAOX/setup/conda_env_base.yml``
5. ``conda env export > /opt/MagAOX/source/MagAOX/setup/conda_env_pinned.yml``
6.  ::

      $ cd /opt/MagAOX/source/MagAOX/setup
      $ git add conda_env_pinned.yml
      $ git commit -m "Updated pinned packages for conda upgrade"
      $ git push


You will also need to rerun some of the files in
``/opt/MagAOX/source/MagAOX/setup/steps`` that install Python packages
into the environment. A (possibly incomplete) list:

::

   cd /opt/MagAOX/source/MagAOX/setup/steps && \
   bash install_purepyindi.sh && \
   bash install_imagestreamio_python.sh && \
   bash install_magpyx.sh && \
   bash install_sup.sh

Replicate across all the machines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SSH to the other machines and:

1. Move ``/opt/miniconda3`` out of the way
   (i.e. ``sudo mv /opt/miniconda3 /opt/miniconda3.bak``)
2. Update the MagAO-X source:
   ``cd /opt/MagAOX/source/MagAOX && git pull``
3. Install Python via miniconda:
   ``bash /opt/MagAOX/source/MagAOX/setup/install_python.sh``
4. Configure Python via conda environment files:
   ``bash /opt/MagAOX/source/MagAOX/setup/configure_python.sh``
5. Ensure all our custom packages get installed::

      cd /opt/MagAOX/source/MagAOX/setup/steps && \
      bash install_purepyindi.sh && \
      bash install_imagestreamio_python.sh && \
      bash install_magpyx.sh && \
      bash install_sup.sh
