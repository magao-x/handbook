#!/bin/bash
# Sphinx generates a PDF for each of the `latex_documents` in conf.py
# but we need to make them part of the HTML version by adding them to
# _static. Needs LaTeX.
set -e
make clean && make latexpdf && cp -v _build/latex/*.pdf _static/handling/