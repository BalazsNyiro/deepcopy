#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time, sys, typing

print("""
      Python image library (PIL) is important to load images. If the 'PIL import' is unsuccessful,
      please install pillow: 'pip install pillow'
      """)
from PIL import Image


def pixels_load_from_image(imagePath: str) -> tuple[list[tuple[tuple[int, int, int], ...]], list[str], list[str]]:
    """return with one RGB matrix as the image representation.

    Grayscale images are converted to RGB, Alpha channel is neglected.

    """
    errors = []
    warnings = []

    if not os.path.isfile(imagePath):
        errors.append(f"unknown image file path, cannot load: {imagePath}")

    pixelsAllRow: list[tuple[tuple[int, int, int], ...]] = []
    if not errors:

        imageLoaded = Image.open(imagePath)

        ##################################################################################
        colorSamplePixelMaybeIntMaybeTuple = imageLoaded.getpixel((0, 0))

        if isinstance(colorSamplePixelMaybeIntMaybeTuple, int):
            colorSamplePixelTuple = tuple([colorSamplePixelMaybeIntMaybeTuple]) # convert one element integer to a tuple

        if isinstance(colorSamplePixelMaybeIntMaybeTuple, tuple):
            colorSamplePixelTuple = colorSamplePixelMaybeIntMaybeTuple
            # myPy is a nightmare here, the tuple has to be built up one-by-one


        if len(colorSamplePixelTuple) not in [1, 3]: # so the num of channels are not 3 or 1
            warnings.append(
                f"Please use images with 1 or 3 color channels without Alpha - probably Alpha channel is detected and NEGLECTED in file {imagePath}. "
                "if the result is not fine for you, please use files without alpha channels (rgb or grayscale images, not cmyk or other color spaces.")
        ##################################################################################

        imgWidth, imgHeight = imageLoaded.size

        # these loops run more hundred thousand times with a bigger image,
        # so it worth to repeat/separate the cases and use different loops

        # one color channel:
        if len(colorSamplePixelTuple) == 1:  # so colorVal will be an integer, not a tuple in this loop:
            for y in range(0, imgHeight):
                pixelRow: list[tuple[int, int, int], ] = []
                for x in range(0, imgWidth):
                    colorVal = imageLoaded.getpixel((x, y))
                    # print(colorVal)
                    if isinstance(colorVal, int):   # int, but myPy...
                        # pixelRow.append((colorVal, colorVal, colorVal))
                        pixelRow.append((colorVal, colorVal, colorVal))
                pixelsAllRow.append(tuple(pixelRow))

        elif len(colorSamplePixelTuple) == 2:  # colorVal is a tuple in this loop
            for y in range(0, imgHeight):
                pixelRow = []
                for x in range(0, imgWidth):
                    colorVal = imageLoaded.getpixel((x, y))
                    if isinstance(colorVal, tuple):  # tuple, but myPy gives an error without type checking
                        # < 3   grayscale + Alpha.  Alpha is not processed, use only grayscale val.
                        if isinstance(colorVal[0], int):
                            pixelRow.append( (colorVal[0], colorVal[0], colorVal[0]) )

                pixelsAllRow.append(tuple(pixelRow))

        elif len(colorSamplePixelTuple) >= 3: # 3 or more channels, imageLoaded.getpixel() output is a tuple
            for y in range(0, imgHeight):
                pixelRow = []
                for x in range(0, imgWidth):

                    colorVal = imageLoaded.getpixel((x, y))
                    # imageLoaded.getpixel() output:
                    # if it's a grayscale img, it is a simple int
                    # RGB:  3 elements are in the tuple
                    # RGBA: 4 elements are in the tuple
                    # 3 or more channels, RGB value has 3 elems, RGBA has 4

                    if isinstance(colorVal, tuple):  # tuple, but myPy gives an error without type checking
                        pixelRow.append((colorVal[0], colorVal[1], colorVal[2]))

                pixelsAllRow.append(tuple(pixelRow))

    return pixelsAllRow, errors, warnings



class PixelGroup:

    groupCounter = 0

    def __init__(self):
        self.pixels = dict()
        self.x_min = -1
        self.x_max = -1
        self.y_min = -1
        self.y_max = -1

        self.groupId = PixelGroup.groupCounter
        PixelGroup.groupCounter += 1


    def addPixelActive(self, x: int, y: int, rgbTuple: tuple[int, int, int]):
        if not self.pixels:
            self.x_min = x
            self.x_max = x
            self.y_min = y
            self.y_max = y

        self.pixels[(x,y)] = rgbTuple

        self.x_max = max(self.x_max, x)
        self.x_min = min(self.x_min, x)
        self.y_max = max(self.y_max, y)
        self.y_min = min(self.y_min, y)

    def hasPixels(self) -> bool:
        return len(self.pixels) > 0


