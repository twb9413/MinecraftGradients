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

def colorTreeSearch(target_rgb):
    global PALETTE_TREE
    global BLOCK_DICT
    global PALETTE
    distance, index = PALETTE_TREE.query()
    closest_color = PALETTE[index]
    for bl, bl_color in BLOCK_DICT.items():
        if bl_color == closest_color:
            return bl 


