# NICO Font Tool - Python

[![PyPI](https://img.shields.io/pypi/v/nico-font-tool)](https://pypi.org/project/nico-font-tool/)

A tool for converting fonts to [NICO Game Framework](https://github.com/ftsf/nico) format fonts.

This is the Python version. The Nim version see: [nico-font-tool](https://github.com/TakWolf/nico-font-tool).

## Installation

```commandline
pip install nico-font-tool
```

## Usage

### Command

Use `nicofont -h` to learn more.

```commandline
nicofont ./assets/fonts/quan/quan.ttf ./build/quan quan --font_size 8 -gaw -1
```

### Scripts

See: [Demo](examples/demo.py)

```python
sheet_data, alphabet = nico_font_tool.create_sheet(
    font_file_path,
    font_size,
    glyph_offset_x,
    glyph_offset_y,
    glyph_adjust_width,
    glyph_adjust_height,
)

nico_font_tool.save_palette_png(sheet_data, outputs_dir, outputs_name)
nico_font_tool.save_dat_file(alphabet, outputs_dir, outputs_name)
    
nico_font_tool.save_rgba_png(sheet_data, outputs_dir, outputs_name)
nico_font_tool.save_dat_file(alphabet, outputs_dir, outputs_name)
```

## License

Under the [MIT license](LICENSE).