# white: 255,255,255 black: 0,0,0
def pixelGroupSelector_default(rNow: int, gNow: int, bNow:int, params: dict ) -> bool:
    """if the value is less than the limit, so the pixel is darker, then select)"""
    isActive = False
    if rNow < params.get("rMax_toSelect", 127):
        if gNow < params.get("gMax_toSelect", 127):
            if bNow < params.get("bMax_toSelect", 127):
                isActive = True

    return isActive








def isActiveCheckAllSelector(onePixelRgb: tuple[int, int, int], selectorFunctions: list[tuple[typing.Callable, dict]]) -> bool:
    isActiveByAllFun = True
    for (funDecideIsActive, paramsToSelector) in selectorFunctions:
        r, g, b = onePixelRgb

        isActiveByThisFun = funDecideIsActive(r, g, b, paramsToSelector)

        if not isActiveByThisFun:  # one way: if any of the func decides that the pixel is not active, it is not active
            isActiveByAllFun = False

    return isActiveByAllFun


def coordsNeighbour(x: int, y: int,
                    xMinValidPossibleCoordValue: int, yMinValidPossibleCoordValue: int,
                    xMaxValidPossibleCoordValue: int, yMaxValidPossibleCoordValue: int) -> list[tuple[int, int], ...]:
    """return with possible neighbour coordinates"""
    neighbours = list()
    for xNeighbour in range(x-1, x+2):
        for yNeighbour in range(y-1, y+2):

            if xNeighbour == x and yNeighbour == y:
                continue  # the orig point is NOT a neighbour

            if xNeighbour < xMinValidPossibleCoordValue or yNeighbour < yMinValidPossibleCoordValue:
                continue

            if xNeighbour > xMaxValidPossibleCoordValue or yNeighbour > yMaxValidPossibleCoordValue:
                continue

            neighbours.append( (xNeighbour, yNeighbour) )

    return neighbours

def pixelGroups_active_select(pixelsAll: list[list[tuple[int, int, int]]],
                              selectorFunctions=[(pixelGroupSelector_default, {"rMax_toSelect":127, "gMax_toSelect": 127, "bMax_toSelect": 127})]) -> dict[tuple[int, int], PixelGroup]:

    """

    :param pixelsAll: (r,g,b) values in rows in columns, double embedded list
                      rgb values are organised into 'ONE ROW / ONE LIST, X-axis' and
                      list of rows represents Y axis.

    :param selectorFunctions:  one or more selector fun, and params for the selector.
                               by default the pixels are active, so part of a character.
                               if any of the selector thinks that the pixel is not active, the end result is NotActive.
    :return:
    """

    coordsAnalysedOnce = set()

    pixelGroups: dict[tuple[int, int], PixelGroup] = dict()

    pixelGroupNow = PixelGroup()

    for y, row in enumerate(pixelsAll):
        for x in range(0, len(row)):

            checkTheseCoords = [(x,y)]


            while checkTheseCoords:

                (coordNowX, coordNowY) = checkTheseCoords.pop(0)

                if (coordNowX, coordNowY) in coordsAnalysedOnce:
                    continue
                coordsAnalysedOnce.add( (coordNowX, coordNowY) )

                # pixelsAll: have rows, one row represent one row of pixels in a line, so the first selector is Y coord.
                onePixelRgb = pixelsAll[coordNowY][coordNowX]  # this is correct, here Y is the first selector

                if isActiveCheckAllSelector(onePixelRgb, selectorFunctions):
                    print(f"active pixel detected: {pixelGroupNow.groupId}", coordNowX, coordNowY)
                    pixelGroupNow.addPixelActive(coordNowX, coordNowY, onePixelRgb)

                    # maybe the neighbours are detected from multiple places, insert them only once
                    for (xPossibleNeighbour, yPossibleNeighbour) in coordsNeighbour(coordNowX, coordNowY, 0, 0, len(row)-1, len(pixelsAll)-1):
                        if (xPossibleNeighbour, yPossibleNeighbour) not in checkTheseCoords:
                            checkTheseCoords.append( (xPossibleNeighbour, yPossibleNeighbour))

            # only Active pixels are inserted into the Groups, so a new group has to be created ONLY if the previous one has any active Pixels
            if pixelGroupNow.hasPixels():
                # the top-left coord of the group is the registration point
                pixelGroups[(pixelGroupNow.x_min, pixelGroupNow.y_min)] = pixelGroupNow

                pixelGroupNow = PixelGroup()  # create a new one

    return pixelGroups




