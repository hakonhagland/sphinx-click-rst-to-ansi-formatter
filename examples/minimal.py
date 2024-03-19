from typing import Optional

import click
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

base_url = "https://example.github.io/example/main/"


@click.command(cls=make_rst_to_ansi_formatter(base_url))
@click.option("--template", type=str, help="specify the template to use")
def minimal(template: Optional[str]) -> None:  # pragma: no cover
    """
    ``minimal-example`` let's you view a `minimal` example of a Click command.
    See :doc:`Minimal example <minimal>` for more *information*.

    If the ``--template`` option is not used, a default template is used.
    See :doc:`/template` for more information about the default template and
    https://example.com for an example of a custom template. See also

    EXAMPLES
    ========

    Some examples ::

      $ minimal-example
      $ minimal-example --template mytemlate.txt


    For more information about the minimal example script see :doc:`/history`.
    """
    pass


if __name__ == "__main__":  # pragma: no cover
    minimal()
