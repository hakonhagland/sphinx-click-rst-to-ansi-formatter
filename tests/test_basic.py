import logging
import os
import sys

# import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner
# from pytest_mock.plugin import MockerFixture

import sphinx_click.rst_to_ansi_formatter.formatter as formatter
from sphinx_click.rst_to_ansi_formatter.colors import Colors

# Append the parent directory to sys.path to make 'examples' package available
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from examples.minimal import minimal as click_function


class TestMain:
    def test_help_opt(self, caplog: LogCaptureFixture) -> None:
        caplog.set_level(logging.INFO)
        runner = CliRunner()
        # TODO: click_function = import minimal from examples.minimal
        result = runner.invoke(click_function, ["--help"])
        assert result.stdout.startswith("Usage: minimal [OPTIONS]")


class TestColors:
    def test_ansi_color_coding(self, colors: Colors) -> None:
        docstring = """Code example
        Heading
        -------
        This is some code: ``print("Hello")``.

        Visit https://example.com for more info.
        """
        base_url = "https://example.github.io/example/main/"
        converter = formatter.RstToAnsiConverter(docstring, base_url)
        converted_text = converter.convert()

        # Check if the heading, code, and URL are correctly colored
        assert colors.colors["code"]["fg"] in converted_text

    def test_emphasized_text_coloring(self, colors: Colors) -> None:
        docstring = """
        This is an *emphasized* text example.
        """
        base_url = "https://example.github.io/example/main/"
        converter = formatter.RstToAnsiConverter(docstring, base_url)
        converted_text = converter.convert()

        # Assuming emphasized text is colored similarly to code
        assert colors.colors["code"]["fg"] in converted_text


class TestURLs:
    def test_internal_reference_handling(self) -> None:
        docstring = """
        See the :doc:`usage guide <usage>` for more information.
        """
        base_url = "https://example.github.io/example/main/"
        converter = formatter.RstToAnsiConverter(docstring, base_url)
        converted_text = converter.convert()

        # Check if the URL replacement for internal reference works correctly
        assert "https://example.github.io/example/main/usage.html" in converted_text

    def test_url_listing_at_end(self, colors: Colors) -> None:
        docstring = """
        Visit :doc:`/example` and :doc:`/another-example` for more info.
        The :doc:`/example` has more information.
        """
        base_url = "https://example.github.io/example/main/"
        converter = formatter.RstToAnsiConverter(docstring, base_url)
        converted_text = converter.convert()

        ansi1 = colors.color_heading("Referenced URLs:")
        ansi2 = colors.color_url("1.") + f" {base_url}example.html"
        ansi3 = colors.color_url("2.") + f" {base_url}another-example.html"
        # Check if URLs are correctly appended at the end
        expected_url_listing = f"{ansi1}\n\n\b\n{ansi2}\n{ansi3}"
        assert expected_url_listing in converted_text


class TestLiteralBlocks:
    def test_literal_block_handling(self, colors: Colors) -> None:
        docstring = """
        Example code block:

        .. code-block:: python

            def hello():
                print("Hello, world!")

        End of example.
        """
        base_url = "https://example.github.io/example/main/"
        converter = formatter.RstToAnsiConverter(docstring, base_url)
        converted_text = converter.convert()

        # Check if the literal block is correctly preserved and colored
        assert "\n\n\b\n" + colors.colors["code"]["fg"] in converted_text
        assert "def hello():" in converted_text


class TestIndentation:
    def test_first_line_indentation_preservation(self) -> None:
        docstring = """First line not indented.
        Second line indented.
        """
        # Expected to adjust the first line to match the second line's indentation
        adjusted_docstring = formatter.RstToAnsiConverter.fix_first_line_indentation(
            docstring
        )
        assert adjusted_docstring.startswith(
            "        First line not indented.\n        Second line indented."
        )

    def test_indentation_not_found(self) -> None:
        docstring = """First line not indented.

        """
        # Expected to adjust the first line to match the second line's indentation
        adjusted_docstring = formatter.RstToAnsiConverter.fix_first_line_indentation(
            docstring
        )
        assert adjusted_docstring.startswith("First line not indented.")


class TestEmphasis:
    def test_emphasis_handling(self, colors: Colors) -> None:
        docstring = """
        This is an *emphasized* text example.
        """
        base_url = "https://example.github.io/example/main/"
        converter = formatter.RstToAnsiConverter(docstring, base_url)
        converted_text = converter.convert()
        ansi1 = colors.color_code("emphasized")
        # Check if the emphasized text is correctly colored
        assert ansi1 in converted_text
