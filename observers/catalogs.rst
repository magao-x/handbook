Preparing an Observing Catalog
==============================

In order to observe at LCO you need to prepare your targets in a catalog file. This file is a simple tab-delimited file with target information. The full description can be found at the `LCO website <http://lco.cl/technical-documentation/observing-catalogs-format>`_. To make it simple, there is an online app that lets you build up a target list using SIMBAD queries and then produces a catalog file (https://magellan-tcs-cat.streamlit.app/). 

AO Bright Star Catalog
----------------------

A catalog file can be produced for the MagAO-X AO bright star catalog from this url: https://ao-stars.streamlit.app/. Note that the exported cat file leaves spaces in the "Name" field, which is invalid and needs to be changed manually.

Uploading your Catalog to Guanaco
---------------------------------

``guanaco`` is the name of the server we upload the catalog files to. The simplest way to upload your file is to upload first to ``exao1``, and then to ``guanaco``, like so:

.. code-block::

    scp semester_observer.cat exao1:
    ssh exao1
    scp semester_observer.cat guanaco:

There is an SSH key on ``exao1`` available to all users that enables them access to ``guanaco``. If you cannot ``scp`` using just ``guanaco`` as the server name, something is wrong.
