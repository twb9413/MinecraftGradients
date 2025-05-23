"""
Author: twb9413
File: main.py

Desc: 
The main file responsible for determining average color of a photo
"""
from PIL import Image
import imageProcessor
import os

def main():
    image_directory = os.path.join(os.getcwd(), "images")
    imageProcessor.showImages(image_directory)


if __name__ == "__main__":
    main()



