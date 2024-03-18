# import typing
import pytest
from pathlib import Path

from sphinx_click.rst_to_ansi_formatter.colors import Colors


@pytest.fixture(scope="session")
def tests_assets_path() -> Path:
    return Path(__file__).parent / "assets"


@pytest.fixture(scope="session")
def colors() -> Colors:
    return Colors()
