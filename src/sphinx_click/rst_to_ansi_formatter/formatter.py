import docutils.core
import docutils.nodes
import docutils.utils
import re
import textwrap
import typing
from typing import Any

import click

from .colors import Colors
from .types import ColorDict


# Visitor that will transform the document tree into plain text
class PlainTextVisitor(docutils.nodes.NodeVisitor):
    def __init__(self, document: docutils.nodes.document, colors: Colors):
        docutils.nodes.NodeVisitor.__init__(self, document)
        # Main content buffer: Collect the parts of the docstring here
        self.parts: list[str] = []
        self.urls: list[str] = []  # Store URLs to be listed at the end of the docstring
        # Temporary buffer to store the current list item
        self.current_list_item: list[str] = []
        self.current_buffer: list[str] = (
            self.parts
        )  # Initially points to the main buffer
        self.in_literal = (
            False  # Flag to indicate if we're inside a literal block (quoted text)
        )
        self.in_bullet_list = False  # Flag to indicate if we're inside a bullet list
        self.colors = colors
        self.wrap_width = 80

    def color_heading(self, txt: str) -> str:
        return self.colors.color_heading(txt)

    def color_url(self, txt: str) -> str:
        return self.colors.color_url(txt)

    def color_code(self, txt: str) -> str:
        return self.colors.color_code(txt)

    def depart_bullet_list(self, node: docutils.nodes.bullet_list) -> None:
        self.in_bullet_list = False

    def depart_emphasis(
        self, node: docutils.nodes.emphasis
    ) -> None:  # pragma: no cover
        # NOTE: this method will not be called since visit_emphasis raises
        #       a docutils.nodes.SkipNode exception at the end
        pass

    def depart_list_item(self, node: docutils.nodes.list_item) -> None:
        # Process the accumulated list item content now that we've traversed the whole item
        item_text = "".join(self.current_list_item)
        wrapped_text = textwrap.fill(
            item_text, width=self.wrap_width, subsequent_indent="  "
        )
        self.parts.append(
            "• " + wrapped_text + "\n"
        )  # Append formatted content to main buffer
        self.current_buffer = self.parts  # Switch back to using the main buffer

    def depart_literal_block(
        self, node: docutils.nodes.literal_block
    ) -> None:  # pragma: no cover
        # NOTE: this method will not be called since visit_literal_block() raises
        #       a docutils.nodes.SkipNode exception at the end
        pass

    def depart_literal(self, node: docutils.nodes.literal) -> None:
        self.in_literal = False  # Exiting a literal block

    def depart_paragraph(self, node: docutils.nodes.paragraph) -> None:
        # No action needed on departure for paragraph nodes yet
        pass

    def depart_reference(
        self, node: docutils.nodes.reference
    ) -> None:  # pragma: no cover
        # NOTE: this method will not be called since visit_reference() raises
        #       a docutils.nodes.SkipNode exception at the end
        pass

    def depart_Text(self, node: docutils.nodes.Text) -> None:
        # No action needed on departure for Text nodes yet
        pass

    def depart_title_reference(
        self, node: docutils.nodes.title_reference
    ) -> None:  # pragma: no cover
        # NOTE: this method will not be called since visit_title_reference() raises
        #       a docutils.nodes.SkipNode exception at the end
        pass

    # At the end of processing, append all URLs:
    def finalize(self) -> None:
        if self.urls:
            self.parts.append(
                "\n\n" + self.color_heading("Referenced URLs:") + "\n\n\b\n"
            )
            for index, url in enumerate(self.urls, start=1):
                self.parts.append(self.color_url(f"{index}.") + f" {url}\n")

    def visit_bullet_list(self, node: docutils.nodes.bullet_list) -> None:
        # Prepend with backspace and a newline to ensure the list is not rewrapped by Click
        # and to maintain the desired spacing. See comment for visit_literal_block() for
        # more information.
        self.in_bullet_list = True
        self.parts.append("\n\n\b\n")
        pass

    def visit_emphasis(self, node: docutils.nodes.emphasis) -> None:
        # This method is called for each emphasis node in the document. That is, for
        # text in asterisks or underscores (e.g. *text* or _text_).
        txt = node.astext()
        # check if the emphasis is a URL
        if txt.startswith("http://") or txt.startswith("https://"):
            # Check if the URL is already in the list
            if txt not in self.urls:
                self.urls.append(txt)
                idx = len(self.urls)
            else:
                idx = self.urls.index(txt)
            # Replace the URL with a placeholder
            txt = f"[{idx}]"
        # Prepend and append the emphasis with ANSI color codes
        self.current_buffer.append(self.color_code(txt))
        # Skip further processing of children by docutils since we've manually
        #  processed the text
        raise docutils.nodes.SkipNode

    def visit_list_item(self, node: docutils.nodes.list_item) -> None:
        # This method is called for each list item node in the document.
        # For example, for each item in a bullet list (unordered list
        # in reStructuredText).
        self.current_list_item = []
        self.current_buffer = (
            self.current_list_item
        )  # Switch to using the list item buffer

    def visit_literal(self, node: docutils.nodes.literal) -> None:
        self.in_literal = True  # Entering a literal block

    def visit_literal_block(self, node: docutils.nodes.literal_block) -> None:
        txt = node.astext()
        # According to the click documentation:
        #   https://click.palletsprojects.com/en/8.1.x/api/#formatting
        # If paragraphs are handled, a paragraph can be prefixed with an empty line containing
        # the \b character (\x08) to indicate that no rewrapping should happen in that block.
        self.current_buffer.append("\n\n\b\n" + self.color_code(txt) + "\n\n")
        # Prevent further processing of child nodes, as we've already processed the text
        raise docutils.nodes.SkipNode

    def visit_paragraph(self, node: docutils.nodes.paragraph) -> None:
        if not self.in_bullet_list:
            self.current_buffer.append("\n\n")

    def visit_reference(self, node: docutils.nodes.reference) -> None:
        # This method is called for each reference node in the document. That is, for
        # - URLS: https://example.com
        # - Internal references:
        txt = node.astext()
        if txt.startswith("http://") or txt.startswith("https://"):
            # No special colors for URLs yet
            self.current_buffer.append(txt)
        else:
            # No special colors for internal references yet
            self.current_buffer.append(txt)  # pragma: no cover
        raise docutils.nodes.SkipNode

    def visit_Text(self, node: docutils.nodes.Text) -> None:
        txt = node.astext()
        if self.in_literal:
            # Wrap the text in ANSI codes for bright cyan
            self.current_buffer.append(self.color_code(txt))
        else:
            self.current_buffer.append(txt)

    def visit_title(self, node: docutils.nodes.title) -> None:
        # This method processes the section titles.
        txt = node.astext()
        self.current_buffer.append("\n\n" + self.color_heading(txt) + "\n\n")
        raise docutils.nodes.SkipNode

    def visit_title_reference(self, node: docutils.nodes.title_reference) -> None:
        # This method is called for each title_reference node in the document.
        # For example text in backticks (`text`).
        txt = node.astext()
        # TODO: How to color the text in backticks?
        self.current_buffer.append(txt)
        # Prevent further processing of child nodes, as we've already processed the text
        raise docutils.nodes.SkipNode

    def unknown_visit(self, node: docutils.nodes.Node) -> None:
        # This method is called for nodes for which no visit_ method exists.
        pass

    def unknown_departure(self, node: docutils.nodes.Node) -> None:
        # This method is called for nodes for which no depart_ method exists.
        # It's important to implement this to avoid errors on node departure.
        pass


