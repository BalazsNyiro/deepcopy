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

sys.path.append("../0_base")


def pixels_load_from_string(txt: str, activePixelRgb: tuple[int,int,int]=(0, 0, 0),
                            inactivePixelRgb: tuple[int, int, int]=(255, 255, 255),
                            activePixelRepresenter: str="*", inactivePixelRepresenter: str=".",
                            callerPlaceName=""
                            ) -> tuple[list[tuple[tuple[int, int, int], ...]], list[str], list[str]]:
    """
    Typically used from tests, or development process

    :param txt: newline separated text, active pixel: *   inactivePixels: anythingElse, _ for example
    :return:
    """
    errors: list[str] = []
    warnings: list[str] = []
    pixelsAllRow: list[tuple[tuple[int, int, int], ...]] = []


    rowLengthsUsed = set()  # theoretically all rows have similar num of pixels,
                            # practically if we have more than one length, maybe that is a mistake

    for row in txt.split("\n"):
        pixelRow: list[tuple[int, int, int],] = []

        for oneChar in row:
            if oneChar == activePixelRepresenter:
                pixelRow.append(activePixelRgb)
            elif oneChar == inactivePixelRepresenter:
                pixelRow.append(inactivePixelRgb)

        # in normal images it is impossible that a row is empty,
        # but in test situations it is possible that there is no active or inactive pixels in a test row,
        # so add the row only if it is not empy
        if pixelRow:
            pixelsAllRow.append(tuple(pixelRow))

            rowLengthsUsed.add(len(pixelRow))
            if len(rowLengthsUsed) > 1:
                msg = f"ERROR: <{callerPlaceName}> the num of pixels in the rows are different - that is impossible in case of a normal image."
                errors.append(msg)
                print(msg)

    return pixelsAllRow, errors, warnings


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

    (0, 0) coord represents the left-top corner.
    """
    groupCounter = 0

    def __init__(self, backgroundInactiveGroupRepresenter=False) -> None:
        self.pixels : dict[tuple[int, int], dict[str, tuple[int, int, int] | PixelGroup_Glyph]] = dict()
        self.x_min = -1
        self.x_max = -1
        self.y_min = -1
        self.y_max = -1

        self.groupId = PixelGroup_Glyph.groupCounter
        PixelGroup_Glyph.groupCounter += 1

        ###########################################################
        self.matrix_representation: list[list[PixelGroup_Glyph]] = []
        # matrixRepresentation is y,x based!!!

        # Detailed example:
        # one list represents one row, one row represents (x=0...x=N) pixels,
        #
        # line 0, y=0: '.**.' left: readable human version,   ['.', '*', '*', '.']
        # line 1, y=1: '*..*' in reality the line of pixels:  ['*', '.', '.', '*']
        # line 2, y=2: '****'                                 ['*', '*', '*', '*']
        # line 3, y=3: '*  *'                                 ['*', ' ', ' ', '*']

        """
        Check this input and the representation:
        the first column is TOTALLY EMPTY, it is not part of a representation. 
        v this first column is NOT in the representation of A !!!!
        .....**.......   ->  0: ....**....
        ....*..*......       1: ...*..*...
        ...******...**       2: ..******..
        ..*......*....       3: .*......*.
        .*........*...       4: *........*
        """


        # an image can have a lot of active pixels, but the significant part of the image is inactive (thousands)
        # in the matrix_representation every pixel has an object, but because the background elems are not important,
        # only one object represents them.
        self.isBackgroundInactivePixelGroup = backgroundInactiveGroupRepresenter
        # if this is True, the x_min,y_min,x_max,y_max values are invalid, because the biggest part of the image
        # is inactive. in this case this is only a filler pixel.
        ###########################################################


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


    #################################################################################
    def matrix_representation_refresh(self,
        addExtraEmptyBorderAroundArea: tuple[int, int, int, int] = (0, 0, 0, 0) ):
        self.matrix_representation = matrix_representation_of_more_pixelgroups([self], addExtraEmptyBorderAroundArea)
        return self.matrix_representation


    def matrix_representation_display_in_terminal(self):
        print(f"=========== {self.groupId} ==========")
        self.matrix_representation_refresh()
        pixel_group_matrix_representation_print(self.matrix_representation)


def pixel_group_matrix_representation_print(matrix_representation:list[list[PixelGroup_Glyph]]) -> str:
    """display matrix representation of a pixel group or more pixel groups, a print command.
    The representation is given back as a string.

        # matrixRepresentation is y,x based!!!!
    """
    fullOut = []
    for rowNum, row in enumerate(matrix_representation):
        rowDisplayed = []
        for pixelRepresentation in row:
            if pixelRepresentation.has_pixels():
                rowDisplayed.append("*")
            else:
                rowDisplayed.append(".")
        fullOut.append(f"{rowNum:>4}: " + "".join(rowDisplayed))

    fullOutStr = "\n".join(fullOut)
    print(fullOutStr)
    return fullOutStr


#################################################################
pixelGroupForBackgroundNonActivePixels = PixelGroup_Glyph(backgroundInactiveGroupRepresenter=True)
# TODO: maybe a new background collector has to be created for every page? not only one general?



def matrix_representation_empty_area_create(
        pixelGroupBackgroundRepresenter: PixelGroup_Glyph, x_min: int=0, x_max: int=100, y_min: int=0, y_max: int=100 ) -> list[list[PixelGroup_Glyph]]:
    """create an empty area

    Be careful: list of rows, a row: list of strings, string: one char, represents one pixel.
    different from
    """

    matrix_representation: list[list[PixelGroup_Glyph]] = list()
    for _y in range(y_min, y_max + 1):
        row = []
        for _x in range(x_min, x_max + 1):
            row.append(pixelGroupBackgroundRepresenter)  # in the matrix the background pixels are represented with this Glyph
        matrix_representation.append(row)
    return matrix_representation
#################################################################


def matrix_representation_of_more_pixelgroups(pixelGroupElems: list[PixelGroup_Glyph],
                                              addExtraEmptyBorderAroundArea: tuple[int, int, int, int] = (0, 0, 0, 0)
                                              ) -> list[list[PixelGroup_Glyph]]:
    """can create a merged matrix representation for MORE PixelGroup elems

    :param addExtraEmptyBorderAroundArea: the thickness of the border
    """

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


    ####################################################################################################
    # add extra emtpy border around the area
    extraBorderTop, extraBorderRight, extraBorderBottom, extraBorderLeft = addExtraEmptyBorderAroundArea
    xMinGlobal -= extraBorderLeft
    xMaxGlobal += extraBorderRight
    yMinGlobal -= extraBorderTop
    yMaxGlobal += extraBorderBottom
    ####################################################################################################



    # empty space where new pixels are placed
    areaPixels = matrix_representation_empty_area_create(
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






