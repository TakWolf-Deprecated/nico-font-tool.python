import logging
import math
import os

import png
from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

logger = logging.getLogger('font-service')

color_transparent = 0
color_solid = 1
color_border = 2


def create_font_sheet(
        font_size,
        output_name,
        output_dir,
        font_file_path,
        rasterize_offset_xy=(0, 0),
        rasterize_adjust_width=0,
        rasterize_adjust_height=0,
):
    # 加载字体文件
    font = TTFont(font_file_path)
    units_per_em = font['head'].unitsPerEm
    px_units = units_per_em / font_size
    hhea = font['hhea']
    metrics = font['hmtx'].metrics
    cmap = font.getBestCmap()
    image_font = ImageFont.truetype(font_file_path, font_size)
    logger.info(f'loaded font file: {font_file_path}')

    # 计算行高
    line_height = math.ceil((hhea.ascent - hhea.descent) / px_units)
    line_height += rasterize_adjust_height

    # 图集对象，初始化左边界
    sheet_data = [[color_border] for _ in range(line_height)]

    # 字母表
    alphabet = []

    # 遍历字体全部字符
    for code_point, glyph_name in cmap.items():
        c = chr(code_point)
        if not c.isprintable():
            continue

        advance_width = math.ceil(metrics[glyph_name][0] / px_units)
        advance_width += rasterize_adjust_width
        if advance_width <= 0:
            continue

        # 栅格化
        glyph_image = Image.new('RGBA', (advance_width, line_height), (0, 0, 0, 0))
        ImageDraw.Draw(glyph_image).text(rasterize_offset_xy, c, fill=(0, 0, 0), font=image_font)
        logger.info(f'rasterize char: {code_point} - {c}')

        # 二值化字形，合并到图集
        for y in range(line_height):
            sheet_data_row = sheet_data[y]
            for x in range(advance_width):
                alpha = glyph_image.getpixel((x, y))[3]
                if alpha > 127:
                    sheet_data_row.append(color_solid)
                else:
                    sheet_data_row.append(color_transparent)
            sheet_data_row.append(color_border)

        # 添加到字母表
        alphabet.append(c)

    # 图集底部添加 1 像素边界
    sheet_data.append([color_border for _ in range(len(sheet_data[0]))])

    # 创建 L 输出文件夹
    output_l_dir = os.path.join(output_dir, 'L')
    if not os.path.exists(output_l_dir):
        os.makedirs(output_l_dir)

    # 写入 L .png 图集
    output_l_png_file_path = os.path.join(output_l_dir, f'{output_name}.png')
    image = png.from_array(sheet_data, 'L')
    image.save(output_l_png_file_path)
    logger.info(f'make {output_l_png_file_path}')

    # 写入 L .dat 字母表
    output_l_dat_file_path = os.path.join(output_l_dir, f'{output_name}.png.dat')
    with open(output_l_dat_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f'make {output_l_dat_file_path}')

    # 创建 RGBA 输出文件夹
    output_rgba_dir = os.path.join(output_dir, 'RGBA')
    if not os.path.exists(output_rgba_dir):
        os.makedirs(output_rgba_dir)

    # 写入 RGBA .png 图集
    output_rgba_png_file_path = os.path.join(output_rgba_dir, f'{output_name}.png')
    output_rgba_bitmap = []
    for sheet_data_row in sheet_data:
        output_rgba_bitmap_row = []
        for color in sheet_data_row:
            if color == color_transparent:
                output_rgba_bitmap_row.append(0)
                output_rgba_bitmap_row.append(0)
                output_rgba_bitmap_row.append(0)
                output_rgba_bitmap_row.append(0)
            elif color == color_solid:
                output_rgba_bitmap_row.append(0)
                output_rgba_bitmap_row.append(0)
                output_rgba_bitmap_row.append(0)
                output_rgba_bitmap_row.append(255)
            else:
                output_rgba_bitmap_row.append(255)
                output_rgba_bitmap_row.append(0)
                output_rgba_bitmap_row.append(255)
                output_rgba_bitmap_row.append(255)
        output_rgba_bitmap.append(output_rgba_bitmap_row)
    image = png.from_array(output_rgba_bitmap, 'RGBA')
    image.save(output_rgba_png_file_path)
    logger.info(f'make {output_rgba_png_file_path}')

    # 写入 RGBA .dat 字母表
    output_rgba_dat_file_path = os.path.join(output_rgba_dir, f'{output_name}.png.dat')
    with open(output_rgba_dat_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f'make {output_rgba_dat_file_path}')
