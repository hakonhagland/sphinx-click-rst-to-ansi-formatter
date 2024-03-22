Usage
=====

Example
-------

Here is a minimal example of a Click command that uses ``sphinx-click.rst_to_ansi_formatter`` and a reST formatted docstring:

.. code-block:: python

    import click
    from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

    base_url = "https://example.github.io/example/main/"
    @click.command(cls=make_rst_to_ansi_formatter(base_url))
    def minimal():
        """``minimal-example`` displays a `minimal` example of a Click command that uses
        ``sphinx-click.rst_to_ansi_formatter`` and its method ``make_rst_to_ansi_formatter()``
        to convert this reST formatted docstring to an ANSI formatted string to be displayed
        in a terminal.

        See :doc:`Minimal example <minimal>` for more *information*.

        EXAMPLES
        ========

        Some examples ::

          $ minimal-example
          $ minimal-example --help


        For more information about the minimal example script see :doc:`/history`.
        """
        pass

Notice the line ``@click.command(cls=make_rst_to_ansi_formatter(base_url))``.
Without the custom ``cls`` value the console help output
would look like this (gnome-terminal):

.. image:: images/minimal-example2.png
    :align: center
    :width: 100%

Notice for example, that the two lines in the code block have been wrapped into a single
line. This would likely be confusing and difficult to read for a user of your app.
Also notice that the links are not substituted by the target URL
but rather rendered unprocessed as e.g. ``:doc:`Minimal example <minimal>```. Not very user-friendly!

However, by using the custom ``cls`` value in the code example,
the console output becomes:

.. image:: images/minimal-example1.png
    :align: center
    :width: 100%

.. raw:: html

    <div style="margin-top:20px;"></div>

which is hopefully more user-friendly.

Signature
---------

The signature for ``make_rst_to_ansi_formatter`` is:

.. automodule:: sphinx_click.rst_to_ansi_formatter.formatter
   :exclude-members: ClickRstToAnsiFormatter, PlainTextVisitor, RstToAnsiConverter
