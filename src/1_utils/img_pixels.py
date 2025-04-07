#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

print("""
      Python image library (PIL) is important to load images. If the 'PIL import' is unsuccessful,
      please install pillow: 'pip install pillow'
      """)
from PIL import Image


def img_load_pixels(imagePath):
    """return with one RGB matrix as the image representation.

    Grayscale images are converted to RGB, Alpha channel is neglected.

    """
    errors = []
    warnings = []
    alphaDetectedWarningAdded = False

    pixelsAllRow = []

    if not os.path.isfile(imagePath):
        errors.append(f"unknown image file path, cannot load: {imagePath}")

    if not errors:
        imageLoaded = Image.open(imagePath)

        imgWidth, imgHeight = imageLoaded.size

        for y in range(0, imgHeight):
            pixelRow = []
            for x in range(0, imgWidth):

                colorVal = imageLoaded.getpixel((x, y))
                if isinstance(colorVal, int):
                    colorVal = (colorVal,)  # convert to be tuple with 1 elem to use tuple everywhere as a type

                # if it's a grayscale img, it is a simple int
                # RGB:  3 elements are in the tuple
                # RGBA: 4 elements are in the tuple

                if len(colorVal) <= 2 : # grayscale OR grayscale + Alpha.  Alpha is not processed, use only grayscale val.
                    rgbDetected = (colorVal[0], colorVal[0], colorVal[0])

                elif len(colorVal) >= 3: #
                    rgbDetected = colorVal[0:3] # RGB value has 3 elems, RGBA has 4

                pixelRow.append(rgbDetected)

                if len(colorVal) not in [1, 3] and not alphaDetectedWarningAdded:
                    alphaDetectedWarningAdded = True
                    warnings.append(f"Please use images with 1 or 3 color channels without Alpha - probably Alpha channel is detected and NEGLECTED in file {imagePath}. "
                                    "if the result is not fine for you, please use files without alpha channels (rgb or grayscale images, not cmyk or other color spaces.")

            pixelsAllRow.append(pixelRow)

    return pixelsAllRow, errors, warnings


