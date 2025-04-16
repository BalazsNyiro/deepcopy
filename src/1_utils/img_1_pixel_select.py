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


import typing
import img_0_pixels

direction_standards_in_the_whole_project = \
"""
    relative directionsStandards, . represents the current point,
    so 1 represents a dot above the current point, 3 is the right.:
    
      812
      7.3
      654

"""



def coords_neighbours(x: int, y: int,
                      xMinValidPossibleCoordValue: int, yMinValidPossibleCoordValue: int,
                      xMaxValidPossibleCoordValue: int, yMaxValidPossibleCoordValue: int,
                      allowedDirections: set[int]={1,2,3,4,5,6,7,8}
                      ) -> list[tuple[int, int], ]:
    """return with possible direct neighbour coordinates (select pixels next to <x,y> ) """

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

    return sorted(neighbours)


########################################################################################################################
# TODO: dedicated unittest for this:
def coords_drop_collect_pixelgroups_from_starting_point(
        pixelGroup_glyph_matrix_representation: list[list[tuple[int, int, img_0_pixels.PixelGroup_Glyph]]],
        xStartInMatrix: int=0,
        yStartInMatrix: int=0,

        allowedDirections: set[int] = {1, 3, 5, 7},
        wantedRepresentedPixelGroupNames: set[str] = {img_0_pixels.pixelsNameForegroundActive}
        # it means that the collection cannot move diagonal, only horizontal/vertical

) -> img_0_pixels.PixelGroup_Glyph:
    """collect all coords, in a given direction.

    :param allowedDirections: direction standards are documented in img_1_pixels_select.py

    TODO?: receive a parameter: conditionFunToCollect(matrix_representation, currentX, currentY)
    """
    pixelGroup_collected = img_0_pixels.PixelGroup_Glyph()

    pixelCoords_to_analyse = [(xStartInMatrix, yStartInMatrix)]
    pixelCoordsInMatrix_analysed = set()

    x_max_in_representation = len(pixelGroup_glyph_matrix_representation[0])-1
    y_max_in_representation = len(pixelGroup_glyph_matrix_representation)-1

    while pixelCoords_to_analyse:
        (pixelXinMatrix, pixelYinMatrix) = pixelCoordNowInMatrix = pixelCoords_to_analyse.pop(0)
        if pixelCoordNowInMatrix in pixelCoordsInMatrix_analysed: continue

        pixelCoordsInMatrix_analysed.add(pixelCoordNowInMatrix)

        (xAbs, yAbs, objBehindPixelNow) = pixelGroup_glyph_matrix_representation[pixelYinMatrix][pixelXinMatrix]


        # if any of the current flags are in the wanted flags:
        if len(objBehindPixelNow.representedPixelGroupNames & wantedRepresentedPixelGroupNames)>0:

            pixelGroup_collected.pixel_add(xAbs, yAbs,
                                           objBehindPixelNow.pixels[(xAbs, yAbs)]["rgb"])

            neighbours = coords_neighbours(
                pixelCoordNowInMatrix[0], pixelCoordNowInMatrix[1], 0, 0,
                x_max_in_representation, y_max_in_representation, allowedDirections=allowedDirections)

            for neighbourXyCoord in neighbours:
                pixelCoords_to_analyse.append(neighbourXyCoord)

    return pixelGroup_collected
########################################################################################################################



# white: 255,255,255 black: 0,0,0
def pixelGroupSelector_default(rNow: int, gNow: int, bNow:int, params: dict ) -> bool:
    """if the value is less than the limit, so the pixel is darker, then select"""

    # if any channel param is acceptable, set Active
    if rNow < params.get("rMax_toSelect", 127):
        return True

    if gNow < params.get("gMax_toSelect", 127):
        return True

    if bNow < params.get("bMax_toSelect", 127):
        return True

    return False



def isActive_checkAllSelectors(onePixelRgb: tuple[int, int, int],
                               selectorFunctions: list[tuple[typing.Callable, dict]]) -> bool:
    """is the current pixel RGB value is active/part of a wanted patter or not?"""

    isActiveByAllFun = True
    for (funDecideIsActive, paramsToSelector) in selectorFunctions:
        r, g, b = onePixelRgb

        isActiveByThisFun = funDecideIsActive(r, g, b, paramsToSelector)

        if not isActiveByThisFun:  # one way: if any of the func decides that the pixel is not active, it is not active
            isActiveByAllFun = False

    return isActiveByAllFun



def pixelGroups_active_select(pixelsAll: list[list[tuple[int, int, int]]],
                              selectorFunctions=[(pixelGroupSelector_default,
                                                  {"rMax_toSelect":127, "gMax_toSelect": 127, "bMax_toSelect": 127})]) \
        -> list[img_0_pixels.PixelGroup_Glyph]:

    """

    :param pixelsAll: (r,g,b) values in rows in columns, double embedded list
                      rgb values are organised into 'ONE ROW / ONE LIST, X-axis' and
                      list of rows represents Y axis.

    :param selectorFunctions:  one or more selector fun, and params for the selector.
                               by default the pixels are active, so part of a character.
                               if any of the selector thinks that the pixel is not active, the end result is NotActive.

    :return: coord->glyph, and list of glyphs
    """

    coordsAnalysedOnce = set()

    pixelGroups: list[img_0_pixels.PixelGroup_Glyph] = list()

    pixelGroupNow = img_0_pixels.PixelGroup_Glyph()

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
                # print(f"onePixelRgb: ", onePixelRgb)

                if isActive_checkAllSelectors(onePixelRgb, selectorFunctions):
                    # print(f"active pixel detected: {pixelGroupNow.groupId}", coordNowX, coordNowY)
                    pixelGroupNow.pixel_add(coordNowX, coordNowY, onePixelRgb)

                    # maybe the neighbours are detected from multiple places, insert them only once
                    for (xPossibleNeighbour, yPossibleNeighbour) in coords_neighbours(coordNowX, coordNowY, 0, 0, len(row) - 1, len(pixelsAll) - 1):
                        if (xPossibleNeighbour, yPossibleNeighbour) not in checkTheseCoords:
                            checkTheseCoords.append( (xPossibleNeighbour, yPossibleNeighbour))

            # only Active pixels are inserted into the Groups, so a new group has to be created ONLY if the previous one has any active Pixels
            if pixelGroupNow.has_pixels():
                # the top-left coord of the group is the registration point
                pixelGroups.append(pixelGroupNow)

                pixelGroupNow = img_0_pixels.PixelGroup_Glyph()  # create a new one

    return pixelGroups



