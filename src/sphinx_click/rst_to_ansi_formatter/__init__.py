import colorama

# Import the make_rst_to_ansi_formatter function to make it available at the package level
from .formatter import make_rst_to_ansi_formatter

# Initialize colorama to auto-reset styles after each print
colorama.init(autoreset=True)

# Define __all__ to explicitly declare which names are supposed to be
# public when * importing
__all__ = ["make_rst_to_ansi_formatter"]
