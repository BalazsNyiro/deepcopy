#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, sys

print("""
      Python image library (PIL) is important to load images. If the 'PIL import' is unsuccessful,
      please install pillow: 'pip install pillow'
      """)
from PIL import Image


def pixels_load_from_image(imagePath: str) -> tuple[list[list[tuple[int, int, int]]], list[str], list[str]]:
    """return with one RGB matrix as the image representation.

    Grayscale images are converted to RGB, Alpha channel is neglected.

    """
    errors = []
    warnings = []

    if not os.path.isfile(imagePath):
        errors.append(f"unknown image file path, cannot load: {imagePath}")

    pixelsAllRow = []
    if not errors:

        imageLoaded = Image.open(imagePath)

        ##################################################################################
        colorSamplePixel= imageLoaded.getpixel((0, 0))

        if isinstance(colorSamplePixel, int):
            colorSamplePixel = (colorSamplePixel,) # convert it to tuple

        if len(colorSamplePixel) not in [1, 3]: # so the num of channels are not 3 or 1
            warnings.append(
                f"Please use images with 1 or 3 color channels without Alpha - probably Alpha channel is detected and NEGLECTED in file {imagePath}. "
                "if the result is not fine for you, please use files without alpha channels (rgb or grayscale images, not cmyk or other color spaces.")
        ##################################################################################

        imgWidth, imgHeight = imageLoaded.size

        # these loops run more hundred thousand times with a bigger image,
        # so it worth to repeat/separate the cases and use different loops

        # one color channel:
        if len(colorSamplePixel) == 1:  # so colorVal will be an integer, not a tuple in this loop:
            for y in range(0, imgHeight):
                pixelRow = []
                for x in range(0, imgWidth):
                    colorVal = imageLoaded.getpixel((x, y))
                    pixelRow.append((colorVal, colorVal, colorVal))
                pixelsAllRow.append(tuple(pixelRow))

        elif len(colorSamplePixel) == 2:  # colorVal is a tuple in this loop
            for y in range(0, imgHeight):
                pixelRow = []
                for x in range(0, imgWidth):
                    colorVal = imageLoaded.getpixel((x, y))
                    # < 3   grayscale + Alpha.  Alpha is not processed, use only grayscale val.
                    pixelRow.append( (colorVal[0], colorVal[0], colorVal[0]) )
                pixelsAllRow.append(tuple(pixelRow))

        elif len(colorSamplePixel) >= 3: # 3 or more channels, imageLoaded.getpixel() output is a tuple
            for y in range(0, imgHeight):
                pixelRow = []
                for x in range(0, imgWidth):

                    colorVal = imageLoaded.getpixel((x, y))
                    # imageLoaded.getpixel() output:
                    # if it's a grayscale img, it is a simple int
                    # RGB:  3 elements are in the tuple
                    # RGBA: 4 elements are in the tuple
                    # 3 or more channels, RGB value has 3 elems, RGBA has 4
                    pixelRow.append(colorVal[0:3])

                pixelsAllRow.append(tuple(pixelRow))

    return pixelsAllRow, errors, warnings



class PixelGroup:

    def __init__(self):
        self.pixels = dict()
        self.x_min = -1
        self.x_max = -1
        self.y_min = -1
        self.y_max = -1

    def addPixelActive(self, x, y):
        if not self.pixels:
            self.x_min = x
            self.x_max = x
            self.y_min = y
            self.y_max = y

        self.pixels[(x,y)] = True

        self.x_max = max(self.x_max, x)
        self.x_min = min(self.x_min, x)
        self.y_max = max(self.y_max, y)
        self.y_min = min(self.y_min, y)


# white: 255,255,255 black: 0,0,0
def pixelGroupSelector_default(rNow: int, gNow: int, bNow:int, params: dict ):
    """if the value is less than the limit, so the pixel is darker, then select)"""
    isActive = False
    if rNow < params.get("rMax_toSelect"):
        if gNow < params.get("gMax_toSelect"):
            if bNow < params.get("bMax_toSelect"):
                isActive = True

    return isActive








def isActiveCheckAllSelector(onePixelRgb: tuple[int, int, int], selectorFunctions: list[tuple[callable, dict]]) -> bool:
    isActiveByAllFun = True
    for (funDecideIsActive, paramsToSelector) in selectorFunctions:
        r, g, b = onePixelRgb

        isActiveByThisFun = funDecideIsActive(r, g, b, paramsToSelector)

        if not isActiveByThisFun:  # one way: if any of the func decides that the pixel is not active, it is not active
            isActiveByAllFun = False

    return isActiveByAllFun


def pixelGroups_active_select(pixelsAll: list[list[tuple[int, int, int]]],
                              selectorFunctions=[(pixelGroupSelector_default, {"rMax_toSelect":127, "gMax_toSelect": 127, "bMax_toSelect": 127})]) -> dict[PixelGroup]:

    """

    :param pixelsAll: (r,g,b) values in rows in columns, double embedded list
                      rgb values are organised into 'ONE ROW / ONE LIST, X-axis' and
                      list of rows represents Y axis.

    :param selectorFunctions:  one or more selector fun, and params for the selector.
                               by default the pixels are active, so part of a character.
                               if any of the selector thinks that the pixel is not active, the end result is NotActive.
    :return:
    """

    dectectedActiveCoords = set()


    for y, row in enumerate(pixelsAll):
        for x, onePixelRgb in enumerate(row):

            if isActiveCheckAllSelector(onePixelRgb, selectorFunctions):
                print(f"active pixel detected:", x, y)
                if (x, y) not in dectectedActiveCoords:
                    dectectedActiveCoords.add((x,y))






