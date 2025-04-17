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


################################################################
pixelsNameBackgroundInactive = "pixelsBackgroundInactive"
pixelsNameForegroundActive = "pixelsForegroundActive_partOfGlyph"

inactivePixelRgbDefaultVal = (255, 255, 255)
################################################################

typeAlias_pixelRgb = tuple[int, int, int]
typeAlias_row_pixelRgb = tuple[typeAlias_pixelRgb, ...]
typeAlias_matrix_pixelRgb = list[typeAlias_row_pixelRgb]
################################################################



def pixels_load_from_string(txt: str, activePixelRgb: typeAlias_pixelRgb=(0, 0, 0),
                            inactivePixelRgb: typeAlias_pixelRgb=inactivePixelRgbDefaultVal,
                            activePixelRepresenter: str="*", inactivePixelRepresenter: str=".",
                            callerPlaceName=""
                            ) -> tuple[typeAlias_matrix_pixelRgb, list[str], list[str]]:
    """
    Typically used from tests, or development process

    :param txt: newline separated text, active pixel: *   inactivePixels: anythingElse, _ for example
    :return:
    """
    errors: list[str] = []
    warnings: list[str] = []
    pixelsAllRow: typeAlias_matrix_pixelRgb = []


    rowLengthsUsed = set()  # theoretically all rows have similar num of pixels,
                            # practically if we have more than one length, maybe that is a mistake

    for row in txt.split("\n"):
        pixelRow: list[typeAlias_pixelRgb] = []

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


def pixels_load_from_image(imagePath: str) -> tuple[typeAlias_matrix_pixelRgb, list[str], list[str]]:
    """return with one RGB matrix as the image representation.

    Grayscale images are converted to RGB, Alpha channel is neglected.

    """
    errors = []
    warnings = []

    if not os.path.isfile(imagePath):
        errors.append(f"unknown image file path, cannot load: {imagePath}")

    pixelsAllRow: typeAlias_matrix_pixelRgb = []
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
                pixelRow: list[typeAlias_pixelRgb ] = []
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

    def __init__(self, representedPixelGroupName: str=pixelsNameForegroundActive) -> None:
        self.pixels : dict[tuple[int, int], Pixel_elem_in_PixelGroup_Glyph] = dict()
        self.x_min = -1
        self.x_max = -1
        self.y_min = -1
        self.y_max = -1

        self.groupId = PixelGroup_Glyph.groupCounter
        PixelGroup_Glyph.groupCounter += 1

        ###########################################################
        self.matrix_representation: list[list[tuple[int, int, PixelGroup_Glyph]]] = []
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
        # the pixelGroup_glyph objects are pixel collectors.

        # one pixel group can have more than one flags/names
        self.representedPixelGroupNames: set[str] = set()
        self.representedPixelGroupNames.add(representedPixelGroupName)
        # if this is True, the x_min,y_min,x_max,y_max values are invalid, because the biggest part of the image
        # is inactive. in this case this is only a filler pixel.
        ###########################################################


    def pixels_remove(self, xyCoordAll: list[tuple[int, int]]):
        for xyCoord in xyCoordAll:
            if xyCoord in self.pixels:
                print(f"remove pixel:", xyCoord )
                del self.pixels[xyCoord]
            else:
                print(f"warning: coord was not in pixels: {xyCoord}")


    def pixels_add_with_nonimportant_rgb(
            self, xStart: int, yStart: int,
            xEnd: int, yEnd: int, rgb=inactivePixelRgbDefaultVal,
    ):
        """the object is a pixel collector only, sometime the rgb val is not important"""
        for x in range(xStart, xEnd+1):
            for y in range(yStart, yEnd+1):
                self.pixel_add(x, y, rgbTuple=rgb)

    def pixel_add(self, x: int, y: int, rgbTuple: typeAlias_pixelRgb):
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
        self.matrix_representation = pixelGroup_matrix_representation_of_more_pixelgroups([self], addExtraEmptyBorderAroundArea)
        return self.matrix_representation


    def matrix_representation_display_in_terminal(self, refreshTheMatrix: bool=True):
        print(f"=========== matrix group id: {self.groupId} names: {self.representedPixelGroupNames}==========")
        if refreshTheMatrix:
            self.matrix_representation_refresh()
            # print(self.matrix_representation)
        pixelGroup_matrix_representation_str(self.matrix_representation, printStr=True)


    def matrix_representation_xAbsLeft_yAbsTop_xAbsRight_yAbsBottom(self) -> tuple[tuple[int, int, int, int], list[str]]:
        """the current matrix representations coords (can be different from glyphs coords, if extra border is added!"""
        errors = []
        if self.pixels:
            xAbsLeft   = self.matrix_representation[0][0][0]  # the first elem is the abs x pos
            yAbsTop    = self.matrix_representation[0][0][1]  # the second elem is the abs y pos
            xAbsRight  = self.matrix_representation[0][-1][0]  # last pixels's first X coord
            yAbsBottom = self.matrix_representation[-1][-1][ 1]  # last line, last pixels Y coord, second elem
            retVal = (xAbsLeft, yAbsTop, xAbsRight, yAbsBottom)
        else:
            retVal = (-1, -1, -1, -1)
            errors = ["noPixelInGlyph"]
        return retVal, errors


