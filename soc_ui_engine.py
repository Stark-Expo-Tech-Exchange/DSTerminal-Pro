import os
import shutil
import unicodedata
from wcwidth import wcswidth


class SOCUIEngine:
    """
    Auto-resizing SOC dashboard renderer
    - terminal-aware layout
    - emoji-safe centering
    - cross-platform compatibility
    """

    def __init__(self, padding=2):
        self.padding = padding

    # -----------------------------
    # TERMINAL SIZE DETECTION
    # -----------------------------
    def get_terminal_size(self):
        size = shutil.get_terminal_size(fallback=(120, 40))
        return size.columns, size.lines

    # -----------------------------
    # SAFE STRING WIDTH (emoji-aware)
    # -----------------------------
    def display_width(self, text: str) -> int:
        """
        Returns correct visual width (handles emojis properly)
        """
        if not text:
            return 0
        return max(0, wcswidth(text))

    # -----------------------------
    # CENTER TEXT
    # -----------------------------
    def center_line(self, text: str, width: int) -> str:
        text_width = self.display_width(text)
        if text_width >= width:
            return text[:width]
        spaces = (width - text_width) // 2
        return " " * spaces + text

    # -----------------------------
    # RENDER BOX
    # -----------------------------
    def render_box(self, lines):
        term_width, _ = self.get_terminal_size()
        content_width = term_width - self.padding * 2

        top = "╔" + "═" * (term_width - 2) + "╗"
        bottom = "╚" + "═" * (term_width - 2) + "╝"
        separator = "╠" + "═" * (term_width - 2) + "╣"

        output = [top]

        for line in lines:
            clean_line = self.center_line(line, content_width)
            padded = clean_line.ljust(content_width)

            output.append(
                "║" + " " * self.padding + padded + " " * self.padding + "║"
            )

        output.append(bottom)
        return "\n".join(output)

    # -----------------------------
    # RENDER HEADER (SOC READY)
    # -----------------------------
    def render_header(self, title_lines):
        return self.render_box(title_lines)