import argparse
import logging
import os

import nico_font_tool

logging.basicConfig(level=logging.DEBUG)


def execute(args: argparse.Namespace):
    font_file_path: str = args.font_file_path
    outputs_dir: str = args.outputs_dir
    outputs_name: str = args.outputs_name
    font_size: int | None = args.font_size
    glyph_offset_x: int = args.glyph_offset_x
    glyph_offset_y: int = args.glyph_offset_y
    glyph_adjust_width: int = args.glyph_adjust_width
    glyph_adjust_height: int = args.glyph_adjust_height
    mode: str = args.mode

    if mode != 'palette' and mode != 'rgba':
        raise Exception(f"Unsupported png mode: '{mode}'")

    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    sheet_data, alphabet = nico_font_tool.create_sheet(
        font_file_path,
        font_size,
        glyph_offset_x,
        glyph_offset_y,
        glyph_adjust_width,
        glyph_adjust_height,
    )

    if mode == 'palette':
        nico_font_tool.save_palette_png(sheet_data, outputs_dir, outputs_name)
        nico_font_tool.save_dat_file(alphabet, outputs_dir, outputs_name)
    elif mode == 'rgba':
        nico_font_tool.save_rgba_png(sheet_data, outputs_dir, outputs_name)
        nico_font_tool.save_dat_file(alphabet, outputs_dir, outputs_name)


def main():
    parser = argparse.ArgumentParser(
        prog='NICO Font Tool',
        description='A tool for converting fonts to NICO Game Framework format fonts',
    )
    parser.add_argument('font_file_path', type=str, help='The OpenType or BDF font file path.')
    parser.add_argument('outputs_dir', type=str, help='Output files dir.')
    parser.add_argument('outputs_name', type=str, help='Output files name.')
    parser.add_argument('-fs', '--font_size', type=int, help='Glyph rasterize size when using OpenType font.')
    parser.add_argument('-gox', '--glyph_offset_x', type=int, default=0, help='Glyph offset x.')
    parser.add_argument('-goy', '--glyph_offset_y', type=int, default=0, help='Glyph offset y.')
    parser.add_argument('-gaw', '--glyph_adjust_width', type=int, default=0, help='Glyph adjust width.')
    parser.add_argument('-gah', '--glyph_adjust_height', type=int, default=0, help='Glyph adjust height.')
    parser.add_argument('-m', '--mode', type=str, default='palette', help="Png sheet color mode, can be 'palette' or 'rgba', default is 'palette'.")
    execute(parser.parse_args())


if __name__ == '__main__':
    main()
