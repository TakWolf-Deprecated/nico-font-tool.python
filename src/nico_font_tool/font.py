from abc import ABCMeta, abstractmethod
from typing import Iterator


class FontRasterizer(metaclass=ABCMeta):
    def __init__(
            self,
            ascent: int,
            descent: int,
            glyph_offset_x: int = 0,
            glyph_offset_y: int = 0,
            glyph_adjust_width: int = 0,
            glyph_adjust_height: int = 0,
    ):
        self.ascent = ascent
        self.descent = descent
        self.glyph_offset_x = glyph_offset_x
        self.glyph_offset_y = glyph_offset_y
        self.glyph_adjust_width = glyph_adjust_width
        self.glyph_adjust_height = glyph_adjust_height

    @property
    def line_height(self) -> int:
        return self.ascent - self.descent

    @property
    def adjusted_line_height(self) -> int:
        return self.line_height + self.glyph_adjust_height

    @abstractmethod
    def rasterize_glyphs_in_order(self) -> Iterator[tuple[str, list[list[int]], int]]:
        raise NotImplementedError()
