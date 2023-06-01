import os

from bdffont import BdfFont

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
        self.font = BdfFont.load(font_file_path)

        ascent = self.font.properties.font_ascent
        descent = -self.font.properties.font_descent
        if ascent is None or descent is None:
            max_top = 0
            min_bottom = 0
            for glyph in self.font.code_point_to_glyph.values():
                (_, bounding_box_height), (_, bounding_box_offset_y), _ = glyph.get_8bit_aligned_bitmap(optimize_bitmap=True)
                top = bounding_box_height + bounding_box_offset_y
                if top > max_top:
                    max_top = top
                bottom = bounding_box_offset_y
                if bottom < min_bottom:
                    min_bottom = bottom
            if ascent is None:
                ascent = max_top
            if descent is None:
                descent = min_bottom

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
