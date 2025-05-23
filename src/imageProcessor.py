"""
Author: twb9413
File: imageProcessor.py

Desc:
This file hanldes all functions image related
"""

import os
from PIL import Image
import numpy as np

def TestStuff(image_file):
    im = Image.open("test-block.png")
    imgArr = np.asarray(im, dtype=np.uint32)
    rSum = 0
    gSum = 0
    bSum = 0
    rAvg = 0
    gAvg = 0
    bAvg = 0
    width = im.width
    for lineArr in imgArr:
        for pixelArr in lineArr:
            rSum += pixelArr[0]
            gSum += pixelArr[1]
            bSum += pixelArr[2]
        # do the running avg, reset sums
        rAvg = ((rAvg + rSum) // (width + 1))
        gAvg = ((gAvg + gSum) // (width + 1))
        bAvg = ((bAvg + bSum) // (width + 1))
        print(rAvg, gAvg, bAvg)

        rSum = 0
        gSum = 0
        bSum = 0
    print(rAvg, gAvg, bAvg)



def showImages(image_dir):
    for filename in os.listdir(image_dir):
        f = os.path.join(image_dir, filename)
        if os.path.isfile(f):
            print(f)
            showImage(f)


def showImage(image_file):
    im = Image.open(image_file)
    im.show()

TestStuff(0)
