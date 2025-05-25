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
os.environ['DISPLAY'] = ''

def createBlockDict(im_dir):
    for im_f in os.listdir(im_dir):
        im_f = os.path.join(im_dir, im_f)
        with Image.open(im_f).convert('RGB') as im:
            avgRGB = im_pr.getAverageColor(im)
            BLOCK_DICT[im_f] = avgRGB
        print(BLOCK_DICT)

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
    new_color = np.array([0, 0, 0], dtype=np.uint8)
    distance, index = PALETTE_TREE.query(new_color)
    closest_color = PALETTE[index]
    for k, v in BLOCK_DICT.items():
        if v == closest_color:
            print(k)
            print(v)
            return

testDir = os.path.join(os.getcwd(), "blocks")
createBlockDict(testDir)
createPaletteTree()
colorTreeSearch()
