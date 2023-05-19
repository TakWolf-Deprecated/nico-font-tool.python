import logging
import os

import nico_font_tool
from examples import fonts_dir, outputs_dir

logging.basicConfig(level=logging.DEBUG)


def convert_font(
        font_file_name: str,
        outputs_name: str,
        font_size: int = None,
        glyph_offset_x: int = 0,
        glyph_offset_y: int = 0,
        glyph_adjust_width: int = 0,
        glyph_adjust_height: int = 0,
):
    font_file_path = os.path.join(fonts_dir, font_file_name)
    sheet_data, alphabet = nico_font_tool.create_sheet(
        font_file_path,
        font_size,
        glyph_offset_x,
        glyph_offset_y,
        glyph_adjust_width,
        glyph_adjust_height,
    )

    palette_outputs_dir = os.path.join(outputs_dir, 'palette')
    if not os.path.exists(palette_outputs_dir):
        os.makedirs(palette_outputs_dir)
    nico_font_tool.save_palette_png(sheet_data, palette_outputs_dir, outputs_name)
    nico_font_tool.save_dat_file(alphabet, palette_outputs_dir, outputs_name)
    
    rgba_outputs_dir = os.path.join(outputs_dir, 'rgba')
    if not os.path.exists(rgba_outputs_dir):
        os.makedirs(rgba_outputs_dir)
    nico_font_tool.save_rgba_png(sheet_data, rgba_outputs_dir, outputs_name)
    nico_font_tool.save_dat_file(alphabet, rgba_outputs_dir, outputs_name)


def main():
    convert_font(
        font_file_name='quan/quan.ttf',
        outputs_name='quan',
        font_size=8,
    )
    convert_font(
        font_file_name='fusion-pixel-monospaced/fusion-pixel-monospaced.otf',
        outputs_name='fusion-pixel-monospaced',
        font_size=12,
    )
    convert_font(
        font_file_name='fusion-pixel-proportional/fusion-pixel-proportional.otf',
        outputs_name='fusion-pixel-proportional',
        font_size=12,
    )
    convert_font(
        font_file_name='galmuri/Galmuri9.ttf',
        outputs_name='galmuri9',
        font_size=10,
    )
    convert_font(
        font_file_name='galmuri/Galmuri9.bdf',
        outputs_name='galmuri9-bdf',
    )
    convert_font(
        font_file_name='unifont/unifont-15.0.01.ttf',
        outputs_name='unifont',
        font_size=16,
    )
    convert_font(
        font_file_name='unifont/unifont-15.0.01.bdf',
        outputs_name='unifont-bdf',
    )
    convert_font(
        font_file_name='roboto/Roboto-Regular.ttf',
        outputs_name='roboto',
        font_size=24,
    )


if __name__ == '__main__':
    main()
