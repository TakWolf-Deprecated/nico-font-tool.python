import logging
import os

import nico_font_tool
from examples import fonts_dir, outputs_dir

logging.basicConfig(level=logging.DEBUG)


def main():
    nico_font_tool.create_font_sheet(
        font_size=8,
        outputs_name='quan',
        outputs_dir=outputs_dir,
        font_file_path=os.path.join(fonts_dir, 'quan', 'quan.ttf'),
        glyph_adjust_width=-1,
        glyph_adjust_height=-1,
    )
    nico_font_tool.create_font_sheet(
        font_size=12,
        outputs_name='fusion-pixel-monospaced',
        outputs_dir=outputs_dir,
        font_file_path=os.path.join(fonts_dir, 'fusion-pixel-monospaced', 'fusion-pixel-monospaced.otf'),
        glyph_offset_y=-1,
        glyph_adjust_width=-1,
        glyph_adjust_height=-1,
    )
    nico_font_tool.create_font_sheet(
        font_size=12,
        outputs_name='fusion-pixel-proportional',
        outputs_dir=outputs_dir,
        font_file_path=os.path.join(fonts_dir, 'fusion-pixel-proportional', 'fusion-pixel-proportional.otf'),
        glyph_offset_y=-1,
        glyph_adjust_width=-1,
        glyph_adjust_height=-1,
    )
    nico_font_tool.create_font_sheet(
        font_size=16,
        outputs_name='unifont',
        outputs_dir=outputs_dir,
        font_file_path=os.path.join(fonts_dir, 'unifont', 'unifont-15.0.01.ttf'),
        glyph_adjust_width=-1,
    )
    nico_font_tool.create_font_sheet(
        font_size=24,
        outputs_name='roboto',
        outputs_dir=outputs_dir,
        font_file_path=os.path.join(fonts_dir, 'roboto', 'Roboto-Regular.ttf'),
    )


if __name__ == '__main__':
    main()
