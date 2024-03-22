Introduction
============

The `sphinx-click <https://github.com/click-contrib/sphinx-click>`_ module lets you
extract documentation from your `Click-based <https://github.com/pallets/click>`_
command-line interfaces and automatically generates a Sphinx documentation page for them.

This makes it convenient to write the docstrings for your Click commands
in the same format as the rest of your Sphinx documentation (reST). The only issue
is that if the docstrings contain reST markup, the Sphinx documentation will render
it correctly, but the console help output will not.
This module extends the functionality of ``sphinx-click`` by adding support for
converting reST formatted docstrings to ANSI colored text when printing
the click help text to the console.
