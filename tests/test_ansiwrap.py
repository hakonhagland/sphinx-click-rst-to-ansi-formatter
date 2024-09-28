# test_ansiwrap.py

import pytest
from sphinx_click.rst_to_ansi_formatter.textutils import ansiwrap_fill


def test_simple_text() -> None:
    text = "This is a simple text without ANSI codes."
    expected = "This is a simple text without ANSI\ncodes."
    result = ansiwrap_fill(text, width=35)
    assert result == expected


def test_text_with_ansi_codes() -> None:
    text = "This is a \x1b[31mred\x1b[0m text with ANSI codes."
    expected = "This is a \x1b[31mred\x1b[0m text with ANSI\ncodes."
    result = ansiwrap_fill(text, width=30)
    assert result == expected


def test_long_word_exceeds_width() -> None:
    text = "ThisIsAnExtremelyLongWordThatExceedsTheWidth"
    expected = "ThisIsAnExtremelyLongWordThatExceedsTheWidth"
    result = ansiwrap_fill(text, width=20)
    assert result == expected


def test_subsequent_indent() -> None:
    text = "This text should be indented on subsequent lines."
    expected = "This text should be indented\n    on subsequent lines."
    result = ansiwrap_fill(text, width=30, subsequent_indent="    ")
    assert result == expected


def test_empty_string() -> None:
    text = ""
    expected = ""
    result = ansiwrap_fill(text, width=50)
    assert result == expected


def test_unicode_characters() -> None:
    text = "Unicode test: 😊 🚀 🌟"
    expected = "Unicode test: 😊 🚀 🌟"
    result = ansiwrap_fill(text, width=50)
    assert result == expected


def test_text_with_newlines() -> None:
    text = "Line1\nLine2\nLine3"
    expected = "Line1\nLine2\nLine3"
    result = ansiwrap_fill(text, width=50)
    assert result == expected


def test_wrapping_with_ansi_and_indent() -> None:
    text = "This is a \x1b[31mred\x1b[0m text that should wrap and indent properly."
    expected = (
        "This is a \x1b[31mred\x1b[0m text that should wrap\n"
        "    and indent properly."
    )
    result = ansiwrap_fill(text, width=35, subsequent_indent="    ")
    assert result == expected


def test_width_smaller_than_longest_word() -> None:
    text = "This is a test with alongwordthatexceedsthewidth."
    expected = "This is a test with\nalongwordthatexceedsthewidth."
    result = ansiwrap_fill(text, width=20)
    assert result == expected


def test_multiple_consecutive_spaces() -> None:
    text = "This    text  has   multiple spaces."
    expected = "This    text  has   multiple\nspaces."
    result = ansiwrap_fill(text, width=30)
    assert result == expected


def test_non_printable_characters() -> None:
    text = "This text has non-printable characters: \x07\x08\x0c"
    expected = "This text has non-printable\ncharacters: \x07\x08\x0c"
    result = ansiwrap_fill(text, width=35)
    assert result == expected


def test_long_text_with_ansi() -> None:
    text = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "\x1b[32mUt enim ad minim veniam\x1b[0m, quis nostrud exercitation ullamco "
        "laboris nisi ut aliquip ex ea commodo consequat."
    )
    expected = (
        "Lorem ipsum dolor sit amet,\n"
        "consectetur adipiscing elit. Sed do\n"
        "eiusmod tempor incididunt ut labore\n"
        "et dolore magna aliqua. \x1b[32mUt enim ad\n"
        "minim veniam\x1b[0m, quis nostrud\n"
        "exercitation ullamco laboris nisi\n"
        "ut aliquip ex ea commodo consequat."
    )
    result = ansiwrap_fill(text, width=35)
    assert result == expected


def test_indent_affects_line_width() -> None:
    text = "1 2 3 4 5 6 7 8 9 0"
    expected = "1 2 3 4\n  5 6 7\n  8 9 0"
    result = ansiwrap_fill(text, width=8, subsequent_indent="  ")
    assert result == expected


def test_multiple_ansi_codes_in_word() -> None:
    text = "\x1b[31mR\x1b[32me\x1b[34md\x1b[0m text with multiple ANSI codes."
    expected = "\x1b[31mR\x1b[32me\x1b[34md\x1b[0m text with multiple ANSI\ncodes."
    result = ansiwrap_fill(text, width=30)
    assert result == expected


def test_ansi_codes_at_line_wrap() -> None:
    text = "This is a test with \x1b[31mred text\x1b[0m that wraps."
    expected = "This is a test with \x1b[31mred\ntext\x1b[0m that wraps."
    result = ansiwrap_fill(text, width=25)
    assert result == expected


def test_line_ends_with_ansi_code() -> None:
    text = "Test \x1b[31mred\x1b[0m"
    expected = "Test \x1b[31mred\x1b[0m"
    result = ansiwrap_fill(text, width=10)
    assert result == expected


def test_text_with_tabs() -> None:
    text = "Column1\tColumn2\tColumn3"
    expected = "Column1\tColumn2\tColumn3"
    result = ansiwrap_fill(text, width=50)
    assert result == expected


def test_trailing_spaces_preserved() -> None:
    text = "Trailing spaces    "
    expected = "Trailing spaces"
    result = ansiwrap_fill(text, width=20)
    assert result == expected


def test_leading_spaces_preserved() -> None:
    text = "    Leading spaces"
    expected = "    Leading spaces"
    result = ansiwrap_fill(text, width=20)
    assert result == expected


def test_wrapping_preserves_internal_spaces() -> None:
    text = "This  text   has    multiple     spaces."
    expected = "This  text   has    multiple\nspaces."
    result = ansiwrap_fill(text, width=35)
    assert result == expected


def test_zero_width() -> None:
    text = "Text with zero width."
    with pytest.raises(ValueError):
        ansiwrap_fill(text, width=0)


def test_negative_width() -> None:
    text = "Text with negative width."
    with pytest.raises(ValueError):
        ansiwrap_fill(text, width=-10)


def test_non_integer_width() -> None:
    text = "Text with non-integer width."
    with pytest.raises(TypeError):
        ansiwrap_fill(text, width="twenty")  # type: ignore[arg-type]


def test_subsequent_indent_longer_than_width() -> None:
    text = "This text tests subsequent_indent longer than width."
    with pytest.raises(ValueError):
        ansiwrap_fill(text, width=20, subsequent_indent=" " * 21)


def test_non_string_subsequent_indent() -> None:
    text = "This text has a non-string subsequent_indent."
    with pytest.raises(TypeError):
        ansiwrap_fill(text, width=40, subsequent_indent=5)  # type: ignore[arg-type]


def test_skip_leading_spaces_after_wrap() -> None:
    text = "Word    Word"
    expected = "Word\nWord"
    result = ansiwrap_fill(text, width=5)
    assert result == expected


def test_wrapping_with_leading_spaces() -> None:
    text = "This is a test with  multiple   spaces that will cause wrapping."
    expected = (
        "This is a test with\n" "  multiple   spaces that\n  will cause wrapping."
    )
    result = ansiwrap_fill(text, width=25, subsequent_indent="  ")
    assert result == expected