class Pixel_elem_in_PixelGroup_Glyph(typing.TypedDict):
    rgb: tuple[int, int, int]
    pixelGroupObj: PixelGroup_Glyph




def pixelGroup_matrix_representation_str(matrix_representation:list[list[tuple[int, int, PixelGroup_Glyph]]], printStr=False, wantedFlagsToDisplay: set[str]={pixelsNameForegroundActive}) -> str:
    """display matrix representation of a pixel group or more pixel groups, a print command.
    The representation is given back as a string.

        # matrixRepresentation is y,x based!!!!
    """
    fullOut = []
    for row in matrix_representation:
        rowDisplayed = []

        yAbs = -9

        for (_xAbs, yAbs, pixelRepresentation) in row:
            display = False
            for wantedFlag in wantedFlagsToDisplay:
                if wantedFlag in pixelRepresentation.representedPixelGroupNames:
                    display = True
                    break

            if display:
                rowDisplayed.append("*")
            else:
                rowDisplayed.append(".")

        fullOut.append(f"{yAbs:>4}: " + "".join(rowDisplayed))

    fullOutStr = "\n".join(fullOut)
    if printStr:
        print(fullOutStr)
    return fullOutStr


#################################################################
pixelGroupForBackgroundNonActivePixels = PixelGroup_Glyph(representedPixelGroupName=pixelsNameBackgroundInactive)
# TODO: maybe a new background collector has to be created for every page? not only one general?



def pixelGroup_matrix_representation_empty_area_create(
        pixelGroupBackgroundRepresenter: PixelGroup_Glyph, x_min: int=0, x_max: int=100, y_min: int=0, y_max: int=100,
        defaultEmptyColors: tuple[int, int, int] = inactivePixelRgbDefaultVal
) -> list[list[tuple[int, int, PixelGroup_Glyph]]]:
    """create an empty area

    Be careful: list of rows, a row: list of strings, string: one char, represents one pixel.
    different from
    """

    matrix_representation: list[list[tuple[int, int, PixelGroup_Glyph]]] = list()
    for yAbs in range(y_min, y_max + 1):
        row = []
        for xAbs in range(x_min, x_max + 1):
            row.append((xAbs, yAbs, pixelGroupBackgroundRepresenter))  # in the matrix the background pixels are represented with this Glyph
            pixelGroupBackgroundRepresenter.pixel_add(xAbs, yAbs, defaultEmptyColors)
        matrix_representation.append(row)
    return matrix_representation
