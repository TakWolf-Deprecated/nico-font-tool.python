import os
import shutil

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
fonts_dir = os.path.join(project_root_dir, 'assets', 'fonts')
outputs_dir = os.path.join(project_root_dir, 'build', 'tests')

if os.path.exists(outputs_dir):
    shutil.rmtree(outputs_dir)
os.makedirs(outputs_dir)
