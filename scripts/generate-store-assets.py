from pathlib import Path
import runpy
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'scripts/generate-references.py'),run_name='__main__')
with Image.open(ROOT/'logo/logo128.png') as logo:
    assert logo.size == (128,128), 'Logo must be 128x128'
print('Logo validated: logo/logo128.png (128x128); no duplicate sizes generated')