#################################################################


def pixelGroup_matrix_representation_of_more_pixelgroups(pixelGroupElems: list[PixelGroup_Glyph],
                                                         addExtraEmptyBorderAroundArea: tuple[int, int, int, int] = (0, 0, 0, 0)
                                                         ) -> list[list[tuple[int, int, PixelGroup_Glyph]]]:
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
    areaPixels = pixelGroup_matrix_representation_empty_area_create(
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
            areaPixels[yInAreaPixels][xInAreaPixels] = (xAbsPosInOrigImage, yAbsPosInOrigImage, pixelGroup)

    return areaPixels


def pixelGroup_matrix_representation_collect_relative_matrix_coords_with_represented_names(
pixelGroup_glyph_matrix_representation: list[list[tuple[int, int, PixelGroup_Glyph]]],
        wantedRepresentedNames: set[str]
) -> list[tuple[int, int]]:
    """the matrix coords are different from th represented pixel coords, because the matrix is smaller.
    collect coords where in the background the PixelGlyph has a special flag/represented name
    """

    collector = []
    for yRow, row in enumerate(pixelGroup_glyph_matrix_representation):
        for xRow, (xAbs, yAbs, pixelGroup_glyph_obj) in enumerate(row):
            if wantedRepresentedNames & pixelGroup_glyph_obj.representedPixelGroupNames:
                collector.append((xRow, yRow))

    return collector





def pixelGroup_matrix_representation_has_emptyborder_around_glyph(
        pixelGroup_glyph_matrix_representation: list[list[tuple[int, int, PixelGroup_Glyph]]],
        raiseExceptionIfNoBorder: bool=True) -> bool:
    """True/False decision: is the outer border of a glyph representation is totally empty?
    This can be important if a pixel detection has to start from a guaranteed non-active place
    and the connected pixels can go around the glyph totally (so the border has to be totally inactive)


    From the caller side the empty border can be added, so if the program is absolute correct,
    this validation is not necessary.

    if the answer is False, that can cause problems in character recognition.

    you need to see an empty border around the character, so first/last lines and columns are totally empty:
    0: ............
    1: .....**.....
    2: ....*..*....
    3: ...******...
    4: ..*......*..
    5: .*........*.
    6: ............

    """

    # with a normal image this situation cannot happen.
    # (missing pixel data from lines, or missing lines)
    if len(pixelGroup_glyph_matrix_representation) == 0 or \
        len(pixelGroup_glyph_matrix_representation[0]) == 0:

        if raiseExceptionIfNoBorder:
            raise ValueError("EmtpyBorder: incorrect input, no real data in matrix representation")

        return False



    isEmptyBorderDetected = True

    coordsToCheck = set()

    xLen = len(pixelGroup_glyph_matrix_representation[0])
    yLen = len(pixelGroup_glyph_matrix_representation)

    # add all X coords in first/last lines
    for x in range(0, xLen):
        coordsToCheck.add((x, 0     )) # first line
        coordsToCheck.add((x, yLen-1)) # last  line

    # add left/right columns
    for y in range(0, yLen):
        coordsToCheck.add((0,      y)) # first column
        coordsToCheck.add((xLen-1, y)) # last  column

    for (x, y) in coordsToCheck:
        # print(f"border coords check: {(x, y)}")
        (_xAbs, _yAbs, pixelNow) = pixelGroup_glyph_matrix_representation[y][x]
        if pixelsNameBackgroundInactive not in pixelNow.representedPixelGroupNames:

            isEmptyBorderDetected = False

            matrixStr = pixelGroup_matrix_representation_str(pixelGroup_glyph_matrix_representation)
            errMsg = f"missing empty border around the pixelGroup {(x, y)} \n {matrixStr}"
            if raiseExceptionIfNoBorder:
                raise ValueError(errMsg)
            else:
                print(errMsg)
            break

    return isEmptyBorderDetected
