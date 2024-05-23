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


    For more information about the minimal example script see :doc:`/history` and
    `the source code <https://github.com/hakonhagland/sphinx-click-rst-to-ansi-formatter>`_.
    """
    pass


if __name__ == "__main__":  # pragma: no cover
    minimal()
