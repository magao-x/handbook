Documenting MagAO-X
===================

Where the documentation lives
-----------------------------

This source code for this documentation lives in the
`magao-x/handbook <https://github.com/magao-x/handbook>`_ repository.
Parts of the documentation pertaining to the core C++ code are generated
from the code in `magao-x/MagAOX <https://github.com/magao-x/MagAOX>`_,
which is documented in Doxygen. (TODO: explain how to make
cross-references.)

The built copy of this documentation is hosted at
https://magao-x.github.io/handbook/ via `GitHub Pages free
hosting <https://pages.github.com/>`_. When changes are pushed to the
``master`` branch of
`magao-x/handbook <https://github.com/magao-x/handbook>`_, a CircleCI
job builds and updates the ``gh-pages`` branch of the repository, with
changes reflected on the GitHub Pages site 1-15 minutes later.

How to make changes: in brief (e.g. for typo corrections)
---------------------------------------------------------

If you need to make an edit on the fly, without installing any software,
it is best to simply edit the file directly on GitHub.

1. Go to https://github.com/magao-x/handbook and browse to the source
   for the document you want to edit (e.g. `this document <https://github.com/magao-x/handbook/blob/master/appendices/documenting.rst>`_)
2. Click the pencil icon

   -  If you are allowed to edit directly, you will see this:

      .. image:: edit_on_github_authorized.png

   -  If not, you will instead see this:

      .. image:: edit_on_github_unauthorized.png

3. Make your changes, optionally previewing them with the “Preview
   changes” tab
4. Scroll down to the “Commit changes” or “Propose changes” form (below
   the main editor) and fill in a brief description of what you changed.
5. Click “Commit changes” or “Propose change”
6. If you committed directly, your changes will be live in 5-15 minutes.
   If you proposed a change, someone else will have to merge it first.

How to make bigger changes
--------------------------

Installing the required software
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will need Python 3.5 or newer (with ``pip``) and a recent version of
``git``.

1. Clone https://github.com/magao-x/handbook to your own computer

   .. code-block:: bash

      # full clone
      $ git clone https://github.com/magao-x/handbook.git

      # shallow clone (faster)
      $ git clone --depth=1 https://github.com/magao-x/handbook.git

2. Change into the directory where you just cloned the documentation and
   install software so you can preview your changes.

   .. code-block:: bash

      cd handbook/

      # if 'pip' and 'python' are provided by Python 3.x:
      $ pip install --user -r requirements.txt

      # if your OS calls pip for Python 3.x 'pip3':
      $ pip3 install --user -r requirements.txt

   (Installing Python 3 is outside the scope of this document, but
   `Anaconda <https://www.anaconda.com/distribution/>`__ is a popular
   installer.)

3. Ensure ``sphinx-build`` is on the path by running ``which sphinx-build``
   at the prompt

   .. code-block:: bash

      $ which sphinx-build
      /Users/jlong/miniconda3/bin/sphinx-build
   
   (If you’re using your OS-provided Python, and don’t see anything output
   when you run ``which sphinx-build``, you should make sure
   ``$HOME/.local/bin`` is on ``$PATH``.)

You now have a copy of the sources for the handbook. If you’re just
editing an existing document, :ref:`skip ahead <edit-and-publish>`.

Creating a brand new document
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Create a new plain text file with the name you want and the extension 
   ``.rst`` for reStructuredText (see :ref:`markup`)
2. Open the ``index.rst`` file in the folder for the section you're adding
   to and find the ``.. toctree::``. Add the base name of your file to the list
   that follows (e.g. ``funny-business.rst`` would be called ``funny-business``
   in the toctree)

.. _edit-and-publish:

Edit and publish
~~~~~~~~~~~~~~~~

Finally, to preview and publish your edits:

1. Edit the document you want to change
2. Run ``make html`` (in the directory you cloned into)
3. Open ``_build/html/index.html`` to see the updated site, and verify
   your changes look good
4. ``git add ./path/to/file/you/changed.md`` and
   ``git commit -m "Description of your changes"``
5. ``git push origin master``

If everything looks good, the public copy of the docs will update
automatically!

.. _markup:

Markup
------

New documentation should be written in `reStructuredText <http://www.sphinx-doc.org/en/stable/usage/restructuredtext/basics.html>`_, the native markup
format of the `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ documentation
tool (abbreviated "reST"). The rest of this section contains a cheat sheet for common things you
may need to write your document, but you can also consult the `primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_ and
the `docutils documentation <https://docutils.readthedocs.io/en/sphinx-docs/ref/rst/directives.html>`_ for more advanced topics.

Existing documents may be written in Markdown
(`CommonMark <https://spec.commonmark.org/0.29/>`_ variant), in which case the
filename will end with ``.md``. Markdown has certain disadvantages for
embedding mathematical expressions, download links, tables of contents,
or other things not part of the original specification. Therefore, its
use is discouraged for new documentation.

In either case, if you want to see how a particular bit of formatting was 
achieved, you can click the “Page source” link at the bottom of any page.

Headings and paragraphs
~~~~~~~~~~~~~~~~~~~~~~~

Paragraphs are separated with a blank line. reST follows a somewhat mysterious process to infer hierarchy from headings. Each heading
is followed by a line of the same length, made up of a punctuation character like ``=`` or ``~``.

When editing an existing document, use the other headings in it as a guide to which punctuation character to use for consistency.

**Markup:**

