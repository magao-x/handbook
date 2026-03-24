Python environments
===================

Plenty of MagAO-X software is written in Python, so we need a consistent environment. We use the ``mamba`` distribution of the ``conda`` package manager (c.f. Anaconda) to manage it. (A mamba is a fast snake, and the ``mamba install`` command is orders of magnitude faster at solving environment installation requirements than plain old ``conda``.)

Environment specifications are tracked in https://github.com/magao-x/magao-x-setup/tree/main/conda_envs.

``xpy3_13.yml`` stores just the top-level dependencies (i.e. not everything they depend on) without versions.

.. warning::

   Why not pin versions? It turns out that subtle forms of drift (yanked releases,
   x86 vs. ARM differences, etc.) mean that pinning specific versions does not work
   as well as you'd hope.


Adding a package
----------------

If there's a package you need for your work on the instrument machines,
it's a good idea to make it part of the environment so a rebuild is sure
to install it.

Installation
~~~~~~~~~~~~

We use the ``mamba`` tool and require root access to install packages, so become root first::

   you$ sudo -i
   root$

Install as normal, preferring ``conda`` packages if possible. ::

   root$ mamba install foopkg
   # *only* if it's not found:
   root$ pip install foopkg

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

Updating the instrument base environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add it to the template, you need a copy of the setup files::

   cd
   git clone https://github.com/magao-x/magao-x-setup/
   cd magao-x-setup

If you have an existing clone, make sure to update it::

   cd ~/magao-x-setup
   git pull
   # resolve any conflicts

Then open ``conda_envs/xpy3_13.yml``. You'll
see something like what ``conda env export`` outputs, but without the version
numbers. Add your package name (but not version, unless you know what
you're doing) to the list. If it was installed using ``pip``, be sure to put it
under the ``pip:`` heading.

Storing in version control
~~~~~~~~~~~~~~~~~~~~~~~~~~

Follow these steps to commit the updates to these files to version control
and push them to the central copy.

::

   git add conda_envs
   $ git commit -m "Added Python package foopkg to conda envs"
   $ git push

Replicating across all the machines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you just performed these steps on AOC, now you need to connect to ICC
and RTC and run the following steps:

::

   git clone https://github.com/magao-x/magao-x-setup/
   cd magao-x-setup
   sudo mamba env update -f conda_envs/xpy3_13.yml

(Or, if you made the change another one of the machines, just run the above
steps on the two **other** ones.)

Updating ``conda``
------------------

If there are updates to ``conda`` itself, it'll probably tell you. You
can run ``conda update -n base -c defaults conda`` to update it.

Performing a fresh conda install/upgrade
----------------------------------------

Generally only something to do if things are totally messed up, there's
a new version of the Python interpreter itself, or both.

1. Move ``/opt/conda`` out of the way
   (i.e. ``mv /opt/conda /opt/conda.bak``)
2. Edit ``~/magao-x-setup/steps/install_python.sh`` (adjust for path to your magao-x-setup clone) and change
   ``MINICONDA_VERSION="X-pyXX_X.Y.Z"`` appropriately, and commit/push
   to version control.
3. Run ``bash ~/magao-x-setup/steps/install_python.sh`` to
   download and install the new ``conda`` to ``/opt/conda`` with
   appropriate permissions

At this point you should **log out** and back in to reset any environment
variables that were set by the old ``conda``.


**Finally,** Run ``bash ~/magao-x-setup/steps/install_python_libs.sh``
to install all our non-pip, non-conda dependencies.


Replicate across all the machines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Repeat these steps on the other MagAO-X computers (or suffer the consequences).