class RstToAnsiConverter:
    def __init__(
        self, docstring: str, base_url: str | None, colors: ColorDict | None = None
    ) -> None:
        # In reStructuredText (reST), indentation is significant, so if we want
        # to keep the docstring nicely formatted, i.e. with indentation according to
        # function where the docstring is defined, we need to dedent it here.
        # For example. if the docstring is defined as:
        # def my_function():
        #     """
        #     This is a docstring
        #     -------------------
        #     """
        #     pass
        #
        # The docstring will be indented by 4 spaces, and docutils will not be able to
        # parse it correctly giving an error of the form:
        #   Unexpected section title.
        #
        # To fix this we will use textwrap.dedent() to remove the common leading whitespace.
        # However, if the docstring is defined as:
        # def my_function():
        #     """This is a docstring
        #     -------------------
        #     """
        #     pass
        #
        # the first line is not indented the same way as the rest of the docstring, so
        # dedent() will not work as expected. We fix this using the method
        # fix_first_line_indentation():
        docstring = RstToAnsiConverter.fix_first_line_indentation(docstring)
        self.docstring = textwrap.dedent(docstring).strip()
        self.base_url = base_url
        self.colors = Colors(colors)

    def convert(self) -> str:
        preprocessed_docstring = self.preprocess_docstring()
        # Parse the reST docstring into a document tree
        doctree = docutils.core.publish_doctree(
            source=preprocessed_docstring,
            source_path=None,
            settings=None,
            settings_overrides={"input_encoding": "unicode"},
        )

        # Create a new document for the visitor to populate
        visitor = PlainTextVisitor(docutils.utils.new_document("<string>"), self.colors)
        doctree.walkabout(visitor)
        # Call finalize to append URLs
        visitor.finalize()
        # Join the collected parts into a single string
        return "".join(visitor.parts).strip()

    @staticmethod
    def fix_first_line_indentation(docstring: str) -> str:
        lines = docstring.splitlines()

        if len(lines) > 1:
            # Find the indentation of the first indented line
            for line in lines[1:]:
                stripped_line = line.lstrip()
                if stripped_line:  # Ignore completely empty lines
                    first_indentation = len(line) - len(stripped_line)
                    break
            else:
                # If no indented line is found, set default indentation
                first_indentation = 0

            # Apply the same indentation to the first line if it's not indented
            if not lines[0].startswith(" " * first_indentation):
                lines[0] = " " * first_indentation + lines[0]

        # Join the lines back together and dedent
        adjusted_docstring = "\n".join(lines)
        return adjusted_docstring

    # The sphinx :doc: role is used to link to other documentation files. It is not part
    # of the reStructuredText standard, but is commonly used in Sphinx projects. Since we
    # are using docutils to parse the docstrings, we need to preprocess the docstrings to
    # handle the :doc: role. This function preprocesses the docstring to replace
    # :doc:`path` and :doc:`text <path>` with
    # URLs to the documentation files. The URLs are constructed based on the base URL and the
    # path to the documentation file.
    def preprocess_docstring(self) -> str:
        # This pattern matches :doc:`text <path>` and captures "text" and "path" separately.
        # It also matches :doc:`path` directly when there's no "text <path>" format.
        pattern = r":doc:`(?:([^`<]+)<)?([^`>]+)>?`"

        def replace_with_url(match: re.Match) -> str:  # type: ignore
            text = match.group(1)  # "text" part or None if not present
            path = match.group(2).lstrip(
                "/"
            )  # "path" part, leading slash removed if present

            # Construct full URL
            doc_url = self.base_url + path + ".html"

            # If there was descriptive text, insert it in double quotes
            if text:
                display_text = '"' + text.strip() + '" '
            else:
                display_text = ""

            # Return formatted string with "text" followed by the URL in emphasis
            return f"{display_text}*{doc_url}*"

        # Replace :doc:`some-text` or :doc:`text <path>` with formatted string
        processed_docstring = re.sub(pattern, replace_with_url, self.docstring)
        return processed_docstring