.. code-block:: rest

   Example heading
   """""""""""""""

   Body paragraph text

   Subheading
   ^^^^^^^^^^

   Body paragraph number 2

**Output:**

-------------

Example heading
"""""""""""""""

Body paragraph text

Subheading
^^^^^^^^^^

Body paragraph number 2

-------------

Outside links
~~~~~~~~~~~~~

Plain URLs are linkified automatically, but you can customize the link text if you want.

**Markup:**

.. code-block:: rest

   `reStructuredText <http://www.sphinx-doc.org/en/stable/usage/restructuredtext/basics.html>`_

   http://www.sphinx-doc.org/en/stable/usage/restructuredtext/basics.html

**Output:**

-------------

`reStructuredText <http://www.sphinx-doc.org/en/stable/usage/restructuredtext/basics.html>`_

http://www.sphinx-doc.org/en/stable/usage/restructuredtext/basics.html

-------------

Other handbook documents
~~~~~~~~~~~~~~~~~~~~~~~~

Links within the handbook use document names (without file extensions).

.. code-block:: rest

   :doc:`../operating/index`

   :doc:`Operating section <../operating/index>`

   :doc:`/operating/index`

   :doc:`Operating section </operating/index>`

**Output:**

-------------

:doc:`../operating/index`

:doc:`Operating section <../operating/index>`

:doc:`/operating/index`

:doc:`Operating section </operating/index>`

-------------

Internal references
~~~~~~~~~~~~~~~~~~~

Internal references require a target, indicated with ``.. _label-goes-here:``
preceding a heading, like so:

**Markup:**

.. code-block:: rest

   .. _my-label-name:

   Example heading reference
   """""""""""""""""""""""""

   Example paragraph

**Output:**

-------------

.. _my-label-name:

Example heading reference
"""""""""""""""""""""""""

Example paragraph

-------------

Now you can link to a particular heading using its label and ``:ref:``

**Markup:**

.. code-block:: rest

   Read about it in :ref:`my-label-name` or :ref:`see previous section <my-label-name>`

**Output:**

-------------

Read about it in :ref:`my-label-name` or :ref:`see previous section <my-label-name>`

-------------

Inline code
~~~~~~~~~~~

To include some code inline, enclose it in double backticks (left of the ``1``
key on most US keyboards).

**Example markup:**

.. code-block:: rest

   Before starting, execute ``sudo do-things`` in your terminal

**Output:**

Before starting, execute ``sudo do-things`` in your terminal

Blocks of code
~~~~~~~~~~~~~~

**Markup:**

.. code-block:: rest

   .. code-block:: rest

      Example :ref:`markup`

   .. code-block::

   def example():
      return f'Example {python}'

   .. code-block:: bash

      export EXAMPLE="$EXAMPLE:bash/shell/script/"

Note that the language follows the ``::``, and Python is the default.

**Output:**

-------------

.. code-block:: rest

   Example :ref:`markup`

.. code-block::

   def example():
      return f'Example {python}'

.. code-block:: bash

   export EXAMPLE="$EXAMPLE:bash/shell/script/"

-------------

Math
~~~~

Equations can be inserted as a special variety of code block.

**Markup:**

.. code-block:: rest

   .. math::

      \mu = m - M = 5 \log_{10}\left(\frac{d}{10\,\mathrm{pc}}\right)

**Output:**

-------------

.. math::

   \mu = m - M = 5 \log_{10}\left(\frac{d}{10\,\mathrm{pc}}\right)

-------------

Static files
~~~~~~~~~~~~

This handbook uses a custom ``:static:`` role to handle including certain
data files in the web version.

The example shows a link to
``_static/ref/filters/magaox_sci1-ch4_bs-65-35_scibs-5050.dat`` (`view on GitHub <https://github.com/magao-x/handbook/blob/master/_static/ref/filters/magaox_sci1-ch4_bs-65-35_scibs-5050.dat>`_), which
will get copied to
https://magao-x.org/docs/handbook/_static/ref/filters/magaox_sci1-ch4_bs-65-35_scibs-5050.dat on publication.

(You *could* use a full URL and the normal link syntax, but the link
would only work after publication and you couldn't preview.)

**Markup:**

.. code-block:: rest

   :static:`Click here to download some filter curve <ref/filters/magaox_sci1-ch4_bs-65-35_scibs-5050.dat>`

**Output:**

-------------

:static:`Click here to download some filter curve <ref/filters/magaox_sci1-ch4_bs-65-35_scibs-5050.dat>`

-------------

Downloadable files
~~~~~~~~~~~~~~~~~~

Downloadable files are similar to static files, but the filename is
given relative to the current document. For instance, if you wanted
to make a download link to the ``mini-star.png`` image in this folder:

**Markup:**

.. code-block:: rest

   :download:`Click here to download the star logo <mini-star.png>`

**Output:**

-------------

:download:`Click here to download the star logo <mini-star.png>`

-------------

Images
~~~~~~

By default, images are included inline and left aligned.

**Markup:**

.. code-block:: rest

   .. image:: mini-star.png
      :alt: Mini star logo

   .. image:: mini-star.png
      :alt: Mini star logo (click to go home)
      :align: right
      :scale: 50%

**Output:**

-------------

.. image:: mini-star.png
   :alt: Mini star logo

.. image:: mini-star.png
   :alt: Mini star logo (click to go home)
   :align: right
   :scale: 50%
