
class FontRasterizer:
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

    def get_code_point_sequence(self) -> list[int]:
        raise NotImplementedError()

    def rasterize_glyph(self, code_point: int) -> tuple[list[list[int]] | None, int | None]:
        raise NotImplementedError()
