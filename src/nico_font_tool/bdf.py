import os

import bdffont

from nico_font_tool.font import FontRasterizer


class BdfRasterizer(FontRasterizer):
    def __init__(
            self,
            font_file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
            glyph_offset_x: int = 0,
            glyph_offset_y: int = 0,
            glyph_adjust_width: int = 0,
            glyph_adjust_height: int = 0,
    ):
        self.font = bdffont.load_bdf(font_file_path)

        ascent = self.font.properties.font_ascent
        if ascent is None:
            ascent = self.font.bounding_box_height + self.font.bounding_box_offset_y
        descent = -self.font.properties.font_descent
        if descent is None:
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
        glyph = self.font.get_glyph(code_point)
        advance_width = glyph.device_width_x
        if advance_width <= 0:
            return None, None
        adjusted_advance_width = advance_width + self.glyph_adjust_width
        if adjusted_advance_width <= 0:
            return None, None

        glyph_data = [[color for color in bitmap_row] for bitmap_row in glyph.bitmap]
        # Bottom
        append_bottom = glyph.bounding_box_offset_y - self.descent + self.glyph_adjust_height - self.glyph_offset_y
        while append_bottom > 0:
            append_bottom -= 1
            glyph_data.append([])
        while append_bottom < 0:
            append_bottom += 1
            if len(glyph_data) > 0:
                glyph_data.pop()
        # Top
        while len(glyph_data) < self.adjusted_line_height:
            glyph_data.insert(0, [])
        while len(glyph_data) > self.adjusted_line_height:
            glyph_data.pop(0)
        # Left
        append_left = glyph.bounding_box_offset_x + self.glyph_offset_x
        while append_left > 0:
            append_left -= 1
            for glyph_data_row in glyph_data:
                glyph_data_row.insert(0, 0)
        while append_left < 0:
            append_left += 1
            for glyph_data_row in glyph_data:
                if len(glyph_data_row) > 0:
                    glyph_data_row.pop(0)
        # Right
        for glyph_data_row in glyph_data:
            while len(glyph_data_row) < adjusted_advance_width:
                glyph_data_row.append(0)
            while len(glyph_data_row) > adjusted_advance_width:
                glyph_data_row.pop()

        return glyph_data, adjusted_advance_width
