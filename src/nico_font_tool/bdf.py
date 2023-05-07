import os

import bdffont
from bdffont import BdfFont

from nico_font_tool.font import FontRasterizer


class BdfRasterizer(FontRasterizer):
    font: BdfFont

    def __init__(
            self,
            font_file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
            glyph_offset_x: int = 0,
            glyph_offset_y: int = 0,
            glyph_adjust_width: int = 0,
            glyph_adjust_height: int = 0,
    ):
        self.font = bdffont.load_bdf(font_file_path)

        if 'FONT_ASCENT' in self.font.properties:
            ascent = self.font.properties.font_ascent
        else:
            ascent = self.font.bounding_box_height + self.font.bounding_box_offset_y

        if 'FONT_DESCENT' in self.font.properties:
            descent = -self.font.properties.font_descent
        else:
            descent = self.font.bounding_box_offset_y

        super().__init__(
            ascent,
            descent,
            glyph_offset_x,
            glyph_offset_y,
            glyph_adjust_width,
            glyph_adjust_height,
        )

    def get_code_point_sequence(self) -> list[int]:
        sequence = list(self.font.code_point_to_glyph.keys())
        sequence.sort()
        return sequence

    def rasterize_glyph(self, code_point: int) -> tuple[list[list[int]] | None, int | None]:
        glyph = self.font.code_point_to_glyph[code_point]
        advance_width = glyph.device_width_x
        if advance_width <= 0:
            return None, None
        adjusted_advance_width = advance_width + self.glyph_adjust_width
        if adjusted_advance_width <= 0:
            return None, None

        glyph_data = []
        for y in range(self.adjusted_line_height):
            glyph_data_row = []
            for x in range(adjusted_advance_width):
                x -= self.glyph_offset_x
                y -= self.glyph_offset_y
                if 0 <= y < len(glyph.bitmap):
                    bitmap_row = glyph.bitmap[y]
                    if 0 <= x < len(bitmap_row):
                        glyph_data_row.append(bitmap_row[x])
                    else:
                        glyph_data_row.append(0)
                else:
                    glyph_data_row.append(0)
            glyph_data.append(glyph_data_row)

        return glyph_data, adjusted_advance_width
