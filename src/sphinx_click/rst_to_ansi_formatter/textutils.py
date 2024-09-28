import re


# NOTE: The ansiwrap module on PyPI does not work for Python 3.12+. So this is temporary
#    replacement until the ansiwrap module is updated.
def ansiwrap_fill(text: str, width: int, subsequent_indent: str = "") -> str:
    """
    Wrap text containing ANSI escape sequences.

    Args:
        text (str): The input text containing ANSI escape sequences.
        width (int): The maximum line width.
        subsequent_indent (str): String that will be prepended to all lines of text except the first.

    Returns:
        str: The wrapped text.
    """
    # Input validation
    if not isinstance(width, int):
        raise TypeError("Width must be an integer.")
    if width <= 0:
        raise ValueError("Width must be greater than zero.")
    if not isinstance(subsequent_indent, str):
        raise TypeError("Subsequent indent must be a string.")
    if len(subsequent_indent) >= width:
        raise ValueError("Subsequent indent length must be less than width.")

    # Regular expression to match ANSI escape sequences
    ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")

    # Tokenize the text into ANSI codes, words, and spaces
    def tokenize(text: str) -> list[tuple[str, str]]:
        tokens = []
        pos = 0
        while pos < len(text):
            # Match ANSI escape codes
            m = ANSI_ESCAPE_RE.match(text, pos)
            if m:
                tokens.append(("ansi", m.group()))
                pos = m.end()
            elif text[pos].isspace():
                # Match spaces
                end = pos
                while (
                    end < len(text)
                    and text[end].isspace()
                    and not ANSI_ESCAPE_RE.match(text, end)
                ):
                    end += 1
                tokens.append(("space", text[pos:end]))
                pos = end
            else:
                # Match words (non-space, non-ANSI sequences)
                end = pos
                while (
                    end < len(text)
                    and not text[end].isspace()
                    and not ANSI_ESCAPE_RE.match(text, end)
                ):
                    end += 1
                tokens.append(("word", text[pos:end]))
                pos = end
        return tokens

    tokens = tokenize(text)

    lines = []
    line = ""
    line_len = 0
    indent = ""
    i = 0
    while i < len(tokens):
        # Adjust current width based on the length of the indent
        current_width = width - len(indent)

        token_type, token_value = tokens[i]
        if token_type == "ansi":
            # Add ANSI codes directly to the line
            line += token_value
        elif token_type == "space":
            # Check if adding spaces would exceed the width
            space_len = len(token_value)
            if line_len + space_len > current_width and line_len > 0:
                # Wrap to next line
                lines.append(indent + line.rstrip(" "))
                line = ""
                line_len = 0
                indent = subsequent_indent
                # Skip leading spaces after wrapping
                while i < len(tokens) and tokens[i][0] == "space":
                    i += 1
                continue  # Reprocess the current token with updated indent and width
            else:
                # Add spaces directly to the line and count their length
                line += token_value
                line_len += space_len
        elif token_type == "word":
            # Measure word length without ANSI codes
            word = token_value
            word_len = len(word)
            if line_len + word_len > current_width and line_len > 0:
                # Wrap to next line
                lines.append(indent + line.rstrip())
                line = ""
                line_len = 0
                indent = subsequent_indent
                continue  # Reprocess the current token with updated indent and width
            line += word
            line_len += word_len
        i += 1

    if line:
        lines.append(indent + line.rstrip(" "))

    return "\n".join(lines)
