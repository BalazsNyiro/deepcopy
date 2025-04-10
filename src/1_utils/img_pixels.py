#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2025 Balazs Nyiro
# All rights reserved.

# This source code (all file in this repo)
# is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Please read the complete LICENSE file
# in the root directory of this source tree.




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



class PixelGroup_Glyph:
    """represents active pixels, next to each other, together forming a glyph.
    A character can be represented by multiple glyphs, so by multiple PixelGroups
    """
    groupCounter = 0


    def __init__(self) -> None:
        self.pixels : dict[tuple[int, int], dict[str, tuple[int, int, int] | PixelGroup_Glyph]] = dict()
        self.x_min = -1
        self.x_max = -1
        self.y_min = -1
        self.y_max = -1
        self.matrix_representation: list[list[PixelGroup_Glyph]] = []

        self.groupId = PixelGroup_Glyph.groupCounter
        PixelGroup_Glyph.groupCounter += 1


    def add_pixel_active(self, x: int, y: int, rgbTuple: tuple[int, int, int]):
        if not self.pixels:
            self.x_min = x
            self.x_max = x
            self.y_min = y
            self.y_max = y

        # the original coords from the orig image are saved here, as (x, y)
        self.pixels[(x,y)] = {"rgb": rgbTuple, "pixelGroupObj": self}  # every point knows who is the parent group

        self.x_max = max(self.x_max, x)
        self.x_min = min(self.x_min, x)
        self.y_max = max(self.y_max, y)
        self.y_min = min(self.y_min, y)

    def has_pixels(self) -> bool:
        return len(self.pixels) > 0

    def display_in_terminal(self):
        print(f"=========== {self.groupId} ==========")
        self.matrix_representation = matrix_representation_shared_for_more_pixelgroups([self])
        pixel_group_matrix_representation_print(self.matrix_representation)


def pixel_group_matrix_representation_print(matrix_representation:list[list[PixelGroup_Glyph]]):
    """display matrix representation of a pixel group or more pixel groups"""
    for row in matrix_representation:
        rowDisplayed = []
        for pixelRepresentation in row:
            if pixelRepresentation.has_pixels():
                rowDisplayed.append("*")
            else:
                rowDisplayed.append(" ")
        print("".join(rowDisplayed))


#################################################################
pixelGroupForBackgroundNonActivePixels = PixelGroup_Glyph()
# TODO: maybe a new background collector has to be created for every page? not only one general?


def matrix_representation_empty_area_create_list_of_lists(
        pixelGroupBackgroundCollector: PixelGroup_Glyph, x_min: int=0, x_max: int=100, y_min: int=0, y_max: int=100 ) -> list[list[PixelGroup_Glyph]]:
    """create an empty area

    Be careful: list of rows, a row: list of strings, string: one char, represents one pixel.
    different from
    """

    matrix_representation: list[list[PixelGroup_Glyph]] = list()
    for _y in range(y_min, y_max + 1):
        row = []
        for _x in range(x_min, x_max + 1):
            row.append(pixelGroupBackgroundCollector)
        matrix_representation.append(row)
    return matrix_representation
#################################################################



def matrix_representation_shared_for_more_pixelgroups(pixelGroupElems: list[PixelGroup_Glyph]) -> list[list[PixelGroup_Glyph]]:
    """can create a merged matrix representation for MORE PixelGroup elems"""

    xMinGlobal = -1
    xMaxGlobal = -1
    yMinGlobal = -1
    yMaxGlobal = -1

    for groupCounter, pixelGroup in enumerate(pixelGroupElems):
        if groupCounter == 0:
            xMinGlobal = pixelGroup.x_min
            xMaxGlobal = pixelGroup.x_max
            yMinGlobal = pixelGroup.y_min
            yMaxGlobal = pixelGroup.y_max

        xMinGlobal = min(pixelGroup.x_min, xMinGlobal)
        xMaxGlobal = max(pixelGroup.x_max, xMaxGlobal)
        yMinGlobal = min(pixelGroup.y_min, yMinGlobal)
        yMaxGlobal = max(pixelGroup.y_max, yMaxGlobal)

    # empty space where new pixels are placed
    areaPixels = matrix_representation_empty_area_create_list_of_lists(
        pixelGroupForBackgroundNonActivePixels,
        x_min=xMinGlobal, x_max=xMaxGlobal,
        y_min=yMinGlobal, y_max=yMaxGlobal
    )

    for pixelGroup in pixelGroupElems:

        for (xAbsPosInOrigImage, yAbsPosInOrigImage) in pixelGroup.pixels:

            xInAreaPixels = xAbsPosInOrigImage - xMinGlobal
            yInAreaPixels = yAbsPosInOrigImage - yMinGlobal

            # add the pixel obj
            # print("add pixel obj into representation MORE pixelgroups:", type(pixelGroup))
            areaPixels[yInAreaPixels][xInAreaPixels] = pixelGroup

    return areaPixels


