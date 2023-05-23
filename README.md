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
nicofont your/font/file/path.ttf outputs/dir outputs_name --font_size 8
```

### Scripts

See: [demo](examples/demo.py)

```python
import nico_font_tool

sheet_data, alphabet = nico_font_tool.create_sheet(
    font_file_path='your/font/file/path.ttf', 
    font_size=8,
)

nico_font_tool.save_palette_png(sheet_data, 'outputs/palette/dir', 'outputs_name')
nico_font_tool.save_dat_file(alphabet, 'outputs/palette/dir', 'outputs_name')
    
nico_font_tool.save_rgba_png(sheet_data, 'outputs/rgba/dir', 'outputs_name')
nico_font_tool.save_dat_file(alphabet, 'outputs/rgba/dir', 'outputs_name')
```

## Dependencies

- [FontTools](https://github.com/fonttools/fonttools)
- [Brotli](https://github.com/google/brotli)
- [BdfFont](https://github.com/TakWolf/bdffont)
- [Pillow](https://github.com/python-pillow/Pillow)
- [PyPNG](https://gitlab.com/drj11/pypng)

## License

Under the [MIT license](LICENSE).
