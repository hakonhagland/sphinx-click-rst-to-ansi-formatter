import click
from click.testing import CliRunner

from sphinx_click.rst_to_ansi_formatter import (
    RstToAnsiCommand,
    RstToAnsiGroup,
    make_rst_to_ansi_formatter,
)

BASE_URL = "https://example.github.io/example/main/"
HELP = "See the :doc:`usage guide <usage>` for more information."


class DocCommand(RstToAnsiCommand):
    base_url = BASE_URL


class DocGroup(RstToAnsiGroup):
    base_url = BASE_URL


def test_command_subclass() -> None:
    @click.command(cls=DocCommand, help=HELP)
    def cli() -> None:
        pass  # pragma: no cover

    result = CliRunner().invoke(cli, ["--help"])
    assert f"{BASE_URL}usage.html" in result.output


def test_group_subclass() -> None:
    @click.group(cls=DocGroup, help=HELP)
    def cli() -> None:
        pass  # pragma: no cover

    @cli.command()
    def sub() -> None:
        pass  # pragma: no cover

    result = CliRunner().invoke(cli, ["--help"])
    assert f"{BASE_URL}usage.html" in result.output
    assert "sub" in result.output


def test_factory_command_class() -> None:
    colors = {"code": {"fg": "", "style": ""}}
    cls = make_rst_to_ansi_formatter(BASE_URL, colors)
    assert issubclass(cls, RstToAnsiCommand)
    assert cls.base_url == BASE_URL
    assert cls.colors == colors


def test_factory_group_class() -> None:
    cls = make_rst_to_ansi_formatter(BASE_URL, group=True)
    assert issubclass(cls, RstToAnsiGroup)
    assert cls.base_url == BASE_URL
