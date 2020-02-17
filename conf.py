# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

from recommonmark.transform import AutoStructify
project = 'MagAO-X Instrument Handbook'
copyright = '2019, Extreme Wavefront Control Lab, The University of Arizona'
author = 'Extreme Wavefront Control Lab, The University of Arizona'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.


import sys, os.path
sys.path.append(os.path.abspath('.')) # Make xsphinx.py discoverable

extensions = [
    'sphinx_markdown_tables',
    'recommonmark',
    'xsphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': True,
}
html_logo = '_static/magao-x_logo_white.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for LaTeX output

latex_documents = [
    # (startdocname, targetname, title, author, documentclass, toctree_only)
    ('handling/electronics_packing', 'electronics_packing.tex', 'Packing the MagAO-X Electronics at LCO', author, 'howto', False),
    ('handling/instrument_packing', 'instrument_packing.tex', 'Packing the MagAO-X Table at LCO for Shipment', author, 'howto', False),
    ('handling/telescope_install', 'telescope_install.tex', 'Installing MagAO-X on the Telescope', author, 'howto', False),
    ('handling/telescope_removal', 'telescope_removal.tex', 'Removing MagAO-X from the Telescope', author, 'howto', False),
]

#   - Disable page-clearing for chapter titles
#   - Enforces a maximum width on images included as a brute force
#     method of making more content fit on a page.
_latex_preamble = r'''

\usepackage{etoolbox}
\makeatletter
\patchcmd{\chapter}{\if@openright\cleardoublepage\else\clearpage\fi}{}{}{}
\makeatother


\usepackage{letltxmacro}
\LetLtxMacro{\oldincludegraphics}{\includegraphics}

\newlength\MaxWidth \newsavebox\IBox
\MaxWidth=300pt

\renewcommand*\includegraphics[2][]{%
  \sbox\IBox{\oldincludegraphics[#1]{#2}}%
  \ifdim\wd\IBox>\MaxWidth \resizebox{\MaxWidth}{!}{\usebox\IBox}%
  \else\usebox\IBox\fi}
'''
latex_elements = {
    'preamble': _latex_preamble,
}

def setup(app):
    # Enable reCommonMark extensions to Markdown syntax
    # see https://recommonmark.readthedocs.io/en/latest/auto_structify.html
    app.add_config_value('recommonmark_config', {
        'enable_auto_toc_tree': True,
        'auto_toc_tree_section': 'Contents',
    }, True)
    app.add_transform(AutoStructify)

    # Add Matomo analytics
    app.add_javascript('stats.js')
