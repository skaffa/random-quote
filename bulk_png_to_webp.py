# this script is used for initializing the images if the server is fresh

import glob
import os
from webptools import cwebp

png_files = glob.glob('static/images/*.png')

for png_file in png_files:
    webp_file = png_file.replace('.png', '.webp')
    cwebp(png_file, webp_file, "-q 95")
    os.remove(png_file)

    print(f"Converted {png_file} to {webp_file}")

print("Initialization complete.")
