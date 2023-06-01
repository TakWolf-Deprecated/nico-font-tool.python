import logging
import os

import png

from nico_font_tool.bdf import BdfRasterizer
from nico_font_tool.font import FontRasterizer
from nico_font_tool.opentype import OpenTypeRasterizer

logger = logging.getLogger('nico-font-tool')

_GLYPH_DATA_TRANSPARENT = 0
_GLYPH_DATA_SOLID = 1
_GLYPH_DATA_BORDER = 2


def create_sheet(
        font_file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        font_size: int = None,
        glyph_offset_x: int = 0,
        glyph_offset_y: int = 0,
        glyph_adjust_width: int = 0,
        glyph_adjust_height: int = 0,
) -> tuple[list[list[int]], list[str]]:
    font_rasterizer: FontRasterizer
    font_ext = os.path.splitext(font_file_path)[1]
    if font_ext == '.otf' or font_ext == '.ttf' or font_ext == '.woff' or font_ext == '.woff2':
        if font_size is None:
            raise Exception('OpenType need a font size')
        font_rasterizer = OpenTypeRasterizer(
            font_file_path,
            font_size,
            glyph_offset_x,
            glyph_offset_y,
            glyph_adjust_width,
            glyph_adjust_height,
        )
    elif font_ext == '.bdf':
        font_rasterizer = BdfRasterizer(
            font_file_path,
            glyph_offset_x,
            glyph_offset_y,
            glyph_adjust_width,
            glyph_adjust_height,
        )
    else:
        raise Exception(f'Font file type not supported: {font_ext}')
    logger.info(f"Loaded font file: '{font_file_path}'")

    sheet_data = [[_GLYPH_DATA_BORDER] for _ in range(font_rasterizer.adjusted_line_height)]
    alphabet = []

    for code_point in font_rasterizer.get_code_point_sequence():
        c = chr(code_point)
        if not c.isprintable():
            continue

        glyph_data, adjusted_advance_width = font_rasterizer.rasterize_glyph(code_point)
        if glyph_data is None:
            continue
        logger.info(f'Rasterize glyph: {code_point} - {c} - {adjusted_advance_width}')

        for y in range(font_rasterizer.adjusted_line_height):
            for x in range(adjusted_advance_width):
                if glyph_data[y][x] > 0:
                    sheet_data[y].append(_GLYPH_DATA_SOLID)
                else:
                    sheet_data[y].append(_GLYPH_DATA_TRANSPARENT)
            sheet_data[y].append(_GLYPH_DATA_BORDER)

        alphabet.append(c)

    return sheet_data, alphabet


def save_palette_png(
        sheet_data: list[list[int]],
        outputs_dir: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        outputs_name: str,
):
    palette = [(255, 255, 255), (0, 0, 0), (255, 0, 255)]
    writer = png.Writer(len(sheet_data[0]), len(sheet_data), palette=palette)
    png_file_path = os.path.join(outputs_dir, f'{outputs_name}.png')
    with open(png_file_path, 'wb') as file:
        writer.write(file, sheet_data)
    logger.info(f"Make: '{png_file_path}'")


def save_rgba_png(
        sheet_data: list[list[int]],
        outputs_dir: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        outputs_name: str,
):
    rgba_bitmap = []
    for sheet_data_row in sheet_data:
        rgba_bitmap_row = []
        for color in sheet_data_row:
            if color == _GLYPH_DATA_TRANSPARENT:
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(0)
            elif color == _GLYPH_DATA_SOLID:
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(255)
            else:
                rgba_bitmap_row.append(255)
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(255)
                rgba_bitmap_row.append(255)
        rgba_bitmap.append(rgba_bitmap_row)
    image = png.from_array(rgba_bitmap, 'RGBA')
    png_file_path = os.path.join(outputs_dir, f'{outputs_name}.png')
    image.save(png_file_path)
    logger.info(f"Make: '{png_file_path}'")


def save_dat_file(
        alphabet: list[str],
        outputs_dir: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        outputs_name: str,
):
    dat_file_path = os.path.join(outputs_dir, f'{outputs_name}.png.dat')
    with open(dat_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f"Make: '{dat_file_path}'")
