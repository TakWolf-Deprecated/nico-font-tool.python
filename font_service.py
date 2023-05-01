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
        outputs_name,
        outputs_dir,
        font_file_path,
        glyph_offset_x=0,
        glyph_offset_y=0,
        glyph_adjust_width=0,
        glyph_adjust_height=0,
):
    # 加载字体文件
    font = TTFont(font_file_path)
    px_units = font['head'].unitsPerEm / font_size
    hhea = font['hhea']
    metrics = font['hmtx'].metrics
    cmap = font.getBestCmap()
    image_font = ImageFont.truetype(font_file_path, font_size)
    logger.info(f'loaded font file: {font_file_path}')

    # 计算行高
    line_height = math.ceil((hhea.ascent - hhea.descent) / px_units)
    line_height += glyph_adjust_height

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
        if advance_width <= 0:
            continue
        advance_width += glyph_adjust_width
        if advance_width <= 0:
            continue

        # 栅格化
        glyph_image = Image.new('RGBA', (advance_width, line_height), (0, 0, 0, 0))
        ImageDraw.Draw(glyph_image).text((glyph_offset_x, glyph_offset_y), c, fill=(0, 0, 0), font=image_font)
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

    # 创建 palette 输出文件夹
    outputs_palette_dir = os.path.join(outputs_dir, 'palette')
    if not os.path.exists(outputs_palette_dir):
        os.makedirs(outputs_palette_dir)

    # 写入 palette .png 图集
    palette_png_file_path = os.path.join(outputs_palette_dir, f'{outputs_name}.png')
    palette = [(255, 255, 255), (0, 0, 0), (255, 0, 255)]
    writer = png.Writer(len(sheet_data[0]), len(sheet_data), palette=palette)
    with open(palette_png_file_path, 'wb') as file:
        writer.write(file, sheet_data)
    logger.info(f'make {palette_png_file_path}')

    # 写入 palette .dat 字母表
    palette_dat_file_path = os.path.join(outputs_palette_dir, f'{outputs_name}.png.dat')
    with open(palette_dat_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f'make {palette_dat_file_path}')

    # 创建 rgba 输出文件夹
    outputs_rgba_dir = os.path.join(outputs_dir, 'rgba')
    if not os.path.exists(outputs_rgba_dir):
        os.makedirs(outputs_rgba_dir)

    # 写入 rgba .png 图集
    rgba_png_file_path = os.path.join(outputs_rgba_dir, f'{outputs_name}.png')
    rgba_bitmap = []
    for sheet_data_row in sheet_data:
        rgba_bitmap_row = []
        for color in sheet_data_row:
            if color == color_transparent:
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(0)
                rgba_bitmap_row.append(0)
            elif color == color_solid:
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
    image.save(rgba_png_file_path)
    logger.info(f'make {rgba_png_file_path}')

    # 写入 rgba .dat 字母表
    rgba_dat_file_path = os.path.join(outputs_rgba_dir, f'{outputs_name}.png.dat')
    with open(rgba_dat_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f'make {rgba_dat_file_path}')