# white: 255,255,255 black: 0,0,0
def pixelGroupSelector_default(rNow: int, gNow: int, bNow:int, params: dict ) -> bool:
    """if the value is less than the limit, so the pixel is darker, then select"""
    isActive = False

    # if any channel param is acceptable, set Active
    if rNow < params.get("rMax_toSelect", 127):
        isActive = True

    if gNow < params.get("gMax_toSelect", 127):
        isActive = True

    if bNow < params.get("bMax_toSelect", 127):
        isActive = True

    return isActive




def isActive_checkAllSelectors(onePixelRgb: tuple[int, int, int], selectorFunctions: list[tuple[typing.Callable, dict]]) -> bool:
    isActiveByAllFun = True
    for (funDecideIsActive, paramsToSelector) in selectorFunctions:
        r, g, b = onePixelRgb

        isActiveByThisFun = funDecideIsActive(r, g, b, paramsToSelector)

        if not isActiveByThisFun:  # one way: if any of the func decides that the pixel is not active, it is not active
            isActiveByAllFun = False

    return isActiveByAllFun


def coords_neighbours(x: int, y: int,
                      xMinValidPossibleCoordValue: int, yMinValidPossibleCoordValue: int,
                      xMaxValidPossibleCoordValue: int, yMaxValidPossibleCoordValue: int,
                      allowedDirections: set[int]={1,2,3,4,5,6,7,8}
                      ) -> list[tuple[int, int], ]:
    """return with possible neighbour coordinates"""

    neighbours = list()

    directions = { 1: (x,   y-1),
                   2: (x+1, y-1),
                   3: (x+1, y  ),
                   4: (x+1, y+1),
                   5: (x,   y+1),
                   6: (x-1, y+1),
                   7: (x-1, y  ),
                   8: (x-1, y-1)
                 }

    for direction, (xNeighbour, yNeighbour) in directions.items():

        if direction not in allowedDirections:
            continue

        if xNeighbour < xMinValidPossibleCoordValue or yNeighbour < yMinValidPossibleCoordValue:
            continue # cannot go over the limits...

        if xNeighbour > xMaxValidPossibleCoordValue or yNeighbour > yMaxValidPossibleCoordValue:
            continue # cannot go over the limits...

        neighbours.append( (xNeighbour, yNeighbour) )

    return neighbours


def pixelGroups_active_select(pixelsAll: list[list[tuple[int, int, int]]],
                              selectorFunctions=[(pixelGroupSelector_default, {"rMax_toSelect":127, "gMax_toSelect": 127, "bMax_toSelect": 127})]) -> dict[tuple[int, int], PixelGroup_Glyph]:

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

    pixelGroups: dict[tuple[int, int], PixelGroup_Glyph] = dict()

    pixelGroupNow = PixelGroup_Glyph()

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

                if isActive_checkAllSelectors(onePixelRgb, selectorFunctions):
                    # print(f"active pixel detected: {pixelGroupNow.groupId}", coordNowX, coordNowY)
                    pixelGroupNow.add_pixel_active(coordNowX, coordNowY, onePixelRgb)

                    # maybe the neighbours are detected from multiple places, insert them only once
                    for (xPossibleNeighbour, yPossibleNeighbour) in coords_neighbours(coordNowX, coordNowY, 0, 0, len(row) - 1, len(pixelsAll) - 1):
                        if (xPossibleNeighbour, yPossibleNeighbour) not in checkTheseCoords:
                            checkTheseCoords.append( (xPossibleNeighbour, yPossibleNeighbour))

            # only Active pixels are inserted into the Groups, so a new group has to be created ONLY if the previous one has any active Pixels
            if pixelGroupNow.has_pixels():
                # the top-left coord of the group is the registration point
                pixelGroups[(pixelGroupNow.x_min, pixelGroupNow.y_min)] = pixelGroupNow

                pixelGroupNow = PixelGroup_Glyph()  # create a new one

    return pixelGroups




