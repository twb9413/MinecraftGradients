"""
Author: twb9413
File: mcPaletteGen.py

Determine closest minecraft block to a given pixel color
"""
from scipy.spatial import KDTree
import numpy as np
import os
import imageProcessor as im_pr
from PIL import Image


BLOCK_DICT = {}
PALETTE = []
PALETTE_TREE = None

def createBlockDict(im_dir):
    for im_f in os.listdir(im_dir):
        im_f = os.path.join(im_dir, im_f)
        im = Image.open(im_f)
        avgRGB = im_pr.getAverageColor(im)
        BLOCK_DICT[im_f] = avgRGB

def createPaletteTree():
    global PALETTE_TREE
    global BLOCK_DICT
    global PALETTE
    for k, v in BLOCK_DICT.items():
        PALETTE.append(v)
    npPalette = np.array(PALETTE, dtype=np.uint8)
    PALETTE_TREE = KDTree(npPalette)
 
def colorTreeSearch():
    global PALETTE_TREE
    global BLOCK_DICT
    global PALETTE
    new_color = np.array([255, 255, 255], dtype=np.uint8)
    distance, index = PALETTE_TREE.query(new_color)
    closest_color = PALETTE[index]
    for k, v in BLOCK_DICT.items():
        if v == closest_color:
            print(k)
            print(v)
            return

testDir = os.path.join(os.getcwd(), "test-blocks")
createBlockDict(testDir)
createPaletteTree()
colorTreeSearch()