class FormatHelpMixin:
    def __init__(self, base_url: str | None = None, colors: ColorDict | None = None):
        self.base_url = base_url
        self.colors = colors

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        # Assume that the click command superclass has a help attribute
        # See click source code:
        # https://github.com/pallets/click/blob/f8857cb03268b5b952b88b2acb3e11d9f0f7b6e4/src/click/core.py#L1042
        help_text: str | None = typing.cast(str | None, getattr(self, "help", None))
        if help_text is not None:
            updated_help_text = RstToAnsiConverter(
                help_text, self.base_url, self.colors
            ).convert()
            setattr(self, "help", updated_help_text)
        super().format_help(ctx, formatter)  # type: ignore # Call the superclass method


# Factory function that creates a custom formatter class with a base URL
def make_rst_to_ansi_formatter(
    base_url: str, colors: ColorDict | None = None, group: bool = False
) -> "CustomRstToAnsiFormatter":  # type: ignore  # noqa: F821
    """
    Create a reST to ANSI text formatter class.

    :param str base_url: The base url for the documentation page. This will be used to construct URLs for the Sphinx reST ``:doc:`` role.
    :type base_url: str
    :param dict[str, dict] colors: The colors to use when translating reST formatting codes. If not provided, default colors will be used. The dictionary should have keys "heading", "url", and "code" with values that are dictionaries with keys "fg" and "style" that specify the foreground color and style to use. The default value is: ``{ "heading": {"fg": Fore.GREEN, "style": Style.BRIGHT}, "url": {"fg": Fore.CYAN, "style": Style.BRIGHT}, "code": {"fg": Fore.CYAN, "style": Style.DIM}, }``. For more information about the "fg" and "style" values, see the `colorama documentation <https://pypi.org/project/colorama/>`_.
    :param bool group: If True, a ``click.Group`` will be returned, otherwise a ``click.Command`` will be returned. The default is False.

    :rtype: ``CustomRstToAnsiFormatter``
    :return: Returns a sub class of ``click.Command`` that can be used to convert help text from reST to ANSI terminal color encoded text
    """
    base_cls = click.Group if group else click.Command

    # NOTE: It is important to have the FormatHelpMixin as the first base class
    #      such that when click calls self.format_help() it will call format_help()
    #      in the FormatHelpMixin class and not the one in the base_cls.
    class CustomRstToAnsiFormatter(FormatHelpMixin, base_cls):  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            # Initialize FormatHelpMixin with specific arguments
            FormatHelpMixin.__init__(self, base_url=base_url, colors=colors)
            # Pass all positional and keyword arguments to the base class initializer
            base_cls.__init__(self, *args, **kwargs)  # type: ignore

    return CustomRstToAnsiFormatter
