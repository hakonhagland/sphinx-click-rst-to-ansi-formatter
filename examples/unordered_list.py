import click
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

base_url = "https://example.github.io/example/main/"


@click.command(cls=make_rst_to_ansi_formatter(base_url))
def minimal():
    """``minimal`` shows a minimal example of a reST formatted docstring with and
    unordered list.

    * This is the first ``item`` in the unordered list. It is a long line that will be wrapped
    * This is the second item in the unordered list.
    * An URL link `first link <https://example.com>`_
    * An URL link `second link <https://example.com>`_
    """
    pass


if __name__ == "__main__":  # pragma: no cover
    minimal()
