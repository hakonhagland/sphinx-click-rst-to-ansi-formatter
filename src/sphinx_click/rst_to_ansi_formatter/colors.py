from colorama import Fore, Style

from .types import ColorDict


class Colors:
    def __init__(self, colors: ColorDict | None = None):
        if colors is None:
            colors = {
                "heading": {"fg": Fore.GREEN, "style": Style.BRIGHT},
                "url": {"fg": Fore.CYAN, "style": Style.BRIGHT},
                "code": {"fg": Fore.CYAN, "style": Style.DIM},
            }
        self.colors = colors

    def apply_color(self, txt: str, color: str) -> str:
        return (  # type: ignore
            self.colors[color]["fg"]
            + self.colors[color]["style"]
            + txt
            + Style.RESET_ALL
        )

    def color_heading(self, txt: str) -> str:
        return self.apply_color(txt, "heading")

    def color_url(self, txt: str) -> str:
        return self.apply_color(txt, "url")

    def color_code(self, txt: str) -> str:
        return self.apply_color(txt, "code")
