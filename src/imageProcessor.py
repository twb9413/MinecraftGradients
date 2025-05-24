"""
Author: twb9413
File: imageProcessor.py

Desc:
This file hanldes all functions image related
"""

import os
from PIL import Image
import numpy as np

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
    for lineArr in imgArr:
        for pixelArr in lineArr:
            try:
                rSum += pixelArr[0]
                gSum += pixelArr[1]
                bSum += pixelArr[2]
            except:
                im.show()
        rAvg = ((rAvg + rSum) // (width + 1))
        gAvg = ((gAvg + gSum) // (width + 1))
        bAvg = ((bAvg + bSum) // (width + 1))
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
    img = Image.new(mode="RGB", size=[n, m])
    imgArr = np.asarray(img, dtype=np.uint8).copy()
    index = 0
    for i in range(imgArr.shape[0]):
        for j in range(imgArr.shape[1]):
            imgArr[i, j] = avgColorArr[index]
            index += 1
    Image.fromarray(imgArr).show()


def buildAvgColorArr(image_file, n, m):
    """
    buildAvgColorArr(image_file, n, m)
    creates the average color <n,m> array
    """
    im = Image.open(image_file)
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


def showImages(image_dir):
    for filename in os.listdir(image_dir):
        f = os.path.join(image_dir, filename)
        if os.path.isfile(f):
            print(f)
            showImage(f)


def showImage(image_file):
    im = Image.open(image_file)
    im.show()

def temp():
    im = Image.open("test-picture.png")
    subRegion = im.transform(size=(7,7), method=Image.EXTENT, data=(1,1,8,8))
    im.show()
    subRegion.show()

def test():
    for n in range(15):
            print(calculateSubImagePoints(170, 80, 5, 3, n))
