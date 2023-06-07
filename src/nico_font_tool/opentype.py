import math
import os
from typing import Iterator

from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

from nico_font_tool.font import FontRasterizer


class OpenTypeRasterizer(FontRasterizer):
    def __init__(
            self,
            font_file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
            font_size: int,
            glyph_offset_x: int = 0,
            glyph_offset_y: int = 0,
            glyph_adjust_width: int = 0,
            glyph_adjust_height: int = 0,
    ):
        self.font = TTFont(font_file_path)
        self.image_font = ImageFont.truetype(font_file_path, font_size)

        self.px_units = self.font['head'].unitsPerEm / font_size
        ascent = math.ceil(self.font['hhea'].ascent / self.px_units)
        descent = math.floor(self.font['hhea'].descent / self.px_units)

        super().__init__(
            ascent,
            descent,
            glyph_offset_x,
            glyph_offset_y,
            glyph_adjust_width,
            glyph_adjust_height,
        )

    def rasterize_glyphs_in_order(self) -> Iterator[tuple[str, list[list[int]], int]]:
        code_points = list(self.font.getBestCmap().keys())
        code_points.sort()
        for code_point in code_points:
            c = chr(code_point)
            if not c.isprintable():
                continue

            glyph_name = self.font.getBestCmap()[code_point]
            advance_width = math.ceil(self.font['hmtx'].metrics[glyph_name][0] / self.px_units)
            if advance_width <= 0:
                continue
            adjusted_advance_width = advance_width + self.glyph_adjust_width
            if adjusted_advance_width <= 0:
                continue

            glyph_image = Image.new('RGBA', (adjusted_advance_width, self.adjusted_line_height), (0, 0, 0, 0))
            ImageDraw.Draw(glyph_image).text(
                xy=(self.glyph_offset_x, self.glyph_offset_y),
                text=chr(code_point),
                fill=(0, 0, 0),
                font=self.image_font,
            )
            glyph_data = []
            for y in range(self.adjusted_line_height):
                glyph_data_row = []
                for x in range(adjusted_advance_width):
                    alpha = glyph_image.getpixel((x, y))[3]
                    if alpha > 127:
                        glyph_data_row.append(1)
                    else:
                        glyph_data_row.append(0)
                glyph_data.append(glyph_data_row)

            yield c, glyph_data, adjusted_advance_width
