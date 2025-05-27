"""
Author: twb9413
File: imageProcessor.py

Desc:
This file hanldes all functions image related
"""

import os
from PIL import Image
import numpy as np
from scipy.spatial import KDTree

BLOCK_DICT = {}
PALETTE = []
PALETTE_TREE = None
os.environ['DISPLAY'] = ''

def mcPG_init(im_dir):
    """
    mcPG_init(im_dir)
    Called to initialize the:
    - block:color dict
    - Palette KDTree
    """
    createBlockDict(im_dir)
    createPaletteTree()

def createBlockDict(im_dir):
    for im_f in os.listdir(im_dir):
        im_f = os.path.join(im_dir, im_f)
        with Image.open(im_f).convert('RGB') as im:
            avgRGB = getAverageColor(im)
            BLOCK_DICT[im_f] = avgRGB

def createPaletteTree():
    global PALETTE_TREE
    global BLOCK_DICT
    global PALETTE
    for k, v in BLOCK_DICT.items():
        PALETTE.append(v)
    npPalette = np.array(PALETTE, dtype=np.uint8)
    PALETTE_TREE = KDTree(npPalette)

def colorTreeSearch(target_rgb):
    global PALETTE_TREE
    global BLOCK_DICT
    global PALETTE
    distance, index = PALETTE_TREE.query(target_rgb)
    closest_color = PALETTE[index]
    for bl, bl_color in BLOCK_DICT.items():
        if bl_color == closest_color:
            return bl 


def getAverageColor(im):
    """
    getAverageColor(image_file)
    Returns the average color of the given image 
    """
    imgArr = np.asarray(im, dtype=np.uint32)
    rSum = 0
    gSum = 0
    bSum = 0
    rAvg = 0
    gAvg = 0
    bAvg = 0
    width = im.width
    calcAverage = False
    for lineArr in imgArr:
        for pixelArr in lineArr:
            try:
                rSum += pixelArr[0]
                gSum += pixelArr[1]
                bSum += pixelArr[2]
            except:
                im.show()
        if calcAverage:
            rAvg = ((rAvg + rSum) // (width + 1))
            gAvg = ((gAvg + gSum) // (width + 1))
            bAvg = ((bAvg + bSum) // (width + 1))
        else:
            rAvg = rSum
            gAvg = gSum
            bAvg = bSum
        calcAverage = True
        rSum = 0
        gSum = 0
        bSum = 0
    avgColorArr = [rAvg, gAvg, bAvg]
    return avgColorArr


def calculateSubImagePoints(width, height, n, m, t):
    """
    splitImage(width, height, n, m, t)
    calculates the x0,y0,x1,y1 points of the sub-image
    n: horizontal number of sections
    m: verital number of sections
    t: this sub image to calculate the boundaries of 
    returns x0,y0,x1,y1
    """
    hsize = (width // n)
    vsize = (height // m)
    x0 = (hsize * (t % n))
    y0 = (vsize * (t // n))
    x1 = x0 + hsize
    y1 = y0 + vsize
    return (x0,y0,x1,y1)


def stitchImage(avgColorArr, n, m):
    img = Image.new(mode="RGB", size=[n*16, m*16])
    for t in range(n*m):
        im_f = colorTreeSearch(avgColorArr[t])
        x0 = ((t % n)*16)
        y0 = ((t // n)*16)
        with Image.open(im_f) as bl:
            img.paste(bl, box=[x0,y0])
    img.show()


def buildAvgColorArr(image_file, n, m):
    """
    buildAvgColorArr(image_file, n, m)
    creates the average color <n,m> array
    """
    im = Image.open("test-block.png")
    subImages = n * m
    w = im.width
    h = im.height
    sw = w // n
    sh = h // m
    avgColorArr = []
    for t in range(subImages):
        data = calculateSubImagePoints(w, h, n, m, t)
        subImage = im.transform(size=(sw, sh), method=Image.EXTENT, data=data)
        avgColor = getAverageColor(subImage)
        avgColorArr.append(avgColor)
    stitchImage(avgColorArr, n, m)


def test():
    blockDir = os.path.join(os.getcwd(), "blocks")
    mcPG_init(blockDir)
    im = Image.open("test-sections.png")
    buildAvgColorArr(im, 20,20)

test()

