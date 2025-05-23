"""
Author: twb9413
File: imageProcessor.py

Desc:
This file hanldes all functions image related
"""

import os
from PIL import Image

def showImages(image_dir):
    for filename in os.listdir(image_dir):
        f = os.path.join(image_dir, filename)
        if os.path.isfile(f):
            print(f)
            showImage(f)


def showImage(image_file):
    im = Image.open(image_file)
    im.show()

